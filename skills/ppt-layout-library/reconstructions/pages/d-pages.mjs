import {C,txt,rect,ellipse,poly,line,arrow,blockArrow,arc,dashRect,hexbar,footer} from '../draw.mjs';

// Hand-built native objects. Coordinates are measured from D004/D006 on a
// 1280 × 720 canvas; source slide images are never embedded.
const PEACH='#FFB59F', SOFTPEACH='#FFD7C9', PALEBLUE='#BDCCFF', GRAY='#B2B2B2';
function caption(s,t,x,y,w,fs=24,color=C.ink,bold=true){
  return txt(s,t,x,y,w,fs,{color,bold,align:'center',raw:true});
}
function fatArrow(s,x1,y1,x2,y2,width,headWidth,headLen,color){
  const len=Math.hypot(x2-x1,y2-y1),ux=(x2-x1)/len,uy=(y2-y1)/len,nx=-uy,ny=ux;
  const b=[x2-ux*headLen,y2-uy*headLen];
  poly(s,[[x1+nx*width/2,y1+ny*width/2],[b[0]+nx*width/2,b[1]+ny*width/2],
    [b[0]+nx*headWidth/2,b[1]+ny*headWidth/2],[x2,y2],
    [b[0]-nx*headWidth/2,b[1]-ny*headWidth/2],[b[0]-nx*width/2,b[1]-ny*width/2],
    [x1-nx*width/2,y1-ny*width/2]],color);
}
function diamondBullet(s,x,y,size=8){poly(s,[[x,y-size/2],[x+size/2,y],[x,y+size/2],[x-size/2,y]],C.blue);}
function dotBullet(s,x,y){ellipse(s,x-2,y-2,4,4,C.ink);}
const charWidth=(c,fs)=>/[\x00-\xff]/.test(c)?(/[il.,:;!|\s]/.test(c)?fs*.27:fs*.55):fs;
// Separate editable text runs preserve the original red emphasis without
// replacing any text with raster assets or abbreviations.
function rich(s,segments,x,y,w,fs=18.6,leading=1.35){
  let xx=x,yy=y,run='',style=null,rx=x;
  function flush(){if(run)txt(s,run,rx,yy,Math.max(12,xx-rx+5),fs,{raw:true,color:style.color??C.ink,bold:style.bold??false,h:fs*leading+5});run='';}
  for(const seg of segments){
    for(const c of seg.text){
      const cw=charWidth(c,fs);
      if(c==='\n'||xx+cw>x+w+.1){flush();xx=x;yy+=fs*leading;style=null;if(c==='\n')continue;}
      if(style!==seg){flush();style=seg;rx=xx;}
      if(!run)rx=xx;
      run+=c;xx+=cw;
    }
  }
  flush();return yy+fs*leading;
}
function badge(s,text,x,y,w,h,color){
  poly(s,[[x,y],[x+w,y],[x+w,y+h-13],[x+w/2,y+h],[x,y+h-13]],color);
  // Fixed per-character positions avoid paragraph leading pushing the sixth
  // character below the short second-stage badge.
  [...text].forEach((c,i)=>txt(s,c,x+3,y+4+i*17.5,w-6,17.2,
    {raw:true,color:C.white,bold:true,align:'center',leading:1,h:24}));
}

function buildD4(deck){
  const s=deck.slides.add();s.background.fill=C.white;
  txt(s,'三、国有企业科技创新规划总体思路：构建国企科技创新活动全生命周期闭环\n管理体系',78,28,1138,30.5,{bold:true,leading:1.12,raw:true});
  txt(s,'以创新规划为引领，匹配资源投入为保障，以体系化创新过程管理为支撑，实现规划到产出的闭环',78,143,1132,20.5,{bold:true,leading:1.15});
  const heads=[['创新规划',80,200],['创新投入',380,225],['创新过程',676,227],['创新产出',973,228]];
  heads.forEach(([t,x,w])=>caption(s,t,x,193,w,31.5,C.blue));
  [['体现引领作用',79,200],['体现保障作用',379,225],['体现支撑作用',675,228],['体现创新成果',970,235]]
    .forEach(([t,x,w])=>caption(s,t,x,234,w,23.5,C.ink,false));
  arrow(s,247,215,379,215,'#595959',1.25,7);
  arrow(s,556,215,675,215,'#595959',1.25,7);
  arrow(s,854,215,969,215,'#595959',1.25,7);

  // Planning decomposes downwards through business, product and technology.
  dashRect(s,82,283,177,364,'#CDCDCD',1.1);
  const planY=[302,441,580];
  ['业务规划','产品规划','技术规划'].forEach((t,i)=>{
    rect(s,104,planY[i],143,55,PALEBLUE,'none',0,10);
    caption(s,t,107,planY[i]+12,137,23.5);
  });
  blockArrow(s,156,376,38,47,SOFTPEACH,'down');
  blockArrow(s,156,520,38,47,SOFTPEACH,'down');

  // Two resource inputs support one planning goal; no extra fourth item.
  caption(s,'规划目标',386,290,145,24);
  ellipse(s,435,329,42,42,C.gray);
  line(s,456,371,345,612,'#AAAAAA',1.3);
  line(s,456,371,570,612,'#AAAAAA',1.3);
  poly(s,[[345,612],[458,577],[570,612],[458,647]],C.mid);
  caption(s,'财力',321,463,80,22.5);
  caption(s,'人力',516,463,80,22.5);
  fatArrow(s,342,512,322,568,24,45,23,'#D7D7D7');
  fatArrow(s,562,512,584,568,24,45,23,'#D7D7D7');
  line(s,331,513,352,521,C.white,1.4);line(s,330,518,350,526,C.white,1.4);
  line(s,551,520,572,512,C.white,1.4);line(s,553,525,574,517,C.white,1.4);

  // Three outer triangles share the central process triangle.
  const top=[759,276],left=[576,650],right=[942,650],ml=[667.5,463],mr=[850.5,463],bottom=[759,650];
  poly(s,[top,left,right],'none',C.mid,1.15);
  line(s,...ml,...mr,C.mid,1.15);line(s,...ml,...bottom,C.mid,1.15);line(s,...mr,...bottom,C.mid,1.15);
  rect(s,750,355,27,32,C.mid);caption(s,'1',750,358,27,20,C.white);
  caption(s,'组织形态',696,405,126,19.5);
  rect(s,642,553,27,32,C.mid);caption(s,'2',642,556,27,20,C.white);
  caption(s,'人才管理',602,592,112,19.5);
  rect(s,832,553,27,32,C.mid);caption(s,'3',832,556,27,20,C.white);
  caption(s,'保障机制',790,592,112,19.5);
  caption(s,'创新过程',681,495,156,26);

  // Outcomes aggregate upwards, opposite to planning decomposition.
  dashRect(s,966,289,215,364,'#CDCDCD',1.1);
  [308,447,586].forEach((y,i)=>{
    rect(s,992,y,175,55,PEACH,'none',0,9);
    caption(s,['实现业务目标','实现产品目标','实现技术目标'][i],997,y+12,165,22.8,C.white);
  });
  blockArrow(s,1056,382,45,47,C.pale,'up');
  blockArrow(s,1056,526,45,47,C.pale,'up');
  footer(s);return s;
}

