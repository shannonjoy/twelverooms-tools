/* The Twelve Rooms: sky calendar pages. No build step.
   1. [data-mercury]: the live "Is Mercury retrograde?" answer. The dates are
      precomputed with the Swiss Ephemeris (bin/sky_calendar.py) and shipped in
      the page as JSON; this only compares them with the visitor's clock.
   2. table.sky-table rows carrying data-utc: mark past rows and the next one.
   3. [data-local-time]: show a UTC moment in the visitor's own timezone.
   4. button[data-copy]: copy the text of the element it names. */
"use strict";
(function () {
  const fmt = (iso, withTime) => {
    const d = new Date(iso);
    const o = withTime
      ? { weekday: "short", month: "short", day: "numeric", year: "numeric", hour: "numeric", minute: "2-digit", timeZoneName: "short" }
      : { weekday: "short", month: "long", day: "numeric", year: "numeric" };
    try { return d.toLocaleString(undefined, o); } catch (e) { return d.toUTCString(); }
  };
  const plural = (n, w) => `${n} ${w}${n === 1 ? "" : "s"}`;
  /* "in 2 days", or "in 9 hours" when it is less than a day away. */
  const until = ms => {
    const h = Math.max(1, Math.round(ms / 3600000));
    return h < 24 ? "in " + plural(h, "hour") : "in " + plural(Math.round(h / 24), "day");
  };

  function mercury(box) {
    const src = document.getElementById(box.dataset.mercury);
    if (!src) return;
    let periods;
    try { periods = JSON.parse(src.textContent); } catch (e) { return; }
    const now = Date.now();
    const t = p => ({ sb: Date.parse(p.shadow_begins), r: Date.parse(p.retrograde), d: Date.parse(p.direct), se: Date.parse(p.shadow_ends) });
    let verdict = "", say = "", phase = "";
    let cur = periods.find(p => now < Date.parse(p.shadow_ends));
    if (!cur) {
      verdict = "No";
      say = "Mercury is moving direct. This page lists dates through the end of its range; a new year's dates are on the way.";
    } else {
      const x = t(cur);
      if (now < x.sb) {
        verdict = "No"; phase = "direct";
        say = `Mercury is moving direct. The next retrograde begins <strong>${fmt(cur.retrograde)}</strong>, ${until(x.r - now)}, and runs to ${fmt(cur.direct)}.`;
      } else if (now < x.r) {
        verdict = "Not yet"; phase = "pre";
        say = `Mercury is in its pre-shadow. It stations retrograde <strong>${fmt(cur.retrograde, true)}</strong>, ${until(x.r - now)}. The ground it will retrace is already being walked.`;
      } else if (now < x.d) {
        verdict = "Yes"; phase = "rx";
        say = `Mercury is retrograde in ${cur.signs}. It turns direct <strong>${fmt(cur.direct, true)}</strong>, ${until(x.d - now)}.`;
      } else {
        verdict = "No"; phase = "post";
        say = `Mercury turned direct ${fmt(cur.direct)} and is in its post-shadow until <strong>${fmt(cur.shadow_ends)}</strong>, clearing the last of the ground it retraced.`;
      }
      box.querySelectorAll("[data-phase]").forEach(el => el.classList.toggle("now", el.dataset.phase === phase));
    }
    const v = box.querySelector(".verdict"), s = box.querySelector(".say"), a = box.querySelector(".asof");
    if (v) v.textContent = verdict;
    if (s) s.innerHTML = say;
    if (a) a.textContent = "Checked against your clock: " + fmt(new Date(now).toISOString(), true) + ". Dates computed with the Swiss Ephemeris.";
  }

  function tables() {
    const now = Date.now();
    document.querySelectorAll("table.sky-table").forEach(tb => {
      let marked = false;
      tb.querySelectorAll("tr[data-utc]").forEach(tr => {
        const end = Date.parse(tr.dataset.end || tr.dataset.utc);
        tr.classList.remove("past", "next");
        if (end < now) tr.classList.add("past");
        else if (!marked) { tr.classList.add("next"); marked = true; }
      });
    });
  }

  function localTimes() {
    document.querySelectorAll("[data-local-time]").forEach(el => {
      el.textContent = fmt(el.dataset.localTime, true);
    });
  }

  function copyButtons() {
    document.querySelectorAll("button[data-copy]").forEach(btn => {
      btn.addEventListener("click", async () => {
        const src = document.getElementById(btn.dataset.copy);
        const text = src ? (src.value || src.textContent) : "";
        try { await navigator.clipboard.writeText(text); btn.textContent = "Copied"; }
        catch (e) { if (src && src.select) { src.select(); } btn.textContent = "Select and copy"; }
        setTimeout(() => { btn.textContent = btn.dataset.label || "Copy"; }, 2200);
      });
    });
  }

  function run() {
    document.querySelectorAll("[data-mercury]").forEach(mercury);
    tables(); localTimes(); copyButtons();
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", run);
  else run();
})();
