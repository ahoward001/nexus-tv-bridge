# Version history

**MAJOR** = a whole new capability · **MINOR** = a feature within one · patch = a bug fix.

Newest first.

---

## v4.3.2 — 2026-08-11

Presentation only, no code changes: Firefox now has a real one-click install link instead of a link back to this page, each asset says what clicking it actually does, and the version history is rebuilt with every release back to 1.0.

**4.3.0** — the button goes **yellow** when a strike newly earns a line.
**4.2.x** — Chrome installs from the Web Store and updates itself; a sync that finds fresh data takes **~2s instead of ~9s**.

[Full version history →](https://github.com/ahoward001/nexus-tv-bridge/blob/main/CHANGELOG.md)

---

## Assets — what clicking each one actually does

**`0-CHROME-SETUP-…​.zip`** — the Chrome extension, as a file.
Clicking **downloads a zip and installs nothing.** Chrome can't install an extension from a file. Unzip it → `chrome://extensions` → turn on **Developer mode** (top right) → **Load unpacked** → select the unzipped **`nexus-tradingview-bridge` folder** (the one with `manifest.json` directly inside — Chrome loads the folder, not the zip). Installed this way it will **not** auto-update.

**`1-FIREFOX-SETUP-…​.xpi`** — the Firefox add-on. Same file as the Install button above; clicking it in Firefox installs it. In Chrome it just downloads something useless.

**`2-COPY-THIS-pine-script-for-tradingview.pine`** — the indicator that draws the columns.
Clicking **downloads a text file and installs nothing.** You paste its contents into TradingView's Pine Editor by hand — usually easier to use the "Open the script" link above and copy it in the browser.

**`3.0-GUIDE-chrome.txt` · `3.1-GUIDE-firefox.txt` · `3.2-GUIDE-pine.md`** — reading, not installing. The long-form walkthroughs if the steps above aren't enough. Readable in your browser: [Chrome](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-chrome-install.txt) · [Firefox](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-firefox-install.txt) · [Pine](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-pine-indicator-setup.md)

*Ignore "Source code (zip/tar.gz)" — GitHub generates those automatically and they aren't the extension.*

---

> **On version currency:** Firefox and the zip above are always this build. **Chrome's Web Store copy can be up to ~24 hours behind** — Google reviews every submission and locks the listing while one is pending, so Store releases land in batches. If you need today's code on Chrome right now, use the `0-CHROME-SETUP` zip and the manual steps above instead of the Store link.

# 4 — Settings, columns, and sharing it with other people

**4.3** — the button goes **yellow** when a strike newly earns a dotted line. Between syncs the watcher re-runs the 2-of-3 significance rule against Nexus's live strike table and diffs it against your last sync. Yellow rather than orange because it's read from a tab that hasn't been reloaded — a hint, not proof. Only additions count, so the button doesn't flicker when a borderline strike drops out.

4.3.1 — release page rewritten around what each file does when you click it; assets renumbered in use order; push time stamped on the page.

**4.2** — **Chrome installs from the Web Store and updates itself**, which it had never done: Chrome blocks off-store installs and ignores `update_url` for anything loaded unpacked, so a GitHub zip can never auto-update. Also the big speed fix — a sync that finds fresh data takes **~2s instead of ~9s**. A click now reads your Nexus tab first and reloads only when the batch is genuinely old or a key wall moved, instead of reloading every time. New setting for that threshold.

4.2.5 — page-load wait cut 4s → 2s; a key wall moving forces a reload even on a young batch.
4.2.2 — Chrome Store uploads automated via the Web Store API.
4.2.1 — Store listing approved and live.

**4.1** — docs stopped assuming a Mac (shortcuts led with ⌘ everywhere; notification settings pointed at a path that doesn't exist on Windows). Pine script published to the repo so it can be copied from a browser. Better defaults: offset 44 bars, bubble size 3, spacing 15, all columns on.

4.1.6 — manifest description shortened to fit the Store's 132-char limit.
4.1.5 — changelog now written by the release command itself, so it can't fall behind.
4.1.4 — internal notes and a build artifact removed from the shipped package.
4.1.2 — turning off "Strike metrics" clears the three column checkboxes; version numbers stamped into every doc at build time.

**4.0** — first build meant to be handed to other people, and the first that updates itself. **Firefox auto-update had never worked once** — `updates.json` advertised a release that was never created, so the link 404'd silently and no install ever updated. The chain is now verified on every release: the link must return 200 and serve a signed build whose hash matches what Mozilla signed. Releases became a single command.

---

# 3 — Price alerts

**3.14** — alerts say **approaching** and nothing else. The old "passed through it" test once fired *"went through Call Wall 723"* on a bar whose high was 722.24; the test is gone, not just the wording — a level that already broke is news too late to act on. Column toggles actually apply (the settings dialog was being opened with a synthetic `dblclick` TradingView ignores, so the writer timed out silently). Settings failures stopped being silent.

**3.11** — signed on addons.mozilla.org; Firefox installs permanently instead of vanishing on restart.

**3.10** — first Firefox build: event page instead of a service worker, explicit add-on ID (without one `storage.sync` silently fails to persist), guarded `importScripts`, and a 1-minute alarm floor because Firefox rejects sub-minute alarms.

**3.6** — red-zone rework: alerts fire on the *bar's* range rather than a 30-second price sample, so a wick into a wall is caught; a level drifting onto a stationary price is no longer treated as an entry.

**3.0** — desktop notifications when price approaches a level, with a quiet window, a clustering rule so levels within a strike count as one, and silence while you're already looking at that chart.

---

# 2 — Strike metrics

**2.6** — the strike table is read from the page **payload** instead of the rendered grid, so it no longer needs a visible Overview tab. This removed the recurring "needs a visible Overview tab — skipping".

**2.5** — significance rule tightened: a level must stand out on **two of three** measures (score, open interest, gamma exposure) before it earns a dotted line. One column alone was drawing lines on strikes their neighbours beat on the other two.

**2.4** — score-driven color gradient stretched across the full range so the top stops flattening out.

**2.1** — OI and GEX box colour scales relative to the board rather than to score.

**2.0** — the +/− controls drive **bubble spacing**; wall-crossing deadband so a wall relabelling as price flirts the line doesn't churn.

**2.0** — **per-strike Score / OI / GEX columns**, drawn by a companion Pine indicator and filled on every sync.

---

# 1 — Sync

**1.16** — emphasis pass: the score *number* is painted on Nexus's own gradient rather than the box.

**1.13–1.14** — always-fresh-on-click, and multi-tab consistency: with several Nexus tabs open, the whole sync reads from one fresh source rather than whichever tab answered first.

**1.11** — colour scheme, title row, and selective lines on the Extra Levels indicator.

**1.10** — every-strike mode.

**1.9** — reads Nexus 2.0's per-strike table from the live dashboard.

**1.4** — content-hash check so a re-stamped batch carrying identical levels isn't reported as fresher.

**1.3** — the truth-age algorithm: level age measured from Nexus's own published stamp against the real clock, rather than the page's embedded timestamps (which never update and measure how long the tab has been open — a tab left overnight reported 17.8 hours for levels 88 seconds old).

**1.0** — one click reads the export from your signed-in Nexus dashboard and pastes it into the Nexus Futures indicator on your chart.