function buildD6(deck){
  const s=deck.slides.add();s.background.fill=C.white;
  txt(s,'五、国有企业科技创新规划步骤二：以财务资源稳定投入和人力资源分阶段配置，\n为创新规划提供双保障',78,28,1138,30.5,{bold:true,leading:1.12,raw:true});
  txt(s,'国有企业科技创新规划投入主要体现在财务资源投入和人力资源投入两方面，二者共同满足创新规划要求',78,143,1134,20.4,{bold:true,leading:1.15});
  hexbar(s,'财务资源投入',81,178,528,40,'#A7A7A7',22.6);
  hexbar(s,'人力资源投入',652,180,541,40,C.blue,22.6);
  rect(s,86,233,515,168,'#F2F2F2');
  const finance=[
    ['科技创新的长周期特性决定了企业研发投入必须保持稳定增长。',239,C.ink,false],
    ['健全以企业投入为主，各类资金共同参与的国有企业科技投入体系。',295,'#FF0000',true],
    ['提高基础研究和前沿性技术研究投入比重。',351,C.ink,false],
    ['加强对企业研发投入产出的科学评价。',378,C.ink,false],
  ];
  finance.forEach(([t,y,c,b])=>{diamondBullet(s,102,y+11,9);txt(s,t,125,y,465,18.4,{leading:1.26,color:c,bold:b});});

  // Faithful reproduction of the source's four-label ring.
  poly(s,[[313,410],[351,410],[332,439]],'#F0F0F0');
  arc(s,331,553,121,108,-123,223,'#D7D7D7',12);
  fatArrow(s,251,489,274,455,12,30,26,'#D7D7D7');
  ellipse(s,274,502,110,98,GRAY);
  caption(s,'四大\n要求',291,525,76,23,C.white);
  const terms=[['稳定提升',279,436,C.blue],['科学评价',164,527,PALEBLUE],['多元投入',392,527,C.mid],['合理结构',279,624,C.light]];
  terms.forEach(([t,x,y,c])=>{rect(s,x,y,101,50,c);caption(s,t,x+4,y+12,93,19.1,C.white);});
  poly(s,[[610,266],[640,438],[610,608]],'#D7D7D7');

  // Human resource requirements retain three stages and all subordinate items.
  const rows=[
    {y:233,h:139,c:'#E8EDFF',bc:C.blue,t:'基础研究阶段'},
    {y:387,h:123,c:'#EEF2FF',bc:C.mid,t:'技术开发阶段'},
    {y:536,h:136,c:'#F7F9FF',bc:'#84B8FE',t:'成果转化阶段'}
  ];
  rows.forEach(r=>{rect(s,685,r.y,495,r.h,r.c);badge(s,r.t,655,r.y,31,r.h+5,r.bc);});
  const normal=t=>({text:t,color:C.ink});const red=t=>({text:t,color:'#FF0000',bold:true});
  dotBullet(s,705,260);rich(s,[normal('打造关键领域领军人才高地')],727,248,437,18.6,1.36);
  dotBullet(s,705,290);rich(s,[normal('强化'),red('青年力量源头储备和早期支持'),normal('，塑造企业基础研究内生动力')],727,278,437,18.6,1.36);
  dotBullet(s,705,420);rich(s,[normal('此阶段研发风险降低，人才更能出成果，注重'),red('支持科研骨干、青年科技人才挑大梁、当主角')],727,408,437,18.6,1.36);
  dotBullet(s,705,572);rich(s,[normal('以研发人才为主向'),red('科研管理、科研服务人才并重'),normal('转变')],727,560,437,18.6,1.36);
  dotBullet(s,705,630);rich(s,[normal('各类科研相关人才紧密配合')],727,618,437,18.6,1.36);
  footer(s);return s;
}

export function buildDPages(deck){return [buildD4(deck),buildD6(deck)];}
