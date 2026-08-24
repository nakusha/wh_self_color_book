# -*- coding: utf-8 -*-
"""Classic Blood 시트와 같은 포맷의 실사 참고 시트 생성기.
실제 유닛 사진 + Citadel / Vallejo 스와치."""
import base64, pathlib

SER = "Georgia,'Times New Roman','Nanum Myeongjo',serif"
SAN = "'Helvetica Neue',Helvetica,Arial,'Apple SD Gothic Neo',sans-serif"

W, H = 1540, 1088
CREAM_A, CREAM_B = "#f7f4ec", "#e7e1d4"
RULE = "#c8bda6"
BODY = "#2c2a26"
SUB = "#6a6459"

def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def txt(x, y, s, size=15, fill=BODY, weight=400, fam=SER, anchor="start", ls=0, style="normal"):
    return (f'<text x="{x}" y="{y}" font-family="{fam}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}" letter-spacing="{ls}" font-style="{style}">{esc(s)}</text>')

MIME = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".webp": "image/webp"}

def b64(p):
    p = pathlib.Path(p)
    return f"data:{MIME.get(p.suffix.lower(), 'image/jpeg')};base64," + \
        base64.b64encode(p.read_bytes()).decode()

def imgsize(p):
    """PNG / JPEG 픽셀 크기를 표준 라이브러리만으로 읽는다."""
    import struct
    d = pathlib.Path(p).read_bytes()
    if d[:8] == b"\x89PNG\r\n\x1a\n":
        w, h = struct.unpack(">II", d[16:24])
        return int(w), int(h)
    if d[:2] == b"\xff\xd8":
        i = 2
        while i < len(d) - 9:
            if d[i] != 0xFF:
                i += 1
                continue
            m = d[i + 1]
            if m in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
                h, w = struct.unpack(">HH", d[i + 5:i + 9])
                return int(w), int(h)
            if m == 0xD8 or 0xD0 <= m <= 0xD9:
                i += 2
                continue
            i += 2 + struct.unpack(">H", d[i + 2:i + 4])[0]
    raise ValueError(f"크기를 읽을 수 없는 이미지: {p} (JPEG/PNG만 지원)")

def find_photo(folder, stem):
    """images/ 폴더에서 photo-<stem>.(jpg|jpeg|png|webp) 를 찾는다."""
    for ext in (".jpg", ".jpeg", ".png", ".webp"):
        f = pathlib.Path(folder) / f"photo-{stem}{ext}"
        if f.exists():
            return f
    return None

# 사진별 모델 영역 (x, y, w, h) — 흰 배경을 제외하고 실측한 값
BBOX = {
    "photo-chaos-rhino":         (32, 226, 841, 529),
    "photo-chaos-rhino-red":     (88, 266, 718, 382),
    "photo-forgefiend":          (54, 95, 786, 688),
    "photo-forgefiend-red":      (54, 95, 786, 688),
    "photo-chaos-lord":          (182, 150, 443, 578),
    "photo-chaos-lord-karkadrak": (247, 147, 394, 558),
    "photo-chaos-chariot":       (169, 232, 516, 405),
}

def auto_crops(nat, n=6, photo=None):
    """디테일 크롭 좌표를 자동 생성 — 중앙 영역을 3x2로 샘플링."""
    nw, nh = nat
    bx, by, bw, bh = BBOX.get(pathlib.Path(photo).stem, None) or (
        int(nw * .18), int(nh * .18), int(nw * .64), int(nh * .64)) if photo else (
        int(nw * .18), int(nh * .18), int(nw * .64), int(nh * .64))
    # 모델 영역 안에서 3x2로 샘플링. 칸 비율은 시트 타일과 같은 185:150.
    cw = int(bw / 2.6)
    ch = int(cw * 150 / 185)
    if ch > bh / 2.1:
        ch = int(bh / 2.1)
        cw = int(ch * 185 / 150)
    xs = [bx + int((bw - cw) * f) for f in (0.0, 0.5, 1.0)]
    ys = [by + int((bh - ch) * f) for f in (0.18, 0.72)]
    return [(x, y, cw, ch) for y in ys for x in xs][:n]


