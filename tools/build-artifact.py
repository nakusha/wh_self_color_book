# -*- coding: utf-8 -*-
import pathlib, re
import os, sys
# 기본 출력: build/scheme-ab.html. 첫 번째 인자로 경로를 넘기면 그곳에 쓴다.
OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "build/scheme-ab.html")
OUT.parent.mkdir(parents=True, exist_ok=True)
STD = "slaves-to-darkness-paint-guide/images/"
WE = "world-eaters-classic-blood/images/"

def svg(p, tag):
    s = pathlib.Path(p).read_text(encoding="utf-8")
    s = re.sub(r'\swidth="\d+"\s+height="\d+"', ' ', s, count=1)
    for i in ("bg", "gloss"):
        s = s.replace(f'id="{i}"', f'id="{i}-{tag}"').replace(f'url(#{i})', f'url(#{i}-{tag})')
    s = re.sub(r'id="cr(\d+)"', rf'id="cr\1-{tag}"', s)
    s = re.sub(r'url\(#cr(\d+)\)', rf'url(#cr\1-{tag})', s)
    return s

HEAD = '''<meta charset="utf-8">
<title>Pale Steel & Dark Gunmetal</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Gowun+Batang:wght@400;700&family=IBM+Plex+Sans+KR:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
:root{--mat:#e6e3da;--plate:#fbfaf6;--rule:#cfc9ba;--text:#22252a;--muted:#5d646d;--dim:#858c95;
 --steel:#4d6377;--blood:#8e2b2b;--brass:#7d6226;--shadow:0 20px 46px -22px rgba(40,36,28,.42);--maxw:1420px}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
 --mat:#101215;--plate:#1a1d22;--rule:#2b3038;--text:#e9e7e1;--muted:#98a0aa;--dim:#6d757f;
 --steel:#8fa6b8;--blood:#b04b45;--brass:#b3924f;--shadow:0 26px 60px -22px rgba(0,0,0,.85)}}
:root[data-theme="dark"]{--mat:#101215;--plate:#1a1d22;--rule:#2b3038;--text:#e9e7e1;--muted:#98a0aa;
 --dim:#6d757f;--steel:#8fa6b8;--blood:#b04b45;--brass:#b3924f;--shadow:0 26px 60px -22px rgba(0,0,0,.85)}
*{box-sizing:border-box}
body{margin:0;background:var(--mat);color:var(--text);font-family:"IBM Plex Sans KR",system-ui,
 -apple-system,"Apple SD Gothic Neo",sans-serif;font-weight:300;line-height:1.7;-webkit-font-smoothing:antialiased}
.wrap{max-width:var(--maxw);margin:0 auto;padding:0 clamp(18px,4vw,52px)}
header.top{padding:clamp(52px,8vw,110px) 0 clamp(30px,4vw,54px);border-bottom:1px solid var(--rule)}
.eyebrow{font-family:"IBM Plex Mono",monospace;font-size:12px;letter-spacing:.22em;text-transform:uppercase;
 color:var(--dim);margin:0 0 18px}
h1{font-family:"Gowun Batang",Georgia,serif;font-weight:700;margin:0;font-size:clamp(38px,6.4vw,76px);
 line-height:1.04;letter-spacing:-.01em;text-wrap:balance}
h1 .sep{color:var(--dim);font-weight:400}
.lede{max-width:62ch;margin:22px 0 0;font-size:clamp(15px,1.25vw,17.5px);color:var(--muted)}
.lede strong{color:var(--text);font-weight:500}
nav.jump{display:flex;flex-wrap:wrap;gap:10px;margin-top:30px}
nav.jump a{font-family:"IBM Plex Mono",monospace;font-size:12.5px;letter-spacing:.06em;text-decoration:none;
 color:var(--muted);border:1px solid var(--rule);border-radius:999px;padding:7px 15px;
 transition:border-color .18s,color .18s,background .18s}
nav.jump a:hover,nav.jump a:focus-visible{color:var(--text);border-color:var(--steel);
 background:color-mix(in oklab,var(--steel) 12%,transparent)}
:focus-visible{outline:2px solid var(--steel);outline-offset:3px}
section{padding:clamp(46px,6vw,86px) 0;border-bottom:1px solid var(--rule)}
.shead{display:flex;align-items:baseline;gap:18px;flex-wrap:wrap;margin:0 0 8px}
.tag{font-family:"IBM Plex Mono",monospace;font-size:11.5px;letter-spacing:.2em;text-transform:uppercase;
 padding:4px 11px;border-radius:4px;border:1px solid currentColor}
.tag.a{color:var(--steel)}.tag.b{color:var(--blood)}.tag.p{color:var(--brass)}
h2{font-family:"Gowun Batang",Georgia,serif;font-weight:700;margin:0;font-size:clamp(26px,3.4vw,42px);
 line-height:1.14;letter-spacing:-.005em}
h3{font-family:"Gowun Batang",Georgia,serif;font-weight:700;margin:38px 0 4px;font-size:clamp(19px,2vw,25px)}
.sub{margin:6px 0 30px;color:var(--muted);max-width:66ch;font-size:15.5px}
.plate{background:var(--plate);border:1px solid var(--rule);border-radius:6px;padding:clamp(10px,1.6vw,22px);
 box-shadow:var(--shadow);overflow-x:auto}
.plate svg{display:block;width:100%;height:auto;min-width:760px}
figure{margin:0}
figcaption{margin-top:14px;font-family:"IBM Plex Mono",monospace;font-size:12px;letter-spacing:.05em;color:var(--dim)}
.stack{display:flex;flex-direction:column;gap:clamp(24px,3vw,40px)}
table{width:100%;border-collapse:collapse;margin-top:30px;font-size:15px;font-variant-numeric:tabular-nums}
caption{text-align:left;font-family:"IBM Plex Mono",monospace;font-size:11.5px;letter-spacing:.2em;
 text-transform:uppercase;color:var(--dim);padding-bottom:12px}
th,td{text-align:left;padding:13px 16px;border-bottom:1px solid var(--rule);vertical-align:top}
thead th{font-weight:500;font-size:12.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
thead th.a{color:var(--steel)}thead th.b{color:var(--blood)}
tbody th{font-weight:400;color:var(--muted);width:20%}
.tblwrap{overflow-x:auto}
.chip{display:inline-block;width:11px;height:11px;border-radius:3px;margin-right:7px;
 border:1px solid #0003;vertical-align:-1px}
.note{border-left:2px solid var(--brass);padding:2px 0 2px 18px;margin:30px 0 0;color:var(--muted);
 font-size:15px;max-width:68ch}
.note strong{color:var(--text);font-weight:500}
ul.plain{margin:16px 0 0;padding:0;list-style:none;color:var(--muted);font-size:15px}
ul.plain li{padding-left:18px;position:relative;margin-bottom:7px}
ul.plain li::before{content:"";position:absolute;left:0;top:.72em;width:6px;height:6px;border-radius:50%;
 background:var(--dim)}
code{font-family:"IBM Plex Mono",monospace;font-size:.9em;color:var(--text);
 background:color-mix(in oklab,var(--rule) 55%,transparent);padding:2px 6px;border-radius:3px}
footer{padding:44px 0 70px;color:var(--dim);font-size:13.5px}
@media (prefers-reduced-motion:reduce){*{transition:none!important;animation:none!important}}
</style>'''

