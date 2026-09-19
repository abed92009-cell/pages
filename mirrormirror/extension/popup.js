// P384. The Compressed Cursor as a Chrome MV3 extension.
//
// WHY THIS IS THE WINNING SURFACE, per the August ruling: it sees the page
// BEFORE the clipboard flattens it, so headings and structure survive that a
// pasteboard copy has already destroyed. And a stranger at an expo can load it
// in under a minute.
//
// LOOPBACK, NEVER THE TAILNET, and that is deliberate. An extension is synced
// across a Chrome profile, so a tailnet hostname baked into it is a piece of
// the house's private network travelling to every machine that profile touches.
// P116b's lesson: a name in a synced file is a credential. 127.0.0.1 is only
// ever this Mac, and the extension is useless on anyone else's machine, which
// is exactly right.
//
// IT REFUSES RATHER THAN PRETENDING. If the Mac is not answering, it says so.
// It never falls back to copying the uncompressed text, because a person
// believing they saved tokens when they did not is the worst possible outcome
// and the one the ledger exists to prevent.
const MAC = "http://127.0.0.1:7727";
const KEY = "cc.tier";

const $ = (s) => document.querySelector(s);
const led = $("#led");
const day = $("#day");

async function tier() {
  const o = await chrome.storage.local.get(KEY);
  return o[KEY] || "";
}
async function paint() {
  const t = await tier();
  document.querySelectorAll("button.t").forEach((b) => {
    b.setAttribute("aria-pressed", (b.dataset.t || "") === t ? "true" : "false");
  });
}
document.querySelectorAll("button.t").forEach((b) => {
  b.addEventListener("click", async () => {
    await chrome.storage.local.set({ [KEY]: b.dataset.t || "" });
    paint();
  });
});

/** Read the page: the selection if there is one, otherwise the visible text. */
function readPage() {
  const sel = String(window.getSelection() || "");
  if (sel.trim()) return sel;
  // innerText, not textContent: it respects what is actually VISIBLE, so
  // hidden menus and scripts do not arrive as content to be compressed.
  return document.body ? document.body.innerText : "";
}

function line(r) {
  const saved = Math.max(0, r.tokensBefore - r.tokensAfter);
  const pct = r.tokensBefore > 0 ? Math.round((saved / r.tokensBefore) * 1000) / 10 : 0;
  const money = typeof r.nzdSaved === "number" ? `, NZD ${r.nzdSaved.toFixed(4)} saved` : ", NZD not set";
  return `${r.level} , ${r.tokensBefore} in , ${r.tokensAfter} out , ${saved} saved (${pct}%)${money}`;
}

async function refreshDay() {
  try {
    const d = await (await fetch(`${MAC}/crunch/ledger`, { cache: "no-store" })).json();
    const t = d && d.day;
    if (!t || typeof t.tokensBefore !== "number") { day.textContent = ""; return; }
    day.textContent = `Today: ${t.runs} capture${t.runs === 1 ? "" : "s"} , ${t.tokensSaved} saved (${t.percentSaved}%)`;
  } catch { day.textContent = ""; }
}

$("#go").addEventListener("click", async () => {
  led.textContent = "Reading the page...";
  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    const [{ result: text }] = await chrome.scripting.executeScript({
      target: { tabId: tab.id }, func: readPage,
    });
    if (!text || !text.trim()) { led.textContent = "Nothing on this page to compress."; return; }

    const body = { text, source: tab.url || "browser" };
    const lvl = await tier();
    if (lvl) body.level = lvl;

    const res = await fetch(`${MAC}/spokes/text`, {
      method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body),
    });
    if (!res.ok) throw new Error(`the Mac answered ${res.status}`);
    const out = await res.json();
    const c = (out.spoke && out.spoke.crunch) || null;
    if (!c) { led.textContent = "It landed on the wheel, but reported no ledger. UNKNOWN, not zero."; return; }

    await navigator.clipboard.writeText(c.text);
    led.textContent = `Copied. ${line(c)} , original kept on the wheel`;
    refreshDay();
  } catch (e) {
    // Named, never silent, and never a fallback to the raw text.
    led.textContent = `MirrorMirror is not answering on this Mac (${e.message}). Nothing was copied.`;
  }
});

paint();
refreshDay();
