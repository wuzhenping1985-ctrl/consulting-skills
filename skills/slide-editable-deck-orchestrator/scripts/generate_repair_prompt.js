#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

function usage() {
  console.log(`Usage: node generate_repair_prompt.js [options]

Generate a implementation-ready prompt for a repair wave.

Options:
  --project <path>       Deck project root (default: .)
  --wave-plan <path>     Repair wave plan JSON
  --wave-index <number>  Zero-based wave index (default: 0)
  --slides <list>        Slide list if no wave plan is provided
  --summary <path>       Visual QA summary path to mention
  --quality-level <lvl>  blocking-zero|polish|strict|canary (default: blocking-zero)
  --quality <level>      Backward-compatible alias for --quality-level
  --out <path>           Optional prompt output path
  --help                 Show this help
`);
}

function parseArgs(argv) {
  const opts = { project: '.', wavePlan: '', waveIndex: 0, slides: '', summary: 'out/visual_qa_summary.json', qualityLevel: 'blocking-zero', out: '' };
  for (let i = 2; i < argv.length; i += 1) {
    const a = argv[i];
    if (a === '--help' || a === '-h') opts.help = true;
    else if (a === '--project') opts.project = argv[++i];
    else if (a === '--wave-plan') opts.wavePlan = argv[++i];
    else if (a === '--wave-index') opts.waveIndex = Number(argv[++i]);
    else if (a === '--slides') opts.slides = argv[++i];
    else if (a === '--summary') opts.summary = argv[++i];
    else if (a === '--quality-level' || a === '--quality') opts.qualityLevel = argv[++i];
    else if (a === '--out') opts.out = argv[++i];
    else throw new Error(`Unknown option: ${a}`);
  }
  return opts;
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, 'utf8'));
}

function parseSlides(value) {
  return value.split(',').map((s) => Number(s.trim())).filter((n) => Number.isInteger(n) && n > 0);
}

function waveFromArgs(opts) {
  if (opts.wavePlan) {
    const plan = readJson(path.resolve(opts.wavePlan));
    const wave = (plan.waves || [])[opts.waveIndex];
    if (!wave) throw new Error(`No wave at index ${opts.waveIndex}`);
    return wave;
  }
  const slides = parseSlides(opts.slides);
  if (!slides.length) throw new Error('Provide --wave-plan or --slides');
  return { id: 'repair-wave-manual', slides, primaryIssueTypes: [], strategies: [], slideDetails: [] };
}

function shellQuote(value) {
  return `'${String(value).replace(/'/g, `'"'"'`)}'`;
}

