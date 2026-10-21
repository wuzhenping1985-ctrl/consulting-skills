import fs from 'node:fs';
import {C,FONT,rect,ellipse,poly,line,dash,dashRect,arrow,arc,txt,wrap,footer,dot} from '../draw.mjs';

// Native reconstruction of E006 and E011, measured against the 1280×720 reference.
// Only the authored text is read from the source transcription. No source slide,
// rendered page, or source graphics are imported.
const E6=JSON.parse(fs.readFileSync(new URL('../E/E006-text.json',import.meta.url),'utf8'));
const E11=JSON.parse(fs.readFileSync(new URL('../E/E011-text.json',import.meta.url),'utf8'));
const find=(rows,prefix)=>rows.find(r=>r.text.startsWith(prefix)).text;

function nav(s,active){
  const names=['规划背景','顶层设计','重点任务','保障机制','实施路径'];
  names.forEach((t,i)=>{rect(s,760+i*104,0,103,27,i===active?C.mid:'#C5C5C5');txt(s,t,764+i*104,3,95,18,{color:C.white,bold:true,align:'center',h:24,raw:true});});
}
function centered(s,t,x,y,w,h,fs,color=C.ink,bold=true){return txt(s,t,x,y,w,fs,{raw:true,align:'center',valign:'middle',h,color,bold,leading:1.2});}
function dashedRound(s,x,y,w,h,r=35,color='#9D9D9D'){
  const pts=[];
  for(const [cx,cy,a,b] of [[x+w-r,y+r,-90,0],[x+w-r,y+h-r,0,90],[x+r,y+h-r,90,180],[x+r,y+r,180,270]]){
    for(let i=0;i<=20;i++){const z=(a+(b-a)*i/20)*Math.PI/180;pts.push([cx+r*Math.cos(z),cy+r*Math.sin(z)]);}
  }
  pts.push(pts[0]);let phase=0;
  for(let i=1;i<pts.length;i++){
    const a=pts[i-1],b=pts[i],L=Math.hypot(b[0]-a[0],b[1]-a[1]);
    for(let p=0;p<L;){const remain=(phase<3?3:5)-phase;const q=Math.min(L,p+remain);if(phase<3)line(s,a[0]+(b[0]-a[0])*p/L,a[1]+(b[1]-a[1])*p/L,a[0]+(b[0]-a[0])*q/L,a[1]+(b[1]-a[1])*q/L,color,.7);phase=(phase+q-p)%5;p=q;}
  }
}
function plainBullets(s,text,x,y,w,fs=16){
  // Draw each line independently. The renderer's paragraph lineSpacing adds
  // extra leading, so explicit baselines keep the square and first line aligned.
  const paragraphs=text.split('\n').map(t=>wrap(t,w-19,fs).split('\n'));
  const count=paragraphs.reduce((n,p)=>n+p.length,0);
  const step=count<=6?28.7:25.0;
  let yy=count<=6?404:399;
  for(const rows of paragraphs){
    rect(s,x,yy+7,8,8,'none',C.ink,1.7);
    for(const row of rows){
      txt(s,row,x+17,yy,w-17,fs,{raw:true,leading:1,h:fs+11});
      yy+=step;
    }
  }
  return yy;
}
const charWidth=(c,fs)=>/[\x00-\xff]/.test(c)?(/[il.,:;!|\s]/.test(c)?fs*.27:/[MW@]/.test(c)?fs*.82:fs*.55):fs;
function richBullet(s,t,x,y,w,fs,blue=[],bold=[]){
  const d=wrap(t,w-18,fs),ranges=[];
  for(const phrase of blue){const a=t.indexOf(phrase);if(a>=0)ranges.push({a,b:a+phrase.length,color:C.blue,bold:true});}
  for(const phrase of bold){const a=t.indexOf(phrase);if(a>=0)ranges.push({a,b:a+phrase.length,color:C.ink,bold:true});}
  const step=33.6;
  rect(s,x,y+8,9,9,'none',C.ink,2);
  let pos=0,yy=y;
  // Native text boxes for each styled line segment keep the original blue
  // emphasis visible in both the editable deck and the exported preview.
  for(const row of d.split('\n')){
    let xx=x+16,rx=xx,run='',style=null;
    const flush=()=>{if(run)txt(s,run,rx,yy,Math.max(12,xx-rx+5),fs,{raw:true,color:style.color,bold:style.bold,leading:1,h:fs+12});run='';};
    for(const ch of row){
      const r=ranges.find(r=>pos>=r.a&&pos<r.b);
      const next={color:r?.color??C.ink,bold:r?.bold??false};
      if(!style||style.color!==next.color||style.bold!==next.bold){flush();style=next;rx=xx;}
      if(!run)rx=xx;
      run+=ch;xx+=charWidth(ch,fs);pos++;
    }
    flush();yy+=step;
  }
  return yy;
}
function checkHeading(s,t,x,y,w){
  ellipse(s,x,y+1,31,31,C.blue);poly(s,[[x+9,y+16],[x+14,y+21],[x+23,y+11]],'none',C.white,3,false);
  txt(s,t,x+43,y+3,w,21.3,{bold:true,raw:true,h:32});
}

