/**
 * Editable presentation primitives. All geometry and numeric font sizes are CSS px.
 * The group helper is a semantic composition scope, not a raster or a PPTX group.
 * It returns the native shapes it added, preserving each object's editability.
 */
import fs from 'node:fs/promises';
import { spawnSync } from 'node:child_process';

export const pxFromPt = pt => pt * 96 / 72;
export const ptFromPx = px => px * 72 / 96;
export const CANVAS = Object.freeze({ width: 1280, height: 720 });

export async function loadPalette(filePath) {
  const p = JSON.parse(await fs.readFile(filePath, 'utf8'));
  return Object.freeze({
    font: p.font,
    blue: `#${p.primary}`,
    white: `#${p.white}`,
    text: `#${p.text}`,
    orange: `#${p.orange}`,
    light: `#${p.tints.at(-1)}`,
    mid: `#${p.accents.find(c => c === '547FFE')}`,
    pale: `#${p.accents.find(c => c === 'C6D4FE')}`,
    gray: `#${p.accents.find(c => c === 'DCDCDC')}`,
    themeColors: {
      accent1:`#${p.primary}`,accent2:'#547FFE',accent3:'#8DAAFE',
      accent4:'#C6D4FE',accent5:'#B3D4FE',accent6:'#DCDCDC',
      bg1:`#${p.white}`,bg2:`#${p.tints.at(-1)}`,tx1:`#${p.text}`,tx2:`#${p.text}`,
      dk1:`#${p.text}`,dk2:`#${p.text}`,lt1:`#${p.white}`,lt2:`#${p.tints.at(-1)}`,
      hlink:`#${p.primary}`,folHlink:`#${p.primary}`,
    },
  });
}

/** Canonicalize exported package defaults that the current exporter reintroduces.
 * Uses only Python stdlib XML/ZIP editing. Does not rasterize or alter slide text.
 * Run before finalization, then reimport and render the finalized package.
 */
