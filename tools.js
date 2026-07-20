/* The Twelve Rooms — shared tools front-end. No build step. */
"use strict";
window.TR = (function () {
  const esc = s => String(s ?? "").replace(/[&<>"]/g,
    c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

  /* Google Analytics (GA4). Set GA_ID to the property's Measurement ID to
     turn it on. Left at the placeholder, analytics stays off, so nothing
     loads until the real ID is in. Birth data never reaches GA: only page
     views and coarse traffic. */
  const GA_ID = "G-M2293ZPFBH";

  function injectAnalytics() {
    if (!GA_ID || GA_ID === "G-XXXXXXXXXX") return;
    const s = document.createElement("script");
    s.async = true;
    s.src = "https://www.googletagmanager.com/gtag/js?id=" + GA_ID;
    document.head.appendChild(s);
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { dataLayer.push(arguments); };
    gtag("js", new Date());
    gtag("config", GA_ID);
  }
  injectAnalytics();

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
  <g class="ticks" stroke="#c9a55c" stroke-width="0.5" opacity="0.85">
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
    ["/almanac", "Almanac"], ["/reports", "Readings"],
  ];

  /* Gold starfield: tiny twinkling dots, scattered asymmetrically, always
     clear of type (z-index below .masthead-inner). Subtle by brand law. */
  function starfield(n) {
    let s = "";
    for (let i = 0; i < n; i++) {
      const x = (Math.random() * 100).toFixed(1), y = (Math.random() * 100).toFixed(1);
      const sz = (Math.random() * 1.5 + 0.8).toFixed(1);
      const dur = (3.5 + Math.random() * 4.5).toFixed(1);
      const del = (-Math.random() * 8).toFixed(1);
      const omax = (0.3 + Math.random() * 0.5).toFixed(2);
      s += `<span class="star-dot" style="left:${x}%;top:${y}%;width:${sz}px;height:${sz}px;--tw:${dur}s;--twd:${del}s;--o-max:${omax}"></span>`;
    }
    return `<div class="stars" aria-hidden="true">${s}</div>`;
  }

  function mast(current) {
    const nav = NAV.map(([href, label]) =>
      `<a href="${href}"${location.pathname.replace(/\.html$/, "") === href ? ' aria-current="page"' : ""}>${label}</a>`).join("");
    return `<header class="masthead">
      ${starfield(26)}
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
    <div><a href="/about">About</a> · <a href="/reports">The readings</a> · <a href="/almanac">Almanac</a></div>
    <div>Positions computed with the Swiss Ephemeris, whole-sign houses.</div>
    <div class="privacy">Your birth details are computed in memory and never stored, logged, or shared. The site uses Google Analytics to measure overall traffic; your birth data is never part of it.</div>
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

  const calmMotion = () =>
    window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* A rare shooting star across the masthead sky. Roughly one every half
     minute, gone in under two seconds, never when motion is reduced. */
  function nightSky() {
    if (calmMotion()) return;
    setInterval(() => {
      if (Math.random() > 0.35) return;
      const m = document.querySelector(".masthead");
      if (!m) return;
      const el = document.createElement("span");
      el.className = "shooting";
      el.style.left = (35 + Math.random() * 55) + "%";
      el.style.top = (8 + Math.random() * 42) + "%";
      m.appendChild(el);
      el.addEventListener("animationend", () => el.remove());
    }, 11000);
  }

  /* Gentle rise-in as sections enter the viewport. Class-based, JS-only,
     so visitors without JS (or with reduced motion) see everything plain. */
  function reveals() {
    if (calmMotion() || !("IntersectionObserver" in window)) return;
    const io = new IntersectionObserver(entries => entries.forEach(e => {
      if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
    }), { rootMargin: "4000px 0px -4% 0px" });
    /* The 4000px top margin counts everything at or above the viewport as
       entered, so a jump (anchor link, fast scroll) can never strand a
       section invisible above the fold. */
    document.querySelectorAll(".wrap > *").forEach(el => {
      el.classList.add("reveal");
      io.observe(el);
    });
  }

  document.addEventListener("DOMContentLoaded", () => {
    injectMasthead(); injectFooter(); nightSky(); reveals();
  });
  return { attachCity, esc };
})();
