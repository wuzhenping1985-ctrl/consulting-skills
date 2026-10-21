import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {makeDeck} from './draw.mjs';
import {buildDPages} from './pages/d-pages.mjs';
import {buildEPages} from './pages/e-pages.mjs';
import {PresentationFile} from '@oai/artifact-tool';
const here=path.dirname(fileURLToPath(import.meta.url));
const dir=path.resolve(process.argv[2] || path.join(here,'generated'));
const deck=makeDeck();buildDPages(deck);buildEPages(deck);
await fs.mkdir(dir,{recursive:true});
await (await PresentationFile.exportPptx(deck)).save(path.join(dir,'candidate.pptx'));
for(let i=0;i<deck.slides.items.length;i++){
 const png=await deck.export({slide:deck.slides.items[i],format:'png',scale:1.25});
 await fs.writeFile(path.join(dir,`slide-${String(i+1).padStart(2,'0')}.png`),new Uint8Array(await png.arrayBuffer()));
}
console.log(`Rebuilt ${deck.slides.items.length} slides at ${dir}`);