export function normalizePptxDefaults(candidatePath,{palette,pythonExecutable}) {
  const script=String.raw`
import sys,json,zipfile,xml.etree.ElementTree as E,pathlib,os
p=pathlib.Path(sys.argv[1]); config=json.loads(sys.argv[2]); font=config['font']; colors=config['colors']
A='http://schemas.openxmlformats.org/drawingml/2006/main'
P='http://schemas.openxmlformats.org/presentationml/2006/main'
R='http://schemas.openxmlformats.org/officeDocument/2006/relationships'
E.register_namespace('a',A);E.register_namespace('p',P);E.register_namespace('r',R)
effect_tags={'outerShdw','innerShdw','prstShdw','glow','softEdge','reflection','blur','scene3d','sp3d'}
records=[]; changed=0; patched=[]
with zipfile.ZipFile(p) as source:
 for info in source.infolist():
  data=source.read(info.filename)
  if info.filename.startswith('ppt/') and info.filename.endswith('.xml'):
   root=E.fromstring(data); count_fonts=0; count_effects=0; count_colors=0
   for el in root.iter():
    if el.tag.startswith('{'+A+'}') and 'typeface' in el.attrib:
     if el.attrib['typeface']!=font: count_fonts+=1
     el.set('typeface',font)
   for parent in root.iter():
    for el in list(parent):
     if el.tag.startswith('{'+A+'}') and el.tag.rsplit('}',1)[-1] in effect_tags:
      parent.remove(el);count_effects+=1
   for scheme in root.iter('{'+A+'}clrScheme'):
    scheme.set('name','CIIC canonical')
    for slot in list(scheme):
     role=slot.tag.rsplit('}',1)[-1]
     if role in colors:
      for child in list(slot):slot.remove(child)
      E.SubElement(slot,'{'+A+'}srgbClr',{'val':colors[role].lstrip('#').upper()});count_colors+=1
   if count_fonts or count_effects or count_colors:
    data=E.tostring(root,encoding='utf-8',xml_declaration=True);changed+=1
    records.append({'part':info.filename,'fonts_changed':count_fonts,'effects_removed':count_effects,'theme_roles_set':count_colors})
  patched.append((info,data))
tmp=p.with_name(p.name+'.normalized.tmp')
with zipfile.ZipFile(tmp,'w') as output:
 for info,data in patched:output.writestr(info,data)
os.replace(tmp,p)
audit=[]; bad_fonts=[];effects=[];bad_colors=[]
with zipfile.ZipFile(p) as check:
 for n in check.namelist():
  if n.startswith('ppt/') and n.endswith('.xml'):
   root=E.fromstring(check.read(n))
   for el in root.iter():
    if el.tag.startswith('{'+A+'}') and 'typeface' in el.attrib and el.attrib['typeface']!=font:bad_fonts.append([n,el.attrib['typeface']])
    if el.tag.startswith('{'+A+'}') and el.tag.rsplit('}',1)[-1] in effect_tags:effects.append([n,el.tag])
   for scheme in root.iter('{'+A+'}clrScheme'):
    roles={el.tag.rsplit('}',1)[-1]:list(el)[0].get('val') for el in scheme if len(el)}
    for role,value in roles.items():
     if value!=colors[role].lstrip('#').upper():bad_colors.append([n,role,value])
    audit.append({'part':n,'roles':roles,'fonts':sorted({el.get('typeface') for el in root.iter() if 'typeface' in el.attrib})})
result={'changed_parts':changed,'changes':records,'themes':audit,'invalid_fonts':bad_fonts,'effects_remaining':effects,'invalid_theme_colors':bad_colors}
print(json.dumps(result,ensure_ascii=False))
if bad_fonts or effects or bad_colors:sys.exit(2)
`;
  const r=spawnSync(pythonExecutable,['-B','-',candidatePath,JSON.stringify({font:palette.font,colors:palette.themeColors})],{input:script,encoding:'utf8',maxBuffer:1024*1024});
  if(r.status!==0)throw new Error(`PPTX default normalization failed: ${r.stderr||r.stdout}`);
  return JSON.parse(r.stdout);
}

/** One affine edge shared by every band of a staged review diagram. */
export function continuousSlope({bottomLeft,topRight}) {
  const [x0,y0]=bottomLeft,[x1,y1]=topRight;
  if(![x0,y0,x1,y1].every(Number.isFinite)||x1<=x0||y1>=y0)throw new Error('continuousSlope requires an upward right-hand stage edge');
  const xAt=y=>{if(y<y1||y>y0)throw new Error('Band boundary lies outside the stage edge');return x0+(y0-y)*(x1-x0)/(y0-y1);};
  return {xAt,angle:Math.atan2(y1-y0,x1-x0)*180/Math.PI,band:(top,bottom)=>{
    if(top>=bottom)throw new Error('Band top must precede its bottom');
    return [[xAt(top),top],[x1,top],[x1,bottom],[xAt(bottom),bottom]];
  }};
}

