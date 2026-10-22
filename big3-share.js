/* The Twelve Rooms: "Share my Big 3". No build step.
   Builds a share link that carries ONLY the three sign names
   (/big-3/<sun>-<moon>-<rising>, or /big-3/<sun>-<moon> without a birth
   time). No birth date, time or place ever goes into the link, the image,
   or the analytics event. The image is drawn on the visitor's own device. */
"use strict";
window.TRBig3 = (function () {
  const SIGNS = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra",
    "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"];
  const GLYPH = { Aries: "♈", Taurus: "♉", Gemini: "♊", Cancer: "♋", Leo: "♌",
    Virgo: "♍", Libra: "♎", Scorpio: "♏", Sagittarius: "♐", Capricorn: "♑",
    Aquarius: "♒", Pisces: "♓" };
  const ok = s => SIGNS.indexOf(s) >= 0;

  function path(b) {
    if (!ok(b.sun) || !ok(b.moon)) return null;
    const parts = [b.sun, b.moon].concat(ok(b.rising) ? [b.rising] : []);
    return "/big-3/" + parts.map(s => s.toLowerCase()).join("-");
  }

  function style() {
    if (document.getElementById("b3-share-style")) return;
    const s = document.createElement("style");
    s.id = "b3-share-style";
    s.textContent = `
.b3-share { margin-top: 14px; padding-top: 14px; border-top: 1px solid var(--line, #e4ddcf); }
.b3-share h3 { font-family: var(--serif, Georgia, serif); font-weight: 400; color: var(--navy, #26355e); font-size: 17px; margin: 0 0 4px; }
.b3-share .linkline { font-size: 13px; word-break: break-all; color: var(--soft, #656b85); margin: 2px 0 10px; }
.b3-share .row { display: flex; flex-wrap: wrap; gap: 8px; }
.b3-share button { font-size: 13.5px; padding: 8px 14px; border-radius: 999px; border: 1px solid var(--gold-soft, #c9a55c);
  background: #fff; color: var(--navy, #26355e); cursor: pointer; }
.b3-share button.primary { background: linear-gradient(135deg, #e3c98b, #b18b45); color: #101830; border-color: transparent; font-weight: 600; }
.b3-share .note { font-size: 12.5px; color: var(--soft, #656b85); margin-top: 8px; min-height: 1em; }`;
    document.head.appendChild(s);
  }

  function track(url) {
    if (typeof gtag === "function") gtag("event", "SHARE", { url: url });
  }

  /* 1080x1350 portrait card, the size Instagram and most phones keep whole. */
  function draw(b) {
    const W = 1080, H = 1350;
    const c = document.createElement("canvas");
    c.width = W; c.height = H;
    const x = c.getContext("2d");
    const g = x.createRadialGradient(W / 2, H * 0.25, 40, W / 2, H * 0.35, H);
    g.addColorStop(0, "#1f2b4e"); g.addColorStop(1, "#101830");
    x.fillStyle = g; x.fillRect(0, 0, W, H);
    x.strokeStyle = "#b18b45"; x.lineWidth = 3; x.strokeRect(40, 40, W - 80, H - 80);
    x.globalAlpha = 0.55; x.lineWidth = 1.5; x.strokeRect(54, 54, W - 108, H - 108); x.globalAlpha = 1;
    /* quiet star dots, kept to the margins */
    [[120, 160, 2.4, .6], [180, 260, 1.6, .45], [940, 180, 2.2, .6], [880, 300, 1.4, .4], [130, 1120, 2, .55],
     [960, 1110, 2.4, .6], [900, 1210, 1.4, .4], [200, 1220, 1.5, .45]].forEach(([sx, sy, r, o]) => {
      x.globalAlpha = o; x.fillStyle = "#e6cf96"; x.beginPath(); x.arc(sx, sy, r, 0, Math.PI * 2); x.fill();
    });
    x.globalAlpha = 1; x.textAlign = "center";
    x.fillStyle = "#e6cf96"; x.font = "500 26px Optima, 'Helvetica Neue', Arial, sans-serif";
    x.fillText("T H E   T W E L V E   R O O M S", W / 2, 170);
    x.fillStyle = "#9aa5c2"; x.font = "24px Optima, 'Helvetica Neue', Arial, sans-serif";
    x.fillText("M Y   B I G   3", W / 2, 236);
    const cols = [["RISING", b.rising], ["SUN", b.sun], ["MOON", b.moon]];
    cols.forEach(([label, sign], i) => {
      const cy = 400 + i * 250;
      x.fillStyle = "rgba(255,255,255,0.05)";
      x.strokeStyle = "rgba(201,165,92,0.45)"; x.lineWidth = 1.5;
      const bx = 170, bw = W - 340, bh = 210, by = cy - 75;
      x.beginPath();
      if (x.roundRect) x.roundRect(bx, by, bw, bh, 22); else x.rect(bx, by, bw, bh);
      x.fill(); x.stroke();
      x.fillStyle = "#c9a55c"; x.font = "64px 'Apple Symbols', 'Segoe UI Symbol', 'DejaVu Sans', sans-serif";
      x.fillText(sign ? GLYPH[sign] + "︎" : "·", W / 2, cy + 40);
      x.fillStyle = "#fbfaf7"; x.font = "52px Didot, 'Bodoni 72', Georgia, serif";
      x.fillText(sign || "Needs a birth time", W / 2, cy + 104);
      x.fillStyle = "#9aa5c2"; x.font = "22px Optima, 'Helvetica Neue', Arial, sans-serif";
      x.fillText(label.split("").join(" "), W / 2, cy - 38);
    });
    x.fillStyle = "#d4b06a"; x.font = "italic 30px Didot, 'Bodoni 72', Georgia, serif";
    x.fillText("The whole sky, written for you.", W / 2, 1175);
    x.fillStyle = "#8b95b3"; x.font = "22px Optima, 'Helvetica Neue', Arial, sans-serif";
    x.fillText("Find yours free at thetwelverooms.com", W / 2, 1220);
    return c;
  }

  function offer(container, b) {
    const p = path(b);
    if (!container || !p) return;
    style();
    const url = location.origin + p;
    const old = container.querySelector(".b3-share");
    if (old) old.remove();
    const box = document.createElement("div");
    box.className = "b3-share";
    box.innerHTML = `<h3>Share my Big 3</h3>
      <p class="linkline"></p>
      <div class="row">
        <button type="button" class="primary" data-a="share">Share</button>
        <button type="button" data-a="copy">Copy link</button>
        <button type="button" data-a="image">Save image</button>
      </div>
      <p class="note" aria-live="polite">The link and the image show your three signs.</p>`;
    box.querySelector(".linkline").textContent = url;
    const note = box.querySelector(".note");
    const title = `${b.sun} Sun, ${b.moon} Moon${ok(b.rising) ? ", " + b.rising + " rising" : ""}`;
    const copy = async () => {
      try { await navigator.clipboard.writeText(url); note.textContent = "Link copied."; }
      catch (e) { note.textContent = url; }
    };
    box.addEventListener("click", async ev => {
      const a = ev.target.closest("button") && ev.target.closest("button").dataset.a;
      if (!a) return;
      track(p);
      if (a === "share") {
        if (navigator.share) {
          try { await navigator.share({ title: "My Big 3: " + title, text: "My Big 3: " + title, url: url }); }
          catch (e) { /* cancelled */ }
        } else { copy(); }
      } else if (a === "copy") {
        copy();
      } else if (a === "image") {
        const canvas = draw(b);
        const name = "my-big-3-" + p.split("/").pop() + ".png";
        canvas.toBlob(async blob => {
          if (!blob) { note.textContent = "Your browser could not draw the image."; return; }
          const file = typeof File === "function" ? new File([blob], name, { type: "image/png" }) : null;
          if (file && navigator.canShare && navigator.canShare({ files: [file] }) && /Mobi|Android|iPhone|iPad/.test(navigator.userAgent)) {
            try { await navigator.share({ files: [file], title: "My Big 3" }); return; } catch (e) { /* fall through */ }
          }
          const link = document.createElement("a");
          link.href = URL.createObjectURL(blob); link.download = name;
          document.body.appendChild(link); link.click(); link.remove();
          setTimeout(() => URL.revokeObjectURL(link.href), 4000);
          note.textContent = "Image saved.";
        }, "image/png");
      }
    });
    container.appendChild(box);
  }

  /* The share page: <div data-big3 data-sun=".." data-moon=".." data-rising=".."> */
  function mount() {
    document.querySelectorAll("[data-big3]").forEach(el =>
      offer(el, { sun: el.dataset.sun, moon: el.dataset.moon, rising: el.dataset.rising || null }));
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", mount);
  else mount();
  return { offer: offer, path: path, draw: draw };
})();