function macosPromptCommands(projectRoot, slidesArg, stem) {
  const userHome = process.env.HOME || '/Users/USER';
  const skillsRoot = process.env.PNGTOPPTX_SKILLS_ROOT || path.join(userHome, '.codex', 'skills');
  const pythonExec = process.env.PNGTOPPTX_PYTHON || path.join(userHome, '.codex', 'venvs', 'pngtopptx', 'bin', 'python3');
  const dualRoot = path.join(skillsRoot, 'slide-image-dual-render');
  const qaRoot = path.join(skillsRoot, 'slide-visual-polish-qa');
  const envScript = path.join(skillsRoot, 'slide-editable-deck-orchestrator', 'scripts', 'macos_env.sh');
  const profile = path.join(dualRoot, 'styles', 'clinical-dark.json');

  return {
    skillIntro: `Use [$slide-image-dual-render](${path.join(dualRoot, 'SKILL.md')}) and [$slide-visual-polish-qa](${path.join(qaRoot, 'SKILL.md')}).`,
    commands: `cd ${shellQuote(projectRoot)}

source ${shellQuote(envScript)}
export SLIDE_PIPELINE_STRICT="1"
export DECK_PROFILE=${shellQuote(profile)}
export DECK_ASSETS="\${PWD}/assets"
export DECK_PXW="1672"
export DECK_PXH="941"

node ${shellQuote(path.join(dualRoot, 'scripts', 'slide_pipeline.js'))} --project . --slides ${slidesArg} --quality reconstruction --require-qa --require-reconstruction --crop-plan work/crop_plan.json --target both --pptx-out out/${stem}.pptx --html-out out/${stem}.html

node ${shellQuote(path.join(dualRoot, 'scripts', 'final_gate.js'))} --project . --slides ${slidesArg} --quality reconstruction --require-qa --require-reconstruction --require-pptx-openable --target both --pptx out/${stem}.pptx --html out/${stem}.html

${shellQuote(pythonExec)} ${shellQuote(path.join(qaRoot, 'scripts', 'rasterize_pptx.py'))} --project . --pptx out/${stem}.pptx --source-slides ${slidesArg} --out-dir work

${shellQuote(pythonExec)} ${shellQuote(path.join(qaRoot, 'scripts', 'capture_html_screenshot.py'))} --project . --html out/${stem}.html --source-slides ${slidesArg} --out-dir work --width 1672 --height 941

${shellQuote(pythonExec)} ${shellQuote(path.join(qaRoot, 'scripts', 'compare_slide_images.py'))} --project . --slides ${slidesArg} --mode qa-polish --source-dir src --qa-dir work --out-summary out/visual_qa_summary_${stem}.json

node ${shellQuote(path.join(qaRoot, 'scripts', 'generate_visual_qa_summary.js'))} --project . --slides ${slidesArg} --out-json out/visual_qa_summary_${stem}.json --out-md out/visual_qa_summary_${stem}.md

node ${shellQuote(path.join(qaRoot, 'scripts', 'enforce_visual_qa.js'))} --project . --slides ${slidesArg} --mode qa-polish --summary out/visual_qa_summary_${stem}.json --require-pptx --require-html`,
  };
}

