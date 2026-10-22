#!/usr/bin/env node
// Submit URLs to IndexNow (Bing, Yandex, Seznam, Naver and the other
// participating engines share one endpoint). Bing feeds ChatGPT Search and
// Copilot, so this is the fastest way to tell answer engines a page changed.
//
// OUTBOUND: this sends the URL list to api.indexnow.org. Run it only after
// Shannon has deployed, and only on her word. It never runs in a build.
//
// The key is the 32-hex file at the site root (<key>.txt, whose content is
// the key). IndexNow fetches https://thetwelverooms.com/<key>.txt to check
// that we own the host, so the file must be live before the first submit.
//
// Usage (from the repo root):
//   node bin/indexnow.mjs --dry-run            # print what would be sent
//   node bin/indexnow.mjs                      # every <loc> in sitemap.xml
//   node bin/indexnow.mjs /moon /natal-chart   # only these paths or URLs
//
// Exit 0 on HTTP 200 or 202. 403 means the key file is not live yet; 422
// means a URL is not on this host. No dependencies (Node 18+ fetch).
import { readFileSync, readdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const HOST = "thetwelverooms.com";
const ORIGIN = `https://${HOST}`;
const ENDPOINT = "https://api.indexnow.org/indexnow";
const BATCH = 10000; // IndexNow's per-request limit

export function findKey(dir = ROOT) {
  const files = readdirSync(dir).filter((f) => /^[0-9a-f]{32}\.txt$/.test(f));
  if (files.length !== 1) throw new Error(`expected one IndexNow key file at the root, found ${files.length}`);
  const key = readFileSync(join(dir, files[0]), "utf8").trim();
  if (`${key}.txt` !== files[0]) throw new Error(`key file ${files[0]} does not contain its own name`);
  return key;
}

export function sitemapUrls(dir = ROOT) {
  const xml = readFileSync(join(dir, "sitemap.xml"), "utf8");
  return [...xml.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => m[1].trim());
}

export function normalise(arg) {
  const url = arg.startsWith("http") ? arg : `${ORIGIN}${arg.startsWith("/") ? "" : "/"}${arg}`;
  if (new URL(url).host !== HOST) throw new Error(`not on ${HOST}: ${arg}`);
  return url;
}

export function payloads(urls, key) {
  const out = [];
  for (let i = 0; i < urls.length; i += BATCH) {
    out.push({ host: HOST, key, keyLocation: `${ORIGIN}/${key}.txt`, urlList: urls.slice(i, i + BATCH) });
  }
  return out;
}

async function main(argv) {
  const dry = argv.includes("--dry-run");
  const args = argv.filter((a) => a !== "--dry-run");
  const key = findKey();
  const urls = [...new Set(args.length ? args.map(normalise) : sitemapUrls())];
  const bodies = payloads(urls, key);
  if (dry) {
    for (const b of bodies) console.log(JSON.stringify({ ...b, urlList: `${b.urlList.length} URLs` }));
    console.log(urls.join("\n"));
    console.log(`dry run: ${urls.length} URLs, nothing sent`);
    return 0;
  }
  let failed = 0;
  for (const body of bodies) {
    const res = await fetch(ENDPOINT, {
      method: "POST",
      headers: { "Content-Type": "application/json; charset=utf-8" },
      body: JSON.stringify(body),
    });
    console.log(`IndexNow ${res.status} ${res.statusText}: ${body.urlList.length} URLs`);
    if (res.status !== 200 && res.status !== 202) failed++;
  }
  return failed ? 1 : 0;
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  main(process.argv.slice(2)).then((c) => process.exit(c), (e) => { console.error(e.message); process.exit(2); });
}