def crop(uid, img, nat, src, dst, radius=3, frame=True):
    """src=(sx,sy,sw,sh) 원본 좌표, dst=(x,y,w,h) 배치 좌표."""
    nw, nh = nat
    sx, sy, sw, sh = src
    x, y, w, h = dst
    k = max(w / sw, h / sh)
    ix, iy = x - sx * k, y - sy * k
    o = [f'<clipPath id="{uid}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}"/></clipPath>']
    o += [f'<g clip-path="url(#{uid})"><image href="{img}" x="{ix:.1f}" y="{iy:.1f}" '
          f'width="{nw*k:.1f}" height="{nh*k:.1f}" preserveAspectRatio="none"/></g>']
    if frame:
        o += [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="none" '
              f'stroke="{RULE}" stroke-width="1.4"/>']
    return "".join(o)

def swatch(x, y, hexv, role, citadel, vallejo, anchor="start", accent="#8a1f1f"):
    """원형 스와치 + 역할명 + Citadel / Vallejo 짝."""
    cx = x + 28 if anchor == "start" else x - 28
    tx = x + 70 if anchor == "start" else x - 70
    o = [f'<circle cx="{cx}" cy="{y}" r="27" fill="{hexv}"/>',
         f'<circle cx="{cx}" cy="{y}" r="27" fill="url(#gloss)"/>',
         f'<circle cx="{cx}" cy="{y}" r="27" fill="none" stroke="#00000026" stroke-width="1"/>']
    o += [txt(tx, y - 9, role.upper(), 16.5, BODY, 700, SER, anchor, 1.6)]
    o += [txt(tx, y + 12, citadel, 14.5, SUB, 400, SER, anchor)]
    o += [txt(tx, y + 31, ("/ " + vallejo) if anchor == "start" else (vallejo + " /"), 14.5, SUB, 400, SER, anchor)]
    x1 = x if anchor == "start" else x - 250
    o += [f'<line x1="{x1}" y1="{y+48}" x2="{x1+250}" y2="{y+48}" stroke="{RULE}" stroke-width="1" opacity=".75"/>']
    return "".join(o)

def ornament(cx, cy, accent):
    o = [f'<line x1="{cx-190}" y1="{cy}" x2="{cx-22}" y2="{cy}" stroke="{RULE}" stroke-width="1.4"/>',
         f'<line x1="{cx+22}" y1="{cy}" x2="{cx+190}" y2="{cy}" stroke="{RULE}" stroke-width="1.4"/>',
         f'<circle cx="{cx}" cy="{cy}" r="9" fill="none" stroke="{accent}" stroke-width="2"/>',
         f'<circle cx="{cx}" cy="{cy}" r="3.4" fill="{accent}"/>']
    for i in range(8):
        import math
        a = math.radians(i * 45)
        o += [f'<line x1="{cx+9*math.cos(a):.1f}" y1="{cy+9*math.sin(a):.1f}" '
              f'x2="{cx+15*math.cos(a):.1f}" y2="{cy+15*math.sin(a):.1f}" stroke="{accent}" stroke-width="1.8"/>']
    return "".join(o)

