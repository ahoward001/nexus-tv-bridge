# Changelog

Newest first. `release.sh` prepends each release automatically, so this file and the
GitHub release pages can't disagree.

`MAJOR.MINOR.PATCH` — MAJOR is a whole new capability (1 = sync, 2 = strike metrics,
3 = alerts, 4 = settings/columns and the first build shared with other people),
MINOR is a feature within one, PATCH is a bug fix.

---

## v4.1.4 — 2026-08-10

Packaging and docs. No behaviour changes.

- **The package no longer ships internal notes.** A porting checklist written before the Firefox build existed (it still said *"nothing here has been tested on Firefox"*), two experiment logs, and the release runbook were all riding along in the download. The package is now four docs: README, INSTALL, and the two setup guides.
- **A build artifact was getting packaged.** `web-ext` drops `.amo-upload-uuid` into the source folder when it signs, and it ended up inside an archive. The build now refuses to package if it finds one.
- **The README's version header was stale** (still said 3.14.3). It's stamped from the manifest now, like the other docs.

## v4.1.3 — 2026-08-10

- **How to reach the Pine code is documented.** The `{ }` brackets icon on the indicator's row in the chart legend opens that script's source. Caveat now written down too: it opens the version *bound to your chart*, which can be a read-only historical snapshot.
- **The "historical version" banner is documented**, including the trap — *"restore this version"* makes the **old** code current, which is backwards. The way out is opening the script from **My scripts**.
- Guides attached as release assets and committed to the repo so they render in a browser.

## v4.1.2 — 2026-08-10

- **Turning off "Strike metrics" clears the three column checkboxes.** They used to stay ticked while the thing that fills them was off — claiming columns were on when nothing would be drawn. They clear and grey out now, and return when re-enabled. Individual column choices still survive a reload; only the master switch cascades.
- **Price alerts moved above Strike metrics** in settings.
- **Version stamping.** The Pine header said `2.5.0` and `INSTALL.txt` said `3.14.3` while the extension was on 4.1.1. Both are stamped from the manifest at build time now.
- The options page is loaded and asserted on every build (21 checks). It had shipped dead twice — a parse-clean file whose first `getElementById` found nothing and threw.

## v4.1.1 — 2026-08-10

- **Better defaults**: offset **44 bars**, bubble size **3 of 5**, spacing **15 bars**, all three columns on, dotted lines on, every strike shown. The old 36 / 2 / 8 sat too close to price and too tight together. Those numbers had also drifted across three internal copies, one disagreeing with the other two — now one set, with the Pine script's own defaults matched so a newly added indicator looks right before the first sync.
- **The Pine script is a release asset**, not just a file inside the download.

## v4.1.0 — 2026-08-10

- **The docs no longer assume a Mac.** Shortcuts led with ⌘ throughout; they lead with **Ctrl** now. Notification instructions pointed at *System Settings → Notifications*, which doesn't exist on Windows — both paths given. `SETUP-PHONE.md` labelled **iPhone only**.
- **The AI-assistant setup prompt is assistant-neutral** instead of naming one.
- **`INSTALL-FIREFOX.txt` rewritten.** It still described the pre-signing world — *"UNTESTED on Firefox"*, version 3.10.2, and `about:debugging` → **Load Temporary Add-on**, which disappears when Firefox closes.
- The Pine script committed to the repo so it can be copied from a browser.

## v4.0.0 — 2026-08-10

First build meant to be handed to other people, and the first that updates itself.

- **Firefox auto-update had never worked once.** `updates.json` advertised v3.11.3 — a release that was never created — so the download link 404'd and no Firefox install ever updated, silently, with nothing to notice. The chain is now built and verified on every release: the link must return 200, and the file it serves must be signed, the right version, and hash-identical to what Mozilla signed.
- Releases became a single command.

## v3.14.6 — 2026-08-10

- **Alerts say "approaching" and nothing else.** No "passed" / "went through" / "crossed". The old pass-through test once fired *"went through Call Wall 723"* on a bar whose high was 722.24 — price never reached it. The test is gone, not just the wording: a level that already broke is news too late to act on.
- Chrome minimum pinned to **111**, the first version supporting the injection mode the column writer needs, so an older Chrome fails loudly instead of silently doing nothing.

## v3.14.5 — 2026-08-10

- The settings header says how to apply changes — "click green sync button in TradingView".

## v3.14.4 — 2026-08-10

- **Column toggles actually apply.** Unchecking Score left the column on the chart. The writer opened TradingView's settings dialog with a single synthetic `dblclick`, which TradingView ignores — so on a real sync it waited 3.5 seconds for a dialog that never appeared and gave up silently. It now sends the full press/release sequence, like the other three dialog-openers already did.
- **Settings failures are no longer silent.** The live-apply path swallowed every error and logged `"look settings applied live"` unconditionally, whether or not anything reached the chart. That one line is why the toggle bug looked fixed several times when it wasn't.
- **Restored the Firefox alarm-floor guard.** Firefox rejects sub-minute alarms; the guard had been lost in a refactor, leaving Firefox users on price alerts with no tick at all.

## v3.14.3 — 2026-08-10

- Past alerts removed from the hover panel.
- **A line could appear on one column's say-so.** 724 was drawn as significant because it held the biggest GEX nearby, while its score *and* open interest were both lower than its immediate neighbours'. A level now has to stand out on **two of three** measures — top-3 in the band *and* above both neighbours. Rejections are logged.