function buildPrompt(opts, wave) {
  const projectRoot = path.resolve(opts.project);
  const slidesArg = wave.slides.join(',');
  const stem = `deck-repair-wave-${slidesArg.replace(/,/g, '-')}`;
  const strategyLines = (wave.strategies || []).length
    ? wave.strategies.map((s) => `- ${s.type}: ${s.strategy}`).join('\n')
    : '- Review visual_polish_fixes.json and apply native reconstruction fixes first.';
  const detailLines = (wave.slideDetails || []).length
    ? wave.slideDetails.map((s) => `- slide ${s.slide}: ${s.status}/${s.severity}; issues: ${(s.issueTypes || []).join(', ') || 'see visual_polish_fixes.json'}`).join('\n')
    : `- slides: ${slidesArg}`;

  let prompt = `Use [$slide-image-dual-render](C:\\Users\\USER\\.pngtopptx\\skills\\slide-image-dual-render\\SKILL.md) and [$slide-visual-polish-qa](C:\\Users\\USER\\.pngtopptx\\skills\\slide-visual-polish-qa\\SKILL.md).

Run a repair wave for slides ${slidesArg}.

This is a deck reconstruction repair task, not Skill development.
Do not modify Skill files.
Do not modify slide-text-layer-inpaint.
If a new Skill bug is found, stop and report it before patching.

Project root:
${projectRoot}

Quality target:
${opts.qualityLevel}

Current visual QA summary:
${opts.summary}

Issue summary:
${detailLines}

Repair strategy:
${strategyLines}

Rules:
- Preserve semantic text as native editable text.
- Do not convert pseudo/decorative text into incorrect semantic text.
- Do not use full-slide screenshot backgrounds.
- Do not weaken hardlocks, gates, crop policy, PPTX openability, or visual QA thresholds.
- Prefer native layout, rule, connector, icon, panel, table, and text fixes first.
- Text/table/label crops are forbidden unless explicitly exception-approved.
- Small crops are allowed only for non-text photoreal/3D/technical/decorative detail with complete metadata.

Run:

cd ${projectRoot}

$env:SLIDE_PIPELINE_STRICT="1"
$env:DECK_PROFILE="$PWD\\styles\\clinical-dark.json"
$env:DECK_ASSETS="$PWD\\assets"
$env:DECK_PXW="1672"
$env:DECK_PXH="941"

node "$env:USERPROFILE\\.pngtopptx\\skills\\slide-image-dual-render\\scripts\\slide_pipeline.js" --project . --slides ${slidesArg} --quality reconstruction --require-qa --require-reconstruction --crop-plan work\\crop_plan.json --node-path .\\node_modules --target both --pptx-out out\\${stem}.pptx --html-out out\\${stem}.html

node "$env:USERPROFILE\\.pngtopptx\\skills\\slide-image-dual-render\\scripts\\final_gate.js" --project . --slides ${slidesArg} --quality reconstruction --require-qa --require-reconstruction --require-pptx-openable --target both --pptx out\\${stem}.pptx --html out\\${stem}.html

python "$env:USERPROFILE\\.pngtopptx\\skills\\slide-visual-polish-qa\\scripts\\rasterize_pptx.py" --project . --pptx out\\${stem}.pptx --source-slides ${slidesArg} --out-dir work

python "$env:USERPROFILE\\.pngtopptx\\skills\\slide-visual-polish-qa\\scripts\\capture_html_screenshot.py" --project . --html out\\${stem}.html --source-slides ${slidesArg} --out-dir work --width 1672 --height 941

python "$env:USERPROFILE\\.pngtopptx\\skills\\slide-visual-polish-qa\\scripts\\compare_slide_images.py" --project . --slides ${slidesArg} --mode qa-polish --source-dir src --qa-dir work --out-summary out\\visual_qa_summary_${stem}.json

node "$env:USERPROFILE\\.pngtopptx\\skills\\slide-visual-polish-qa\\scripts\\generate_visual_qa_summary.js" --project . --slides ${slidesArg} --out-json out\\visual_qa_summary_${stem}.json --out-md out\\visual_qa_summary_${stem}.md

node "$env:USERPROFILE\\.pngtopptx\\skills\\slide-visual-polish-qa\\scripts\\enforce_visual_qa.js" --project . --slides ${slidesArg} --mode qa-polish --summary out\\visual_qa_summary_${stem}.json --require-pptx --require-html

Final response:
- files modified
- crops introduced or adjusted
- hardlock results
- visual QA before/after
- slides moved out of fail/blocking
- remaining issues
`;

  if (process.platform === 'darwin') {
    const macos = macosPromptCommands(projectRoot, slidesArg, stem);
    prompt = prompt.replace(
      'Use [$slide-image-dual-render](C:\\Users\\USER\\.pngtopptx\\skills\\slide-image-dual-render\\SKILL.md) and [$slide-visual-polish-qa](C:\\Users\\USER\\.pngtopptx\\skills\\slide-visual-polish-qa\\SKILL.md).',
      macos.skillIntro,
    );
    const runStart = prompt.indexOf('Run:\n');
    const finalStart = prompt.indexOf('Final response:\n');
    if (runStart >= 0 && finalStart > runStart) {
      prompt = `${prompt.slice(0, runStart)}Run:\n\n${macos.commands}\n\n${prompt.slice(finalStart)}`;
    }
  }

  return prompt;
}

function main() {
  const opts = parseArgs(process.argv);
  if (opts.help) {
    usage();
    return;
  }
  const wave = waveFromArgs(opts);
  const prompt = buildPrompt(opts, wave);
  if (opts.out) {
    const outPath = path.resolve(opts.out);
    fs.mkdirSync(path.dirname(outPath), { recursive: true });
    fs.writeFileSync(outPath, prompt, 'utf8');
    console.log(JSON.stringify({ status: 'ok', out: outPath, slides: wave.slides }, null, 2));
  } else {
    console.log(prompt);
  }
}

try {
  main();
} catch (err) {
  console.error(`[generate_repair_prompt] ${err.message}`);
  process.exit(1);
}