ROWS = [("프라이머","Leadbelcher Spray / Surface Primer Gunmetal","Chaos Black / Surface Primer Black"),
        ("작업 방향","Top-down — 밝은 상태에서 어둡게 눌러 내려감","Bottom-up — 어두운 상태에서 밝혀 올라감"),
        ("갑옷 3단계 (Citadel)","Leadbelcher → Ironbreaker → Runefang Steel","Abaddon Black → Corvus Black → Eshin Grey"),
        ("갑옷 3단계 (Vallejo)","Gunmetal → Chainmail Silver → Silver","Black → Charcoal → Neutral Grey"),
        ("셰이드","Nuln Oil / Game Wash Black — 판 경계에만","Nuln Oil / Game Wash Black — 홈 정리"),
        ("천","Khorne Red / Gory Red — 은색 사이 유일한 색","Khorne Red / Gory Red — 검정 위 포인트"),
        ("베이스","Mournfang Brown / Earth — 마른 갈색 흙","Eshin Grey / Charcoal — 차가운 회색"),
        ("관건","wash 조절. 진하면 갑옷이 탁한 회색이 됨","엣지 면적. 넓으면 회색 갑옷이 됨"),
        ("전군 도색 속도","빠름 — 프라이머가 곧 basecoat","보통 — basecoat를 따로 올림")]

WE_ROWS = [("Primer","#9c2020","Mephiston Red Spray","Red Surface Primer"),
           ("Red Shadow","#5c1414","Khorne Red","Nocturnal Red"),
           ("Shade","#2b0909","Berserker Bloodshade","Game Wash Red"),
           ("Re-layer","#9c2020","Mephiston Red","Scarlet Blood"),
           ("Highlight","#c0392b","Evil Sunz Scarlet","Bloody Red"),
           ("Extreme","#e0632f","Wild Rider Red","Hot Orange"),
           ("Trim","#7a5c2e","Balthasar Gold","Brassy Brass"),
           ("Trim Layer","#b08d4f","Sycorax Bronze","Bright Bronze"),
           ("Metal Under","#1e2124","Abaddon Black","Black"),
           ("Metal","#4f5459","Leadbelcher","Gunmetal"),
           ("Bone","#ded3b0","Ushabti Bone","Bonewhite"),
           ("Glow","#e8862a","Fire Dragon Bright","Orange Fire")]

