# Changelog

Newest first. `release.sh` prepends each release automatically, so this file and the
GitHub release pages can't disagree.

`MAJOR.MINOR.PATCH` — MAJOR is a whole new capability (1 = sync, 2 = strike metrics,
3 = alerts, 4 = settings/columns and the first build shared with other people),
MINOR is a feature within one, PATCH is a bug fix.

---

## v4.3.0 — 2026-08-11

**The button now goes yellow when a strike newly earns a line.**

Between syncs, the watcher re-runs the same 2-of-3 significance rule against Nexus's current strike table and compares it to the line set from your last sync. If a strike that had no dotted line now qualifies, the button goes **yellow**.

Yellow, not orange, on purpose — that reading comes from a tab that hasn't been reloaded, so it's a strong hint rather than proof. Yellow has always meant *"something looks different and I couldn't confirm it."* Clicking sync reloads, confirms, and draws the level for real.

**Only additions count.** A level disappearing doesn't raise anything: it's not something you need to rush to the chart for, and treating both directions as news would make the button flicker every time a borderline strike crossed the rule.

This is separate from the reload triggers — a click still reloads only when the batch is past your age threshold or a key wall moved. Metric churn still never forces a reload; a level *appearing* is structural, and it earns a nudge rather than a 5-second wait.

## v4.2.5 — 2026-08-11

**A click reloads when it should, and only when it should.**

Two things now trigger a reload:

- **The batch is older than your threshold** (default 180s — Nexus republishes about once a minute)
- **A key level moved** — Call Wall, Put Wall or Gamma Flip differs from what was last pasted on this chart. Structural change is worth 5s to be certain, even on a young batch.

Deliberately *not* included: strike metrics. Those churn on every publish with no real consequence, so gating on them would reload every single click and undo the speedup.

This is the **click** path only. The amber staleness cue on the button keeps its own rule — walls are finicky when price sits on them, and a wall twitching shouldn't nag you.

**Faster page-load wait.** The hard wait after a reload dropped from 4s to 2s. It was never the real gate anyway: the reader polls every 80ms for the export code and only accepts it once there's actual content, so waiting longer up front just delayed the polling that does the real work.

When nothing has moved and the data is young, a sync is ~2s instead of ~9s. When something has moved, it pays for the reload.

## v4.2.4 — 2026-08-11

**A sync that finds fresh data now takes about 2 seconds instead of 9.**

The rule was wrong. Every click was reloading your Nexus tab unconditionally — about 5.5 seconds — even when the data it already had was a minute old and perfectly current. That came from reading "every click refreshes everything" as *always reload*, when what it should have meant is *never paste something staler than it claims to be*.

Now a click **reads first, then decides**:

- Batch younger than the threshold → use it. Whole sync finishes in ~2s.
- Batch older, or unreadable → reload for the current one, as before.

`exportAge` is the honest measure here: it's the age of Nexus's own batch as embedded in the page, so a hidden tab that Chrome froze an hour ago reports an hour-old batch — exactly the case a reload fixes — while a tab republished a minute ago is already current.

**New setting:** *Reload Nexus only if its data is older than N seconds*, default **180**. Nexus republishes roughly once a minute, so 180 means "more than about three publishes behind". Lower it for fresher data at ~5.5s a click; raise it for speed. The age is surfaced either way, so nothing is ever silently stale.

Also removed a redundant read that cost ~1.9s on every click regardless.

## v4.2.3 — 2026-08-11

**Sync is roughly 2 seconds faster.** Every click was reading your Nexus tab, then immediately reloading it and throwing that first read away — about 1.9s of a 9.4s sync, on every single click.

That pre-read made sense when the reload was conditional: the decision needed to know how old the current batch was. Once "every click refreshes everything" became unconditional, the pre-read became pure cost. The one thing it still contributed was the previous levels to diff against, and that's already stored on every successful sync — so the "levels CHANGED / nothing actually new" line now comes from the stored hash instead of a second page read.

The reload itself (~5.5s) is unchanged and still mandatory: only a real page load refreshes Nexus's embedded strike payload, so anything cheaper risks pasting Score / OI / GEX from an old snapshot while the levels look current.

*No behaviour change beyond the speed. If a reload fails, the recovery path is unchanged — reload again, then a fresh tab.*

## v4.2.2 — 2026-08-11

- **Chrome releases now publish themselves.** `release.sh` uploads the store build and submits it for review over the Web Store API, so Chrome and Firefox both ship from one command. This is the first release to do it.
- **Assets renumbered** so the list reads in setup order with no gaps: `0-CHROME` zip, `1-SETUP` Firefox, `2-` Pine, then the three guides.

*Nothing changed in how the extension behaves. The Pine script is unchanged.*

## v4.2.1 — 2026-08-11

**The Chrome Web Store listing is live.** Chrome now installs in one click and updates itself, which it has never done before — every previous Chrome fix meant someone re-sending a zip.

> https://chromewebstore.google.com/detail/aolfgeibjdabmhmdbhgeffamkgjkekbi

Both browsers now keep themselves current: Firefox from GitHub, Chrome from the Store.

Docs updated to match — they previously told Chrome users the listing was still in review.

*Nothing changed in how the extension behaves. The Pine script is unchanged.*

## v4.2.0 — 2026-08-10

**Chrome installs from the Web Store now, and updates itself.**

> https://chromewebstore.google.com/detail/aolfgeibjdabmhmdbhgeffamkgjkekbi

Click **Add to Chrome** and you're done — Chrome keeps you current from then on, the same way Firefox already did. The listing is **unlisted**: not searchable, only reachable with that link.

*If that link doesn't open a listing yet, the first version is still in Google's review queue — use the zip below meanwhile and switch over later.*

Why this took a Store listing rather than a GitHub link: **Chrome blocks off-store extension installs** on Windows and macOS and ignores `update_url` for anything loaded unpacked. Hosting the zip on GitHub can never give Chrome users auto-updates. That's a Chrome restriction, not a gap here — and it's why Firefox has had silent updates all along while Chrome needed a zip re-sent for every fix.

The manual **Load Unpacked** path still works and is documented as the fallback, with the tradeoff stated plainly: installed that way, Chrome will never update it.

*Nothing changed in how the extension behaves. The Pine script is unchanged.*

## v4.1.6 — 2026-08-10

- **Shorter extension description.** The manifest description was 151 characters; the Chrome Web Store caps it at 132, so it was rejected at upload. Now 113: *"Copies your Nexus levels onto your TradingView chart and fills per-strike Score / OI / GEX columns on every sync."* It's also a plainer description of what the thing does than the old one was.
- **A Chrome Web Store build.** `package.sh` now also produces a store-ready archive with `manifest.json` at the root — the Store rejects the nested-folder layout the hand-send zip uses, the same way Firefox does.

*Cosmetic only. Nothing changed in how the extension behaves, and the Pine script is unchanged.*

## v4.1.5 — 2026-08-10

- **The changelog now ships with the package.** [CHANGELOG.md](https://github.com/ahoward001/nexus-tv-bridge/blob/main/CHANGELOG.md) covers every version back to 3.14.3 and is written by the release command itself, so it can't fall behind the release pages.
- **The build refuses to package stray files.** `web-ext` leaves a `.amo-upload-uuid` behind in the source folder after signing, and it had already ended up inside an archive once. The build stops rather than shipping it.
- **The README's version header is stamped** from the manifest like the other docs — it had gone stale at 3.14.3 while the extension was several versions ahead.

*Nothing changed in how the extension behaves. No need to re-paste the Pine script.*

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