function buildE6(deck){
  const s=deck.slides.add();s.background.fill=C.white;nav(s,1);
  const head=find(E6,'顶层设计');
  head.replace('人才发展体系','人才发\n展体系').split('\n').forEach((row,i)=>
    txt(s,row,78,38+i*40,1130,29.3,{bold:true,raw:true,leading:1,h:39}));
  // Goal roof, followed by three labelled horizontal strata.
  poly(s,[[47,200],[634,124],[1220,200]],C.mid);
  centered(s,find(E6,'打造自主可控'),340,145,590,54,18.6,C.white,true);
  rect(s,47,211,64,45,'#F1F1F1');centered(s,'原则',47,213,64,42,18.7);
  rect(s,121,209,1099,47,C.bg);dashRect(s,121,209,1099,47,C.light,.65);
  const principles=['战略引领','自主可控','开放协同','市场导向','动态优化'];
  principles.forEach((t,i)=>{const x=143+222.3*i;rect(s,x,213,177,38,C.pale,'none',0,6);centered(s,t,x,215,177,34,18.7);});
  rect(s,47,267,64,329,'#F1F1F1');centered(s,'重点\n任务',47,400,64,73,18.7);
  rect(s,121,267,1099,330,C.bg);dashRect(s,121,267,1099,330,C.light,.65);
  centered(s,find(E6,'构建以全链条'),161,278,1046,33,18.2,C.ink,true);
  rect(s,190,317,188,29,C.mid,'none',0,4);centered(s,'1条主线',190,318,188,27,18.7,C.white);
  rect(s,748,317,188,29,C.mid,'none',0,4);centered(s,'3大核心抓手',748,318,188,27,18.7,C.white);
  // These two enclosures are essential: one main line, then three grouped enablers.
  rect(s,134,355,300,233,C.white,'none',0,38);dashedRound(s,134,355,300,233,38);
  rect(s,442,355,769,233,C.white,'none',0,38);dashedRound(s,442,355,769,233,38);
  const columns=[
    {x:143,w:278,title:'全链条核心技术攻关',text:find(E6,'构建“基础研究'),fill:'#D9E9FD'},
    {x:452,w:243,title:'创新平台建设',text:find(E6,'搭建“决策'),fill:'#EFF5FE'},
    {x:704,w:243,title:'成果转化体系',text:find(E6,'构建“源头激活'),fill:'#EFF5FE'},
    {x:955,w:243,title:'人才发展体系',text:find(E6,'构建“选-用'),fill:'#EFF5FE'}
  ];
  columns.forEach((p,i)=>{
    centered(s,p.title,p.x,360,p.w,29,18.7,i===0?C.blue:C.mid,true);
    rect(s,p.x,391,p.w,184,p.fill);
    plainBullets(s,p.text,p.x+11,402,p.w-19,15.7,1.53,1.5);
  });
  rect(s,47,608,64,45,'#F1F1F1');centered(s,'机制\n保障',47,607,64,46,17.7);
  rect(s,121,607,1099,46,C.bg);dashRect(s,121,607,1099,46,C.light,.65);
  ['资金保障','能力保障','知识产权保障','文化保障'].forEach((t,i)=>{
    const x=131+277.1*i,w=247,y=614,h=35;
    poly(s,[[x,y],[x+w-18,y],[x+w,y+h/2],[x+w-18,y+h],[x,y+h],[x+18,y+h/2]],'#B8CAFE');
    centered(s,t,x+15,y+1,w-30,h-2,18.7);
  });
  footer(s);return s;
}