def fig(path, tag, cap):
    return f'<figure><div class="plate">{svg(path, tag)}</div><figcaption>{cap}</figcaption></figure>'

tr = "".join(f'<tr><th scope="row">{k}</th><td>{a}</td><td>{b}</td></tr>' for k, a, b in ROWS)
wetr = "".join(f'<tr><th scope="row"><span class="chip" style="background:{h}"></span>{r}</th>'
               f'<td><code>{h}</code></td><td>{c}</td><td>{v}</td></tr>' for r, h, c, v in WE_ROWS)

html = f'''{HEAD}
<div class="wrap">
<header class="top">
  <p class="eyebrow">Warhammer Self Color Book</p>
  <h1>Pale Steel <span class="sep">/</span> Dark Gunmetal</h1>
  <p class="lede">Slaves to Darkness를 두 스킴으로 정리한 참고 시트와, 실제 도색 사진에서
  <strong>픽셀 단위로 추출한 색</strong>으로 만든 Chaos 차량 시트입니다. 모든 스와치에
  Citadel과 Vallejo 도료를 짝으로 표기했습니다.</p>
  <nav class="jump" aria-label="바로가기">
    <a href="#a">A안 Pale Steel</a><a href="#b">B안 Dark Gunmetal</a><a href="#compare">비교표</a>
    <a href="#units">캐릭터 · 전차</a><a href="#we">World Eaters 프라이밍</a>
  </nav>
</header>

<section id="a">
  <div class="shead"><span class="tag a">A안</span><h2>Pale Steel</h2></div>
  <p class="sub">밝게 닦인 강철 판금. 갑옷이 주인공이고, 짙은 적색 천·검은 털·갈색 흙 베이스가
  그 밝기를 감싸는 어두운 액자 역할을 합니다.</p>
  {fig(STD + "scheme-a-pale-steel-reference-sheet.svg", "A", "scheme-a-pale-steel-reference-sheet.svg")}
  <ul class="plain">
    <li>금속 프라이머가 basecoat를 겸하므로 전군 도색이 가장 빠릅니다.</li>
    <li>완성도는 하이라이트가 아니라 <strong>판 경계의 어둠</strong>이 결정합니다.</li>
    <li><code>Silver</code>는 면이 아니라 선과 점으로만 씁니다.</li>
  </ul>
</section>

<section id="b">
  <div class="shead"><span class="tag b">B안</span><h2>Dark Gunmetal</h2></div>
  <p class="sub">검게 눌린 철갑. 프라이머가 그대로 그림자가 되고, 모서리만 좁게 밝혀
  형태를 읽히게 합니다.</p>
  {fig(STD + "scheme-b-dark-gunmetal-reference-sheet.svg", "B", "scheme-b-dark-gunmetal-reference-sheet.svg")}
  <ul class="plain">
    <li>회색 하이라이트가 전체 면의 5~10%를 넘으면 회색 갑옷이 됩니다.</li>
    <li>청동 trim과 적색 천의 대비가 A안보다 훨씬 강하게 살아납니다.</li>
  </ul>
</section>

<section id="compare">
  <div class="shead"><h2>어느 쪽을 고를까</h2></div>
  <p class="sub">나머지 부위(청동, 뼈, 가죽, 털)는 두 안이 같습니다. 실제로 바뀌는 것은
  갑옷 3단계와 베이스뿐입니다.</p>
  <div class="tblwrap"><table><caption>스킴 비교</caption>
    <thead><tr><th scope="col">항목</th><th scope="col" class="a">A안 · Pale Steel</th>
    <th scope="col" class="b">B안 · Dark Gunmetal</th></tr></thead><tbody>{tr}</tbody></table></div>
  <p class="note"><strong>한 부대에 두 안을 섞지 마세요.</strong> 갑옷 밝기가 부대의 인상을 결정하기 때문에,
  섞으면 같은 군대로 보이지 않습니다. 기준 모델 한 명을 먼저 완성해 실제 조명 아래에서 보고
  결정하는 편이 가장 확실합니다.</p>
</section>

<section id="units">
  <div class="shead"><span class="tag b">B안 적용</span><h2>캐릭터와 전차</h2></div>
  <p class="sub">보내주신 사진이 모두 검은 갑옷이라 B안 Dark Gunmetal 팔레트로 연결했습니다.
  Chariot은 요청하신 대로 A안 버전도 함께 만들어 두었습니다.</p>
  <div class="stack">
    {fig(STD + "unit-chaos-lord-reference-sheet.svg", "L", "unit-chaos-lord-reference-sheet.svg")}
    {fig(STD + "unit-chaos-lord-karkadrak-reference-sheet.svg", "K", "unit-chaos-lord-karkadrak-reference-sheet.svg")}
    {fig(STD + "unit-chaos-chariot-b-dark-gunmetal-reference-sheet.svg", "C", "unit-chaos-chariot-b-dark-gunmetal-reference-sheet.svg")}
  </div>
</section>

<section id="we">
  <div class="shead"><span class="tag p">World Eaters</span><h2>Classic Blood — 붉은 차량</h2></div>
  <p class="sub">범례는 <strong>Classic Blood</strong> 그대로 두고, 사진을 그 색에 맞췄습니다.
  Rhino는 실제 붉은 도색 사진이고, Forgefiend는 원본을 범례 색으로 리컬러한 시뮬레이션입니다.
  갑옷만 붉게 바꾸고 브라스 trim·강철 무기·트랙은 각자의 재질로 남겼습니다.</p>
  <div class="stack">
    {fig(WE + "unit-chaos-rhino-reference-sheet.svg", "R", "unit-chaos-rhino-reference-sheet.svg")}
    {fig(WE + "unit-forgefiend-reference-sheet.svg", "F", "unit-forgefiend-reference-sheet.svg")}
  </div>
  <h3>Classic Blood 범례</h3>
  <div class="tblwrap"><table><caption>Citadel / Vallejo 도료 짝</caption>
    <thead><tr><th scope="col">역할</th><th scope="col">색</th><th scope="col">Citadel</th>
    <th scope="col">Vallejo</th></tr></thead><tbody>{wetr}</tbody></table></div>
  <p class="note"><strong>컬러 프라이머는 순서를 뒤집습니다.</strong> 검은 프라이머는 어두운 상태에서
  밝혀 올라가지만, Mephiston Red는 이미 밝은 상태에서 시작합니다. 그래서 하이라이트가 아니라
  <code>Khorne Red</code> 글레이즈로 <strong>먼저 어둡게 까는 단계</strong>가 들어갑니다.</p>
  <h3>셰이드 · 핀워시 · 글레이즈</h3>
  <p class="sub">셋 다 묽은 도료를 올리는 작업이라 가장 많이 헷갈립니다. 차이는 하나,
  <strong>도료를 어디로 흘러가게 두느냐</strong>입니다.</p>
  <div class="tblwrap"><table><caption>세 가지의 차이</caption>
  <thead><tr><th scope="col"></th><th scope="col">셰이드</th><th scope="col">핀워시</th>
  <th scope="col">글레이즈</th></tr></thead><tbody>
  <tr><th scope="row">하는 일</th><td>홈 전체를 한 번에 어둡게</td><td>선 하나만 어둡게</td>
  <td>넓은 면의 색 자체를 이동</td></tr>
  <tr><th scope="row">농도</th><td>원액 그대로</td><td>셰이드 1 : 물 1</td><td>도료 1 : 물 2~3</td></tr>
  <tr><th scope="row">올리는 법</th><td>붓에 머금어 떨어뜨림</td><td>붓끝을 선에 대고 흘려보냄</td>
  <td>넓게 여러 번, 경계 없이</td></tr>
  <tr><th scope="row">차량에</th><td>넓은 면은 얼룩 — 금지</td><td>패널 라인에 사용</td>
  <td>패널 하단에 사용</td></tr>
  </tbody></table></div>
  <p class="note"><strong>셰이드는 덮는 것, 핀워시는 긋는 것, 글레이즈는 물들이는 것.</strong>
  차량의 넓은 면에 셰이드를 덮으면 마르면서 안료가 가장자리로 밀려 테두리 자국이 남습니다.
  보병에서 통하던 &ldquo;전체 wash&rdquo;가 차량에서 실패하는 이유입니다.</p>
</section>

<footer>사진은 Warhammer Community 공개 이미지를 로컬 참고용으로 저장한 것이며, 저작권은
Games Workshop Limited에 있습니다. 공개 배포 시에는 직접 촬영 이미지로 교체하세요.</footer>
</div>'''
OUT.write_text(html, encoding="utf-8")
print("wrote", OUT, f"{OUT.stat().st_size//1024}KB")