export function primitives(slide, palette) {
  let prefix = '';
  const name = n => prefix ? `${prefix}/${n}` : n;
  const shape = (n, geometry, x, y, w, h, fill='none', stroke='none', sw=0) =>
    slide.shapes.add({ name: name(n), geometry,
      position:{left:x,top:y,width:w,height:h}, fill,
      line:{style:'solid',fill:stroke,width:sw}, shadow:'shadow-none' });
  const rect = (n,x,y,w,h,fill='none',stroke='none',sw=0) => shape(n,'rect',x,y,w,h,fill,stroke,sw);
  function text(n, content, x,y,w,h, opts={}) {
    const t = shape(n,'textbox',x,y,w,h,opts.fill??'none');
    t.text = content;
    t.text.style = {
      typeface: palette.font, fontSize:opts.size??22, bold:opts.bold??false,
      color:opts.color??palette.text, alignment:opts.align??'left',
      verticalAlignment:opts.valign??'top', wrap:opts.wrap??'square',autoFit:'none',
      insets:0, lineSpacing:opts.lineSpacing??1.15,
    };
    return t;
  }
  function line(n,x1,y1,x2,y2,opts={}) {
    const x=Math.min(x1,x2),y=Math.min(y1,y2);
    return slide.shapes.add({ name:name(n),geometry:'custom',
      position:{left:x,top:y,width:Math.max(1,Math.abs(x2-x1)),height:Math.max(1,Math.abs(y2-y1))},
      fill:'none',line:{style:opts.style??'solid',fill:opts.color??palette.blue,width:opts.width??1.5},
      customPaths:[{width:Math.max(1,Math.abs(x2-x1)),height:Math.max(1,Math.abs(y2-y1)),commands:[
        {moveTo:{x:x1-x,y:y1-y}},{lineTo:{x:x2-x,y:y2-y}},
      ]}], shadow:'shadow-none' });
  }
  function polygon(n, points, fill=palette.blue, stroke='none', sw=0) {
    const xs=points.map(p=>p[0]),ys=points.map(p=>p[1]);
    const x=Math.min(...xs),y=Math.min(...ys),w=Math.max(...xs)-x,h=Math.max(...ys)-y;
    return slide.shapes.add({name:name(n),geometry:'custom',
      position:{left:x,top:y,width:w,height:h},fill,
      line:{style:'solid',fill:stroke,width:sw},shadow:'shadow-none',
      customPaths:[{width:w,height:h,commands:[
        {moveTo:{x:points[0][0]-x,y:points[0][1]-y}},
        ...points.slice(1).map(([px,py])=>({lineTo:{x:px-x,y:py-y}})),{close:{}},
      ]}],
    });
  }
  function group(n, build) {
    const before=slide.shapes.items.length,old=prefix;
    prefix=name(n); build(); prefix=old;
    return slide.shapes.items.slice(before);
  }
  function roof(n,x,y,w,h,label,opts={}) {
    return group(n,()=>{
      polygon('silhouette',[[x,y+h],[x+w/2,y],[x+w,y+h]],opts.fill??palette.blue);
      text('shared-goal',label,x+w*.14,y+h*.54,w*.72,h*.42,
        {size:opts.size??24,bold:true,color:palette.white,align:'center',valign:'middle'});
    });
  }
  function heading(title) {
    text('page-title',title,64,40,1152,84,{size:36,bold:true,color:palette.blue,lineSpacing:1.08});
    line('title-rule',64,130,1216,130,{width:2});
  }
  function label(n,label,x,y,w,h,opts={}) {
    return text(n,label,x,y,w,h,{size:24,bold:true,color:palette.blue,...opts});
  }
  /** A header frame whose lead and body start follow this page's real text.
   * Explicit heights/positions may be supplied when matching a reference.
   * It deliberately does not split source points or invent a fixed content grid.
   */
  function pageFrame({title,lead='',x=56,y=28,width=1168,titleSize=32,titleHeight,
    ruleY,leadSize=19,leadHeight,contentTop}={}) {
    if(!title)throw new Error('pageFrame requires a complete title');
    const th=titleHeight??Math.max(48,title.split('\n').length*titleSize*1.25+8);
    const ry=ruleY??y+th+20;
    text('page-title',title,x,y,width,th,{size:titleSize,bold:true,color:palette.blue,lineSpacing:1.08});
    line('title-rule',x,ry,x+width,ry,{width:1.5});
    let bodyTop=ry+28;
    if(lead){const lh=leadHeight??Math.max(30,lead.split('\n').length*leadSize*1.3+8);
      text('page-summary',lead,x,ry+18,width,lh,{size:leadSize,lineSpacing:1.16});
      bodyTop=ry+18+lh+24;
    }
    return {left:x,right:x+width,top:contentTop??bodyTop,bottom:674,width,height:674-(contentTop??bodyTop)};
  }
  /** Native text runs retain one paragraph and selectively emphasize its actions. */
  function richText(n,segments,x,y,w,h,opts={}) {
    const t=text(n,'',x,y,w,h,opts);
    t.text=[segments.map(v=>typeof v==='string'?{run:v,style:{typeface:palette.font}}:{run:v.text,
      style:{typeface:palette.font,fontSize:`${opts.size??22}px`,bold:v.bold??opts.bold??false,color:v.color??opts.color??palette.text}})];
    return t;
  }
  /** Layer label with one shared background and an explicit no-wrap text area.
   * Full code-point counts and a generous line-height allowance are conservative
   * preflight estimates, not a substitute for inspecting final imported renders.
   * Only authored newline characters create rows. The complete label is retained.
   * If it cannot fit at minSize, enlarge/rearrange the component instead of truncating.
   */
  function layerLabel(n,content,x,y,w,h,opts={}) {
    if(typeof content!=='string'||!content.trim())throw new Error(`layerLabel ${n}: a complete nonempty label is required`);
    const size=opts.size??22,minSize=opts.minSize??20;
    const padX=opts.paddingX??4,padY=opts.paddingY??4;
    if(![x,y,w,h,size,minSize,padX,padY].every(Number.isFinite)||w<=0||h<=0||size<=0||minSize<=0||padX<0||padY<0||minSize>size){
      throw new Error(`layerLabel ${n}: invalid dimensions, padding, or readable font-size range`);
    }
    const lines=content.replace(/\r\n?/g,'\n').split('\n');
    // Count every character, including spaces and punctuation. Non-BMP glyphs
    // receive two ems so emoji and symbols do not make the estimate optimistic.
    const lineUnits=lines.map(v=>Array.from(v).reduce((sum,ch)=>sum+(ch==='\t'?4:ch.codePointAt(0)>0xFFFF?2:1),0));
    const innerW=w-2*padX,innerH=h-2*padY;
    const widthPerPx=Math.max(1,...lineUnits)*1.04;
    const heightPerPx=lines.length*1.4;
    const fittedSize=Math.floor(Math.min(size,innerW/widthPerPx,innerH/heightPerPx)*2)/2;
    if(innerW<=0||innerH<=0||fittedSize<minSize){
      throw new Error(`layerLabel ${n}: complete label requires re-layout; ${w}x${h}px with ${padX}/${padY}px padding cannot fit ${lines.length} authored line(s) at the readable minimum ${minSize}px`);
    }
    let background,labelShape;
    const shapes=group(n,()=>{
      background=rect('background',x,y,w,h,opts.fill??palette.light);
      labelShape=text('text',lines.join('\n'),x+padX,y+padY,innerW,innerH,{
        size:fittedSize,bold:true,color:opts.color??palette.text,align:'center',
        valign:'middle',wrap:'none',lineSpacing:1.0,
      });
    });
    return {background,label:labelShape,shapes,fit:{requestedSize:size,fontSize:fittedSize,minSize,
      lineCount:lines.length,lineUnits,innerWidth:innerW,innerHeight:innerH,
      conservativeWidthPx:widthPerPx*fittedSize,conservativeHeightPx:heightPerPx*fittedSize}};
  }
  function bullet(n,content,x,y,w,h,opts={}) {
    rect(`${n}-mark`,x,y+9,7,7,opts.color??palette.blue);
    return text(n,content,x+18,y,w-18,h,{size:22,...opts});
  }
  function arrow(n,x1,y,x2,opts={}) {
    line(`${n}-shaft`,x1,y,x2-9,y,opts);
    polygon(`${n}-head`,[[x2-9,y-5],[x2,y],[x2-9,y+5]],opts.color??palette.blue);
  }
  return {shape,rect,text,line,polygon,group,roof,heading,label,pageFrame,richText,layerLabel,bullet,arrow};
}
