// 원본 사진을 Classic Blood 범례 색으로 리컬러한다.
// 범례는 그대로 두고 사진만 맞추는 용도. 재질별로 다르게 처리한다.
//
//   python3 tools/_devserver.py        # 127.0.0.1:8768, POST /save?path=... 로 결과 저장
//   그다음 브라우저 콘솔에서 이 파일을 실행
//
// 처리 규칙
//   1. 배경과 바닥 그림자 : 테두리에서 flood fill 로 분리해 건드리지 않는다.
//   2. 브라스/황동 (따뜻한 채색) : 그대로 둔다. Classic Blood 에서도 brass trim 이다.
//   3. 밝은 무채색 (도저 블레이드 등) : 그대로 둔다. 강철이다.
//   4. 아래쪽 어두운 부분 (트랙, 다리) : 명암만 눌러 어두운 금속으로 남긴다.
//   5. 나머지 = 갑옷 : 밝기를 Classic Blood 램프에 매핑한다.
//
// 4번의 경계는 yFade 구간에서 서서히 섞어 직선 자국이 생기지 않게 한다.
(async () => {
  // Khorne Red -> Mephiston Red -> Evil Sunz Scarlet -> Wild Rider Red
  const RED = [[0,18,4,4],[25,43,12,12],[45,74,17,17],[70,104,21,21],[100,140,27,27],
               [130,168,34,32],[165,200,58,42],[200,224,99,52],[236,244,190,160]];
  const lerp = (T, L) => {
    for (let i = 0; i < T.length - 1; i++) {
      const a = T[i], b = T[i + 1];
      if (L <= b[0]) { const t = (L - a[0]) / (b[0] - a[0] || 1);
        return [a[1]+(b[1]-a[1])*t, a[2]+(b[2]-a[2])*t, a[3]+(b[3]-a[3])*t]; }
    }
    const z = T[T.length - 1]; return [z[1], z[2], z[3]];
  };

  async function work(src, out, { yFrom, yFade = 90, darkMax }) {
    const img = new Image(); img.src = src; await img.decode();
    const w = img.naturalWidth, h = img.naturalHeight;
    const c = document.createElement("canvas"); c.width = w; c.height = h;
    const g = c.getContext("2d", { willReadFrequently: true }); g.drawImage(img, 0, 0);
    const im = g.getImageData(0, 0, w, h), d = im.data;
    const LU = p => { const i = p*4; return .2126*d[i] + .7152*d[i+1] + .0722*d[i+2]; };
    const CH = p => { const i = p*4;
      return Math.max(d[i],d[i+1],d[i+2]) - Math.min(d[i],d[i+1],d[i+2]); };

    // 1. 배경 + 바닥 그림자
    const bg = new Uint8Array(w * h), ok = p => LU(p) > 162 && CH(p) < 34, st = [];
    for (let x = 0; x < w; x++) { st.push(x); st.push((h-1)*w + x); }
    for (let y = 0; y < h; y++) { st.push(y*w); st.push(y*w + w - 1); }
    while (st.length) {
      const p = st.pop(); if (bg[p] || !ok(p)) continue; bg[p] = 1;
      const x = p % w, y = (p - x) / w;
      if (x > 0) st.push(p-1); if (x < w-1) st.push(p+1);
      if (y > 0) st.push(p-w); if (y < h-1) st.push(p+w);
    }

    const yM = Math.round(h * yFrom);
    for (let p = 0; p < w * h; p++) {
      if (bg[p]) continue;
      const i = p*4, r = d[i], gg = d[i+1], b = d[i+2], L = LU(p), ch = CH(p);
      if (ch >= 44 && r > b) continue;          // 2. 브라스 유지
      if (ch < 26 && L > 118) continue;         // 3. 밝은 강철 유지
      const y = (p - (p % w)) / w;
      let m = 0;                                 // 4. 트랙/다리 혼합 비율
      if (L < darkMax) m = Math.max(0, Math.min(1, (y - yM) / yFade));
      const [nr, ng, nb] = lerp(RED, L);         // 5. 갑옷
      const k = 0.84;
      d[i]   = Math.round(nr * (1-m) + r  * k * m);
      d[i+1] = Math.round(ng * (1-m) + gg * k * m);
      d[i+2] = Math.round(nb * (1-m) + Math.min(255, b * k + 6) * m);
    }
    g.putImageData(im, 0, 0);
    const res = await fetch("/save?path=" + encodeURIComponent(out),
                            { method: "POST", body: c.toDataURL("image/jpeg", 0.9) });
    return await res.text();
  }

  return [
    await work("/world-eaters-classic-blood/images/photo-forgefiend.jpg",
               "world-eaters-classic-blood/images/photo-forgefiend-red.jpg",
               { yFrom: 0.55, yFade: 110, darkMax: 74 }),
  ];
})()