def sheet(out, title, accent, photo, nat, photo_label, left, right, crops, caption, footer,
          photo_box=(300, 172, 940, 674), photo_slot_hint=""):
    img = b64(photo) if photo else None
    px, py, pw, ph = photo_box
    # 모델 영역(BBOX)을 알면 그 영역이 프레임을 채우도록 확대 배치한다.
    bb = BBOX.get(pathlib.Path(photo).stem) if photo else None
    if bb:
        bx, by, bw, bh = bb
        pad = 0.05 * max(bw, bh)
        tx, ty, tw, th = bx - pad, by - pad, bw + 2 * pad, bh + 2 * pad
        k = min(pw / tw, ph / th)
        iw, ih = nat[0] * k, nat[1] * k
        ix = px + pw / 2 - (tx + tw / 2) * k
        iy = py + ph / 2 - (ty + th / 2) * k
    else:
        k = min(pw / nat[0], ph / nat[1])
        iw, ih = nat[0] * k, nat[1] * k
        ix, iy = px + (pw - iw) / 2, py + (ph - ih) / 2
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
         f'viewBox="0 0 {W} {H}" width="{W}" height="{H}">']
    o += [f'<defs><linearGradient id="bg" x1="0" y1="0" x2="0.3" y2="1">'
          f'<stop offset="0" stop-color="{CREAM_A}"/><stop offset="1" stop-color="{CREAM_B}"/>'
          f'</linearGradient>'
          f'<radialGradient id="gloss" cx="34%" cy="26%" r="80%">'
          f'<stop offset="0" stop-color="#ffffff" stop-opacity=".40"/>'
          f'<stop offset=".62" stop-color="#ffffff" stop-opacity="0"/>'
          f'<stop offset="1" stop-color="#000000" stop-opacity=".34"/></radialGradient></defs>']
    o += [f'<rect width="{W}" height="{H}" fill="url(#bg)"/>']
    o += [f'<rect x="14" y="14" width="{W-28}" height="{H-28}" fill="none" stroke="{RULE}" '
          f'stroke-width="1.2" opacity=".7"/>']
    o += [txt(W / 2, 84, title, 50, accent, 700, SER, "middle", 5)]
    o += [ornament(W / 2, 112, accent)]
    o += [txt(W / 2, 152, photo_label, 22, accent, 700, SER, "middle", 3)]
    if img:
        o += [f'<clipPath id="photoClip"><rect x="{px}" y="{py}" width="{pw}" height="{ph}"/></clipPath>']
        o += [f'<g clip-path="url(#photoClip)" style="mix-blend-mode:multiply">'
              f'<image href="{img}" x="{ix:.1f}" y="{iy:.1f}" '
              f'width="{iw:.1f}" height="{ih:.1f}"/></g>']
    else:
        o += [f'<rect x="{px+70}" y="{py+30}" width="{pw-140}" height="{ph-60}" rx="6" fill="#00000006" '
              f'stroke="{RULE}" stroke-width="2" stroke-dasharray="10 8"/>']
        o += [txt(px + pw / 2, py + ph / 2 - 12, "사진 자리", 30, RULE, 700, SER, "middle", 4)]
        o += [txt(px + pw / 2, py + ph / 2 + 22, photo_slot_hint, 15, SUB, 400, SAN, "middle")]
    y0 = 208
    for i, s in enumerate(left):
        o += [swatch(40, y0 + i * 108, *s, anchor="start", accent=accent)]
    for i, s in enumerate(right):
        o += [swatch(W - 40, y0 + i * 108, *s, anchor="end", accent=accent)]
    # 하단 디테일 크롭
    tiles_l = [(40, 866, 185, 150), (232, 866, 185, 150), (424, 866, 185, 150)]
    tiles_r = [(925, 866, 185, 150), (1117, 866, 185, 150), (1309, 866, 185, 150)]
    for i, t in enumerate(tiles_l + tiles_r):
        if img and i < len(crops):
            o += [crop(f"cr{i}", img, nat, crops[i], t)]
        else:
            o += [f'<rect x="{t[0]}" y="{t[1]}" width="{t[2]}" height="{t[3]}" rx="3" fill="#00000006" '
                  f'stroke="{RULE}" stroke-width="1.2" stroke-dasharray="7 6"/>']
    o += [f'<rect x="625" y="866" width="290" height="150" fill="#00000008" stroke="{RULE}" '
          f'stroke-width="1.2" rx="3"/>']
    for j, ln in enumerate(caption):
        o += [txt(770, 896 + j * 21, ln, 14.5, BODY if j else accent, 400, SER, "middle")]
    o += [txt(W / 2, H - 26, footer, 13, SUB, 400, SAN, "middle", .4)]
    o += ["</svg>"]
    pathlib.Path(out).write_text("".join(o), encoding="utf-8")
    print("wrote", out, f"{pathlib.Path(out).stat().st_size//1024}KB")