function buildE11(deck){
  const s=deck.slides.add();s.background.fill=C.white;nav(s,3);
  txt(s,find(E11,'保障机制 |'),78,69,1126,29.3,{bold:true,raw:true,h:48});
  // Shared direction axis, deliberately not a four-stage flow.
  line(s,123,401,1146,401,C.blue,1.5);
  poly(s,[[53,382],[120,382],[133,401],[66,401]],C.blue);
  poly(s,[[66,401],[133,401],[120,419],[53,419]],C.mid);
  // Four open text regions, with alternating upper/lower boundaries.
  [[593,157,401],[1057,157,401],[526,401,645],[997,401,645]].forEach(([x,a,b])=>{dash(s,x,a,x,b,C.blue,1,5,4);dot(s,x,a===401?b:a,3.7,C.blue);});
  // Native elliptical target: pale side face and alternating front rings.
  ellipse(s,1146,251,92,300,C.pale);
  ellipse(s,1087,251,117,300,C.blue);
  ellipse(s,1097,276,97,249,C.white);
  ellipse(s,1107,301,77,198,C.blue);
  ellipse(s,1115,321,61,158,C.white);
  ellipse(s,1132,373,22,55,C.pale);
  arrow(s,123,401,1146,401,C.blue,1.5,6);
  // Small native target icon at the left, retaining its role as a visual cue.
  rect(s,53,228,62,61,C.blue,'none',0,13);
  ellipse(s,66,241,34,34,'none',C.white,3);ellipse(s,73,248,20,20,'none',C.white,2.5);ellipse(s,79,254,8,8,C.white);
  line(s,83,258,102,239,C.white,4);poly(s,[[96,238],[103,237],[102,245]],C.white);
  checkHeading(s,'资金保障',296,154,180);
  checkHeading(s,'能力保障',741,157,180);
  checkHeading(s,'知识产权保障',211,417,235);
  checkHeading(s,'文化保障',675,417,180);
  const funds=find(E11,'统筹设立').split('\n');
  let y=207;
  y=richBullet(s,funds[0],158,y,416,18.7,['专项资金池']);
  richBullet(s,funds[1],158,y,416,18.7,['差异化授权审批机制']);
  const cap=find(E11,'短期：').split('\n');
  y=207;
  y=richBullet(s,cap[0],614,y,431,18.7,['关键市场准入资质','首台套、首批次、首版次'],['短期：']);
  richBullet(s,cap[1],614,y,431,18.7,['建设高水平国家级、省级创新平台与共享中试实证平台'],['中长期：']);
  const ip=find(E11,'围绕战略必争').split('\n');
  y=467;
  y=richBullet(s,ip[0],82,y,432,18.7,['开展知识产权高地前瞻性布局，构建高价值专利组合']);
  richBullet(s,ip[1],82,y,432,18.7,['创造、保护、运用全周期治理体系']);
  const culture=find(E11,'建立科技创新').split('\n');
  y=467;
  y=richBullet(s,culture[0],551,y,432,18.7,['科技创新尽职免责相关制度']);
  richBullet(s,culture[1],551,y,432,18.7,['复盘与经验转化机制']);
  footer(s);return s;
}

export function buildEPages(deck){return [buildE6(deck),buildE11(deck)];}
