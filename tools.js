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

  /* Nav is grouped: a plain [href, label] is a top-level link; an object with
     { label, items } renders a dropdown. Keeps the bar to a few clear
     destinations while every calculator stays one hover/tap away. */
  const NAV = [
    { label: "Tools", items: [
      ["/moon", "Moon now"],
      ["/big-3-calculator", "Big 3"],
      ["/natal-chart", "Natal chart"],
      ["/synastry", "Synastry"],
      ["/saturn-return-calculator", "Saturn return"],
      ["/transit-timeline", "Transit timeline"],
      ["/electional", "Timing"],
    ] },
    ["/almanac", "Almanac"],
    ["/the-twelve-houses", "The houses"],
    ["/reports", "Readings"],
    ["/about", "About"],
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
    const path = location.pathname.replace(/\.html$/, "");
    const link = ([href, label]) =>
      `<a href="${href}"${path === href ? ' aria-current="page"' : ""}>${label}</a>`;
    const nav = NAV.map(item => {
      if (Array.isArray(item)) return link(item);
      const active = item.items.some(([href]) => path === href);
      const menu = item.items.map(link).join("");
      return `<div class="navgroup">
        <button type="button" class="navtoggle" aria-expanded="false" aria-haspopup="true"${active ? ' aria-current="page"' : ""}>${item.label}<span class="caret" aria-hidden="true">▾</span></button>
        <div class="navmenu" role="menu">${menu}</div>
      </div>`;
    }).join("");
    return `<header class="masthead">
      <div class="masthead-sky" aria-hidden="true">
        ${starfield(26)}
        ${SPARK("8%", "22%", 0.7, 0.5)}${SPARK("90%", "18%", 1, 0.6)}${SPARK("84%", "70%", 0.6, 0.45)}${SPARK("14%", "74%", 0.55, 0.4)}
      </div>
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

  /* Nav dropdowns: hover opens them on desktop (CSS); this adds click/tap
     toggling for touch and keyboard, with outside-click and Escape to close. */
  function initNav() {
    const groups = Array.from(document.querySelectorAll(".navgroup"));
    if (!groups.length) return;
    const closeAll = except => groups.forEach(g => {
      if (g === except) return;
      g.classList.remove("open");
      const b = g.querySelector(".navtoggle");
      if (b) b.setAttribute("aria-expanded", "false");
    });
    groups.forEach(g => {
      const btn = g.querySelector(".navtoggle");
      btn.addEventListener("click", e => {
        e.stopPropagation();
        const open = !g.classList.contains("open");
        closeAll(g);
        g.classList.toggle("open", open);
        btn.setAttribute("aria-expanded", String(open));
      });
    });
    document.addEventListener("click", () => closeAll());
    document.addEventListener("keydown", e => { if (e.key === "Escape") closeAll(); });
  }

  const FOOTER = `<footer class="site">
    <div>© 2026 The Twelve Rooms · City data © GeoNames (CC BY 4.0)</div>
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

  /* ---- Remember birth details (opt-in, this device only) ----
     Visitors told us it is tiresome to retype their birthday on every
     calculator. This keeps their birth details in localStorage, on their own
     device — never sent to a server — and prefills them next visit. It stays
     off until the visitor ticks the box; unticking it forgets everything. */
  const BIRTH_KEY = "tr.birth.v1";

  function birthStore() {
    try { return window.localStorage; } catch (e) { return null; }  /* private mode */
  }
  function readAll() {
    const s = birthStore(); if (!s) return {};
    try { return JSON.parse(s.getItem(BIRTH_KEY) || "{}"); } catch (e) { return {}; }
  }
  function writeAll(all) {
    const s = birthStore(); if (!s) return;
    try { s.setItem(BIRTH_KEY, JSON.stringify(all)); } catch (e) { /* quota/blocked */ }
  }
  function loadBirth(slot) { return readAll()[slot] || null; }
  function saveBirth(slot, data) { const all = readAll(); all[slot] = data; writeAll(all); }
  function clearBirth(slot) { const all = readAll(); delete all[slot]; writeAll(all); }

  const byId = x => (typeof x === "string" ? document.getElementById(x) : x);

  /* Wire a birth form to remember and restore its details. Drop-in for the
     page's attachCity call: onPlace(r) runs on both a city pick and a restore,
     so the page keeps setting its own PLACE, hidden lat/lon/tz, and "picked"
     line exactly as before.
     opts: { form, city, results, onPlace, slot="self",
             fields=["date","time"], label } */
  function rememberBirth(opts) {
    const form = byId(opts.form), city = byId(opts.city), results = byId(opts.results);
    const slot = opts.slot || "self";
    /* Map canonical keys (date, time) to this form's input names, so a slot
       saved on one page restores on another even when the inputs are named
       differently (e.g. synastry's "ad"/"at"). */
    const raw = opts.fields || ["date", "time"];
    const fmap = Array.isArray(raw) ? raw.reduce((o, n) => (o[n] = n, o), {}) : raw;
    const names = Object.values(fmap);
    const onPlace = opts.onPlace || function () {};
    let place = null;

    attachCity(city, results, r => { place = r; onPlace(r); persist(); });

    /* Opt-in control, inserted just above the submit button. */
    const box = document.createElement("label");
    box.className = "remember";
    const cb = document.createElement("input"); cb.type = "checkbox";
    const label = document.createElement("span");
    label.textContent = opts.label || "Remember my birth details on this device";
    const note = document.createElement("span"); note.className = "remember-note";
    box.append(cb, label, note);
    const submit = form.querySelector("button[type=submit], button.go") ||
                   form.querySelector("button");
    if (submit) form.insertBefore(box, submit); else form.appendChild(box);

    const snapshot = () => {
      const data = { place };
      for (const key in fmap) { const el = form[fmap[key]]; if (el) data[key] = el.value; }
      return data;
    };
    const showSaved = on => { note.textContent = on ? "Saved on this device" : ""; };
    const persist = () => { if (cb.checked) { saveBirth(slot, snapshot()); showSaved(true); } };

    cb.addEventListener("change", () => {
      if (cb.checked) persist();
      else { clearBirth(slot); showSaved(false); }
    });
    /* Capture phase so this runs regardless of the page's own submit handler. */
    form.addEventListener("submit", persist, true);
    names.forEach(n => { if (form[n]) form[n].addEventListener("change", persist); });

    const saved = loadBirth(slot);
    if (saved) {
      for (const key in fmap) { const el = form[fmap[key]]; if (el && saved[key] != null) el.value = saved[key]; }
      if (saved.place) {
        place = saved.place;
        city.value = `${saved.place.name}, ${saved.place.admin1}`;
        onPlace(saved.place);
      }
      cb.checked = true; showSaved(true);
    }
    return { forget: () => { clearBirth(slot); cb.checked = false; showSaved(false); } };
  }

  const calmMotion = () =>
    window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* A rare shooting star across the masthead sky. Roughly one every half
     minute, gone in under two seconds, never when motion is reduced. */
  function nightSky() {
    if (calmMotion()) return;
    setInterval(() => {
      if (Math.random() > 0.35) return;
      const m = document.querySelector(".masthead-sky") || document.querySelector(".masthead");
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
    injectMasthead(); initNav(); injectFooter(); nightSky(); reveals();
  });
  return { attachCity, rememberBirth, esc };
})();
