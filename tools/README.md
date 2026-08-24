# tools

## gen-reference-sheets.py

Classic Blood 시트와 같은 포맷의 **실사 참고 시트(SVG)** 생성기입니다.
실제 유닛 사진 위에 Citadel / Vallejo 도료를 짝으로 표기합니다.

```bash
python3 tools/gen-reference-sheets.py
```

저장소 루트에서 실행하면 아래 파일이 갱신됩니다.

| 출력 | 사진 |
|---|---|
| `slaves-to-darkness-paint-guide/images/scheme-a-pale-steel-reference-sheet.svg` | `unit-chaos-warriors-01.jpg` |
| `slaves-to-darkness-paint-guide/images/scheme-b-dark-gunmetal-reference-sheet.svg` | `unit-chaos-knights-01.jpg` |
| `slaves-to-darkness-paint-guide/images/unit-chaos-warriors-reference-sheet.svg` | `unit-chaos-warriors-01.jpg` |
| `slaves-to-darkness-paint-guide/images/unit-chaos-knights-reference-sheet.svg` | `unit-chaos-knights-01.jpg` |
| `slaves-to-darkness-paint-guide/images/unit-chaos-chariot-a-pale-steel-reference-sheet.svg` | 자동 인식 |
| `slaves-to-darkness-paint-guide/images/unit-chaos-chariot-b-dark-gunmetal-reference-sheet.svg` | 자동 인식 |
| `slaves-to-darkness-paint-guide/images/unit-chaos-lord-reference-sheet.svg` | 자동 인식 |
| `slaves-to-darkness-paint-guide/images/unit-chaos-lord-karkadrak-reference-sheet.svg` | 자동 인식 |
| `world-eaters-classic-blood/images/unit-chaos-rhino-reference-sheet.svg` | 자동 인식 |
| `world-eaters-classic-blood/images/unit-forgefiend-reference-sheet.svg` | 자동 인식 |

## 사진 자리를 채우려면

파일을 아래 이름으로 폴더에 넣고 스크립트를 다시 실행하면 끝입니다. **다른 수정은 필요 없습니다** —
사진 유무, 픽셀 크기, 하단 디테일 크롭 좌표를 스크립트가 알아서 잡습니다. 사진이 없으면
같은 레이아웃에 "사진 자리" 플레이스홀더가 들어갑니다.

| 유닛 | 넣을 위치와 파일명 |
|---|---|
| Chaos Lord | `slaves-to-darkness-paint-guide/images/photo-chaos-lord.jpg` |
| Chaos Lord on Karkadrak | `slaves-to-darkness-paint-guide/images/photo-chaos-lord-karkadrak.jpg` |
| Chaos Chariot | `slaves-to-darkness-paint-guide/images/photo-chaos-chariot.jpg` |
| Chaos Rhino | `world-eaters-classic-blood/images/photo-chaos-rhino.jpg` |
| Forgefiend | `world-eaters-classic-blood/images/photo-forgefiend.jpg` |

확장자는 `.jpg` `.jpeg` `.png` `.webp` 모두 인식합니다.

### 사진 조건

- **흰색 또는 아주 밝은 배경**이 가장 잘 맞습니다. 시트가 `mix-blend-mode: multiply`로 합성하기 때문에
  흰 배경은 크림색 바탕에 자연스럽게 녹아듭니다. 어두운 배경 사진은 검은 사각형처럼 보입니다.
- 정사각형에 가까운 비율이 좋습니다. 배치 칸이 940×700입니다.
- 가로 1000px 이상을 권장합니다. 하단 디테일 크롭이 원본을 확대해 쓰기 때문입니다.

### 크롭 위치를 직접 고르고 싶다면

자동 크롭은 중앙 영역을 3×2로 샘플링합니다. 특정 부위(어깨판, 아이콘, 배기구 등)를 지정하려면
`auto_crops(nat)` 자리에 원본 픽셀 좌표 `(sx, sy, sw, sh)` 6개를 직접 넘기세요.

```python
[(300, 40, 190, 155), (150, 175, 190, 155), (515, 140, 190, 155),
 (320, 300, 190, 155), (745, 375, 190, 155), (355, 645, 190, 155)]
```

> 사진은 base64로 SVG 안에 embed되므로 파일 하나로 완결됩니다. 일부 뷰어(GitHub 웹)는
> SVG 내부 embed 이미지를 차단할 수 있으니, 웹에서 확인할 때는 PNG로 내보내 쓰세요.