if __name__ == "__main__":
    STD = pathlib.Path("slaves-to-darkness-paint-guide/images")
    warriors = STD / "unit-chaos-warriors-01.jpg"
    knights = STD / "unit-chaos-knights-01.jpg"

    A_LEFT = [
        ("#4c5257", "Primer",     "Leadbelcher Spray",   "Surface Primer Gunmetal"),
        ("#4f555a", "Steel Base", "Leadbelcher",          "Gunmetal"),
        ("#1a1d20", "Shade",      "Nuln Oil",             "Game Wash Black"),
        ("#6b5a3e", "Grime",      "Agrax Earthshade",     "Sepia Wash"),
        ("#8d959b", "Steel Layer","Ironbreaker",          "Chainmail Silver"),
        ("#c6cdd2", "Highlight",  "Runefang Steel",       "Silver"),
    ]
    A_RIGHT = [
        ("#e9ecec", "Extreme", "Stormhost Silver",  "Silver + Off White"),
        ("#a8853f", "Trim",    "Balthasar Gold",    "Brassy Brass"),
        ("#7a2222", "Cloth",   "Khorne Red",        "Gory Red"),
        ("#dcd0ac", "Bone",    "Ushabti Bone",      "Bonewhite"),
        ("#16181a", "Fur",     "Abaddon Black",     "Black"),
        ("#6a5340", "Base",    "Mournfang Brown",   "Earth"),
    ]
    B_LEFT = [
        ("#0d0e10", "Primer",     "Chaos Black",   "Surface Primer Black"),
        ("#1c1e21", "Armor Base", "Abaddon Black", "Black"),
        ("#34383c", "Armor Layer","Corvus Black",  "Charcoal"),
        ("#0f1113", "Shade",      "Nuln Oil",      "Game Wash Black"),
        ("#6e7479", "Highlight",  "Eshin Grey",    "Neutral Grey"),
        ("#9aa0a4", "Edge",       "Dawnstone",     "Neutral Grey + Bonewhite"),
    ]
    B_RIGHT = [
        ("#5b4423", "Trim Base",  "Warplock Bronze", "Tinny Tin"),
        ("#94743a", "Trim Layer", "Balthasar Gold",  "Brassy Brass"),
        ("#5e1b28", "Cloth",      "Khorne Red",      "Gory Red"),
        ("#c8bfa0", "Bone",       "Ushabti Bone",    "Bonewhite"),
        ("#4f555a", "Steel",      "Leadbelcher",     "Gunmetal"),
        ("#2f3336", "Base",       "Eshin Grey",      "Charcoal"),
    ]

    W_CROPS = [(300, 40, 190, 155), (150, 175, 190, 155), (515, 140, 190, 155),
               (320, 300, 190, 155), (745, 375, 190, 155), (355, 645, 190, 155)]
    K_CROPS = [(105, 125, 190, 155), (605, 45, 190, 155), (385, 360, 190, 155),
               (100, 520, 190, 155), (400, 555, 190, 155), (700, 640, 190, 155)]

    sheet(STD / "scheme-a-pale-steel-reference-sheet.svg",
          "A안 · Pale Steel", "#3f4750", warriors, (1000, 1000), "Chaos Warriors",
          A_LEFT, A_RIGHT, W_CROPS,
          ["밝게 닦인 강철 판금.", "낡은 청동 trim.", "짙은 적색 천.",
           "크림빛 뿔과 해골.", "검은 짐승 털.", "마른 갈색 흙 베이스."],
          "실제 유닛 사진 · Warhammer Community. 저작권은 Games Workshop Limited에 있으며 로컬 참고용입니다.")

    sheet(STD / "scheme-b-dark-gunmetal-reference-sheet.svg",
          "B안 · Dark Gunmetal", "#5c1b22", knights, (1000, 958), "Chaos Knights",
          B_LEFT, B_RIGHT, K_CROPS,
          ["검게 눌린 철갑.", "낡은 청동 trim.", "짙은 적색 천.",
           "따뜻한 뼈색 뿔.", "검은 말 털.", "차가운 회색 베이스."],
          "실제 유닛 사진 · Warhammer Community. 저작권은 Games Workshop Limited에 있으며 로컬 참고용입니다.")

    sheet(STD / "unit-chaos-warriors-reference-sheet.svg",
          "Chaos Warriors", "#3f4750", warriors, (1000, 1000), "A안 · Pale Steel 적용",
          A_LEFT, A_RIGHT, W_CROPS,
          ["판 중앙은 밝게,", "판 경계는 어둡게.", "Silver는 선과 점으로만.",
           "무기는 갑옷보다", "한 단계 어둡게.", "천은 유일한 색 포인트."],
          "기준 유닛 · 이 한 명을 먼저 완성한 뒤 같은 레시피를 전 부대에 반복하세요.")

    sheet(STD / "unit-chaos-knights-reference-sheet.svg",
          "Chaos Knights", "#5c1b22", knights, (1000, 958), "B안 · Dark Gunmetal 적용",
          B_LEFT, B_RIGHT, K_CROPS,
          ["말 갑옷은 기수보다", "한 단계 어둡게.", "시선은 lance 끝 →",
           "rider helmet 순서로.", "barding 큰 면에는", "마커를 쓰지 않습니다."],
          "큰 면과 돌격 방향의 유닛 · trim과 rivets만 마커로 초벌하고 나머지는 붓으로 완성하세요.")

    # ---- 사진이 아직 없는 유닛: 동일 포맷 + 사진 자리 ----
    WE = pathlib.Path("world-eaters-classic-blood/images")
    HINT = "이 폴더에 유닛 사진을 넣으면 같은 포맷으로 완성됩니다."

    # ---- Chaos Chariot : A안 / B안 두 장 ----
    ch_photo = find_photo(STD, "chaos-chariot")
    ch_nat = imgsize(ch_photo) if ch_photo else (1000, 1000)
    ch_crops = auto_crops(ch_nat, photo=ch_photo) if ch_photo else []
    for key, accent, L, R, lab in (("a-pale-steel", "#3f4750", A_LEFT, A_RIGHT,
                                    "A안 · Pale Steel 목표색 · 사진은 형태 참고"),
                                   ("b-dark-gunmetal", "#5c1b22", B_LEFT, B_RIGHT, "B안 · Dark Gunmetal 적용")):
        sheet(STD / f"unit-chaos-chariot-{key}-reference-sheet.svg",
              "Chaos Chariot", accent, ch_photo, ch_nat, lab, L, R, ch_crops,
              ["바퀴 스파이크와", "전차함 상단이 가장 밝게.", "짐승 털은 어둡게 두어",
               "전차를 띄웁니다.", "나무 창대와 가죽은", "채도를 낮게 유지."],
              "재질이 가장 많이 섞인 유닛 · 조립 전에 바퀴, 짐승, 전차함, 탑승자를 서브어셈블리로 나누세요.",
              photo_slot_hint=HINT)

    # ---- Chaos Lord (도보 / Karkadrak) : 사진이 검은 갑옷이라 B안 팔레트 ----
    for stem, title in (("chaos-lord", "Chaos Lord"),
                        ("chaos-lord-karkadrak", "Chaos Lord on Karkadrak")):
        ph = find_photo(STD, stem)
        nat = imgsize(ph) if ph else (1000, 1000)
        sheet(STD / f"unit-{stem}-reference-sheet.svg",
              title, "#5c1b22", ph, nat, "B안 · Dark Gunmetal 적용",
              B_LEFT, B_RIGHT, auto_crops(nat, photo=ph) if ph else [],
              ["계급은 밝기로 표현.", "엣지를 한 단계 더", "촘촘하게 넣습니다.",
               "시선점은 헬멧 주변.", "붉은 천과 청동이", "검정 위에서 가장 강합니다."],
              "캐릭터 모델 · 같은 레시피에서 엣지 밀도만 올려 부대와 계급 차이를 만드세요.",
              photo_slot_hint=HINT)

    # ---- World Eaters Classic Blood 범례 (Mephiston Red 프라이밍 기준) ----
    WE_LEFT = [
        ("#9c2020", "Primer",     "Mephiston Red Spray",  "Red Surface Primer"),
        ("#5c1414", "Red Shadow", "Khorne Red",           "Nocturnal Red"),
        ("#2b0909", "Shade",      "Berserker Bloodshade", "Game Wash Red"),
        ("#9c2020", "Re-layer",   "Mephiston Red",        "Scarlet Blood"),
        ("#c0392b", "Highlight",  "Evil Sunz Scarlet",    "Bloody Red"),
        ("#e0632f", "Extreme",    "Wild Rider Red",       "Hot Orange"),
    ]
    WE_RIGHT = [
        ("#7a5c2e", "Trim",        "Balthasar Gold",     "Brassy Brass"),
        ("#b08d4f", "Trim Layer",  "Sycorax Bronze",     "Bright Bronze"),
        ("#1e2124", "Metal Under", "Abaddon Black",      "Black"),
        ("#4f5459", "Metal",       "Leadbelcher",        "Gunmetal"),
        ("#ded3b0", "Bone",        "Ushabti Bone",       "Bonewhite"),
        ("#e8862a", "Glow",        "Fire Dragon Bright", "Orange Fire"),
    ]

    rh_photo = find_photo(WE, "chaos-rhino-red") or find_photo(WE, "chaos-rhino")
    rh_nat = imgsize(rh_photo) if rh_photo else (1000, 1000)
    sheet(WE / "unit-chaos-rhino-reference-sheet.svg",
          "Chaos Rhino", "#7a1d1d", rh_photo, rh_nat,
          "Classic Blood 완성 예",
          WE_LEFT, WE_RIGHT, auto_crops(rh_nat, photo=rh_photo) if rh_photo else [],
          ["패널 하단부터 어둡게.", "셰이드는 패널 라인만.", "금속 아래 검정 한 겹.",
           "칩은 부딪히는 모서리만.", "배기구는 녹 그라데이션.", "blood만 gloss."],
          "실제 도색 사진 · 좌우 범례는 Mephiston Red 프라이밍에서 이 결과까지 가는 순서입니다."
          if rh_photo else "사진 파일을 world-eaters-classic-blood/images/ 에 추가하면 동일 포맷으로 완성됩니다.",
          photo_slot_hint=HINT)

    ff_photo = find_photo(WE, "forgefiend-red") or find_photo(WE, "forgefiend")
    ff_nat = imgsize(ff_photo) if ff_photo else (1000, 1000)
    sheet(WE / "unit-forgefiend-reference-sheet.svg",
          "Forgefiend", "#7a1d1d", ff_photo, ff_nat,
          "Classic Blood 적용 시뮬레이션",
          WE_LEFT, WE_RIGHT, auto_crops(ff_nat, photo=ff_photo) if ff_photo else [],
          ["red는 카라페이스까지.", "다리와 포신은 금속.", "하부를 어둡게 눌러",
           "몸통을 크게 보이게.", "시선점은 아가리·포구·", "카라페이스 세 곳."],
          "원본 사진을 범례 색으로 리컬러한 시뮬레이션입니다 · tools/recolor-classic-blood.js"
          if ff_photo else "사진 파일을 world-eaters-classic-blood/images/ 에 추가하면 동일 포맷으로 완성됩니다.",
          photo_slot_hint=HINT)
