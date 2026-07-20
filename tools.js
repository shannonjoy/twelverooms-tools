/* The Twelve Rooms — shared tools front-end. No build step. */
"use strict";
window.TR = (function () {
  const esc = s => String(s ?? "").replace(/[&<>"]/g,
    c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

  const MEDALLION = `
<svg class="medallion" viewBox="0 0 150 150" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <defs>
    <linearGradient id="tr-gold" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#d4b06a"/><stop offset="0.5" stop-color="#b18b45"/><stop offset="1" stop-color="#96742f"/>
    </linearGradient>
  </defs>
  <circle cx="75" cy="75" r="62" fill="none" stroke="url(#tr-gold)" stroke-width="1.3"/>
  <circle cx="75" cy="75" r="58" fill="none" stroke="url(#tr-gold)" stroke-width="0.4"/>
  <circle cx="75" cy="75" r="34" fill="none" stroke="url(#tr-gold)" stroke-width="0.6"/>
  <g stroke="#c9a55c" stroke-width="0.5" opacity="0.85">
    <line x1="75" y1="17" x2="75" y2="23"/><line x1="75" y1="127" x2="75" y2="133"/><line x1="17" y1="75" x2="23" y2="75"/><line x1="127" y1="75" x2="133" y2="75"/>
    <line x1="34" y1="34" x2="38.2" y2="38.2"/><line x1="111.8" y1="111.8" x2="116" y2="116"/><line x1="116" y1="34" x2="111.8" y2="38.2"/><line x1="38.2" y1="111.8" x2="34" y2="116"/>
  </g>
  <text x="75" y="85" text-anchor="middle" font-family="Didot,'Bodoni 72',Georgia,serif" font-size="27" fill="#e6cf96" letter-spacing="1">XII</text>
</svg>`;

  const SPARK = (x, y, s, o) =>
    `<svg class="spark" style="left:${x};top:${y}" width="${14 * s}" height="${14 * s}" viewBox="-6 -6 12 12" opacity="${o}"><path d="M0 -6 L1.2 -1.2 L6 0 L1.2 1.2 L0 6 L-1.2 1.2 L-6 0 L-1.2 -1.2 Z"/></svg>`;

  const NAV = [
    ["/moon", "Moon now"], ["/natal-chart", "Natal chart"],
    ["/synastry", "Synastry"], ["/electional", "Timing"],
  ];

  function mast(current) {
    const nav = NAV.map(([href, label]) =>
      `<a href="${href}"${location.pathname.replace(/\.html$/, "") === href ? ' aria-current="page"' : ""}>${label}</a>`).join("");
    return `<header class="masthead">
      ${SPARK("8%", "22%", 0.7, 0.5)}${SPARK("90%", "18%", 1, 0.6)}${SPARK("84%", "70%", 0.6, 0.45)}${SPARK("14%", "74%", 0.55, 0.4)}
      <div class="masthead-inner">
        <a href="/" aria-label="The Twelve Rooms home">${MEDALLION}</a>
        <div class="wordmark"><a href="/">THE TWELVE ROOMS</a></div>
        <div class="rule"><span class="dot"></span></div>
        <div class="tagline">The whole sky, written for you.</div>
        <div class="productline">Natal Deep-Dives · Year-Ahead Readings · Chart Art</div>
        <nav>${nav}</nav>
      </div>
    </header>`;
  }

  function injectMasthead() {
    const slot = document.getElementById("masthead");
    if (slot) slot.outerHTML = mast();
  }

  const FOOTER = `<footer class="site">
    <span class="seal">A map of the life you were born to.</span>
    <div>Positions computed with the Swiss Ephemeris, whole-sign houses.</div>
    <div class="privacy">Your birth details are computed in memory and never stored, logged, or shared. No cookies, no analytics.</div>
    <div class="privacy">Free software under the <a href="https://github.com/shannonjoy/twelverooms-tools" rel="noopener">AGPL-3.0</a>. Brand and readings © The Twelve Rooms.</div>
  </footer>`;

  function injectFooter() {
    const slot = document.getElementById("site-footer");
    if (slot) slot.outerHTML = FOOTER;
  }

  /* City typeahead. onPick receives {name, admin1, country, lat, lon, tz}. */
  function attachCity(input, results, onPick) {
    let timer = null;
    const close = () => results.classList.remove("open");
    input.addEventListener("input", () => {
      clearTimeout(timer);
      timer = setTimeout(async () => {
        const q = input.value.trim();
        if (q.length < 2) return close();
        let d;
        try { d = await (await fetch("/api/geo?q=" + encodeURIComponent(q))).json(); }
        catch (e) { return close(); }
        if (!d.results || !d.results.length) return close();
        results.innerHTML = d.results.map(r =>
          `<button type="button" data-r='${esc(JSON.stringify(r))}'>${esc(r.name)}, ${esc(r.admin1)} <span class="sub">${esc(r.country)} · ${esc(r.tz)}</span></button>`).join("");
        results.classList.add("open");
        results.querySelectorAll("button").forEach(b => b.addEventListener("click", () => {
          const r = JSON.parse(b.dataset.r);
          input.value = r.name + ", " + r.admin1;
          onPick(r);
          close();
        }));
      }, 180);
    });
    document.addEventListener("click", e => { if (!e.target.closest(".loc")) close(); });
  }

  document.addEventListener("DOMContentLoaded", () => { injectMasthead(); injectFooter(); });
  return { attachCity, esc };
})();
