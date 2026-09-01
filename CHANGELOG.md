# Version history

**MAJOR** = a whole new capability · **MINOR** = a feature within one · patch = a bug fix.

Newest first.

---

## v5.1.9.1 — 2026-09-01

**Orange has been impossible for everyone. It works again.**

Orange is the one state based on proof: the export code Nexus is publishing right now differs from the code your chart was built from, so a sync *will* move your lines. To check that, the extension reads the export code off the dashboard — and it refused to read anything unless it first found an element called `section.export-panel`.

The dashboard redesign removed that element. Verified live today: there are zero of them on the export view. So the read returned nothing on **every** call, the comparison had nothing to compare, and orange could never fire — no matter how far the levels had moved. It now recognises the export view by finding the code box itself, which is what it was actually looking for.

**And a matching batch no longer counts as confirmation when its age is unknown.** The dashboard renders on the server and freezes at page load, so a Nexus tab left open since yesterday still shows yesterday's export. The extension read it, compared it against a chart pasted from that same frozen tab, found them identical, and called your chart confirmed current — a green button sitting over day-old levels. When there's no timestamp to read, the age of the page itself is now used, because that *is* the age of the data on it.

Together these are why a wall could close in on price with nothing to show for it: the proof path was dead, and the fallback path was quietly agreeing with a frozen page.

### Recent

**v5.1.8.1** — This is why the button stayed green while the walls closed in on price

**v5.1.6.1** — It checks first and looks at the clock last — so a real change reaches you immediately

**v5.1.5.1** — A chart the extension knows nothing about no longer looks like a chart that's up to date

**v5.1.4.1** — Updating the indicator turns the button yellow instead of syncing on its own

[Full version history →](https://github.com/ahoward001/nexus-tv-bridge/blob/main/CHANGELOG.md)

---

## Assets — what clicking each one actually does

**`0-COPY-THIS-pine-script-for-tradingview.pine`** — the indicator that draws the columns.
**You normally never need this file** — the extension installs and updates this script for you on your first sync. It's here as the fallback for when that can't run, and as the readable copy of what's on your chart. Clicking **downloads a text file and installs nothing**; to paste it in by hand, the "Open the script" link above is easier.

**`1-FIREFOX-SETUP-…​.xpi`** — the Firefox add-on. Same file as the Install button above; clicking it in Firefox installs it. In Chrome it just downloads something useless.

**`2-CHROME-SETUP-…​.zip`** — the Chrome extension as a file, for anyone who can't use the Web Store.
Clicking **downloads a zip and installs nothing.** Chrome can't install an extension from a file. Unzip it → `chrome://extensions` → turn on **Developer mode** (top right) → **Load unpacked** → select the unzipped **`nexus-tradingview-bridge` folder** (the one with `manifest.json` directly inside — Chrome loads the folder, not the zip). Installed this way it will **not** auto-update.

**`3.0-GUIDE-chrome.txt` · `3.1-GUIDE-firefox.txt` · `3.2-GUIDE-pine.md`** — reading, not installing. The long-form walkthroughs if the steps above aren't enough. Readable in your browser: [Chrome](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-chrome-install.txt) · [Firefox](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-firefox-install.txt) · [Pine](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-pine-indicator-setup.md)

*Ignore "Source code (zip/tar.gz)" — GitHub generates those automatically and they aren't the extension.*

---

> **On version currency:** Firefox and the zip above are always this build. **Chrome's Web Store copy can be up to ~24 hours behind** — Google reviews every submission and locks the listing while one is pending, so Store releases land in batches. If you need today's code on Chrome right now, use the `2-CHROME-SETUP` zip and the manual steps above instead of the Store link.

## v5.1.8.1 — 2026-09-01

**This is why the button stayed green while the walls closed in on price.**

The watcher compares the levels on your chart against what Nexus shows now. To do that it first needs the current price — and it was reading the page with `innerText`, which depends on the browser having actually laid the page out. In a tab Chrome isn't painting — a background window, which is where the dashboard normally lives — `innerText` returns an **empty string**, while the page still reports itself as "visible".

So the price came back empty, and the comparison bails the moment it has no price to judge distance from: *"can't judge"*. Nothing was compared. A call wall moving from 715 to 710 with price at 710 sailed straight past it.

Measured on the live dashboard today: `innerText` 0 characters, `textContent` 977,361 characters, with every watched level parsing cleanly out of the second one. Same read, before and after the fix: price `null` → **710.87**.

Every page read now falls back to layout-independent text when `innerText` comes up empty, so the watcher works with the dashboard parked on another monitor — which was always the intended setup.

This is the same trap as the loading bar that measured 0×0 last week: a tab that isn't being drawn still answers questions, it just answers them with nothing.

**Also:** the hot window is back to noon ET after yesterday's testing, and each check still logs what it read and what it concluded.

### Recent

**v5.1.6.1** — It checks first and looks at the clock last — so a real change reaches you immediately

**v5.1.5.1** — A chart the extension knows nothing about no longer looks like a chart that's up to date

**v5.1.4.1** — Updating the indicator turns the button yellow instead of syncing on its own

**v5.1.3.1** — It asks before rewriting your Pine script again — and two syncs can no longer collide

[Full version history →](https://github.com/ahoward001/nexus-tv-bridge/blob/main/CHANGELOG.md)

---

## Assets — what clicking each one actually does

**`0-COPY-THIS-pine-script-for-tradingview.pine`** — the indicator that draws the columns.
**You normally never need this file** — the extension installs and updates this script for you on your first sync. It's here as the fallback for when that can't run, and as the readable copy of what's on your chart. Clicking **downloads a text file and installs nothing**; to paste it in by hand, the "Open the script" link above is easier.

**`1-FIREFOX-SETUP-…​.xpi`** — the Firefox add-on. Same file as the Install button above; clicking it in Firefox installs it. In Chrome it just downloads something useless.

**`2-CHROME-SETUP-…​.zip`** — the Chrome extension as a file, for anyone who can't use the Web Store.
Clicking **downloads a zip and installs nothing.** Chrome can't install an extension from a file. Unzip it → `chrome://extensions` → turn on **Developer mode** (top right) → **Load unpacked** → select the unzipped **`nexus-tradingview-bridge` folder** (the one with `manifest.json` directly inside — Chrome loads the folder, not the zip). Installed this way it will **not** auto-update.

**`3.0-GUIDE-chrome.txt` · `3.1-GUIDE-firefox.txt` · `3.2-GUIDE-pine.md`** — reading, not installing. The long-form walkthroughs if the steps above aren't enough. Readable in your browser: [Chrome](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-chrome-install.txt) · [Firefox](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-firefox-install.txt) · [Pine](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-pine-indicator-setup.md)

*Ignore "Source code (zip/tar.gz)" — GitHub generates those automatically and they aren't the extension.*

---

> **On version currency:** Firefox and the zip above are always this build. **Chrome's Web Store copy can be up to ~24 hours behind** — Google reviews every submission and locks the listing while one is pending, so Store releases land in batches. If you need today's code on Chrome right now, use the `2-CHROME-SETUP` zip and the manual steps above instead of the Store link.

## v5.1.6.1 — 2026-09-01

**It checks first and looks at the clock last — so a real change reaches you immediately.**

The staleness clock used to wrap the entire check: nothing was examined at all until the levels on your chart were older than the threshold. That's backwards. A call wall moving in on price is news the moment it happens, not once a timer says your chart is old enough to bother looking at.

The checks now run every minute regardless of age, and the clock is applied at the very end — and only to a guess. If the export code Nexus is publishing differs from what you pasted, a sync **will** move your lines, and that's now reported the moment it's true, whatever the clock says. Unproven signals still wait for the threshold and still respect the quiet minute after a sync, so this doesn't make the button chattier.

**The hot window now runs to noon ET**, up from 11:00 — so the 1-minute staleness bar covers the whole volatile morning. If you'd never changed that setting by hand, it moves for you; if you had, yours is left alone. It's still adjustable in Settings.

Worth knowing what does and doesn't earn a colour: **orange** means the export genuinely differs from what's on your chart, and it's the only state based on proof. **Yellow** means something moved near price, a strike newly earned a dotted line, or the export couldn't be confirmed. The *size* of a move is never itself a criterion — a big move and a small one both show up as a difference in the export, or not at all.

### Recent

**v5.1.5.1** — A chart the extension knows nothing about no longer looks like a chart that's up to date

**v5.1.4.1** — Updating the indicator turns the button yellow instead of syncing on its own

**v5.1.3.1** — It asks before rewriting your Pine script again — and two syncs can no longer collide

**v5.1.2.0** — Charts now pick up a new indicator on their own. This was broken for everyone

[Full version history →](https://github.com/ahoward001/nexus-tv-bridge/blob/main/CHANGELOG.md)

---

## Assets — what clicking each one actually does

**`0-COPY-THIS-pine-script-for-tradingview.pine`** — the indicator that draws the columns.
**You normally never need this file** — the extension installs and updates this script for you on your first sync. It's here as the fallback for when that can't run, and as the readable copy of what's on your chart. Clicking **downloads a text file and installs nothing**; to paste it in by hand, the "Open the script" link above is easier.

**`1-FIREFOX-SETUP-…​.xpi`** — the Firefox add-on. Same file as the Install button above; clicking it in Firefox installs it. In Chrome it just downloads something useless.

**`2-CHROME-SETUP-…​.zip`** — the Chrome extension as a file, for anyone who can't use the Web Store.
Clicking **downloads a zip and installs nothing.** Chrome can't install an extension from a file. Unzip it → `chrome://extensions` → turn on **Developer mode** (top right) → **Load unpacked** → select the unzipped **`nexus-tradingview-bridge` folder** (the one with `manifest.json` directly inside — Chrome loads the folder, not the zip). Installed this way it will **not** auto-update.

**`3.0-GUIDE-chrome.txt` · `3.1-GUIDE-firefox.txt` · `3.2-GUIDE-pine.md`** — reading, not installing. The long-form walkthroughs if the steps above aren't enough. Readable in your browser: [Chrome](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-chrome-install.txt) · [Firefox](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-firefox-install.txt) · [Pine](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-pine-indicator-setup.md)

*Ignore "Source code (zip/tar.gz)" — GitHub generates those automatically and they aren't the extension.*

---

> **On version currency:** Firefox and the zip above are always this build. **Chrome's Web Store copy can be up to ~24 hours behind** — Google reviews every submission and locks the listing while one is pending, so Store releases land in batches. If you need today's code on Chrome right now, use the `2-CHROME-SETUP` zip and the manual steps above instead of the Store link.

## v5.1.5.1 — 2026-09-01

**A chart the extension knows nothing about no longer looks like a chart that's up to date.**

Green means "your chart matches Nexus". To say that, the extension needs a record of the sync that put the levels there. If it has no record, it used to say nothing at all — and the button's resting state is green, so a chart carrying yesterday's levels sat there looking current.

The record lives in extension storage, **which Chrome wipes every time an extension is removed and re-added**. So every reinstall silently reset every open chart to "no baseline" and left them all green until the next manual sync. That's why a big overnight move could go unflagged: nothing was being evaluated at all.

A chart with no baseline now goes **yellow** — "I can't tell how old these levels are" — which is the honest answer. If you've set the button to stay green when unsure, that still wins; this is the definition of unsure.

**What actually turns the button yellow or orange, since it's worth stating plainly:**

- Nothing is evaluated until the levels on your chart are older than the staleness threshold — 1 minute between the open and 11:00 ET, 10 minutes after that.
- **Orange** means a sync *will* move lines: the export code Nexus is publishing now differs from the one you pasted. It's the only state based on proof.
- **Yellow** is a heads-up: the level cards moved near price, or a strike newly earned a dotted line, or the export couldn't be read to confirm either way.
- The *size* of a move isn't a criterion. A large change and a small one both show up the same way — as a difference in the export, or not at all.

### Recent

**v5.1.4.1** — Updating the indicator turns the button yellow instead of syncing on its own

**v5.1.3.1** — It asks before rewriting your Pine script again — and two syncs can no longer collide

**v5.1.2.0** — Charts now pick up a new indicator on their own. This was broken for everyone

**v5.1.1.1** — Cleans up the version line on your chart, and stops trusting a bad one

[Full version history →](https://github.com/ahoward001/nexus-tv-bridge/blob/main/CHANGELOG.md)

---

## Assets — what clicking each one actually does

**`0-COPY-THIS-pine-script-for-tradingview.pine`** — the indicator that draws the columns.
**You normally never need this file** — the extension installs and updates this script for you on your first sync. It's here as the fallback for when that can't run, and as the readable copy of what's on your chart. Clicking **downloads a text file and installs nothing**; to paste it in by hand, the "Open the script" link above is easier.

**`1-FIREFOX-SETUP-…​.xpi`** — the Firefox add-on. Same file as the Install button above; clicking it in Firefox installs it. In Chrome it just downloads something useless.

**`2-CHROME-SETUP-…​.zip`** — the Chrome extension as a file, for anyone who can't use the Web Store.
Clicking **downloads a zip and installs nothing.** Chrome can't install an extension from a file. Unzip it → `chrome://extensions` → turn on **Developer mode** (top right) → **Load unpacked** → select the unzipped **`nexus-tradingview-bridge` folder** (the one with `manifest.json` directly inside — Chrome loads the folder, not the zip). Installed this way it will **not** auto-update.

**`3.0-GUIDE-chrome.txt` · `3.1-GUIDE-firefox.txt` · `3.2-GUIDE-pine.md`** — reading, not installing. The long-form walkthroughs if the steps above aren't enough. Readable in your browser: [Chrome](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-chrome-install.txt) · [Firefox](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-firefox-install.txt) · [Pine](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-pine-indicator-setup.md)

*Ignore "Source code (zip/tar.gz)" — GitHub generates those automatically and they aren't the extension.*

---

> **On version currency:** Firefox and the zip above are always this build. **Chrome's Web Store copy can be up to ~24 hours behind** — Google reviews every submission and locks the listing while one is pending, so Store releases land in batches. If you need today's code on Chrome right now, use the `2-CHROME-SETUP` zip and the manual steps above instead of the Store link.

## v5.1.4.1 — 2026-08-31

**Updating the indicator turns the button yellow instead of syncing on its own.**

When the Pine script was installed or rewritten, the extension immediately started a sync to fill the columns back in. It meant well, but a sync you didn't ask for reloads your Nexus dashboard tab underneath you — and if you clicked the green button around the same moment, the two runs fought over that tab: one reloaded it while the other was mid-read, and the losing run recovered by opening a stray tab.

Now it just goes **yellow**, the same "worth a click" colour as any other chart that wants a sync, with a hover note saying the indicator was updated. Nothing reloads until you decide to.

The collision itself is fixed too, from either direction: a second sync started while one is already running is ignored rather than run alongside it.

### Recent

**v5.1.3.1** — It asks before rewriting your Pine script again — and two syncs can no longer collide

**v5.1.2.0** — Charts now pick up a new indicator on their own. This was broken for everyone

**v5.1.1.1** — Cleans up the version line on your chart, and stops trusting a bad one

**v5.1.1.0** — Cosmetic, but embarrassing: the version number printed inside the files was growing

[Full version history →](https://github.com/ahoward001/nexus-tv-bridge/blob/main/CHANGELOG.md)

---

## Assets — what clicking each one actually does

**`0-COPY-THIS-pine-script-for-tradingview.pine`** — the indicator that draws the columns.
**You normally never need this file** — the extension installs and updates this script for you on your first sync. It's here as the fallback for when that can't run, and as the readable copy of what's on your chart. Clicking **downloads a text file and installs nothing**; to paste it in by hand, the "Open the script" link above is easier.

**`1-FIREFOX-SETUP-…​.xpi`** — the Firefox add-on. Same file as the Install button above; clicking it in Firefox installs it. In Chrome it just downloads something useless.

**`2-CHROME-SETUP-…​.zip`** — the Chrome extension as a file, for anyone who can't use the Web Store.
Clicking **downloads a zip and installs nothing.** Chrome can't install an extension from a file. Unzip it → `chrome://extensions` → turn on **Developer mode** (top right) → **Load unpacked** → select the unzipped **`nexus-tradingview-bridge` folder** (the one with `manifest.json` directly inside — Chrome loads the folder, not the zip). Installed this way it will **not** auto-update.

**`3.0-GUIDE-chrome.txt` · `3.1-GUIDE-firefox.txt` · `3.2-GUIDE-pine.md`** — reading, not installing. The long-form walkthroughs if the steps above aren't enough. Readable in your browser: [Chrome](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-chrome-install.txt) · [Firefox](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-firefox-install.txt) · [Pine](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-pine-indicator-setup.md)

*Ignore "Source code (zip/tar.gz)" — GitHub generates those automatically and they aren't the extension.*

---

> **On version currency:** Firefox and the zip above are always this build. **Chrome's Web Store copy can be up to ~24 hours behind** — Google reviews every submission and locks the listing while one is pending, so Store releases land in batches. If you need today's code on Chrome right now, use the `2-CHROME-SETUP` zip and the manual steps above instead of the Store link.

## v5.1.3.1 — 2026-08-31

**It asks before rewriting your Pine script again — and two syncs can no longer collide.**

v5.1.2.0 rewrote an out-of-date script on the chart without asking. That was a step too far: it should tell you and let you decide, not paste over your chart on its own. It asks again.

What it keeps from v5.1.2.0 is the part that was actually broken. It used to work out whether your script was current by consulting its own record of having installed it — and that record is wiped whenever the extension is removed and re-added, and never existed at all for anyone who pasted the script in by hand. No record meant no notice, ever, however far behind the chart was. It now reads the version stamp off the chart itself, so it can tell you the script is old regardless of who put it there. The message names the version actually on your chart rather than what we last remembered writing.

**Two syncs can't run at once any more.** Finishing a Pine setup starts a sync by itself, so if you also clicked the button you got two — and they fought over the same Nexus dashboard tab. One reloaded it while the other was mid-read, that read came back with no ticker and no export panel, and the losing run "recovered" by opening a fresh tab. That's the double-reload-and-a-stray-tab you saw. A second sync while one is in flight is now ignored; the button still reports the running one's result.

**Version numbering:** the fourth digit marks that the Pine script changed. It's a standing note, not a counter that resets, so it stays put when the other numbers move — hence 5.1.3.**1**.

### Recent

**v5.1.2.0** — Charts now pick up a new indicator on their own. This was broken for everyone

**v5.1.1.1** — Cleans up the version line on your chart, and stops trusting a bad one

**v5.1.1.0** — Cosmetic, but embarrassing: the version number printed inside the files was growing

**v5.1.0.0** — It waits when Nexus is slow, instead of telling you it failed

[Full version history →](https://github.com/ahoward001/nexus-tv-bridge/blob/main/CHANGELOG.md)

---

## Assets — what clicking each one actually does

**`0-COPY-THIS-pine-script-for-tradingview.pine`** — the indicator that draws the columns.
**You normally never need this file** — the extension installs and updates this script for you on your first sync. It's here as the fallback for when that can't run, and as the readable copy of what's on your chart. Clicking **downloads a text file and installs nothing**; to paste it in by hand, the "Open the script" link above is easier.

**`1-FIREFOX-SETUP-…​.xpi`** — the Firefox add-on. Same file as the Install button above; clicking it in Firefox installs it. In Chrome it just downloads something useless.

**`2-CHROME-SETUP-…​.zip`** — the Chrome extension as a file, for anyone who can't use the Web Store.
Clicking **downloads a zip and installs nothing.** Chrome can't install an extension from a file. Unzip it → `chrome://extensions` → turn on **Developer mode** (top right) → **Load unpacked** → select the unzipped **`nexus-tradingview-bridge` folder** (the one with `manifest.json` directly inside — Chrome loads the folder, not the zip). Installed this way it will **not** auto-update.

**`3.0-GUIDE-chrome.txt` · `3.1-GUIDE-firefox.txt` · `3.2-GUIDE-pine.md`** — reading, not installing. The long-form walkthroughs if the steps above aren't enough. Readable in your browser: [Chrome](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-chrome-install.txt) · [Firefox](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-firefox-install.txt) · [Pine](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-pine-indicator-setup.md)

*Ignore "Source code (zip/tar.gz)" — GitHub generates those automatically and they aren't the extension.*

---

> **On version currency:** Firefox and the zip above are always this build. **Chrome's Web Store copy can be up to ~24 hours behind** — Google reviews every submission and locks the listing while one is pending, so Store releases land in batches. If you need today's code on Chrome right now, use the `2-CHROME-SETUP` zip and the manual steps above instead of the Store link.

## v5.1.2.0 — 2026-08-31

**Charts now pick up a new indicator on their own. This was broken for everyone.**

The extension was only willing to tell you about a newer script if it had a record of installing that script itself. That sounds reasonable and was quietly useless, because the record lives in extension storage — **which Chrome wipes every time an extension is removed and re-added.** Anyone who reinstalled the extension, and anyone who pasted the script into TradingView by hand, had no record. No record meant no update, ever, no matter how far behind the chart was. If your team wasn't picking up new scripts, this is why.

It now reads the chart instead of its own notes. On load, if it has nothing it trusts, it opens the Pine Editor, reads the version stamped in the script, and **rewrites it automatically** if it's behind. No prompt, nothing to notice or click.

Two things it will not do:

- **It won't touch a script that isn't ours.** The Pine Editor opens whatever you had open last, which might be your own work. If the open script isn't Nexus Strike Metrics, it says so in the log and stops. A missed update is recoverable; an overwritten script isn't.
- **It won't rewrite your chart on every release.** "Is this current?" is answered by the indicator's actual code, not its version number — every build re-stamps that number whether or not the script changed. Same code means nothing happens.

Setting up a chart that has *no* indicator on it still asks first. That's a different question from keeping an existing script current, and adding an indicator to someone's chart unannounced is a bigger thing to do uninvited.

**Also fixed:** the release tooling reported a broken update chain on v5.1.1.1 when nothing was wrong — it was reading a CDN cache that hadn't caught up yet. It now asks GitHub directly, and treats a lagging cache as the temporary thing it is.

### Recent

**v5.1.1.1** — Cleans up the version line on your chart, and stops trusting a bad one

**v5.1.1.0** — Cosmetic, but embarrassing: the version number printed inside the files was growing

**v5.1.0.0** — It waits when Nexus is slow, instead of telling you it failed

**v5.0.12.0** — The wait on a slow dashboard is now fifteen seconds

[Full version history →](https://github.com/ahoward001/nexus-tv-bridge/blob/main/CHANGELOG.md)

---

## Assets — what clicking each one actually does

**`0-COPY-THIS-pine-script-for-tradingview.pine`** — the indicator that draws the columns.
**You normally never need this file** — the extension installs and updates this script for you on your first sync. It's here as the fallback for when that can't run, and as the readable copy of what's on your chart. Clicking **downloads a text file and installs nothing**; to paste it in by hand, the "Open the script" link above is easier.

**`1-FIREFOX-SETUP-…​.xpi`** — the Firefox add-on. Same file as the Install button above; clicking it in Firefox installs it. In Chrome it just downloads something useless.

**`2-CHROME-SETUP-…​.zip`** — the Chrome extension as a file, for anyone who can't use the Web Store.
Clicking **downloads a zip and installs nothing.** Chrome can't install an extension from a file. Unzip it → `chrome://extensions` → turn on **Developer mode** (top right) → **Load unpacked** → select the unzipped **`nexus-tradingview-bridge` folder** (the one with `manifest.json` directly inside — Chrome loads the folder, not the zip). Installed this way it will **not** auto-update.

**`3.0-GUIDE-chrome.txt` · `3.1-GUIDE-firefox.txt` · `3.2-GUIDE-pine.md`** — reading, not installing. The long-form walkthroughs if the steps above aren't enough. Readable in your browser: [Chrome](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-chrome-install.txt) · [Firefox](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-firefox-install.txt) · [Pine](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-pine-indicator-setup.md)

*Ignore "Source code (zip/tar.gz)" — GitHub generates those automatically and they aren't the extension.*

---

> **On version currency:** Firefox and the zip above are always this build. **Chrome's Web Store copy can be up to ~24 hours behind** — Google reviews every submission and locks the listing while one is pending, so Store releases land in batches. If you need today's code on Chrome right now, use the `2-CHROME-SETUP` zip and the manual steps above instead of the Store link.

## v5.1.1.1 — 2026-08-31

**Cleans up the version line on your chart, and stops trusting a bad one.**

v5.1.1.0 fixed the packaging bug that kept adding `.0` to the version stamped inside the Pine script. It didn't fix the copy already sitting on your chart — that one still reads:

    // Nexus Strike Metrics for Nexus → TradingView Bridge 5.1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0

Reload a chart with the script on it and the extension now offers to rewrite it, stamped cleanly. It's a one-time tidy-up per chart: the indicator's code is unchanged, only the header line, and your settings are kept. Say yes once and it won't ask again.

**It also stops mis-reading these stamps.** Two things were wrong. The pattern that reads the version only ever looked at the first four parts, so `5.1.0.0.0.0.0.0` came back as `5.1.0.0` and looked perfectly valid. And after pasting, the check that confirms the new script landed was a substring test — `"5.1.0.0.0.0"` contains `"5.1.0.0"`, so a stale script could confirm itself as current. Both now read the whole stamp and compare it exactly, which is also why the extension can tell your chart needs the tidy-up at all.

Normal updates are unaffected: the extension still only offers a real update when the indicator's *code* actually changes, not every time a version number moves.

### Recent

**v5.1.1.0** — Cosmetic, but embarrassing: the version number printed inside the files was growing

**v5.1.0.0** — It waits when Nexus is slow, instead of telling you it failed

**v5.0.12.0** — The wait on a slow dashboard is now fifteen seconds

**v5.0.11.0** — It now watches the dashboard's loading bar, and waits while it's up

[Full version history →](https://github.com/ahoward001/nexus-tv-bridge/blob/main/CHANGELOG.md)

---

## Assets — what clicking each one actually does

**`0-COPY-THIS-pine-script-for-tradingview.pine`** — the indicator that draws the columns.
**You normally never need this file** — the extension installs and updates this script for you on your first sync. It's here as the fallback for when that can't run, and as the readable copy of what's on your chart. Clicking **downloads a text file and installs nothing**; to paste it in by hand, the "Open the script" link above is easier.

**`1-FIREFOX-SETUP-…​.xpi`** — the Firefox add-on. Same file as the Install button above; clicking it in Firefox installs it. In Chrome it just downloads something useless.

**`2-CHROME-SETUP-…​.zip`** — the Chrome extension as a file, for anyone who can't use the Web Store.
Clicking **downloads a zip and installs nothing.** Chrome can't install an extension from a file. Unzip it → `chrome://extensions` → turn on **Developer mode** (top right) → **Load unpacked** → select the unzipped **`nexus-tradingview-bridge` folder** (the one with `manifest.json` directly inside — Chrome loads the folder, not the zip). Installed this way it will **not** auto-update.

**`3.0-GUIDE-chrome.txt` · `3.1-GUIDE-firefox.txt` · `3.2-GUIDE-pine.md`** — reading, not installing. The long-form walkthroughs if the steps above aren't enough. Readable in your browser: [Chrome](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-chrome-install.txt) · [Firefox](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-firefox-install.txt) · [Pine](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-pine-indicator-setup.md)

*Ignore "Source code (zip/tar.gz)" — GitHub generates those automatically and they aren't the extension.*

---

> **On version currency:** Firefox and the zip above are always this build. **Chrome's Web Store copy can be up to ~24 hours behind** — Google reviews every submission and locks the listing while one is pending, so Store releases land in batches. If you need today's code on Chrome right now, use the `2-CHROME-SETUP` zip and the manual steps above instead of the Store link.

## v5.1.1.0 — 2026-08-31

**Cosmetic, but embarrassing: the version number printed inside the files was growing.**

The script that stamps the version into the Pine indicator, the install guides and the READMEs was written for three-part version numbers. When numbering moved to four parts, it matched the first three, replaced those, and left the rest behind — adding another `.0` on every release since. By this one the Pine header on your chart read:

    // Nexus Strike Metrics for Nexus → TradingView Bridge 5.1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0

Nothing was broken by it — the extension reads at most four parts when it checks whether your chart's script is current, so `5.1.0.0` still matched and updates still worked. But it was in the Pine header you can see, in `INSTALL.txt`, and in the setup guides attached to these releases.

Both READMEs had the opposite problem from the same cause: the pattern never matched at all, so they'd been frozen at **5.0.0.0** while everything else moved on.

The stamper now matches the whole version, however many parts it has, so it can't leave a tail behind or silently skip a file again. All seven files are correct as of this release.

### Recent

**v5.1.0.0** — It waits when Nexus is slow, instead of telling you it failed

**v5.0.12.0** — The wait on a slow dashboard is now fifteen seconds

**v5.0.11.0** — It now watches the dashboard's loading bar, and waits while it's up

**v5.0.10.0** — "Couldn't reload Nexus" on a slow morning — when the data was seconds away

[Full version history →](https://github.com/ahoward001/nexus-tv-bridge/blob/main/CHANGELOG.md)

---

## Assets — what clicking each one actually does

**`0-COPY-THIS-pine-script-for-tradingview.pine`** — the indicator that draws the columns.
**You normally never need this file** — the extension installs and updates this script for you on your first sync. It's here as the fallback for when that can't run, and as the readable copy of what's on your chart. Clicking **downloads a text file and installs nothing**; to paste it in by hand, the "Open the script" link above is easier.

**`1-FIREFOX-SETUP-…​.xpi`** — the Firefox add-on. Same file as the Install button above; clicking it in Firefox installs it. In Chrome it just downloads something useless.

**`2-CHROME-SETUP-…​.zip`** — the Chrome extension as a file, for anyone who can't use the Web Store.
Clicking **downloads a zip and installs nothing.** Chrome can't install an extension from a file. Unzip it → `chrome://extensions` → turn on **Developer mode** (top right) → **Load unpacked** → select the unzipped **`nexus-tradingview-bridge` folder** (the one with `manifest.json` directly inside — Chrome loads the folder, not the zip). Installed this way it will **not** auto-update.

**`3.0-GUIDE-chrome.txt` · `3.1-GUIDE-firefox.txt` · `3.2-GUIDE-pine.md`** — reading, not installing. The long-form walkthroughs if the steps above aren't enough. Readable in your browser: [Chrome](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-chrome-install.txt) · [Firefox](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-firefox-install.txt) · [Pine](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-pine-indicator-setup.md)

*Ignore "Source code (zip/tar.gz)" — GitHub generates those automatically and they aren't the extension.*

---

> **On version currency:** Firefox and the zip above are always this build. **Chrome's Web Store copy can be up to ~24 hours behind** — Google reviews every submission and locks the listing while one is pending, so Store releases land in batches. If you need today's code on Chrome right now, use the `2-CHROME-SETUP` zip and the manual steps above instead of the Store link.

## v5.1.0.0 — 2026-08-31

**It waits when Nexus is slow, instead of telling you it failed.**

When the dashboard is busy, its export tab shows a progress bar and *"Loading tab data"* while it fetches. The sync couldn't see that, so it gave up on its own schedule and reported a failure — for data that was still on its way. Click again a minute later and it works, which is where the contradictory pair of messages came from: *"couldn't reload Nexus"* followed by a green tick saying nothing had changed.

It now watches for that bar and holds while it's up, for up to 15 seconds past its normal budget. That time is only ever spent while the dashboard is visibly still working, so a normal day is exactly as fast as before. Once the bar is gone and there's still no data, it fails immediately, as it always did.

**When it needs to open a tab of its own,** it now opens in your largest window, maximizes that window if it's small, and brings it to the front. That's partly so it isn't jarring, but mostly because it matters: Nexus only loads a tab's data while that tab is actually on screen, so a tab parked in a cramped or minimized window could stall the very read it was opened to do.

**It also refuses to guess your chart's symbol.** If the symbol won't read for a moment, it changes nothing and says so, rather than falling back to whatever ticker the dashboard happened to be showing — which could put SPX's levels on a QQQ chart under a green tick.

**The install page above is reorganised:** installing the extension and setting up the indicators are now two separate sections. Worth knowing if you're setting someone else up — the **Nexus Strike Metrics** script is no longer something you paste in by hand. The extension writes it, adds it to your chart, and updates it in place when it changes. The manual steps are still there as a fallback.

### Recent

**v5.0.12.0** — The wait on a slow dashboard is now fifteen seconds

**v5.0.11.0** — It now watches the dashboard's loading bar, and waits while it's up

**v5.0.10.0** — "Couldn't reload Nexus" on a slow morning — when the data was seconds away

**v5.0.9.0** — A QQQ chart could get SPX's levels, and be told it worked

[Full version history →](https://github.com/ahoward001/nexus-tv-bridge/blob/main/CHANGELOG.md)

---

## Assets — what clicking each one actually does

**`0-COPY-THIS-pine-script-for-tradingview.pine`** — the indicator that draws the columns.
**You normally never need this file** — the extension installs and updates this script for you on your first sync. It's here as the fallback for when that can't run, and as the readable copy of what's on your chart. Clicking **downloads a text file and installs nothing**; to paste it in by hand, the "Open the script" link above is easier.

**`1-FIREFOX-SETUP-…​.xpi`** — the Firefox add-on. Same file as the Install button above; clicking it in Firefox installs it. In Chrome it just downloads something useless.

**`2-CHROME-SETUP-…​.zip`** — the Chrome extension as a file, for anyone who can't use the Web Store.
Clicking **downloads a zip and installs nothing.** Chrome can't install an extension from a file. Unzip it → `chrome://extensions` → turn on **Developer mode** (top right) → **Load unpacked** → select the unzipped **`nexus-tradingview-bridge` folder** (the one with `manifest.json` directly inside — Chrome loads the folder, not the zip). Installed this way it will **not** auto-update.

**`3.0-GUIDE-chrome.txt` · `3.1-GUIDE-firefox.txt` · `3.2-GUIDE-pine.md`** — reading, not installing. The long-form walkthroughs if the steps above aren't enough. Readable in your browser: [Chrome](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-chrome-install.txt) · [Firefox](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-firefox-install.txt) · [Pine](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-pine-indicator-setup.md)

*Ignore "Source code (zip/tar.gz)" — GitHub generates those automatically and they aren't the extension.*

---

> **On version currency:** Firefox and the zip above are always this build. **Chrome's Web Store copy can be up to ~24 hours behind** — Google reviews every submission and locks the listing while one is pending, so Store releases land in batches. If you need today's code on Chrome right now, use the `2-CHROME-SETUP` zip and the manual steps above instead of the Store link.

## v5.0.12.0 — 2026-08-31

**The wait on a slow dashboard is now fifteen seconds.**

v5.0.11.0 taught the sync to watch for the dashboard's "Loading tab data" bar and keep waiting while it's up. That hold was set to 25 seconds; it's now 15, which is long enough for the slow loads seen in practice without leaving you staring at a sync that won't finish.

Everything else about it is unchanged: the extra time is only ever spent while the loading bar is actually on screen, so a normal day never touches it, and once the bar is gone an empty box still fails immediately.

Also fixed: an unrecognized flag on the release script was silently ignored instead of stopping the run — so a mistyped `--dry` published a real release. Any unknown flag now stops before anything ships.

### Recent

**v5.0.11.0** — It now watches the dashboard's loading bar, and waits while it's up

**v5.0.10.0** — "Couldn't reload Nexus" on a slow morning — when the data was seconds away

**v5.0.9.0** — A QQQ chart could get SPX's levels, and be told it worked

**v5.0.8.0** — Nexus rebuilt the strike table, and the reader that was supposed to catch a stale snapshot could no longer see it

[Full version history →](https://github.com/ahoward001/nexus-tv-bridge/blob/main/CHANGELOG.md)

---

## Assets — what clicking each one actually does

**`0-COPY-THIS-pine-script-for-tradingview.pine`** — the indicator that draws the columns, needed on **both** browsers.
Clicking **downloads a text file and installs nothing.** You paste its contents into TradingView's Pine Editor by hand — usually easier to use the "Open the script" link above and copy it in the browser.

**`1-FIREFOX-SETUP-…​.xpi`** — the Firefox add-on. Same file as the Install button above; clicking it in Firefox installs it. In Chrome it just downloads something useless.

**`2-CHROME-SETUP-…​.zip`** — the Chrome extension as a file, for anyone who can't use the Web Store.
Clicking **downloads a zip and installs nothing.** Chrome can't install an extension from a file. Unzip it → `chrome://extensions` → turn on **Developer mode** (top right) → **Load unpacked** → select the unzipped **`nexus-tradingview-bridge` folder** (the one with `manifest.json` directly inside — Chrome loads the folder, not the zip). Installed this way it will **not** auto-update.

**`3.0-GUIDE-chrome.txt` · `3.1-GUIDE-firefox.txt` · `3.2-GUIDE-pine.md`** — reading, not installing. The long-form walkthroughs if the steps above aren't enough. Readable in your browser: [Chrome](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-chrome-install.txt) · [Firefox](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-firefox-install.txt) · [Pine](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-pine-indicator-setup.md)

*Ignore "Source code (zip/tar.gz)" — GitHub generates those automatically and they aren't the extension.*

---

> **On version currency:** Firefox and the zip above are always this build. **Chrome's Web Store copy can be up to ~24 hours behind** — Google reviews every submission and locks the listing while one is pending, so Store releases land in batches. If you need today's code on Chrome right now, use the `2-CHROME-SETUP` zip and the manual steps above instead of the Store link.

## v5.0.11.0 — 2026-08-31

**It now watches the dashboard's loading bar, and waits while it's up.**

When Nexus is slow, the export tab shows a progress bar and "Loading tab data" while it fetches. The sync couldn't see that, so it gave up on its own schedule and reported a failure — for data that was still on its way. Click again a minute later and it works, which is where the contradictory pair of messages came from.

It now looks for that bar. While it's on screen the data is coming, so the read holds and keeps checking, up to 25 seconds past its normal budget. When the bar is gone and there's still no code, the box is genuinely empty and it fails as before — the extra time is only ever spent when the dashboard is visibly still working, so a normal day is untouched.

This is the fix v5.0.10.0 should have been. That release watched the *page load*, which was the wrong thing to watch: the dashboard finishes loading and reports itself complete long before the export tab's data arrives — measured at 22 seconds and still counting on a slow afternoon, on a page that called itself done. The loading bar is the honest signal. The page-load handling from 5.0.10.0 stays, since it covers genuinely slow navigations.

**When it opens a tab of its own,** it now puts it in your largest window, maximizes that window if it's small, and brings it to the front. Beyond being less jarring, it's load-bearing: Nexus only fetches a tab's data while that tab is actually painting, so a cramped or minimized window could stall the very read the tab was opened to do.

Build artifacts no longer land in your Downloads folder; they're written to the project's own `build/` directory.

### Recent

**v5.0.10.0** — "Couldn't reload Nexus" on a slow morning — when the data was seconds away

**v5.0.9.0** — A QQQ chart could get SPX's levels, and be told it worked

**v5.0.8.0** — Nexus rebuilt the strike table, and the reader that was supposed to catch a stale snapshot could no longer see it

**v5.0.7.0** — A stale snapshot can now be caught on a tab where nothing is rendered at all

[Full version history →](https://github.com/ahoward001/nexus-tv-bridge/blob/main/CHANGELOG.md)

---

## Assets — what clicking each one actually does

**`0-COPY-THIS-pine-script-for-tradingview.pine`** — the indicator that draws the columns, needed on **both** browsers.
Clicking **downloads a text file and installs nothing.** You paste its contents into TradingView's Pine Editor by hand — usually easier to use the "Open the script" link above and copy it in the browser.

**`1-FIREFOX-SETUP-…​.xpi`** — the Firefox add-on. Same file as the Install button above; clicking it in Firefox installs it. In Chrome it just downloads something useless.

**`2-CHROME-SETUP-…​.zip`** — the Chrome extension as a file, for anyone who can't use the Web Store.
Clicking **downloads a zip and installs nothing.** Chrome can't install an extension from a file. Unzip it → `chrome://extensions` → turn on **Developer mode** (top right) → **Load unpacked** → select the unzipped **`nexus-tradingview-bridge` folder** (the one with `manifest.json` directly inside — Chrome loads the folder, not the zip). Installed this way it will **not** auto-update.

**`3.0-GUIDE-chrome.txt` · `3.1-GUIDE-firefox.txt` · `3.2-GUIDE-pine.md`** — reading, not installing. The long-form walkthroughs if the steps above aren't enough. Readable in your browser: [Chrome](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-chrome-install.txt) · [Firefox](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-firefox-install.txt) · [Pine](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-pine-indicator-setup.md)

*Ignore "Source code (zip/tar.gz)" — GitHub generates those automatically and they aren't the extension.*

---

> **On version currency:** Firefox and the zip above are always this build. **Chrome's Web Store copy can be up to ~24 hours behind** — Google reviews every submission and locks the listing while one is pending, so Store releases land in batches. If you need today's code on Chrome right now, use the `2-CHROME-SETUP` zip and the manual steps above instead of the Store link.

## v5.0.10.0 — 2026-08-31

**"Couldn't reload Nexus" on a slow morning — when the data was seconds away.**

Every step of a sync has a time budget, sized for a normal day. When the dashboard is slow, those budgets ran out while the page was still on its way, and the sync then read a page that hadn't rendered yet and reported failure. Click again a moment later and it passes with a green tick — which is where the contradictory pair of messages came from. One of them was wrong, and it was the failure.

The fix is not a longer wait for everybody. That would tax every fast day to pay for the occasional slow one. Instead, when a budget runs out, it now checks whether the tab is *still loading* — Chrome's own loading indicator, the same thing you see spinning. If it is, that's live evidence the page is coming, so it holds on and keeps checking, up to twelve seconds past the budget. If the tab has gone quiet, it gives up exactly as before.

A page that lands on time never touches any of this, so nothing gets slower on a normal day. Measured on the dashboard as it is now: a good load finishes in about 1.7 seconds, well inside the budget.

Worth knowing why it watches the tab and not the page: the dashboard renders on the server and freezes at load — measured live, zero updates and no data fetches happen after the page arrives. There's no spinner inside the page to watch for. The slow part *is* the page load, which is exactly what the tab indicator reports, and it can't be broken by the next dashboard redesign.

Also: the release tooling no longer false-alarms about serving an unsigned Firefox build when a freshly uploaded file simply hasn't finished propagating yet.

### Recent

**v5.0.9.0** — A QQQ chart could get SPX's levels, and be told it worked

**v5.0.8.0** — Nexus rebuilt the strike table, and the reader that was supposed to catch a stale snapshot could no longer see it

**v5.0.7.0** — A stale snapshot can now be caught on a tab where nothing is rendered at all

**v5.0.6.0** — The columns could be a batch behind while the sync insisted they were current

[Full version history →](https://github.com/ahoward001/nexus-tv-bridge/blob/main/CHANGELOG.md)

---

## Assets — what clicking each one actually does

**`0-COPY-THIS-pine-script-for-tradingview.pine`** — the indicator that draws the columns, needed on **both** browsers.
Clicking **downloads a text file and installs nothing.** You paste its contents into TradingView's Pine Editor by hand — usually easier to use the "Open the script" link above and copy it in the browser.

**`1-FIREFOX-SETUP-…​.xpi`** — the Firefox add-on. Same file as the Install button above; clicking it in Firefox installs it. In Chrome it just downloads something useless.

**`2-CHROME-SETUP-…​.zip`** — the Chrome extension as a file, for anyone who can't use the Web Store.
Clicking **downloads a zip and installs nothing.** Chrome can't install an extension from a file. Unzip it → `chrome://extensions` → turn on **Developer mode** (top right) → **Load unpacked** → select the unzipped **`nexus-tradingview-bridge` folder** (the one with `manifest.json` directly inside — Chrome loads the folder, not the zip). Installed this way it will **not** auto-update.

**`3.0-GUIDE-chrome.txt` · `3.1-GUIDE-firefox.txt` · `3.2-GUIDE-pine.md`** — reading, not installing. The long-form walkthroughs if the steps above aren't enough. Readable in your browser: [Chrome](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-chrome-install.txt) · [Firefox](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-firefox-install.txt) · [Pine](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-pine-indicator-setup.md)

*Ignore "Source code (zip/tar.gz)" — GitHub generates those automatically and they aren't the extension.*

---

> **On version currency:** Firefox and the zip above are always this build. **Chrome's Web Store copy can be up to ~24 hours behind** — Google reviews every submission and locks the listing while one is pending, so Store releases land in batches. If you need today's code on Chrome right now, use the `2-CHROME-SETUP` zip and the manual steps above instead of the Store link.

## v5.0.9.0 — 2026-08-31

**A QQQ chart could get SPX's levels, and be told it worked.**

To know which symbol to fetch, the sync reads it off your chart. If that read fails it used to fall back to whichever ticker your Nexus dashboard happened to be showing, and then to QQQ. That fallback makes sense when you sync from the dashboard with no chart involved. It is dangerous when a chart *is* the target and its symbol simply didn't read for a moment — because the run then goes and fetches a different instrument's levels and pastes them onto your chart, with a green tick and nothing to suggest anything is wrong.

Seen live: a QQQ chart drove the dashboard to `ticker=SPX` and applied SPX's levels. A chart tab that has just been dragged between windows, or is still settling, is enough to trigger it.

It now refuses. If there's a chart in front of it and the symbol won't read, nothing is changed and it says so — naming the symbol it *would* have guessed, so you can see what was avoided. The next click reads fine.

Wrong levels that look right are worse than no levels.

### Recent

**v5.0.8.0** — Nexus rebuilt the strike table, and the reader that was supposed to catch a stale snapshot could no longer see it

**v5.0.7.0** — A stale snapshot can now be caught on a tab where nothing is rendered at all

**v5.0.6.0** — The columns could be a batch behind while the sync insisted they were current

**v5.0.5.0** — One click said it couldn't reach Nexus; the next said "no newer levels" with a green tick. Neither had actually reached Nexus

[Full version history →](https://github.com/ahoward001/nexus-tv-bridge/blob/main/CHANGELOG.md)

---

## Assets — what clicking each one actually does

**`0-COPY-THIS-pine-script-for-tradingview.pine`** — the indicator that draws the columns, needed on **both** browsers.
Clicking **downloads a text file and installs nothing.** You paste its contents into TradingView's Pine Editor by hand — usually easier to use the "Open the script" link above and copy it in the browser.

**`1-FIREFOX-SETUP-…​.xpi`** — the Firefox add-on. Same file as the Install button above; clicking it in Firefox installs it. In Chrome it just downloads something useless.

**`2-CHROME-SETUP-…​.zip`** — the Chrome extension as a file, for anyone who can't use the Web Store.
Clicking **downloads a zip and installs nothing.** Chrome can't install an extension from a file. Unzip it → `chrome://extensions` → turn on **Developer mode** (top right) → **Load unpacked** → select the unzipped **`nexus-tradingview-bridge` folder** (the one with `manifest.json` directly inside — Chrome loads the folder, not the zip). Installed this way it will **not** auto-update.

**`3.0-GUIDE-chrome.txt` · `3.1-GUIDE-firefox.txt` · `3.2-GUIDE-pine.md`** — reading, not installing. The long-form walkthroughs if the steps above aren't enough. Readable in your browser: [Chrome](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-chrome-install.txt) · [Firefox](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-firefox-install.txt) · [Pine](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-pine-indicator-setup.md)

*Ignore "Source code (zip/tar.gz)" — GitHub generates those automatically and they aren't the extension.*

---

> **On version currency:** Firefox and the zip above are always this build. **Chrome's Web Store copy can be up to ~24 hours behind** — Google reviews every submission and locks the listing while one is pending, so Store releases land in batches. If you need today's code on Chrome right now, use the `2-CHROME-SETUP` zip and the manual steps above instead of the Store link.

## v5.0.8.0 — 2026-08-31

**Nexus rebuilt the strike table, and the reader that was supposed to catch a stale snapshot could no longer see it.**

There are two ways to read the per-strike numbers: the data Nexus writes into the page, and the table it renders on screen. The first is fast and works on a background tab; the second is always current. Recent releases got better at noticing when the first one had gone stale — and then handed over to a reader that, since today's redesign, finds nothing at all.

Checked against the live dashboard: the row markup this fell back on matches **zero** elements now. There is no HTML table on the page either. The rows moved to ARIA roles — 27 of them on a QQQ overview, one header plus twenty-six strikes.

It now reads those, matching columns by their headings rather than counting positions, so a future reorder corrects itself. The old markup is still tried first-in-line, so an older dashboard keeps working. Verified against the live page: 26 strikes, values matching the screen.

Also fixed alongside it: the section heading has been renamed again, the check for "is a Nexus dashboard even loaded here" was looking for an element that no longer exists, and the GEX column is now the twelfth rather than the eleventh.

### Recent

**v5.0.7.0** — A stale snapshot can now be caught on a tab where nothing is rendered at all

**v5.0.6.0** — The columns could be a batch behind while the sync insisted they were current

**v5.0.5.0** — One click said it couldn't reach Nexus; the next said "no newer levels" with a green tick. Neither had actually reached Nexus

**v5.0.4.0** — "Strike metrics didn't update" — because Nexus changed the shape of its data

[Full version history →](https://github.com/ahoward001/nexus-tv-bridge/blob/main/CHANGELOG.md)

---

## Assets — what clicking each one actually does

**`0-COPY-THIS-pine-script-for-tradingview.pine`** — the indicator that draws the columns, needed on **both** browsers.
Clicking **downloads a text file and installs nothing.** You paste its contents into TradingView's Pine Editor by hand — usually easier to use the "Open the script" link above and copy it in the browser.

**`1-FIREFOX-SETUP-…​.xpi`** — the Firefox add-on. Same file as the Install button above; clicking it in Firefox installs it. In Chrome it just downloads something useless.

**`2-CHROME-SETUP-…​.zip`** — the Chrome extension as a file, for anyone who can't use the Web Store.
Clicking **downloads a zip and installs nothing.** Chrome can't install an extension from a file. Unzip it → `chrome://extensions` → turn on **Developer mode** (top right) → **Load unpacked** → select the unzipped **`nexus-tradingview-bridge` folder** (the one with `manifest.json` directly inside — Chrome loads the folder, not the zip). Installed this way it will **not** auto-update.

**`3.0-GUIDE-chrome.txt` · `3.1-GUIDE-firefox.txt` · `3.2-GUIDE-pine.md`** — reading, not installing. The long-form walkthroughs if the steps above aren't enough. Readable in your browser: [Chrome](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-chrome-install.txt) · [Firefox](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-firefox-install.txt) · [Pine](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-pine-indicator-setup.md)

*Ignore "Source code (zip/tar.gz)" — GitHub generates those automatically and they aren't the extension.*

---

> **On version currency:** Firefox and the zip above are always this build. **Chrome's Web Store copy can be up to ~24 hours behind** — Google reviews every submission and locks the listing while one is pending, so Store releases land in batches. If you need today's code on Chrome right now, use the `2-CHROME-SETUP` zip and the manual steps above instead of the Store link.

## v5.0.7.0 — 2026-08-31

**A stale snapshot can now be caught on a tab where nothing is rendered at all.**

The per-strike numbers come from data Nexus writes into the page when the server renders it. Client-side updates repaint the table but never rewrite that data — so what we read is frozen at page load, and its age is simply the page's age.

The previous release started catching stale snapshots by comparing their values against the table on screen. That works, and it's verified working on a live dashboard. But it needs a table to compare against, and so does the older spot check — and on a Nexus tab sitting in the background, collapsed, neither is there. Measured on a live page: 55 rows of data, **no** grid rendered and **no** readable spot card, so nothing was checking anything and the snapshot was taken on trust.

There is a signal that's always available, and it's the most direct one: how long ago the page was rendered. That's exactly how old the data is. Past two minutes — Nexus republishes about once a minute — the snapshot is treated as stale and the live table is used instead.

Three checks now, in order of how reliable they are: the page's own age, then whether the snapshot's values still match what's on screen, then the old spot comparison as a last resort.

### Recent

**v5.0.6.0** — The columns could be a batch behind while the sync insisted they were current

**v5.0.5.0** — One click said it couldn't reach Nexus; the next said "no newer levels" with a green tick. Neither had actually reached Nexus

**v5.0.4.0** — "Strike metrics didn't update" — because Nexus changed the shape of its data

**v5.0.3.0** — A narrowed Nexus window broke the sync, and the last version cried wolf about it

[Full version history →](https://github.com/ahoward001/nexus-tv-bridge/blob/main/CHANGELOG.md)

---

## Assets — what clicking each one actually does

**`0-COPY-THIS-pine-script-for-tradingview.pine`** — the indicator that draws the columns, needed on **both** browsers.
Clicking **downloads a text file and installs nothing.** You paste its contents into TradingView's Pine Editor by hand — usually easier to use the "Open the script" link above and copy it in the browser.

**`1-FIREFOX-SETUP-…​.xpi`** — the Firefox add-on. Same file as the Install button above; clicking it in Firefox installs it. In Chrome it just downloads something useless.

**`2-CHROME-SETUP-…​.zip`** — the Chrome extension as a file, for anyone who can't use the Web Store.
Clicking **downloads a zip and installs nothing.** Chrome can't install an extension from a file. Unzip it → `chrome://extensions` → turn on **Developer mode** (top right) → **Load unpacked** → select the unzipped **`nexus-tradingview-bridge` folder** (the one with `manifest.json` directly inside — Chrome loads the folder, not the zip). Installed this way it will **not** auto-update.

**`3.0-GUIDE-chrome.txt` · `3.1-GUIDE-firefox.txt` · `3.2-GUIDE-pine.md`** — reading, not installing. The long-form walkthroughs if the steps above aren't enough. Readable in your browser: [Chrome](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-chrome-install.txt) · [Firefox](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-firefox-install.txt) · [Pine](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-pine-indicator-setup.md)

*Ignore "Source code (zip/tar.gz)" — GitHub generates those automatically and they aren't the extension.*

---

> **On version currency:** Firefox and the zip above are always this build. **Chrome's Web Store copy can be up to ~24 hours behind** — Google reviews every submission and locks the listing while one is pending, so Store releases land in batches. If you need today's code on Chrome right now, use the `2-CHROME-SETUP` zip and the manual steps above instead of the Store link.

## v5.0.6.0 — 2026-08-31

**The columns could be a batch behind while the sync insisted they were current.**

The per-strike numbers are read from the dashboard's own data rather than its rendered table — that's what lets a sync work without the Nexus tab being visible or the strike section expanded. But that data is a **snapshot taken when the page loaded**, while the table on screen keeps updating. So the snapshot can fall behind what you're looking at.

There was a check for this, and it asked the wrong question: it compared the snapshot's spot price against the live one and called it stale only if they differed by more than a strike and a half. On a quiet tape spot barely moves while the chain moves plenty. Observed live: strike 715's GEX was **−38.2M** in the snapshot and **−42.5M** on the dashboard, with spot sitting at 715 either way. The check passed, the old numbers went to the chart, and the sync reported success.

It now asks the question that actually matters — do the snapshot's own numbers still appear on screen? It takes the strikes nearest spot and looks for their values in the rendered grid. If the grid is showing numbers and none of them are ours, the snapshot has been overtaken and the live grid is used instead, whatever spot says. When no grid is rendered there is nothing to compare against, so it keeps the snapshot rather than inventing a problem.

### Recent

**v5.0.5.0** — One click said it couldn't reach Nexus; the next said "no newer levels" with a green tick. Neither had actually reached Nexus

**v5.0.4.0** — "Strike metrics didn't update" — because Nexus changed the shape of its data

**v5.0.3.0** — A narrowed Nexus window broke the sync, and the last version cried wolf about it

**v5.0.2.0** — A sync could report success while Nexus Futures drew nothing

[Full version history →](https://github.com/ahoward001/nexus-tv-bridge/blob/main/CHANGELOG.md)

---

## Assets — what clicking each one actually does

**`0-COPY-THIS-pine-script-for-tradingview.pine`** — the indicator that draws the columns, needed on **both** browsers.
Clicking **downloads a text file and installs nothing.** You paste its contents into TradingView's Pine Editor by hand — usually easier to use the "Open the script" link above and copy it in the browser.

**`1-FIREFOX-SETUP-…​.xpi`** — the Firefox add-on. Same file as the Install button above; clicking it in Firefox installs it. In Chrome it just downloads something useless.

**`2-CHROME-SETUP-…​.zip`** — the Chrome extension as a file, for anyone who can't use the Web Store.
Clicking **downloads a zip and installs nothing.** Chrome can't install an extension from a file. Unzip it → `chrome://extensions` → turn on **Developer mode** (top right) → **Load unpacked** → select the unzipped **`nexus-tradingview-bridge` folder** (the one with `manifest.json` directly inside — Chrome loads the folder, not the zip). Installed this way it will **not** auto-update.

**`3.0-GUIDE-chrome.txt` · `3.1-GUIDE-firefox.txt` · `3.2-GUIDE-pine.md`** — reading, not installing. The long-form walkthroughs if the steps above aren't enough. Readable in your browser: [Chrome](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-chrome-install.txt) · [Firefox](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-firefox-install.txt) · [Pine](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-pine-indicator-setup.md)

*Ignore "Source code (zip/tar.gz)" — GitHub generates those automatically and they aren't the extension.*

---

> **On version currency:** Firefox and the zip above are always this build. **Chrome's Web Store copy can be up to ~24 hours behind** — Google reviews every submission and locks the listing while one is pending, so Store releases land in batches. If you need today's code on Chrome right now, use the `2-CHROME-SETUP` zip and the manual steps above instead of the Store link.

## v5.0.5.0 — 2026-08-31

**One click said it couldn't reach Nexus; the next said "no newer levels" with a green tick. Neither had actually reached Nexus.**

Both messages came from the same run of events, and only one of them could be true — which is exactly the right thing to notice.

**"Confirmed" was being claimed without checking.** When the export already on the page was young enough, the sync skipped the reload entirely — sensible, and that's the fast path working as designed. But it then labelled the result the same way as a run that *had* reloaded and compared, so the hover said **"checked Nexus, nothing newer published"** about a run that checked nothing. That now says what actually happened: *"levels already current — Nexus not re-checked this run"*.

**And a failed run no longer hands the next one a free pass.** After a reload that didn't land, the following click would look at the export age, find it under the threshold, take the shortcut and report success. So the failure and the false all-clear were the same data seen twice. A sync that couldn't reach Nexus now forces the next one to do a real reload rather than trusting the age — until one of them actually gets through.

Nothing about the levels themselves changed; this is only about the extension telling you the truth about what it did and didn't verify.

### Recent

**v5.0.4.0** — "Strike metrics didn't update" — because Nexus changed the shape of its data

**v5.0.3.0** — A narrowed Nexus window broke the sync, and the last version cried wolf about it

**v5.0.2.0** — A sync could report success while Nexus Futures drew nothing

**v5.0.1.0** — The iPhone shortcuts now tell you why they failed instead of doing nothing

[Full version history →](https://github.com/ahoward001/nexus-tv-bridge/blob/main/CHANGELOG.md)

---

## Assets — what clicking each one actually does

**`0-COPY-THIS-pine-script-for-tradingview.pine`** — the indicator that draws the columns, needed on **both** browsers.
Clicking **downloads a text file and installs nothing.** You paste its contents into TradingView's Pine Editor by hand — usually easier to use the "Open the script" link above and copy it in the browser.

**`1-FIREFOX-SETUP-…​.xpi`** — the Firefox add-on. Same file as the Install button above; clicking it in Firefox installs it. In Chrome it just downloads something useless.

**`2-CHROME-SETUP-…​.zip`** — the Chrome extension as a file, for anyone who can't use the Web Store.
Clicking **downloads a zip and installs nothing.** Chrome can't install an extension from a file. Unzip it → `chrome://extensions` → turn on **Developer mode** (top right) → **Load unpacked** → select the unzipped **`nexus-tradingview-bridge` folder** (the one with `manifest.json` directly inside — Chrome loads the folder, not the zip). Installed this way it will **not** auto-update.

**`3.0-GUIDE-chrome.txt` · `3.1-GUIDE-firefox.txt` · `3.2-GUIDE-pine.md`** — reading, not installing. The long-form walkthroughs if the steps above aren't enough. Readable in your browser: [Chrome](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-chrome-install.txt) · [Firefox](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-firefox-install.txt) · [Pine](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-pine-indicator-setup.md)

*Ignore "Source code (zip/tar.gz)" — GitHub generates those automatically and they aren't the extension.*

---

> **On version currency:** Firefox and the zip above are always this build. **Chrome's Web Store copy can be up to ~24 hours behind** — Google reviews every submission and locks the listing while one is pending, so Store releases land in batches. If you need today's code on Chrome right now, use the `2-CHROME-SETUP` zip and the manual steps above instead of the Store link.

## v5.0.4.0 — 2026-08-31

**"Strike metrics didn't update" — because Nexus changed the shape of its data.**

The Score / OI / GEX columns are read straight out of the dashboard's own data, which is far more reliable than scraping the rendered table. That reader carved each strike out with a pattern that assumed every row was flat. Nexus's new dashboard nests objects inside each row, and a pattern built that way cannot see past a nested brace — so every row stopped matching at once.

Measured on the live dashboard: **1,347** objects still matched the old pattern and **none** of them carried the fields we need. Hence the columns going stale every sync while the levels kept working perfectly — two different readers, and only one of them broke.

It now reads the strike array properly rather than pattern-matching text, and still falls back to the old approach so an older dashboard keeps working. Checked against the live page: 55 strikes, every value correct.

**The iPhone shortcut had the identical bug** — same pattern, same failure, which is why it returned nothing at all. Fixed the same way. Re-paste it into the Shortcuts app to pick this up.

### Recent

**v5.0.3.0** — A narrowed Nexus window broke the sync, and the last version cried wolf about it

**v5.0.2.0** — A sync could report success while Nexus Futures drew nothing

**v5.0.1.0** — The iPhone shortcuts now tell you why they failed instead of doing nothing

**v5.0.0.0** — The indicator now sets itself up, and fixes itself when something is wrong

[Full version history →](https://github.com/ahoward001/nexus-tv-bridge/blob/main/CHANGELOG.md)

---

## Assets — what clicking each one actually does

**`0-COPY-THIS-pine-script-for-tradingview.pine`** — the indicator that draws the columns, needed on **both** browsers.
Clicking **downloads a text file and installs nothing.** You paste its contents into TradingView's Pine Editor by hand — usually easier to use the "Open the script" link above and copy it in the browser.

**`1-FIREFOX-SETUP-…​.xpi`** — the Firefox add-on. Same file as the Install button above; clicking it in Firefox installs it. In Chrome it just downloads something useless.

**`2-CHROME-SETUP-…​.zip`** — the Chrome extension as a file, for anyone who can't use the Web Store.
Clicking **downloads a zip and installs nothing.** Chrome can't install an extension from a file. Unzip it → `chrome://extensions` → turn on **Developer mode** (top right) → **Load unpacked** → select the unzipped **`nexus-tradingview-bridge` folder** (the one with `manifest.json` directly inside — Chrome loads the folder, not the zip). Installed this way it will **not** auto-update.

**`3.0-GUIDE-chrome.txt` · `3.1-GUIDE-firefox.txt` · `3.2-GUIDE-pine.md`** — reading, not installing. The long-form walkthroughs if the steps above aren't enough. Readable in your browser: [Chrome](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-chrome-install.txt) · [Firefox](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-firefox-install.txt) · [Pine](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-pine-indicator-setup.md)

*Ignore "Source code (zip/tar.gz)" — GitHub generates those automatically and they aren't the extension.*

---

> **On version currency:** Firefox and the zip above are always this build. **Chrome's Web Store copy can be up to ~24 hours behind** — Google reviews every submission and locks the listing while one is pending, so Store releases land in batches. If you need today's code on Chrome right now, use the `2-CHROME-SETUP` zip and the manual steps above instead of the Store link.

## v5.0.3.0 — 2026-08-28

**A narrowed Nexus window broke the sync, and the last version cried wolf about it.**

Two things, and the first is the real one.

**Nexus's view switcher becomes a dropdown in a narrow window.** Side by side with a chart, the row of view tabs collapses into a single **VISTA** menu — and its items are dropdown options, not buttons. The extension only knew how to click buttons and links, so on a narrowed dashboard it could never reach the **Export** view at all. That's the cause of `view=overview`, `export-code not readable`, and `in-place skipped — no export panel` on a dashboard that was sitting there working perfectly. It now drives the dropdown too, including a real `<select>`, which has to be *set* rather than clicked.

**And "Levels didn't stick" was firing on syncs that worked.** The previous release moved the check to after pressing OK — but pressing OK closes the settings dialog, so the field is gone and there is nothing left to read. Every successful sync then looked like a failure. The check is back where it belongs: the field is confirmed to hold the code while the dialog is still open, which is what "the write landed" actually means. The reading after OK is now treated as the bonus it is.

That one is on me — it was introduced yesterday and shipped without being run against a live chart.

### Recent

**v5.0.2.0** — A sync could report success while Nexus Futures drew nothing

**v5.0.1.0** — The iPhone shortcuts now tell you why they failed instead of doing nothing

**v5.0.0.0** — The indicator now sets itself up, and fixes itself when something is wrong

**v4.19.12** — A new dotted line now has to earn the interruption

[Full version history →](https://github.com/ahoward001/nexus-tv-bridge/blob/main/CHANGELOG.md)

---

## Assets — what clicking each one actually does

**`0-COPY-THIS-pine-script-for-tradingview.pine`** — the indicator that draws the columns, needed on **both** browsers.
Clicking **downloads a text file and installs nothing.** You paste its contents into TradingView's Pine Editor by hand — usually easier to use the "Open the script" link above and copy it in the browser.

**`1-FIREFOX-SETUP-…​.xpi`** — the Firefox add-on. Same file as the Install button above; clicking it in Firefox installs it. In Chrome it just downloads something useless.

**`2-CHROME-SETUP-…​.zip`** — the Chrome extension as a file, for anyone who can't use the Web Store.
Clicking **downloads a zip and installs nothing.** Chrome can't install an extension from a file. Unzip it → `chrome://extensions` → turn on **Developer mode** (top right) → **Load unpacked** → select the unzipped **`nexus-tradingview-bridge` folder** (the one with `manifest.json` directly inside — Chrome loads the folder, not the zip). Installed this way it will **not** auto-update.

**`3.0-GUIDE-chrome.txt` · `3.1-GUIDE-firefox.txt` · `3.2-GUIDE-pine.md`** — reading, not installing. The long-form walkthroughs if the steps above aren't enough. Readable in your browser: [Chrome](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-chrome-install.txt) · [Firefox](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-firefox-install.txt) · [Pine](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-pine-indicator-setup.md)

*Ignore "Source code (zip/tar.gz)" — GitHub generates those automatically and they aren't the extension.*

---

> **On version currency:** Firefox and the zip above are always this build. **Chrome's Web Store copy can be up to ~24 hours behind** — Google reviews every submission and locks the listing while one is pending, so Store releases land in batches. If you need today's code on Chrome right now, use the `2-CHROME-SETUP` zip and the manual steps above instead of the Store link.

## v5.0.2.0 — 2026-08-28

**A sync could report success while Nexus Futures drew nothing.**

Two things had to line up, and both were mine.

**"Verified" didn't mean what it said.** After writing the levels the sync checks the field still holds them — but it accepted a second, much weaker signal as good enough: that the value had landed in the dialog *before* OK was pressed. So a write the indicator discarded on apply still logged `verified=true`, and the warning built for exactly this case never fired. Verified now means one thing: the field still holds the code after OK. If the dialog took it and the indicator didn't keep it, that's said plainly, and **"Levels didn't stick"** appears as it always should have.

**The levels field could be the wrong field.** Finding it worked by walking up to five levels of ancestors and matching any that mentioned "Niveles" or "Levels". Walk up far enough and that text is the entire settings dialog — so with more than one text box, the first one won whether or not it was the right one, and the write then verified happily into an input that draws nothing. It now scores candidates by how close and how specific the matching label is and takes the best; if two are genuinely indistinguishable it refuses and says so rather than guessing.

If Nexus changes the shape of that dialog again, this now fails loudly instead of quietly.

### Recent

**v5.0.1.0** — The iPhone shortcuts now tell you why they failed instead of doing nothing

**v5.0.0.0** — The indicator now sets itself up, and fixes itself when something is wrong

**v4.19.12** — A new dotted line now has to earn the interruption

**v4.19.11** — The button turned yellow about five seconds after a clean sync

[Full version history →](https://github.com/ahoward001/nexus-tv-bridge/blob/main/CHANGELOG.md)

---

## Assets — what clicking each one actually does

**`0-COPY-THIS-pine-script-for-tradingview.pine`** — the indicator that draws the columns, needed on **both** browsers.
Clicking **downloads a text file and installs nothing.** You paste its contents into TradingView's Pine Editor by hand — usually easier to use the "Open the script" link above and copy it in the browser.

**`1-FIREFOX-SETUP-…​.xpi`** — the Firefox add-on. Same file as the Install button above; clicking it in Firefox installs it. In Chrome it just downloads something useless.

**`2-CHROME-SETUP-…​.zip`** — the Chrome extension as a file, for anyone who can't use the Web Store.
Clicking **downloads a zip and installs nothing.** Chrome can't install an extension from a file. Unzip it → `chrome://extensions` → turn on **Developer mode** (top right) → **Load unpacked** → select the unzipped **`nexus-tradingview-bridge` folder** (the one with `manifest.json` directly inside — Chrome loads the folder, not the zip). Installed this way it will **not** auto-update.

**`3.0-GUIDE-chrome.txt` · `3.1-GUIDE-firefox.txt` · `3.2-GUIDE-pine.md`** — reading, not installing. The long-form walkthroughs if the steps above aren't enough. Readable in your browser: [Chrome](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-chrome-install.txt) · [Firefox](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-firefox-install.txt) · [Pine](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-pine-indicator-setup.md)

*Ignore "Source code (zip/tar.gz)" — GitHub generates those automatically and they aren't the extension.*

---

> **On version currency:** Firefox and the zip above are always this build. **Chrome's Web Store copy can be up to ~24 hours behind** — Google reviews every submission and locks the listing while one is pending, so Store releases land in batches. If you need today's code on Chrome right now, use the `2-CHROME-SETUP` zip and the manual steps above instead of the Store link.

## v5.0.1.0 — 2026-08-25

**The iPhone shortcuts now tell you why they failed instead of doing nothing.**

Both shortcuts hand their result back to iOS through a single `completion()` call at the very end. Neither wrapped its work in error handling, so anything unexpected on the page meant that call was never reached — and a Shortcut that never calls `completion()` returns **nothing at all**. No text, no error, no clue. Which is exactly what it looks like when the whole thing is broken.

They now always return something. If it worked you get the string as before. If it didn't, you get what was actually on the page:

```
NO DATA — url=dashboard.nexusfutures.net/ · html=412kb · "strike"=0 · "oiNeto"=0 · login=yes
```

That one line answers the question on its own: whether you were signed in, whether the page had loaded, and whether Nexus's per-strike data was present at all. If the script itself fell over you get `FAILED —` and the error instead.

Nothing else about them changed — the output format is untouched, and it still matches what the extension writes.

### Recent

**v5.0.0.0** — The indicator now sets itself up, and fixes itself when something is wrong

**v4.19.12** — A new dotted line now has to earn the interruption

**v4.19.11** — The button turned yellow about five seconds after a clean sync

**v4.19.10** — Setup stops apologising for how it did the job

[Full version history →](https://github.com/ahoward001/nexus-tv-bridge/blob/main/CHANGELOG.md)

---

## Assets — what clicking each one actually does

**`0-COPY-THIS-pine-script-for-tradingview.pine`** — the indicator that draws the columns, needed on **both** browsers.
Clicking **downloads a text file and installs nothing.** You paste its contents into TradingView's Pine Editor by hand — usually easier to use the "Open the script" link above and copy it in the browser.

**`1-FIREFOX-SETUP-…​.xpi`** — the Firefox add-on. Same file as the Install button above; clicking it in Firefox installs it. In Chrome it just downloads something useless.

**`2-CHROME-SETUP-…​.zip`** — the Chrome extension as a file, for anyone who can't use the Web Store.
Clicking **downloads a zip and installs nothing.** Chrome can't install an extension from a file. Unzip it → `chrome://extensions` → turn on **Developer mode** (top right) → **Load unpacked** → select the unzipped **`nexus-tradingview-bridge` folder** (the one with `manifest.json` directly inside — Chrome loads the folder, not the zip). Installed this way it will **not** auto-update.

**`3.0-GUIDE-chrome.txt` · `3.1-GUIDE-firefox.txt` · `3.2-GUIDE-pine.md`** — reading, not installing. The long-form walkthroughs if the steps above aren't enough. Readable in your browser: [Chrome](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-chrome-install.txt) · [Firefox](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-firefox-install.txt) · [Pine](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-pine-indicator-setup.md)

*Ignore "Source code (zip/tar.gz)" — GitHub generates those automatically and they aren't the extension.*

---

> **On version currency:** Firefox and the zip above are always this build. **Chrome's Web Store copy can be up to ~24 hours behind** — Google reviews every submission and locks the listing while one is pending, so Store releases land in batches. If you need today's code on Chrome right now, use the `2-CHROME-SETUP` zip and the manual steps above instead of the Store link.

## v5.0.0.0 — 2026-08-20

**The indicator now sets itself up, and fixes itself when something is wrong.**

Getting **Nexus Strike Metrics** onto a chart used to be yours to do: open the Pine Editor, select all, paste, save, add to chart, save the layout. Miss a step and the columns quietly showed yesterday's numbers. This release does the whole thing, and — more usefully — notices when it needs doing.

**It offers when it matters.** If a sync can't fill the columns because the indicator isn't on the chart, or because it's an older build whose inputs don't match, the warning now comes with the fix attached: **Set it up** or **Update it**, chosen by reading your chart at the moment you press the button rather than when the message appeared. Update keeps every input you've tuned.

**Three buttons in Settings** for doing it deliberately: **Write the script**, **Update the script**, and **Copy the script** for doing it by hand. Press the wrong one of the first two and it does the right thing anyway and tells you so.

**It finishes the job.** The Pine editor closes when it's done, a sync runs so the levels and columns are actually filled, and a card lingers for a minute asking whether the chart looks right — with the script one click from your clipboard if it doesn't.

**Yellow means something again.** The button stays quiet for ninety seconds after a sync, because clicking again inside that window returns the same batch Nexus already gave you. And a strike that newly earns a dotted line only raises a flag if it lands where you're trading: nearer to price than the Call Wall, Put Wall and Gamma Flip, or within two strikes outside one of them while price is pressed against that same wall.

**Settings are in a usable order** — placement beside the levels controls it affects, the plumbing moved out of the way, the indicator box at the bottom. The amber on/off switch is gone; in its place, a straight choice about what happens when the extension *can't tell* whether your levels moved: go yellow, or stay green.

**The panel reads NEG GEX or POS GEX**, in red or green, rather than an uncoloured "NEGATIVE".

---

*Version numbers gain a fourth position from here: `MAJOR.MINOR.PATCH.PINE`. The last one moves when the Pine script itself changes — the one part of this that nobody updates for you.*

### Recent

**v4.19.12** — A new dotted line now has to earn the interruption

**v4.19.11** — The button turned yellow about five seconds after a clean sync

**v4.19.10** — Setup stops apologising for how it did the job

**v4.19.9** — "Expected exactly one instance after adding, found 0" — on a chart where it had plainly just been added

[Full version history →](https://github.com/ahoward001/nexus-tv-bridge/blob/main/CHANGELOG.md)

---

## Assets — what clicking each one actually does

**`0-COPY-THIS-pine-script-for-tradingview.pine`** — the indicator that draws the columns, needed on **both** browsers.
Clicking **downloads a text file and installs nothing.** You paste its contents into TradingView's Pine Editor by hand — usually easier to use the "Open the script" link above and copy it in the browser.

**`1-FIREFOX-SETUP-…​.xpi`** — the Firefox add-on. Same file as the Install button above; clicking it in Firefox installs it. In Chrome it just downloads something useless.

**`2-CHROME-SETUP-…​.zip`** — the Chrome extension as a file, for anyone who can't use the Web Store.
Clicking **downloads a zip and installs nothing.** Chrome can't install an extension from a file. Unzip it → `chrome://extensions` → turn on **Developer mode** (top right) → **Load unpacked** → select the unzipped **`nexus-tradingview-bridge` folder** (the one with `manifest.json` directly inside — Chrome loads the folder, not the zip). Installed this way it will **not** auto-update.

**`3.0-GUIDE-chrome.txt` · `3.1-GUIDE-firefox.txt` · `3.2-GUIDE-pine.md`** — reading, not installing. The long-form walkthroughs if the steps above aren't enough. Readable in your browser: [Chrome](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-chrome-install.txt) · [Firefox](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-firefox-install.txt) · [Pine](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-pine-indicator-setup.md)

*Ignore "Source code (zip/tar.gz)" — GitHub generates those automatically and they aren't the extension.*

---

> **On version currency:** Firefox and the zip above are always this build. **Chrome's Web Store copy can be up to ~24 hours behind** — Google reviews every submission and locks the listing while one is pending, so Store releases land in batches. If you need today's code on Chrome right now, use the `2-CHROME-SETUP` zip and the manual steps above instead of the Store link.

## v4.19.12 — 2026-08-20

**A new dotted line now has to earn the interruption.**

Any strike crossing the two-of-three rule used to turn the button yellow, wherever it sat on the chart. A line appearing eight points away from price is real, but it isn't a reason to stop what you're doing — and it was what turned the button yellow seconds after a clean sync.

A newly-lined strike now only colours the button if it is either:

- **inside the walls** — nearer to price than the Call Wall, the Put Wall *and* the Gamma Flip. That's where you're actually trading, so a line appearing there is worth knowing; or
- **just outside one of them** — within two strikes of that wall, and only when price is *also* within two strikes of the same wall. A line forming beyond a wall matters when you're pressed up against it, and not otherwise.

Anything else is drawn on the chart as usual and simply doesn't raise a flag. If the walls or the current price can't be read there's nothing to measure against, so it flags as before rather than swallowing the signal quietly.

Together with the ninety-second quiet period after a sync, yellow should now only appear when clicking would actually change something on your chart.

### Recent

**v4.19.11** — The button turned yellow about five seconds after a clean sync

**v4.19.10** — Setup stops apologising for how it did the job

**v4.19.9** — "Expected exactly one instance after adding, found 0" — on a chart where it had plainly just been added

**v4.19.8** — Setup could save and add an empty script

[Full version history →](https://github.com/ahoward001/nexus-tv-bridge/blob/main/CHANGELOG.md)

---

## Assets — what clicking each one actually does

**`0-COPY-THIS-pine-script-for-tradingview.pine`** — the indicator that draws the columns, needed on **both** browsers.
Clicking **downloads a text file and installs nothing.** You paste its contents into TradingView's Pine Editor by hand — usually easier to use the "Open the script" link above and copy it in the browser.

**`1-FIREFOX-SETUP-…​.xpi`** — the Firefox add-on. Same file as the Install button above; clicking it in Firefox installs it. In Chrome it just downloads something useless.

**`2-CHROME-SETUP-…​.zip`** — the Chrome extension as a file, for anyone who can't use the Web Store.
Clicking **downloads a zip and installs nothing.** Chrome can't install an extension from a file. Unzip it → `chrome://extensions` → turn on **Developer mode** (top right) → **Load unpacked** → select the unzipped **`nexus-tradingview-bridge` folder** (the one with `manifest.json` directly inside — Chrome loads the folder, not the zip). Installed this way it will **not** auto-update.

**`3.0-GUIDE-chrome.txt` · `3.1-GUIDE-firefox.txt` · `3.2-GUIDE-pine.md`** — reading, not installing. The long-form walkthroughs if the steps above aren't enough. Readable in your browser: [Chrome](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-chrome-install.txt) · [Firefox](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-firefox-install.txt) · [Pine](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-pine-indicator-setup.md)

*Ignore "Source code (zip/tar.gz)" — GitHub generates those automatically and they aren't the extension.*

---

> **On version currency:** Firefox and the zip above are always this build. **Chrome's Web Store copy can be up to ~24 hours behind** — Google reviews every submission and locks the listing while one is pending, so Store releases land in batches. If you need today's code on Chrome right now, use the `2-CHROME-SETUP` zip and the manual steps above instead of the Store link.

---

> ### ⚠️ The Pine indicator changed on Aug 11, 2026
>
> If you have not re-pasted **`nexus-strike-metrics.pine`** since **4.4.0**, do it — nothing updates it for you, on any browser. Copy it from **step 0** above, paste over the old one, **Ctrl+S**. Your saved settings survive.

## v4.19.11 — 2026-08-20

**The button turned yellow about five seconds after a clean sync.**

Yellow means "something looks different but couldn't be confirmed — click to be sure". Seconds after a sync that is never true: Nexus republishes roughly once a minute, so clicking again would hand back the same batch it just pasted.

Three things lined up to cause it. During the morning hot window the staleness bar drops to one minute, and Nexus's export is frequently already about sixty seconds old when it's taken — so levels arrived on the chart *already past* the bar. The watcher then re-read Nexus, recomputed which strikes deserve a dotted line, and found one that had crossed the two-of-three threshold by a point since the last read. Ordinary drift between two reads a minute apart, reported as news.

A guess is now ignored for ninety seconds after a paste. **Orange is deliberately exempt** — that's a confirmed change to Nexus's own export, and if your lines really are about to move, five seconds later is exactly when you want to hear about it.

### Recent

**v4.19.10** — Setup stops apologising for how it did the job

**v4.19.9** — "Expected exactly one instance after adding, found 0" — on a chart where it had plainly just been added

**v4.19.8** — Setup could save and add an empty script

**v4.19.7** — Setup no longer hangs on TradingView's "save before adding" question, and no longer refuses to do the obvious thing

[Full version history →](https://github.com/ahoward001/nexus-tv-bridge/blob/main/CHANGELOG.md)

---

## Assets — what clicking each one actually does

**`0-COPY-THIS-pine-script-for-tradingview.pine`** — the indicator that draws the columns, needed on **both** browsers.
Clicking **downloads a text file and installs nothing.** You paste its contents into TradingView's Pine Editor by hand — usually easier to use the "Open the script" link above and copy it in the browser.

**`1-FIREFOX-SETUP-…​.xpi`** — the Firefox add-on. Same file as the Install button above; clicking it in Firefox installs it. In Chrome it just downloads something useless.

**`2-CHROME-SETUP-…​.zip`** — the Chrome extension as a file, for anyone who can't use the Web Store.
Clicking **downloads a zip and installs nothing.** Chrome can't install an extension from a file. Unzip it → `chrome://extensions` → turn on **Developer mode** (top right) → **Load unpacked** → select the unzipped **`nexus-tradingview-bridge` folder** (the one with `manifest.json` directly inside — Chrome loads the folder, not the zip). Installed this way it will **not** auto-update.

**`3.0-GUIDE-chrome.txt` · `3.1-GUIDE-firefox.txt` · `3.2-GUIDE-pine.md`** — reading, not installing. The long-form walkthroughs if the steps above aren't enough. Readable in your browser: [Chrome](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-chrome-install.txt) · [Firefox](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-firefox-install.txt) · [Pine](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-pine-indicator-setup.md)

*Ignore "Source code (zip/tar.gz)" — GitHub generates those automatically and they aren't the extension.*

---

> **On version currency:** Firefox and the zip above are always this build. **Chrome's Web Store copy can be up to ~24 hours behind** — Google reviews every submission and locks the listing while one is pending, so Store releases land in batches. If you need today's code on Chrome right now, use the `2-CHROME-SETUP` zip and the manual steps above instead of the Store link.

---

> ### ⚠️ The Pine indicator changed on Aug 11, 2026
>
> If you have not re-pasted **`nexus-strike-metrics.pine`** since **4.4.0**, do it — nothing updates it for you, on any browser. Copy it from **step 0** above, paste over the old one, **Ctrl+S**. Your saved settings survive.

## v4.19.10 — 2026-08-20

**Setup stops apologising for how it did the job.**

Adding the indicator to the chart has two possible routes: pressing TradingView's button, or the keyboard shortcut that button advertises. The button was tried first — but its label changes depending on whether the script has been applied before, and it isn't drawn at all while the script is unsaved. So the usual sequence was: fail to find the button, quietly fall back to the shortcut, succeed, and then report *"couldn't find the Add to chart button, so the keyboard shortcut was used instead"*. Perfectly true, and of no use to anyone reading it.

The shortcut is now simply how it's done. It can't be renamed or restyled out from under us, and it has worked every time. The button is still there as a second route if the shortcut doesn't take.

**And when it finishes, it asks instead of explaining.** The card now stays for a minute and says *"Nexus Strike Metrics is on the chart — everything look ok?"*, with **Copy the script** if it isn't and **All good** to dismiss. That's the one question worth asking once the work is done, and the one useful thing to hand you if the answer is no.

### Recent

**v4.19.9** — "Expected exactly one instance after adding, found 0" — on a chart where it had plainly just been added

**v4.19.8** — Setup could save and add an empty script

**v4.19.7** — Setup no longer hangs on TradingView's "save before adding" question, and no longer refuses to do the obvious thing

**v4.19.6** — A successful setup was reporting itself as a failure

[Full version history →](https://github.com/ahoward001/nexus-tv-bridge/blob/main/CHANGELOG.md)

---

## Assets — what clicking each one actually does

**`0-COPY-THIS-pine-script-for-tradingview.pine`** — the indicator that draws the columns, needed on **both** browsers.
Clicking **downloads a text file and installs nothing.** You paste its contents into TradingView's Pine Editor by hand — usually easier to use the "Open the script" link above and copy it in the browser.

**`1-FIREFOX-SETUP-…​.xpi`** — the Firefox add-on. Same file as the Install button above; clicking it in Firefox installs it. In Chrome it just downloads something useless.

**`2-CHROME-SETUP-…​.zip`** — the Chrome extension as a file, for anyone who can't use the Web Store.
Clicking **downloads a zip and installs nothing.** Chrome can't install an extension from a file. Unzip it → `chrome://extensions` → turn on **Developer mode** (top right) → **Load unpacked** → select the unzipped **`nexus-tradingview-bridge` folder** (the one with `manifest.json` directly inside — Chrome loads the folder, not the zip). Installed this way it will **not** auto-update.

**`3.0-GUIDE-chrome.txt` · `3.1-GUIDE-firefox.txt` · `3.2-GUIDE-pine.md`** — reading, not installing. The long-form walkthroughs if the steps above aren't enough. Readable in your browser: [Chrome](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-chrome-install.txt) · [Firefox](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-firefox-install.txt) · [Pine](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-pine-indicator-setup.md)

*Ignore "Source code (zip/tar.gz)" — GitHub generates those automatically and they aren't the extension.*

---

> **On version currency:** Firefox and the zip above are always this build. **Chrome's Web Store copy can be up to ~24 hours behind** — Google reviews every submission and locks the listing while one is pending, so Store releases land in batches. If you need today's code on Chrome right now, use the `2-CHROME-SETUP` zip and the manual steps above instead of the Store link.

---

> ### ⚠️ The Pine indicator changed on Aug 11, 2026
>
> If you have not re-pasted **`nexus-strike-metrics.pine`** since **4.4.0**, do it — nothing updates it for you, on any browser. Copy it from **step 0** above, paste over the old one, **Ctrl+S**. Your saved settings survive.

## v4.19.9 — 2026-08-20

**"Expected exactly one instance after adding, found 0" — on a chart where it had plainly just been added.**

After adding the indicator, setup counts the rows in the chart legend to confirm it landed. TradingView doesn't always draw that row straight away, and it is slower still when the Pine editor is in the way — so the count ran, saw nothing yet, and declared the whole thing a failure while the indicator sat visibly in the legend a second later. The message even suggested deleting a duplicate that was never there.

Finding **two** copies is real damage and still stops everything — that is what the check was built for. Finding **none** is a failed observation, not a failure, and now waits longer and then says so plainly instead of crying wolf.

**The Pine editor closes properly now.** Only the bottom-toolbar button was being used, and that button is a *toggle* — if anything else had already changed the panel's state it would just as happily reopen it, which is why runs kept ending on "couldn't close the Pine editor". It now uses the editor's own close control, found by walking outward from the editor itself so it can only ever match something inside that panel, and falls back to the toggle.

**And it stops padding the clock.** There was a flat four seconds of watching for a dialog followed by another flat four seconds of nothing, spent in full even when the work had finished instantly — most of the ten-second pause in the middle of an otherwise quick run. It now watches for the actual result and moves on the moment it appears.

### Recent

**v4.19.8** — Setup could save and add an empty script

**v4.19.7** — Setup no longer hangs on TradingView's "save before adding" question, and no longer refuses to do the obvious thing

**v4.19.6** — A successful setup was reporting itself as a failure

**v4.19.5** — Setup could never finish on the one chart it exists for — an empty Pine editor

[Full version history →](https://github.com/ahoward001/nexus-tv-bridge/blob/main/CHANGELOG.md)

---

## Assets — what clicking each one actually does

**`0-COPY-THIS-pine-script-for-tradingview.pine`** — the indicator that draws the columns, needed on **both** browsers.
Clicking **downloads a text file and installs nothing.** You paste its contents into TradingView's Pine Editor by hand — usually easier to use the "Open the script" link above and copy it in the browser.

**`1-FIREFOX-SETUP-…​.xpi`** — the Firefox add-on. Same file as the Install button above; clicking it in Firefox installs it. In Chrome it just downloads something useless.

**`2-CHROME-SETUP-…​.zip`** — the Chrome extension as a file, for anyone who can't use the Web Store.
Clicking **downloads a zip and installs nothing.** Chrome can't install an extension from a file. Unzip it → `chrome://extensions` → turn on **Developer mode** (top right) → **Load unpacked** → select the unzipped **`nexus-tradingview-bridge` folder** (the one with `manifest.json` directly inside — Chrome loads the folder, not the zip). Installed this way it will **not** auto-update.

**`3.0-GUIDE-chrome.txt` · `3.1-GUIDE-firefox.txt` · `3.2-GUIDE-pine.md`** — reading, not installing. The long-form walkthroughs if the steps above aren't enough. Readable in your browser: [Chrome](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-chrome-install.txt) · [Firefox](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-firefox-install.txt) · [Pine](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-pine-indicator-setup.md)

*Ignore "Source code (zip/tar.gz)" — GitHub generates those automatically and they aren't the extension.*

---

> **On version currency:** Firefox and the zip above are always this build. **Chrome's Web Store copy can be up to ~24 hours behind** — Google reviews every submission and locks the listing while one is pending, so Store releases land in batches. If you need today's code on Chrome right now, use the `2-CHROME-SETUP` zip and the manual steps above instead of the Store link.

---

> ### ⚠️ The Pine indicator changed on Aug 11, 2026
>
> If you have not re-pasted **`nexus-strike-metrics.pine`** since **4.4.0**, do it — nothing updates it for you, on any browser. Copy it from **step 0** above, paste over the old one, **Ctrl+S**. Your saved settings survive.

## v4.19.8 — 2026-08-20

**Setup could save and add an empty script.**

When the paste failed to land, the run carried on regardless: it saved the empty editor, answered TradingView's *"Save this script before adding?"*, added nothing to the chart, and then failed its own final check with *"expected exactly one instance after adding, found 0"* — a message that reads like a duplicate problem when the real problem was that nothing had been pasted at all.

That was a bad edge in an otherwise good rule. Not being able to read the version stamp is genuinely inconclusive and should only warn — an unread line says nothing about whether the paste worked. **No content at all is not inconclusive.** It is proof the paste didn't land, and it was being waved through under the same rule.

Setup now checks the editor actually holds something before going any further. If it doesn't, it re-focuses and pastes once more, and if it is still empty it stops there — before saving anything, before adding anything — and tells you the script is on your clipboard and the editor is waiting.

**Also fixed on the way:** the dialog matcher no longer treats any element mentioning "unsaved changes" as a window it should answer, and now requires an actual Save button before pressing anything.

### Recent

**v4.19.7** — Setup no longer hangs on TradingView's "save before adding" question, and no longer refuses to do the obvious thing

**v4.19.6** — A successful setup was reporting itself as a failure

**v4.19.5** — Setup could never finish on the one chart it exists for — an empty Pine editor

**v4.19.4** — "No Add to chart button" — on a chart where the button was plainly sitting there

[Full version history →](https://github.com/ahoward001/nexus-tv-bridge/blob/main/CHANGELOG.md)

---

## Assets — what clicking each one actually does

**`0-COPY-THIS-pine-script-for-tradingview.pine`** — the indicator that draws the columns, needed on **both** browsers.
Clicking **downloads a text file and installs nothing.** You paste its contents into TradingView's Pine Editor by hand — usually easier to use the "Open the script" link above and copy it in the browser.

**`1-FIREFOX-SETUP-…​.xpi`** — the Firefox add-on. Same file as the Install button above; clicking it in Firefox installs it. In Chrome it just downloads something useless.

**`2-CHROME-SETUP-…​.zip`** — the Chrome extension as a file, for anyone who can't use the Web Store.
Clicking **downloads a zip and installs nothing.** Chrome can't install an extension from a file. Unzip it → `chrome://extensions` → turn on **Developer mode** (top right) → **Load unpacked** → select the unzipped **`nexus-tradingview-bridge` folder** (the one with `manifest.json` directly inside — Chrome loads the folder, not the zip). Installed this way it will **not** auto-update.

**`3.0-GUIDE-chrome.txt` · `3.1-GUIDE-firefox.txt` · `3.2-GUIDE-pine.md`** — reading, not installing. The long-form walkthroughs if the steps above aren't enough. Readable in your browser: [Chrome](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-chrome-install.txt) · [Firefox](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-firefox-install.txt) · [Pine](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-pine-indicator-setup.md)

*Ignore "Source code (zip/tar.gz)" — GitHub generates those automatically and they aren't the extension.*

---

> **On version currency:** Firefox and the zip above are always this build. **Chrome's Web Store copy can be up to ~24 hours behind** — Google reviews every submission and locks the listing while one is pending, so Store releases land in batches. If you need today's code on Chrome right now, use the `2-CHROME-SETUP` zip and the manual steps above instead of the Store link.

---

> ### ⚠️ The Pine indicator changed on Aug 11, 2026
>
> If you have not re-pasted **`nexus-strike-metrics.pine`** since **4.4.0**, do it — nothing updates it for you, on any browser. Copy it from **step 0** above, paste over the old one, **Ctrl+S**. Your saved settings survive.

## v4.19.7 — 2026-08-19

**Setup no longer hangs on TradingView's "save before adding" question, and no longer refuses to do the obvious thing.**

TradingView puts up two different windows partway through, and only one of them was being answered. *"Save script — new script name"* was handled; *"Save this script before adding?"* was not, because it has no name field and is worded differently. Setup sat waiting for a window it could not see, and eventually gave up. Both are answered now, and the run waits for the add to actually happen afterwards rather than measuring a chart the indicator never reached.

**The offer now does what it offers.** It decided whether to install or update at the moment the card appeared, then refused if that had changed by the time you pressed the button — *"Stopped: already on the chart — this is the update path, not install"*. The card can sit there for minutes while a sync, another tab, or you change the answer. It now looks at the chart when you press the button and does whichever is right.

Same for the two Settings buttons. **Write the script** on a chart that already has it now updates instead of refusing, and **Update the script** on a chart without it writes and adds it. Either way it tells you which it did. This can't produce a duplicate: the update path never adds, and the install path still stops if a copy is already there.

### Recent

**v4.19.6** — A successful setup was reporting itself as a failure

**v4.19.5** — Setup could never finish on the one chart it exists for — an empty Pine editor

**v4.19.4** — "No Add to chart button" — on a chart where the button was plainly sitting there

**v4.19.3** — Setting up the indicator from Settings, or from a warning, failed instantly and said nothing useful

[Full version history →](https://github.com/ahoward001/nexus-tv-bridge/blob/main/CHANGELOG.md)

---

## Assets — what clicking each one actually does

**`0-COPY-THIS-pine-script-for-tradingview.pine`** — the indicator that draws the columns, needed on **both** browsers.
Clicking **downloads a text file and installs nothing.** You paste its contents into TradingView's Pine Editor by hand — usually easier to use the "Open the script" link above and copy it in the browser.

**`1-FIREFOX-SETUP-…​.xpi`** — the Firefox add-on. Same file as the Install button above; clicking it in Firefox installs it. In Chrome it just downloads something useless.

**`2-CHROME-SETUP-…​.zip`** — the Chrome extension as a file, for anyone who can't use the Web Store.
Clicking **downloads a zip and installs nothing.** Chrome can't install an extension from a file. Unzip it → `chrome://extensions` → turn on **Developer mode** (top right) → **Load unpacked** → select the unzipped **`nexus-tradingview-bridge` folder** (the one with `manifest.json` directly inside — Chrome loads the folder, not the zip). Installed this way it will **not** auto-update.

**`3.0-GUIDE-chrome.txt` · `3.1-GUIDE-firefox.txt` · `3.2-GUIDE-pine.md`** — reading, not installing. The long-form walkthroughs if the steps above aren't enough. Readable in your browser: [Chrome](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-chrome-install.txt) · [Firefox](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-firefox-install.txt) · [Pine](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-pine-indicator-setup.md)

*Ignore "Source code (zip/tar.gz)" — GitHub generates those automatically and they aren't the extension.*

---

> **On version currency:** Firefox and the zip above are always this build. **Chrome's Web Store copy can be up to ~24 hours behind** — Google reviews every submission and locks the listing while one is pending, so Store releases land in batches. If you need today's code on Chrome right now, use the `2-CHROME-SETUP` zip and the manual steps above instead of the Store link.

---

> ### ⚠️ The Pine indicator changed on Aug 11, 2026
>
> If you have not re-pasted **`nexus-strike-metrics.pine`** since **4.4.0**, do it — nothing updates it for you, on any browser. Copy it from **step 0** above, paste over the old one, **Ctrl+S**. Your saved settings survive.

## v4.19.6 — 2026-08-19

**A successful setup was reporting itself as a failure.**

After adding the indicator, setup counts the entries in the chart legend to confirm exactly one copy landed. It did that while the Pine editor was still open — and TradingView doesn't draw legend rows while that panel covers them. So the count came back zero on a chart where the indicator had just been added successfully, and the run ended on *"expected exactly one instance after adding, found 0"*, sending you looking for a duplicate that never existed.

This was watched happening on a live chart: the editor's own console logged **"Added to chart"**, the legend still read zero, and it read one the instant the panel closed. Setup now closes the editor first and counts afterwards.

**The editor also closes when a run stops early.** It was only being closed after a clean finish, so anything that ended early left the panel sitting over half the chart with nothing to say it was done with it. Every path closes it now — success, warning, or failure.

### Recent

**v4.19.5** — Setup could never finish on the one chart it exists for — an empty Pine editor

**v4.19.4** — "No Add to chart button" — on a chart where the button was plainly sitting there

**v4.19.3** — Setting up the indicator from Settings, or from a warning, failed instantly and said nothing useful

**v4.19.2** — Setting the indicator up now works, and stops quitting on things it merely couldn't check

[Full version history →](https://github.com/ahoward001/nexus-tv-bridge/blob/main/CHANGELOG.md)

---

## Assets — what clicking each one actually does

**`0-COPY-THIS-pine-script-for-tradingview.pine`** — the indicator that draws the columns, needed on **both** browsers.
Clicking **downloads a text file and installs nothing.** You paste its contents into TradingView's Pine Editor by hand — usually easier to use the "Open the script" link above and copy it in the browser.

**`1-FIREFOX-SETUP-…​.xpi`** — the Firefox add-on. Same file as the Install button above; clicking it in Firefox installs it. In Chrome it just downloads something useless.

**`2-CHROME-SETUP-…​.zip`** — the Chrome extension as a file, for anyone who can't use the Web Store.
Clicking **downloads a zip and installs nothing.** Chrome can't install an extension from a file. Unzip it → `chrome://extensions` → turn on **Developer mode** (top right) → **Load unpacked** → select the unzipped **`nexus-tradingview-bridge` folder** (the one with `manifest.json` directly inside — Chrome loads the folder, not the zip). Installed this way it will **not** auto-update.

**`3.0-GUIDE-chrome.txt` · `3.1-GUIDE-firefox.txt` · `3.2-GUIDE-pine.md`** — reading, not installing. The long-form walkthroughs if the steps above aren't enough. Readable in your browser: [Chrome](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-chrome-install.txt) · [Firefox](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-firefox-install.txt) · [Pine](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-pine-indicator-setup.md)

*Ignore "Source code (zip/tar.gz)" — GitHub generates those automatically and they aren't the extension.*

---

> **On version currency:** Firefox and the zip above are always this build. **Chrome's Web Store copy can be up to ~24 hours behind** — Google reviews every submission and locks the listing while one is pending, so Store releases land in batches. If you need today's code on Chrome right now, use the `2-CHROME-SETUP` zip and the manual steps above instead of the Store link.

---

> ### ⚠️ The Pine indicator changed on Aug 11, 2026
>
> If you have not re-pasted **`nexus-strike-metrics.pine`** since **4.4.0**, do it — nothing updates it for you, on any browser. Copy it from **step 0** above, paste over the old one, **Ctrl+S**. Your saved settings survive.

## v4.19.5 — 2026-08-19

**Setup could never finish on the one chart it exists for — an empty Pine editor.**

Before touching anything, the installer waits for the editor to be usable. It decided that by counting rendered lines of code. A brand-new Pine script is **empty**, so there are none — and filling it is the whole job. That check could never pass on a fresh editor, so setup waited twelve seconds and then stopped with *"the editor didn't render — bring this tab to the front and retry"*, on a tab that was already in front and an editor that was working perfectly.

This was checked against a live chart rather than guessed at: the editor measured 655×694 with a working text area and a live **Add to chart** button, and the old test still read it as not rendered. It now looks for the things that make an editor usable — a visible box, the text area TradingView routes typing through, and the container code is drawn into — instead of demanding that code already be there.

**Also:** the button that puts the script on the chart is labelled **Add to chart** or **Update on chart** depending on whether that script has ever been applied before. Only the first was recognised, so a script you had previously used stopped the run with *"no Add to chart button"* while the button sat there reading *Update on chart*. Both are accepted now. What actually confirms success is unchanged and unchanged on purpose: exactly one copy of the indicator in the chart legend afterwards, or it stops and tells you.

### Recent

**v4.19.4** — "No Add to chart button" — on a chart where the button was plainly sitting there

**v4.19.3** — Setting up the indicator from Settings, or from a warning, failed instantly and said nothing useful

**v4.19.2** — Setting the indicator up now works, and stops quitting on things it merely couldn't check

**v4.18.0** — Setup now fixes a read-only script instead of giving up on it

[Full version history →](https://github.com/ahoward001/nexus-tv-bridge/blob/main/CHANGELOG.md)

---

## Assets — what clicking each one actually does

**`0-COPY-THIS-pine-script-for-tradingview.pine`** — the indicator that draws the columns, needed on **both** browsers.
Clicking **downloads a text file and installs nothing.** You paste its contents into TradingView's Pine Editor by hand — usually easier to use the "Open the script" link above and copy it in the browser.

**`1-FIREFOX-SETUP-…​.xpi`** — the Firefox add-on. Same file as the Install button above; clicking it in Firefox installs it. In Chrome it just downloads something useless.

**`2-CHROME-SETUP-…​.zip`** — the Chrome extension as a file, for anyone who can't use the Web Store.
Clicking **downloads a zip and installs nothing.** Chrome can't install an extension from a file. Unzip it → `chrome://extensions` → turn on **Developer mode** (top right) → **Load unpacked** → select the unzipped **`nexus-tradingview-bridge` folder** (the one with `manifest.json` directly inside — Chrome loads the folder, not the zip). Installed this way it will **not** auto-update.

**`3.0-GUIDE-chrome.txt` · `3.1-GUIDE-firefox.txt` · `3.2-GUIDE-pine.md`** — reading, not installing. The long-form walkthroughs if the steps above aren't enough. Readable in your browser: [Chrome](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-chrome-install.txt) · [Firefox](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-firefox-install.txt) · [Pine](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-pine-indicator-setup.md)

*Ignore "Source code (zip/tar.gz)" — GitHub generates those automatically and they aren't the extension.*

---

> **On version currency:** Firefox and the zip above are always this build. **Chrome's Web Store copy can be up to ~24 hours behind** — Google reviews every submission and locks the listing while one is pending, so Store releases land in batches. If you need today's code on Chrome right now, use the `2-CHROME-SETUP` zip and the manual steps above instead of the Store link.

---

> ### ⚠️ The Pine indicator changed on Aug 11, 2026
>
> If you have not re-pasted **`nexus-strike-metrics.pine`** since **4.4.0**, do it — nothing updates it for you, on any browser. Copy it from **step 0** above, paste over the old one, **Ctrl+S**. Your saved settings survive.

## v4.19.4 — 2026-08-19

**"No Add to chart button" — on a chart where the button was plainly sitting there.**

The installer looked for that control by one hardcoded attribute, `title="Add to chart"`. TradingView now draws it as an icon whose label lives in a floating tooltip, so that attribute is gone and the search matched nothing. Setup then stopped one step from done, having already pasted and saved the script correctly, and blamed a button it simply couldn't see.

It now checks every place a label can hide — title, aria-label, tooltip attributes, the element's own name and its text — and looks inside the editor's own toolbar first so it can't click something unrelated. If none of that matches, it falls back to the keyboard shortcut the tooltip itself advertises, **⌘/Ctrl + Enter**. A shortcut can't be restyled or renamed out from under it the way a DOM element can. Either way the result is checked the same way as before: exactly one copy of the indicator in the chart legend, or it stops and says so.

**The editor also wouldn't scroll to the top**, so the version stamp on line 3 was never on screen to verify. Monaco only accepts keys while its text area holds focus, and anything between the paste and the check — a dialog, a click, the tab coming forward — takes it. Focus is now reclaimed before the scroll keys are sent. This one was only ever a warning; it never stopped a run.

**"The editor didn't render — bring this tab to the front" on a tab that was already in front.**

A closed Pine panel was reporting itself as open. The check asked only whether the editor existed in the page, and TradingView keeps it there when the panel is collapsed — so setup never clicked to open it, then waited twelve seconds for a collapsed panel to draw text it was never going to draw, and blamed the tab. It now measures whether the editor is actually visible, and clicks the toggle a second time if the first click landed while the tab was still coming forward.

### Recent

**v4.19.3** — Setting up the indicator from Settings, or from a warning, failed instantly and said nothing useful

**v4.19.2** — Setting the indicator up now works, and stops quitting on things it merely couldn't check

**v4.18.0** — Setup now fixes a read-only script instead of giving up on it

**v4.17.0** — Setup failed against a read-only script, and gave up too quickly

[Full version history →](https://github.com/ahoward001/nexus-tv-bridge/blob/main/CHANGELOG.md)

---

## Assets — what clicking each one actually does

**`0-COPY-THIS-pine-script-for-tradingview.pine`** — the indicator that draws the columns, needed on **both** browsers.
Clicking **downloads a text file and installs nothing.** You paste its contents into TradingView's Pine Editor by hand — usually easier to use the "Open the script" link above and copy it in the browser.

**`1-FIREFOX-SETUP-…​.xpi`** — the Firefox add-on. Same file as the Install button above; clicking it in Firefox installs it. In Chrome it just downloads something useless.

**`2-CHROME-SETUP-…​.zip`** — the Chrome extension as a file, for anyone who can't use the Web Store.
Clicking **downloads a zip and installs nothing.** Chrome can't install an extension from a file. Unzip it → `chrome://extensions` → turn on **Developer mode** (top right) → **Load unpacked** → select the unzipped **`nexus-tradingview-bridge` folder** (the one with `manifest.json` directly inside — Chrome loads the folder, not the zip). Installed this way it will **not** auto-update.

**`3.0-GUIDE-chrome.txt` · `3.1-GUIDE-firefox.txt` · `3.2-GUIDE-pine.md`** — reading, not installing. The long-form walkthroughs if the steps above aren't enough. Readable in your browser: [Chrome](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-chrome-install.txt) · [Firefox](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-firefox-install.txt) · [Pine](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-pine-indicator-setup.md)

*Ignore "Source code (zip/tar.gz)" — GitHub generates those automatically and they aren't the extension.*

---

> **On version currency:** Firefox and the zip above are always this build. **Chrome's Web Store copy can be up to ~24 hours behind** — Google reviews every submission and locks the listing while one is pending, so Store releases land in batches. If you need today's code on Chrome right now, use the `2-CHROME-SETUP` zip and the manual steps above instead of the Store link.

---

> ### ⚠️ The Pine indicator changed on Aug 11, 2026
>
> If you have not re-pasted **`nexus-strike-metrics.pine`** since **4.4.0**, do it — nothing updates it for you, on any browser. Copy it from **step 0** above, paste over the old one, **Ctrl+S**. Your saved settings survive.

## v4.19.3 — 2026-08-19

**Setting up the indicator from Settings, or from a warning, failed instantly and said nothing useful.**

Clicking **Write the script** stopped with *"Cannot access 'iv' before initialization"*, and the *"Strike metrics didn't update"* warning never offered to fix anything at all. Same cause: the routine that waits for the chart to be ready cleared its own timers from inside a function defined *before* those timers existed. When the chart was still loading it took a slower path and worked, which is why setup-on-page-load was fine. When the chart was **already** loaded it took the immediate path and threw every time — and every button and every warning that acts on a chart you are already looking at takes exactly that path.

So the two features added for acting on a settled chart were the two that could never work. Both do now.

**Nothing about your setup caused it, and nothing needs redoing** — it failed before touching the editor or the chart.

### Recent

**v4.19.2** — Setting the indicator up now works, and stops quitting on things it merely couldn't check

**v4.18.0** — Setup now fixes a read-only script instead of giving up on it

**v4.17.0** — Setup failed against a read-only script, and gave up too quickly

**v4.16.0** — Alert quiet-time is now a four-way choice, and it reads the page instead of the tab bar

[Full version history →](https://github.com/ahoward001/nexus-tv-bridge/blob/main/CHANGELOG.md)

---

## Assets — what clicking each one actually does

**`0-COPY-THIS-pine-script-for-tradingview.pine`** — the indicator that draws the columns, needed on **both** browsers.
Clicking **downloads a text file and installs nothing.** You paste its contents into TradingView's Pine Editor by hand — usually easier to use the "Open the script" link above and copy it in the browser.

**`1-FIREFOX-SETUP-…​.xpi`** — the Firefox add-on. Same file as the Install button above; clicking it in Firefox installs it. In Chrome it just downloads something useless.

**`2-CHROME-SETUP-…​.zip`** — the Chrome extension as a file, for anyone who can't use the Web Store.
Clicking **downloads a zip and installs nothing.** Chrome can't install an extension from a file. Unzip it → `chrome://extensions` → turn on **Developer mode** (top right) → **Load unpacked** → select the unzipped **`nexus-tradingview-bridge` folder** (the one with `manifest.json` directly inside — Chrome loads the folder, not the zip). Installed this way it will **not** auto-update.

**`3.0-GUIDE-chrome.txt` · `3.1-GUIDE-firefox.txt` · `3.2-GUIDE-pine.md`** — reading, not installing. The long-form walkthroughs if the steps above aren't enough. Readable in your browser: [Chrome](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-chrome-install.txt) · [Firefox](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-firefox-install.txt) · [Pine](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-pine-indicator-setup.md)

*Ignore "Source code (zip/tar.gz)" — GitHub generates those automatically and they aren't the extension.*

---

> **On version currency:** Firefox and the zip above are always this build. **Chrome's Web Store copy can be up to ~24 hours behind** — Google reviews every submission and locks the listing while one is pending, so Store releases land in batches. If you need today's code on Chrome right now, use the `2-CHROME-SETUP` zip and the manual steps above instead of the Store link.

---

> ### ⚠️ The Pine indicator changed on Aug 11, 2026
>
> If you have not re-pasted **`nexus-strike-metrics.pine`** since **4.4.0**, do it — nothing updates it for you, on any browser. Copy it from **step 0** above, paste over the old one, **Ctrl+S**. Your saved settings survive.

## v4.19.2 — 2026-08-18

**Setting the indicator up now works, and stops quitting on things it merely couldn't check.**

Every keyboard shortcut the installer sent TradingView was silently doing nothing. Monaco — the editor behind the Pine window — reads the deprecated numeric `keyCode`, and the browser refuses to set that when an event is built in code: it always arrives as zero, so every shortcut resolved to "no key pressed". Two things followed from that one bug. Select-all never selected, so each paste *inserted* rather than replaced, leaving TradingView's starter script sitting underneath your code where it would never compile. And scroll-to-top never scrolled, so the version stamp on line 3 was never on screen to be read — which the installer then reported as a failure and gave up on. The same call also held Ctrl and Cmd down together, which is a third shortcut bound to nothing at all.

**No version check can end a run any more.** Not seeing the version it expected means it could not *confirm* — which is not the same as knowing something failed. It now says so and carries on, as it does for a save it couldn't watch complete, and for an editor pinned to an old version that wouldn't unpin (it pastes anyway rather than refusing in advance). Two things still stop it, and neither is about version numbers: TradingView's starter script still sitting in the buffer after a paste, and more than one copy of the indicator on the chart. Those are facts read off the page, and carrying on past either one damages something. Any run that ends less than clean now puts the script on your clipboard automatically, so doing it by hand is one paste away.

**Saving a brand-new script no longer stalls on its name.** A script you've saved before saves silently; one you haven't puts up "Save script — new script name" and waits. Setup always begins in a fresh untitled script, so it always met that dialog, and then sat watching a Save button that a waiting dialog was never going to release. It fills the dialog in and confirms it. If TradingView adds a number to the name because it's taken, it tells you — that means an older copy is still sitting in your Pine list.

**"Settings didn't reach the chart" now comes with the fix attached.** That notification used to end on "check the indicator is on the chart", which is the extension telling you to go and do the one thing it can do for you. It now reads the chart legend and offers the right action: **Set it up** when Nexus Strike Metrics isn't there, **Update it** when it is but is an older build whose inputs don't match. If there's more than one copy on the chart it says that plainly instead, because that's also a reason settings stop landing and it isn't something the extension will fix on its own.

**Three buttons in Settings**, where there was one: **Write the script** for a chart that hasn't got it, **Update the script** for one that has — which keeps the inputs you've tuned — and **Copy the script** for doing it by hand. Write and Update stay separate on purpose: the difference between adding and pasting over is the difference between one copy of the indicator and two. Both drive your open chart, bringing that tab to the front, and report progress on the chart itself.

**The floating panel says NEG GEX or POS GEX**, in a light red or green, instead of an uncoloured "NEGATIVE". The age keeps its own freshness colour beside it.

**Settings are in a usable order.** Placement moved up beneath the column checkboxes, next to the Levels controls it works with. The Nexus reload timing and the notification auto-delete moved down out of the way. The indicator box moved to the bottom, since it's the thing you touch once.

**The amber on/off switch is gone.** It gated the whole staleness watcher, including the orange "a sync will move lines" state — so turning it off made the button lie to you. In its place: when the extension **can't tell** whether your levels have moved, either go yellow (more cautious) or stay green (less distracting). Orange and the market-closed clock are unaffected either way. If you had amber switched off, you're moved to green, which is what you were asking for.

**"Strike metrics didn't update" now offers to fix it.** That warning fires when the columns can't be written — most often because Nexus Strike Metrics isn't on the chart at all. It said so and left you to sort it out. It now reads the chart legend and offers the right action, the same as the other settings warnings do. It stays quiet for failures that re-pasting the script wouldn't fix — a dialog that wouldn't open, a timeout, a logged-out Nexus — so it only speaks up when there is something to press.

**The install links on this page never go stale again.** The Firefox button used to point at *this release's* file, so an old page — or an old link someone saved — installed an old build with nothing to indicate it. Every release now also carries two fixed-name copies, `nexus-tv-bridge-latest.xpi` and `nexus-tradingview-bridge-latest.zip`, and the button points at those through GitHub's "latest" path. Any link to it, from any version, lands on the current build.

### Recent

**v4.18.0** — Setup now fixes a read-only script instead of giving up on it

**v4.17.0** — Setup failed against a read-only script, and gave up too quickly

**v4.16.0** — Alert quiet-time is now a four-way choice, and it reads the page instead of the tab bar

**v4.15.3** — A quiet price alert now says why it was quiet

[Full version history →](https://github.com/ahoward001/nexus-tv-bridge/blob/main/CHANGELOG.md)

---

## Assets — what clicking each one actually does

**`0-COPY-THIS-pine-script-for-tradingview.pine`** — the indicator that draws the columns, needed on **both** browsers.
Clicking **downloads a text file and installs nothing.** You paste its contents into TradingView's Pine Editor by hand — usually easier to use the "Open the script" link above and copy it in the browser.

**`1-FIREFOX-SETUP-…​.xpi`** — the Firefox add-on. Same file as the Install button above; clicking it in Firefox installs it. In Chrome it just downloads something useless.

**`2-CHROME-SETUP-…​.zip`** — the Chrome extension as a file, for anyone who can't use the Web Store.
Clicking **downloads a zip and installs nothing.** Chrome can't install an extension from a file. Unzip it → `chrome://extensions` → turn on **Developer mode** (top right) → **Load unpacked** → select the unzipped **`nexus-tradingview-bridge` folder** (the one with `manifest.json` directly inside — Chrome loads the folder, not the zip). Installed this way it will **not** auto-update.

**`3.0-GUIDE-chrome.txt` · `3.1-GUIDE-firefox.txt` · `3.2-GUIDE-pine.md`** — reading, not installing. The long-form walkthroughs if the steps above aren't enough. Readable in your browser: [Chrome](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-chrome-install.txt) · [Firefox](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-firefox-install.txt) · [Pine](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-pine-indicator-setup.md)

*Ignore "Source code (zip/tar.gz)" — GitHub generates those automatically and they aren't the extension.*

---

> **On version currency:** Firefox and the zip above are always this build. **Chrome's Web Store copy can be up to ~24 hours behind** — Google reviews every submission and locks the listing while one is pending, so Store releases land in batches. If you need today's code on Chrome right now, use the `2-CHROME-SETUP` zip and the manual steps above instead of the Store link.

---

> ### ⚠️ The Pine indicator changed on Aug 11, 2026
>
> If you have not re-pasted **`nexus-strike-metrics.pine`** since **4.4.0**, do it — nothing updates it for you, on any browser. Copy it from **step 0** above, paste over the old one, **Ctrl+S**. Your saved settings survive.

## v4.18.0 — 2026-08-17

**Setup now fixes a read-only script instead of giving up on it.**

TradingView leaves the Pine editor pinned to whichever version of a script you last looked at, and that view is read-only — pasting into it does nothing at all, silently. That state is sticky, lives on your account rather than in the browser, and survives new charts, new layouts and cleared cookies. It is a completely ordinary state to be in.

Until now the installer detected it and stopped. It now clears it: restores the pinned version so the script becomes editable, then pastes the current source over it and saves. The script ends up holding exactly what it should; the restore is just an extra entry in the version history.

The restore link is one of TradingView's controls that ignores a scripted click, so it goes through the React handler directly — the same approach used elsewhere in the extension for controls that refuse synthetic events.

**If anything fails after the restore**, it says so specifically — that the script is currently holding old code and needs the paste, with the source already on your clipboard — rather than leaving you to work out why the indicator looks wrong.

### Recent

**v4.17.0** — Setup failed against a read-only script, and gave up too quickly

**v4.16.0** — Alert quiet-time is now a four-way choice, and it reads the page instead of the tab bar

**v4.15.3** — A quiet price alert now says why it was quiet

**v4.15.2** — The update prompt now fires only when the indicator actually changed

[Full version history →](https://github.com/ahoward001/nexus-tv-bridge/blob/main/CHANGELOG.md)

---

## Assets — what clicking each one actually does

**`0-COPY-THIS-pine-script-for-tradingview.pine`** — the indicator that draws the columns, needed on **both** browsers.
Clicking **downloads a text file and installs nothing.** You paste its contents into TradingView's Pine Editor by hand — usually easier to use the "Open the script" link above and copy it in the browser.

**`1-FIREFOX-SETUP-…​.xpi`** — the Firefox add-on. Same file as the Install button above; clicking it in Firefox installs it. In Chrome it just downloads something useless.

**`2-CHROME-SETUP-…​.zip`** — the Chrome extension as a file, for anyone who can't use the Web Store.
Clicking **downloads a zip and installs nothing.** Chrome can't install an extension from a file. Unzip it → `chrome://extensions` → turn on **Developer mode** (top right) → **Load unpacked** → select the unzipped **`nexus-tradingview-bridge` folder** (the one with `manifest.json` directly inside — Chrome loads the folder, not the zip). Installed this way it will **not** auto-update.

**`3.0-GUIDE-chrome.txt` · `3.1-GUIDE-firefox.txt` · `3.2-GUIDE-pine.md`** — reading, not installing. The long-form walkthroughs if the steps above aren't enough. Readable in your browser: [Chrome](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-chrome-install.txt) · [Firefox](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-firefox-install.txt) · [Pine](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-pine-indicator-setup.md)

*Ignore "Source code (zip/tar.gz)" — GitHub generates those automatically and they aren't the extension.*

---

> **On version currency:** Firefox and the zip above are always this build. **Chrome's Web Store copy can be up to ~24 hours behind** — Google reviews every submission and locks the listing while one is pending, so Store releases land in batches. If you need today's code on Chrome right now, use the `2-CHROME-SETUP` zip and the manual steps above instead of the Store link.

---

> ### ⚠️ The Pine indicator changed on Aug 11, 2026
>
> If you have not re-pasted **`nexus-strike-metrics.pine`** since **4.4.0**, do it — nothing updates it for you, on any browser. Copy it from **step 0** above, paste over the old one, **Ctrl+S**. Your saved settings survive.

## v4.17.0 — 2026-08-17

**Setup failed against a read-only script, and gave up too quickly.**

TradingView marks an old version of a script read-only, and pasting into it does nothing at all — silently. The installer checked for that, but only matched one of the two ways TradingView words it: it looks for *"a historical version"* and your editor said *"an **older** version… revert to this version"*. So it pasted into a buffer that ignored it. The version-stamp check afterwards caught the result and refused to save, which is the outcome you want, but it should never have got that far. Both phrasings are matched now.

**It also declared failure too fast.** After pasting it looked once, about a second later, to confirm the new version stamp was at the top. Monaco re-renders asynchronously, so that single look could still be reading the old lines and call a good paste a failure. It now watches for up to seven seconds.

**And it never ends empty-handed.** Whatever stops it, the script is put on your clipboard immediately, so the fallback is one paste rather than another decision. When the cause is a pinned old version, it says exactly that and how to clear it.

**Nexus Futures is now linked from every release page** — this extension fills that indicator in rather than replacing it, so without it on your chart there is nothing for the levels to paste into.

### Recent

**v4.16.0** — Alert quiet-time is now a four-way choice, and it reads the page instead of the tab bar

**v4.15.3** — A quiet price alert now says why it was quiet

**v4.15.2** — The update prompt now fires only when the indicator actually changed

**v4.15.1** — The panel shows the regime again, and the age instead of a clock time

[Full version history →](https://github.com/ahoward001/nexus-tv-bridge/blob/main/CHANGELOG.md)

---

## Assets — what clicking each one actually does

**`0-COPY-THIS-pine-script-for-tradingview.pine`** — the indicator that draws the columns, needed on **both** browsers.
Clicking **downloads a text file and installs nothing.** You paste its contents into TradingView's Pine Editor by hand — usually easier to use the "Open the script" link above and copy it in the browser.

**`1-FIREFOX-SETUP-…​.xpi`** — the Firefox add-on. Same file as the Install button above; clicking it in Firefox installs it. In Chrome it just downloads something useless.

**`2-CHROME-SETUP-…​.zip`** — the Chrome extension as a file, for anyone who can't use the Web Store.
Clicking **downloads a zip and installs nothing.** Chrome can't install an extension from a file. Unzip it → `chrome://extensions` → turn on **Developer mode** (top right) → **Load unpacked** → select the unzipped **`nexus-tradingview-bridge` folder** (the one with `manifest.json` directly inside — Chrome loads the folder, not the zip). Installed this way it will **not** auto-update.

**`3.0-GUIDE-chrome.txt` · `3.1-GUIDE-firefox.txt` · `3.2-GUIDE-pine.md`** — reading, not installing. The long-form walkthroughs if the steps above aren't enough. Readable in your browser: [Chrome](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-chrome-install.txt) · [Firefox](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-firefox-install.txt) · [Pine](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-pine-indicator-setup.md)

*Ignore "Source code (zip/tar.gz)" — GitHub generates those automatically and they aren't the extension.*

---

> **On version currency:** Firefox and the zip above are always this build. **Chrome's Web Store copy can be up to ~24 hours behind** — Google reviews every submission and locks the listing while one is pending, so Store releases land in batches. If you need today's code on Chrome right now, use the `2-CHROME-SETUP` zip and the manual steps above instead of the Store link.

---

> ### ⚠️ The Pine indicator changed on Aug 11, 2026
>
> If you have not re-pasted **`nexus-strike-metrics.pine`** since **4.4.0**, do it — nothing updates it for you, on any browser. Copy it from **step 0** above, paste over the old one, **Ctrl+S**. Your saved settings survive.

## v4.16.0 — 2026-08-17

**Alert quiet-time is now a four-way choice, and it reads the page instead of the tab bar.**

The old rule was a checkbox — "only alert when I'm not looking at that chart" — and it decided by asking whether the tab was active in the frontmost window. That counted you as watching while the chart sat completely hidden behind fullscreen DevTools, so a genuine first touch of a level was detected and then silently thrown away.

**When should alerts stay quiet?**

- **Always notify me**
- **Quiet only while I'm focused on that chart** — the new default
- **Quiet whenever that chart is on screen**
- **Never notify me**

"Focused" now means the chart itself holds the keyboard, so a chart behind DevTools or a background window counts as *not* focused and still alerts. "On screen" is the stricter reading for people who genuinely watch one chart all day.

**A suppressed touch is recorded rather than discarded.** Hover the sync button and it tells you what was silenced, when, and why — so a quiet alert can never again be mistaken for a broken one.

Your existing setting is carried over: the old checkbox becomes "quiet only while I'm focused".

---

> ### ⚠️ The Pine indicator changed on Aug 11, 2026
>
> If you have not re-pasted **`nexus-strike-metrics.pine`** since **4.4.0**, do it — nothing updates it for you, on any browser. Copy it from **step 0** above, paste over the old one, **Ctrl+S**. Your saved settings survive.

## v4.15.3 — 2026-08-17

**A quiet price alert now says why it was quiet.**

Silence had several legitimate causes — price already sitting inside a level's zone (the rule that stops a level you're hovering from nagging), the quiet window, or you being on that chart — and none of them were distinguishable from "the alerts are broken".

Once a minute per symbol, the console now names the nearest level, the distance, the band, and the reason:

```
price-alerts: QQQ 734.58 — nearest Vanna Flip 734.29 (0.29 away, band 1.00)
  — already inside the zone, so no NEW entry to report (it re-arms once price clears it)
```

---

> ### ⚠️ The Pine indicator changed on Aug 11, 2026
>
> If you have not re-pasted **`nexus-strike-metrics.pine`** since **4.4.0**, do it — nothing updates it for you, on any browser. Copy it from **step 0** above, paste over the old one, **Ctrl+S**. Your saved settings survive.

## v4.15.2 — 2026-08-14

**The update prompt now fires only when the indicator actually changed.**

It compared version numbers — but every release stamps a new version into the Pine header whether or not a line of the script changed. The script is byte-identical between 4.9.0 and 4.15.1 apart from that stamp, so the prompt would have offered an "update" that changed nothing, on every release.

It now fingerprints the script's code with the stamp line excluded, so a release that doesn't touch the indicator stays silent — which is what "relevant patches only" has to mean.

---

> ### ⚠️ The Pine indicator changed on Aug 11, 2026
>
> If you have not re-pasted **`nexus-strike-metrics.pine`** since **4.4.0**, do it — nothing updates it for you, on any browser. Copy it from **step 0** above, paste over the old one, **Ctrl+S**. Your saved settings survive.

## v4.15.1 — 2026-08-14

**The panel shows the regime again, and the age instead of a clock time.**

4.13.0 replaced the ticker with a regime label, but it read the positioning metric as if it were a plain number when it's actually an object — so the label silently never appeared and the line showed only a timestamp. It now reads:

```
POSITIVE · 1m
```

The regime lean, and how old the data is — which is the form that was wanted; the absolute clock time was my misreading of "timestamp".

---

> ### ⚠️ The Pine indicator changed on Aug 11, 2026
>
> If you have not re-pasted **`nexus-strike-metrics.pine`** since **4.4.0**, do it — nothing updates it for you, on any browser. Copy it from **step 0** above, paste over the old one, **Ctrl+S**. Your saved settings survive.

## v4.15.0 — 2026-08-14

**The indicator can now set itself up.** One button, about ten seconds, instead of copy-paste-save-add-save.

When a chart doesn't have **Nexus Strike Metrics** on it, a card offers to set it up. When a chart has an older version *that the extension installed*, it offers to update. Both always include **Copy the script** as the escape hatch, and **Not now** to be left alone.

**Setting up and updating are deliberately different operations.** Setting up pastes the source, saves, and adds the indicator exactly once. Updating pastes over the existing script and saves — and *never* adds, because saving already applies the new source to the indicator on your chart. That's what keeps your tuned settings: a fresh add would come back with code defaults.

Everything it does, it checks:

- It reads the **chart legend**, not the editor's "Add to chart" button — that button silently reverts after a page reload and is a large part of why duplicate indicators happen.
- It counts legend **rows** and compares names by prefix, because duplicates share a name and differ only by a version suffix.
- It **refuses to act on a chart that already has two**, and tells you to remove one by hand. It never removes an indicator for you.
- It verifies the paste actually **replaced** the file rather than appending to it, by checking the version stamp at the top.
- It won't paste into a **read-only historical version** of the script, where pastes fail silently — it tells you to reload, which clears it.
- It refuses to run when the editor isn't rendering, since it could act but not verify.
- It saves the layout only with **both** Nexus indicators present.
- It prompts once per chart per version. Never during a sync.

---

> ### ⚠️ The Pine indicator changed on Aug 11, 2026
>
> If you have not re-pasted **`nexus-strike-metrics.pine`** since **4.4.0**, do it — nothing updates it for you, on any browser. Copy it from **step 0** above, paste over the old one, **Ctrl+S**. Your saved settings survive.

## v4.14.0 — 2026-08-14

**Groundwork for setting up the indicator automatically — detection only, nothing acts on it yet.**

The extension can now tell what state the Pine indicator is in on a chart: **missing**, **installed**, or **duplicated**. It logs that and does nothing else — no clicking, no prompts, no opening the editor.

That restraint is the point. Detection got this wrong twice during development: a name-based counter reported "no duplicate" while two instances were sitting on the chart, because duplicates share a name and differ only by a version suffix (`Nexus Strike Metrics · 46.0` vs `· 45.0`). It counts legend rows now and compares on the name prefix. It also ignores the editor's "Add to chart / Update on chart" button, which looks like a state signal but silently expires on page reload — and is very likely how duplicate indicators get created in the first place.

Nothing gets built on top of this until it's been proven right on real charts.

---

> ### ⚠️ The Pine indicator changed on Aug 11, 2026
>
> If you have not re-pasted **`nexus-strike-metrics.pine`** since **4.4.0**, do it — nothing updates it for you, on any browser. Copy it from **step 0** above, paste over the old one, **Ctrl+S**. Your saved settings survive.

## v4.13.1 — 2026-08-14

**Strike spacing is now measured rather than looked up.** The last hardcoded assumption: a small table said SPX was 5, NDX was 25, and everything else was 1 — fine for the majors, a guess for GLD, USO, IBIT, ETHA and anything added later.

Every sync that reads the strike grid now learns the real spacing for that ticker from the rows themselves and remembers it, so the guess is replaced by a measurement the first time you sync. The table survives only as a first-sync fallback, and the console says when a measurement disagrees with it.

---

> ### ⚠️ The Pine indicator changed on Aug 11, 2026
>
> If you have not re-pasted **`nexus-strike-metrics.pine`** since **4.4.0**, do it — nothing updates it for you, on any browser. Copy it from **step 0** above, paste over the old one, **Ctrl+S**. Your saved settings survive.

## v4.13.0 — 2026-08-14

**Dotted lines were effectively dead on NDX and thin on SPX.** The "how far from price do we look" setting is written in *strikes* — but it was being compared against a raw price distance. Ten points on NDX, where strikes are 25 apart, admits a single strike, so there was almost nothing to choose lines from. It now multiplies by what a strike is actually worth on that chart: ±10 points on QQQ, ±50 on SPX, ±250 on NDX — ten strikes in every case. QQQ is unchanged.

**The lingering panel says something more useful.** It read `QQQ · 1m` — but you know which chart you're on, and a relative age is only right for about a minute and then quietly goes stale while the panel sits there. It now reads:

```
NEGATIVE · 12:36 PM
```

The regime lean, and the clock time the data was actually published. The ticker is still in the hover, along with everything else.

---

> ### ⚠️ The Pine indicator changed on Aug 11, 2026
>
> If you have not re-pasted **`nexus-strike-metrics.pine`** since **4.4.0**, do it — nothing updates it for you, on any browser. Copy it from **step 0** above, paste over the old one, **Ctrl+S**. Your saved settings survive.

## v4.12.1 — 2026-08-14

**Two fixes for charts that aren't QQQ.**

**The columns never drew on NDX.** The check that asks "is this strike data centred where price actually is?" used a flat $2 tolerance — sensible on QQQ at ~$730 with $1 strikes, meaningless on NDX at ~30,000 with 25-point strikes, where a 2.7-point difference is 0.009%. It tripped on every sync, so the Score / OI / GEX columns were rejected as stale every time. The tolerance now scales with the instrument's own strike width.

**Switching ticker opened an unnecessary tab.** When your Nexus tab is on QQQ and the chart is NDX, the extension navigates that tab to the new ticker — a full page load of a ~3MB app, not a quick reload. It was only given the two seconds a reload needs, the read came back empty, and the sync fell through to opening a throwaway tab. A ticker change now gets the time a navigation actually takes; same-URL reloads are unchanged and still fast.

---

> ### ⚠️ The Pine indicator changed on Aug 11, 2026
>
> If you have not re-pasted **`nexus-strike-metrics.pine`** since **4.4.0**, do it — nothing updates it for you, on any browser. Copy it from **step 0** above, paste over the old one, **Ctrl+S**. Your saved settings survive.

## v4.12.0 — 2026-08-14

**New setting: "Include odd strikes that only appear near expiry."** Off by default.

4.11.0 started ignoring QQQ's half-dollar strikes entirely — they exist only on the nearest **Friday** expiries, seven per expiry every $5 around spot, and they were wedging a row between every dollar level while quietly halving the price-alert band on those days.

Off is right for most people. But they are real contracts, and on a **Friday 0DTE** they can carry real gamma — so if you trade that, the switch puts them back everywhere at once: drawn, and counted toward lines, proximity and alerts.

The filter still only applies where the dominant grid is a dollar or more, so a ticker whose chain is genuinely half-dollar keeps its whole board either way.

---

> ### ⚠️ The Pine indicator changed on Aug 11, 2026
>
> If you have not re-pasted **`nexus-strike-metrics.pine`** since **4.4.0**, do it — nothing updates it for you, on any browser. Copy it from **step 0** above, paste over the old one, **Ctrl+S**. Your saved settings survive.

## v4.11.0 — 2026-08-14

**Half-dollar strikes are ignored completely** — not drawn, and not counted toward lines, proximity or alerts.

QQQ lists $0.50 strikes, but only on the nearest **Friday** expiries: seven of them, every $5 around spot. Monday through Thursday have none, and expiries a few weeks out have none yet. They're real contracts, they just aren't part of the grid you trade — and with open interest in the dozens they were adding a cluttered row between every dollar level.

**They were also breaking price alerts, one day a week.** The extension learns "what is a strike on this ticker" from the gaps between rows, taking the smallest — so a single 732.5 convinced it QQQ trades on a $0.50 grid. A red zone set to 1 strike became ±$0.50, and the re-alert distance halved with it. Every Friday, silently, since whenever Nexus first published one.

They're filtered at the source now, upstream of drawing, line selection, the session colour range and alert arming, so nothing downstream can see them.

**Tickers whose chain is genuinely half-dollar are unaffected.** The filter only applies when the dominant gap is a dollar or more, so a $14 ETF listing every $0.50 keeps its whole board.

---

> ### ⚠️ The Pine indicator changed on Aug 11, 2026
>
> If you have not re-pasted **`nexus-strike-metrics.pine`** since **4.4.0**, do it — nothing updates it for you, on any browser. Copy it from **step 0** above, paste over the old one, **Ctrl+S**. Your saved settings survive.

## v4.10.0 — 2026-08-14

**The hover now confirms both writes separately.** A sync does two independent things — it pastes Nexus's levels, and it fills the Score / OI / GEX columns — from two different reads that can succeed or fail on their own. The hover only ever reported the levels, so "applied" told you nothing about whether the columns had updated, which is exactly the ambiguity that let stale columns sit there looking current.

It now reads:

```
Last sync 8:56 AM (just now)
QQQ · applied — new levels
Levels posted 8:55 AM (1m old at sync)
Strike metrics 8:56 AM · 27 strikes · verified
```

And when the columns *didn't* update it says so, with the reason — "couldn't read the strike table", "strike read looked stale", or "off in settings" — instead of staying silent.

---

> ### ⚠️ The Pine indicator changed on Aug 11, 2026
>
> If you have not re-pasted **`nexus-strike-metrics.pine`** since **4.4.0**, do it — nothing updates it for you, on any browser. Copy it from **step 0** above, paste over the old one, **Ctrl+S**. Your saved settings survive.

## v4.9.0 — 2026-08-13

**The indicator now ships inside the extension, with a copy button.**

The Pine script lives in TradingView, not in the extension, so nothing can install or update it for you — on any browser. But fetching it was the awkward part: a Store install arrived with no script and a link to go find one, which is the single step setup couldn't help with.

Settings now has an **indicator** section at the top with the script bundled in, the version it matches, and one button that puts it on your clipboard. Then it's paste, save, add to chart, save the layout. The instructions are on the page, including the trap where the editor says *"this is a historical version of the script"* — that state is read-only and pasting into it silently does nothing.

The copy is guaranteed to match the build you're running, because it's the same file the extension ships. No more wondering whether the script on your chart is older than the extension driving it.

**The Store build no longer strips it.** It was excluded to keep the package small, which meant Store users were the ones who most needed the GitHub link.

---

> ### ⚠️ The Pine indicator changed on Aug 11, 2026
>
> If you have not re-pasted **`nexus-strike-metrics.pine`** since **4.4.0**, do it — nothing updates it for you, on any browser. Copy it from **step 0** above, paste over the old one, **Ctrl+S**. Your saved settings survive.

## v4.8.1 — 2026-08-13

Indicator only. **You do not need to re-paste for this one** unless you want the shipped script to match — the change is a default, and any value you have saved wins over it.

**The column titles sit a little further right by default** — "Header nudge (bars)" goes from 2.0 to **2.33**, which is where they read as centred over their bubbles at Normal label size.

The stepper moves in **0.1** now instead of 0.5, because 0.5 couldn't reach the value that actually looked right. You can type any value into the field regardless of the step.

Why this is tuned by eye rather than computed: the header chips are centred on their anchor while the bubbles hang from a corner, and Pine has no way to measure label width — so the right offset depends on how wide the numbers happen to be and on your label size.

---

> ### ⚠️ The Pine indicator changed on Aug 11, 2026
>
> If you have not re-pasted **`nexus-strike-metrics.pine`** since **4.4.0**, do it — nothing updates it for you, on any browser. Copy it from **step 0** above, paste over the old one, **Ctrl+S**. Your saved settings survive.

## v4.8.0 — 2026-08-13

Extension only — no Pine change, nothing to re-paste.

**Price alerts now name levels that are actually on your chart.** They were armed from the dashboard cards, which run ahead of the export your chart is drawn from — so an alert could warn about a Call Wall that existed on the dashboard and nowhere on your screen. They're armed from the same batch snapshot the dotted lines use, so an alert can only ever mention a level you can see.

**An alert never says "approaching" about a level price has left.** Entries are held through the quiet window on purpose, and with one-minute sampling a fast move straight through a band registers as an entry at the far side of it — so a notification could arrive announcing a level price was already well past and still leaving. An entry is now dropped if price is outside the zone *and* further from it than when it was detected. A level price came back toward still sends.

**Clustered levels show their prices.** When two levels sit within a strike of each other they're merged into one line, and that line was printing the word "cluster" instead of the price — "Gamma Flip + Call Wall cluster · 0.90 away", with no number to reconcile against the chart. It shows the range now.

**Removed the score-50 line override** added in 4.6.4. It dated from before the "already drawn" rule was anchored to the export; with that fixed, a big score satisfies the ordinary conditions on its own, and two rules doing one job just makes the behaviour harder to reason about.

---

> ### ⚠️ The Pine indicator changed on Aug 11, 2026
>
> If you have not re-pasted **`nexus-strike-metrics.pine`** since **4.4.0**, do it — nothing updates it for you, on any browser. Copy it from **step 0** above, paste over the old one, **Ctrl+S**. Your saved settings survive.

## v4.7.0 — 2026-08-13

⚠️ **Re-paste the Pine script** — the indicator changed too.

**"Nexus already draws this" now tracks the export, not the dashboard cards.** Your chart is drawn from the export code; the cards are live and run ahead of it. So the moment a wall moved, the cards called the new strike a wall while the indicator was still drawing the old one — and the new strike got skipped for a line that didn't exist. Caught live: **730 scoring 82, with the biggest OI and the biggest GEX on the board, carrying no line from anyone** until the export caught up minutes later.

The export code's hash changes exactly when Nexus publishes a new batch, so the wall values are now snapshotted at that instant and that snapshot decides what counts as already-drawn. It updates the moment the export does, and it never claims a level the batch hasn't published. When the cards have moved on since the batch, the console says so and names the levels.

**The Score bubble's pointer is back at the bottom-left corner**, matching OI and GEX. Only its position is nudged; 4.6.3 had centred it to line it up with its header, which changed the pointer's shape as a side effect. The box stays where it was.

---

> ### ⚠️ The Pine indicator changed on Aug 11, 2026
>
> If you have not re-pasted **`nexus-strike-metrics.pine`** since **4.4.0**, do it — nothing updates it for you, on any browser. Copy it from **step 0** above, paste over the old one, **Ctrl+S**. Your saved settings survive.

## v4.6.4 — 2026-08-13

**A major level could end up with no line from anyone.** Skipping levels Nexus already draws assumed the chart has a line there — but your chart is drawn from the **export code**, while "Nexus already draws this" was read from the dashboard **cards**. The cards lead and the export lags, so the moment a wall moves, the cards call the new strike a wall while the indicator is still drawing the old one. We'd skip the new strike for a line that doesn't exist yet.

Caught live: **730 scoring 82 with the biggest OI and biggest GEX on the board, maxed on both heat scales, and not a line from anyone** until the export caught up minutes later.

Two guarantees now override the skip:

- **A 3-of-3 sweep always draws**, even on an exported level. It's the most concentrated strike in the band; a dotted line over a wall band is a small cost, a missing line on the day's biggest level is not.
- **Any score of 50 or more always draws** — the same bar the price alerts use. A level can carry a monster score while one neighbour edges it on OI, and that shouldn't cost it a line.

Neither can be squeezed out by the five-line cap; they sort first.

---

> ### ⚠️ The Pine indicator changed on Aug 11, 2026
>
> If you have not re-pasted **`nexus-strike-metrics.pine`** since **4.4.0**, do it — nothing updates it for you, on any browser. Copy it from **step 0** above, paste over the old one, **Ctrl+S**. Your saved settings survive.

## v4.6.3 — 2026-08-12

⚠️ **Re-paste the Pine script** — indicator-only.

**Reverts 4.6.2's anchoring change.** That release centred every bubble on its anchor so the columns would line up with their headers at any text width. It worked, but it moved all three columns off where they were wanted — the anchoring wasn't the problem.

**The Score column is the only one that needed it.** Its text is one or two characters, so hanging it off a corner leaves it visibly left of its header while the wide OI and GEX boxes look fine. Score is now centred on its own anchor and bumped two bars right; OI and GEX are exactly as they were before 4.6.2.

Also: **Header nudge is back to a default of 2** bars, matching where the titles already sat.

---

> ### ⚠️ The Pine indicator changed on Aug 11, 2026
>
> If you have not re-pasted **`nexus-strike-metrics.pine`** since **4.4.0**, do it — nothing updates it for you, on any browser. Copy it from **step 0** above, paste over the old one, **Ctrl+S**. Your saved settings survive.

## v4.6.2 — 2026-08-12

⚠️ **Re-paste the Pine script** — indicator-only, and it needs one settings change, below.

**The columns now line up under their headers.** The header chips were centred on their anchor while the bubbles hung up-and-to-the-right of theirs, so every bubble drifted right by half its own text width — barely visible on a two-character score, obvious on `+154.1M`. Bubbles are centred now too, so they align at any text width rather than by a tuned offset that only holds for one number length.

**After pasting, set "Header nudge (bars)" to 0** in the indicator settings. It defaulted to 2 to compensate for the old misalignment, and your saved value survives a re-paste.

## v4.6.1 — 2026-08-12

**No dotted line next to one of Nexus's own levels unless it sweeps all three columns.** A line one strike off a wall reads as a second wall, and at 2 of 3 it usually isn't one — it's the shoulder of the wall's own concentration.

**Nexus's own levels never get a dotted line**, on any chain. The "is this the same level" test was a fixed distance in price, which worked on a $1 chain and was far too tight on SPX's $5 one; it's measured in strikes now.

**Fixed: on SPX and NDX, every strike drew a line.** Neighbours were found by looking up "the strike one dollar above and below", which assumes a $1 chain — on a $5 or $25 chain every lookup missed, a missing neighbour counted as beaten, and so every strike scored a phantom 3 of 3. It also misfired on a $1 chain anywhere the table skipped a strike. Neighbours are now the rows actually either side, whatever the spacing.

## v4.6.0 — 2026-08-12

**Dotted lines are decided differently.** A strike now earns one by out-doing *both* of its immediate neighbours on at least **two of the three columns** — of the six comparisons (score, OI and GEX against the strike above and the strike below), four have to go its way, and they have to make up two whole columns.

Score is no longer a benchmark on its own. Before, a score of 30+ drew a line unaided while OI and GEX had no say, so a lone score bump got a line and genuinely concentrated strikes went bare. Score is now one of three equal votes, with a floor of **20** — there to keep noise out, not to confer significance.

When more than five strikes qualify, the ones sweeping all **3 of 3** columns go first, then whichever tops a column outright, then score, then proximity to price.

**And it won't leave you with an empty chart.** The bar steps down until something qualifies — first the score floor is dropped, then the two-column requirement, and on a genuinely flat board it draws the single highest score. The console says which step produced the lines, so a thin day is distinguishable from a broken read.

## v4.5.3 — 2026-08-12

**The brightness slider runs the other way** — left fades the overlay out, right pushes it toward solid. Same control, same centre, just the direction that matches how you read it. Your saved setting carries over unchanged; the flip happens between the slider and storage, so the indicator's own input keeps its original meaning and a chart you haven't re-pasted still behaves.

## v4.5.2 — 2026-08-12

**A sync that couldn't read your Nexus tab wasted three and a half seconds finding out.** The in-place read polls for a few seconds on purpose — Nexus is a single-page app, and on a tab that's mid-load the export panel hasn't appeared yet, so that patience is what makes the usual sync take about two seconds. The cost was that a tab which could *never* answer burned the whole budget before falling back to a reload.

There's now a ~50ms check first. If the page has settled and has no export panel, polling can't help, so the reload starts immediately. If it's still loading, the wait still applies. The check only reads state; it doesn't click or navigate anything.

**Nothing waits longer than two seconds before reloading.** Past two seconds a tab isn't slow, it's stuck. The read that happens *after* a reload keeps its longer budget deliberately — a page that's actively loading will finish.

## v4.5.1 — 2026-08-12

⚠️ **Re-paste the Pine script** — indicator-only change.

**GEX spacing, split the difference.** 4.5.0 pulled the GEX column in by 15% of the column gap and that overshot; it's 8% now, which lands it one bar in rather than two at typical spacing. Still a fraction of the spacing rather than a fixed number, so the spacing slider continues to move all three columns together.

### From 4.4.5

**The GEX column sits a hair closer**, correcting the same visual imbalance Score got in 4.4.0 — OI's labels are wide, so the gap before GEX read larger than the one before it. Both nudges are fractions of the column spacing, so your spacing slider still moves all three together.

### From 4.4.4

**The Score / OI / GEX columns could silently stop updating mid-session** — a sync that reloaded Nexus and got back an unchanged export kept the older read, whose spot price came from a frozen tab. The freshness check then compared today's strike data against a stale price and discarded the fresh half.

### From 4.4.3

**A sync could never reload Nexus if your dashboard lived in a second window** — selecting a tab only brings it forward within its own window, so the page stayed hidden and unreadable. It now raises the window and hands focus back to the chart.

**The feed clock could read five hours stale**, because Nexus renders that stamp in UTC before the page settles and in your own timezone afterwards.

**Two installed copies no longer fight** over the same Nexus tab.

### Recent

**4.4.1** — fixed a 14-second sync: a check added in 4.3.3 clicked TradingView's Overview nav to test whether the strike table was readable, which navigated the Nexus tab off the Export view and broke the *next* sync.

**4.4.0** — brightness slider; the Score column sits a quarter-gap closer so the three columns look evenly spaced.

[Full version history →](https://github.com/ahoward001/nexus-tv-bridge/blob/main/CHANGELOG.md)

---

## Assets — what clicking each one actually does

**`0-COPY-THIS-pine-script-for-tradingview.pine`** — the indicator that draws the columns, needed on **both** browsers.
Clicking **downloads a text file and installs nothing.** You paste its contents into TradingView's Pine Editor by hand — usually easier to use the "Open the script" link above and copy it in the browser.

**`1-FIREFOX-SETUP-…​.xpi`** — the Firefox add-on. Same file as the Install button above; clicking it in Firefox installs it. In Chrome it just downloads something useless.

**`2-CHROME-SETUP-…​.zip`** — the Chrome extension as a file, for anyone who can't use the Web Store.
Clicking **downloads a zip and installs nothing.** Chrome can't install an extension from a file. Unzip it → `chrome://extensions` → turn on **Developer mode** (top right) → **Load unpacked** → select the unzipped **`nexus-tradingview-bridge` folder** (the one with `manifest.json` directly inside — Chrome loads the folder, not the zip). Installed this way it will **not** auto-update.

**`3.0-GUIDE-chrome.txt` · `3.1-GUIDE-firefox.txt` · `3.2-GUIDE-pine.md`** — reading, not installing. The long-form walkthroughs if the steps above aren't enough. Readable in your browser: [Chrome](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-chrome-install.txt) · [Firefox](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-firefox-install.txt) · [Pine](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-pine-indicator-setup.md)

*Ignore "Source code (zip/tar.gz)" — GitHub generates those automatically and they aren't the extension.*

---

> **On version currency:** Firefox and the zip above are always this build. **Chrome's Web Store copy can be up to ~24 hours behind** — Google reviews every submission and locks the listing while one is pending, so Store releases land in batches. If you need today's code on Chrome right now, use the `2-CHROME-SETUP` zip and the manual steps above instead of the Store link.

---

> ### ⚠️ The Pine indicator changed on Aug 11, 2026
>
> If you have not re-pasted **`nexus-strike-metrics.pine`** since **4.4.0**, do it — nothing updates it for you, on any browser. Copy it from **step 0** above, paste over the old one, **Ctrl+S**. Your saved settings survive.

## v4.5.0 — 2026-08-12

⚠️ **Re-paste the Pine script** — the indicator changed again. This covers 4.4.5's spacing fix too, so one paste gets both.

**Brightness now works in both directions, from the middle.** The slider used to start hard left at "as configured" and only wash things out. It's now centred: drag left to push the whole overlay toward solid, right to fade it. Both directions are proportional, so the weighting that makes big levels read heavier than small ones survives either way — and the readout says *"20% bolder"* or *"20% fainter"* rather than a bare number, since a centred slider showing "−20" tells you nothing about which way that is.

**The alert settings are a real section now.** They were a stack of full-width boxes with headings above them, which read as unrelated fields rather than one rule. They're grouped under **Notifications** and **Price alerts**, and each number now sits inside its own sentence — *"Re-alert after price gets ⟨1⟩ strikes clear, having reached ⟨2⟩ strikes away, and stayed out that far for ⟨5⟩ minutes."*

### From 4.4.5

**The GEX column sits a hair closer**, correcting the same visual imbalance Score got in 4.4.0 — OI's labels are wide, so the gap before GEX read larger than the one before it. Both nudges are fractions of the column spacing, so your spacing slider still moves all three together.

### From 4.4.4

**The Score / OI / GEX columns could silently stop updating mid-session** — a sync that reloaded Nexus and got back an unchanged export kept the older read, whose spot price came from a frozen tab. The freshness check then compared today's strike data against a stale price and discarded the fresh half.

### From 4.4.3

**A sync could never reload Nexus if your dashboard lived in a second window** — selecting a tab only brings it forward within its own window, so the page stayed hidden and unreadable. It now raises the window and hands focus back to the chart.

**The feed clock could read five hours stale**, because Nexus renders that stamp in UTC before the page settles and in your own timezone afterwards.

**Two installed copies no longer fight** over the same Nexus tab.

### Recent

**4.4.1** — fixed a 14-second sync: a check added in 4.3.3 clicked TradingView's Overview nav to test whether the strike table was readable, which navigated the Nexus tab off the Export view and broke the *next* sync.

**4.4.0** — brightness slider; the Score column sits a quarter-gap closer so the three columns look evenly spaced.

[Full version history →](https://github.com/ahoward001/nexus-tv-bridge/blob/main/CHANGELOG.md)

---

## Assets — what clicking each one actually does

**`0-COPY-THIS-pine-script-for-tradingview.pine`** — the indicator that draws the columns, needed on **both** browsers.
Clicking **downloads a text file and installs nothing.** You paste its contents into TradingView's Pine Editor by hand — usually easier to use the "Open the script" link above and copy it in the browser.

**`1-FIREFOX-SETUP-…​.xpi`** — the Firefox add-on. Same file as the Install button above; clicking it in Firefox installs it. In Chrome it just downloads something useless.

**`2-CHROME-SETUP-…​.zip`** — the Chrome extension as a file, for anyone who can't use the Web Store.
Clicking **downloads a zip and installs nothing.** Chrome can't install an extension from a file. Unzip it → `chrome://extensions` → turn on **Developer mode** (top right) → **Load unpacked** → select the unzipped **`nexus-tradingview-bridge` folder** (the one with `manifest.json` directly inside — Chrome loads the folder, not the zip). Installed this way it will **not** auto-update.

**`3.0-GUIDE-chrome.txt` · `3.1-GUIDE-firefox.txt` · `3.2-GUIDE-pine.md`** — reading, not installing. The long-form walkthroughs if the steps above aren't enough. Readable in your browser: [Chrome](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-chrome-install.txt) · [Firefox](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-firefox-install.txt) · [Pine](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-pine-indicator-setup.md)

*Ignore "Source code (zip/tar.gz)" — GitHub generates those automatically and they aren't the extension.*

---

> **On version currency:** Firefox and the zip above are always this build. **Chrome's Web Store copy can be up to ~24 hours behind** — Google reviews every submission and locks the listing while one is pending, so Store releases land in batches. If you need today's code on Chrome right now, use the `2-CHROME-SETUP` zip and the manual steps above instead of the Store link.

---

> ### ⚠️ The Pine indicator changed on Aug 11, 2026
>
> If you have not re-pasted **`nexus-strike-metrics.pine`** since **4.4.0**, do it — nothing updates it for you, on any browser. Copy it from **step 0** above, paste over the old one, **Ctrl+S**. Your saved settings survive.

## v4.4.5 — 2026-08-12

⚠️ **Re-paste the Pine script for this one** — the change is in the indicator, and nothing updates it for you.

**The GEX column sits a hair closer.** All three columns are spaced by the same number of bars, but OI's own labels are wide (`+8.7K`), so the whitespace before GEX read larger than the gap before it. GEX now comes back in by a fixed fraction of the spacing — the mirror image of the correction Score already got in 4.4.0. It scales with the spacing slider rather than being a flat number, so widening the columns keeps the proportions.

### From 4.4.4

**The Score / OI / GEX columns could silently stop updating mid-session** — a sync that reloaded Nexus and got back an unchanged export kept the older read, whose spot price came from a frozen tab. The freshness check then compared today's strike data against a stale price and discarded the fresh half.

### From 4.4.3

**A sync could never reload Nexus if your dashboard lived in a second window** — selecting a tab only brings it forward within its own window, so the page stayed hidden and unreadable. It now raises the window and hands focus back to the chart.

**The feed clock could read five hours stale**, because Nexus renders that stamp in UTC before the page settles and in your own timezone afterwards.

**Two installed copies no longer fight** over the same Nexus tab.

### Recent

**4.4.1** — fixed a 14-second sync: a check added in 4.3.3 clicked TradingView's Overview nav to test whether the strike table was readable, which navigated the Nexus tab off the Export view and broke the *next* sync.

**4.4.0** — brightness slider; the Score column sits a quarter-gap closer so the three columns look evenly spaced.

[Full version history →](https://github.com/ahoward001/nexus-tv-bridge/blob/main/CHANGELOG.md)

---

## Assets — what clicking each one actually does

**`0-COPY-THIS-pine-script-for-tradingview.pine`** — the indicator that draws the columns, needed on **both** browsers.
Clicking **downloads a text file and installs nothing.** You paste its contents into TradingView's Pine Editor by hand — usually easier to use the "Open the script" link above and copy it in the browser.

**`1-FIREFOX-SETUP-…​.xpi`** — the Firefox add-on. Same file as the Install button above; clicking it in Firefox installs it. In Chrome it just downloads something useless.

**`2-CHROME-SETUP-…​.zip`** — the Chrome extension as a file, for anyone who can't use the Web Store.
Clicking **downloads a zip and installs nothing.** Chrome can't install an extension from a file. Unzip it → `chrome://extensions` → turn on **Developer mode** (top right) → **Load unpacked** → select the unzipped **`nexus-tradingview-bridge` folder** (the one with `manifest.json` directly inside — Chrome loads the folder, not the zip). Installed this way it will **not** auto-update.

**`3.0-GUIDE-chrome.txt` · `3.1-GUIDE-firefox.txt` · `3.2-GUIDE-pine.md`** — reading, not installing. The long-form walkthroughs if the steps above aren't enough. Readable in your browser: [Chrome](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-chrome-install.txt) · [Firefox](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-firefox-install.txt) · [Pine](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-pine-indicator-setup.md)

*Ignore "Source code (zip/tar.gz)" — GitHub generates those automatically and they aren't the extension.*

---

> **On version currency:** Firefox and the zip above are always this build. **Chrome's Web Store copy can be up to ~24 hours behind** — Google reviews every submission and locks the listing while one is pending, so Store releases land in batches. If you need today's code on Chrome right now, use the `2-CHROME-SETUP` zip and the manual steps above instead of the Store link.

---

> ### ⚠️ The Pine indicator changed on Aug 11, 2026
>
> If you have not re-pasted **`nexus-strike-metrics.pine`** since **4.4.0**, do it — nothing updates it for you, on any browser. Copy it from **step 0** above, paste over the old one, **Ctrl+S**. Your saved settings survive.

## v4.4.4 — 2026-08-12

**The Score / OI / GEX columns could silently stop updating mid-session.** A sync that reloaded Nexus and got back an unchanged export kept the *older* of the two reads. The levels in it were identical either way — but so was the spot price it carried, taken from a tab that had been sitting hidden and frozen. The freshness check then compared today's strike data against yesterday's price, decided the strike data must be stale, and left the columns untouched with a *"Strike metrics look stale"* warning. It was throwing away the fresh half.

The reloaded read is now used regardless, and when the two prices genuinely disagree the check settles it against the live price from your chart's own tab rather than assuming which side is wrong.

### From 4.4.3

**A sync could never reload Nexus if your dashboard lived in a second window** — selecting a tab only brings it forward within its own window, so the page stayed hidden and unreadable. It now raises the window and hands focus back to the chart.

**The feed clock could read five hours stale**, because Nexus renders that stamp in UTC before the page settles and in your own timezone afterwards.

**Two installed copies no longer fight** over the same Nexus tab.

### Recent

**4.4.1** — fixed a 14-second sync: a check added in 4.3.3 clicked TradingView's Overview nav to test whether the strike table was readable, which navigated the Nexus tab off the Export view and broke the *next* sync.

**4.4.0** — brightness slider; the Score column sits a quarter-gap closer so the three columns look evenly spaced.

[Full version history →](https://github.com/ahoward001/nexus-tv-bridge/blob/main/CHANGELOG.md)

---

## Assets — what clicking each one actually does

**`0-COPY-THIS-pine-script-for-tradingview.pine`** — the indicator that draws the columns, needed on **both** browsers.
Clicking **downloads a text file and installs nothing.** You paste its contents into TradingView's Pine Editor by hand — usually easier to use the "Open the script" link above and copy it in the browser.

**`1-FIREFOX-SETUP-…​.xpi`** — the Firefox add-on. Same file as the Install button above; clicking it in Firefox installs it. In Chrome it just downloads something useless.

**`2-CHROME-SETUP-…​.zip`** — the Chrome extension as a file, for anyone who can't use the Web Store.
Clicking **downloads a zip and installs nothing.** Chrome can't install an extension from a file. Unzip it → `chrome://extensions` → turn on **Developer mode** (top right) → **Load unpacked** → select the unzipped **`nexus-tradingview-bridge` folder** (the one with `manifest.json` directly inside — Chrome loads the folder, not the zip). Installed this way it will **not** auto-update.

**`3.0-GUIDE-chrome.txt` · `3.1-GUIDE-firefox.txt` · `3.2-GUIDE-pine.md`** — reading, not installing. The long-form walkthroughs if the steps above aren't enough. Readable in your browser: [Chrome](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-chrome-install.txt) · [Firefox](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-firefox-install.txt) · [Pine](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-pine-indicator-setup.md)

*Ignore "Source code (zip/tar.gz)" — GitHub generates those automatically and they aren't the extension.*

---

> **On version currency:** Firefox and the zip above are always this build. **Chrome's Web Store copy can be up to ~24 hours behind** — Google reviews every submission and locks the listing while one is pending, so Store releases land in batches. If you need today's code on Chrome right now, use the `2-CHROME-SETUP` zip and the manual steps above instead of the Store link.

---

> ### ⚠️ The Pine indicator changed on Aug 11, 2026
>
> If you have not re-pasted **`nexus-strike-metrics.pine`** since **4.4.0**, do it — nothing updates it for you, on any browser. Copy it from **step 0** above, paste over the old one, **Ctrl+S**. Your saved settings survive.

## v4.4.3 — 2026-08-11

**A sync could never reload Nexus if your dashboard lived in a second window.** Clicking sync selected the Nexus tab, but selecting a tab only moves it to the front *within its own window* — if that window sat behind another one, macOS kept the page hidden, and Nexus refuses to draw the export panel on a hidden page. Every read against it failed, so the sync gave up with *"Couldn't reload Nexus"* and pasted whatever it already had, sometimes 13 minutes old. It now brings the **window** forward, the same way it has always done for your chart, and hands focus straight back when it's finished.

**The feed clock could read five hours stale.** Nexus renders its freshness stamp in UTC when the page first arrives and re-renders it in your own timezone a moment later, so the same stamp says both "08:04 PM" and "03:04 PM". We always read it as UTC, so once the page settled the clock looked hours old and the button leaned yellow for no reason. It now reads both ways and takes the one that makes sense.

**Two copies of the extension no longer fight.** Installing from the Web Store while an unpacked copy is still loaded gave you two green tabs stacked exactly on top of each other, two background workers reloading the same Nexus tab, and each one breaking the other's read. The second copy now stands down with a note in the console instead. **Running two is still a bad idea** — only one gets to drive, so disable the one you aren't using at `chrome://extensions`.

### Recent

**4.4.1** — fixed a 14-second sync: a check added in 4.3.3 clicked TradingView's Overview nav to test whether the strike table was readable, which navigated the Nexus tab off the Export view and broke the *next* sync.

**4.4.0** — brightness slider; the Score column sits a quarter-gap closer so the three columns look evenly spaced.

[Full version history →](https://github.com/ahoward001/nexus-tv-bridge/blob/main/CHANGELOG.md)

---

## Assets — what clicking each one actually does

**`0-COPY-THIS-pine-script-for-tradingview.pine`** — the indicator that draws the columns, needed on **both** browsers.
Clicking **downloads a text file and installs nothing.** You paste its contents into TradingView's Pine Editor by hand — usually easier to use the "Open the script" link above and copy it in the browser.

**`1-FIREFOX-SETUP-…​.xpi`** — the Firefox add-on. Same file as the Install button above; clicking it in Firefox installs it. In Chrome it just downloads something useless.

**`2-CHROME-SETUP-…​.zip`** — the Chrome extension as a file, for anyone who can't use the Web Store.
Clicking **downloads a zip and installs nothing.** Chrome can't install an extension from a file. Unzip it → `chrome://extensions` → turn on **Developer mode** (top right) → **Load unpacked** → select the unzipped **`nexus-tradingview-bridge` folder** (the one with `manifest.json` directly inside — Chrome loads the folder, not the zip). Installed this way it will **not** auto-update.

**`3.0-GUIDE-chrome.txt` · `3.1-GUIDE-firefox.txt` · `3.2-GUIDE-pine.md`** — reading, not installing. The long-form walkthroughs if the steps above aren't enough. Readable in your browser: [Chrome](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-chrome-install.txt) · [Firefox](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-firefox-install.txt) · [Pine](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-pine-indicator-setup.md)

*Ignore "Source code (zip/tar.gz)" — GitHub generates those automatically and they aren't the extension.*

---

> **On version currency:** Firefox and the zip above are always this build. **Chrome's Web Store copy can be up to ~24 hours behind** — Google reviews every submission and locks the listing while one is pending, so Store releases land in batches. If you need today's code on Chrome right now, use the `2-CHROME-SETUP` zip and the manual steps above instead of the Store link.

---

> ### ⚠️ The Pine indicator changed on Aug 11, 2026
>
> If you have not re-pasted **`nexus-strike-metrics.pine`** since **4.4.0**, do it — nothing updates it for you, on any browser. Copy it from **step 0** above, paste over the old one, **Ctrl+S**. Your saved settings survive.

## v4.4.2 — 2026-08-11

Page and packaging only — no code changes. Assets renumbered so the **Pine script is step 0** (both browsers need it, and nothing installs it for you), Chrome and Firefox are 1 and 2 now that both are genuinely one click, and `about:addons` is a real link.

### Recent

**4.4.1** — fixed a 14-second sync: a check added in 4.3.3 clicked TradingView's Overview nav to test whether the strike table was readable, which navigated the Nexus tab off the Export view and broke the *next* sync.

**4.4.0** — brightness slider; the Score column sits a quarter-gap closer so the three columns look evenly spaced.

**4.2.x** — Chrome installs from the Web Store and updates itself; a sync that finds fresh data takes **~2 seconds instead of ~9**.

[Full version history →](https://github.com/ahoward001/nexus-tv-bridge/blob/main/CHANGELOG.md)

---

## Assets — what clicking each one actually does

**`0-COPY-THIS-pine-script-for-tradingview.pine`** — the indicator that draws the columns, needed on **both** browsers.
Clicking **downloads a text file and installs nothing.** You paste its contents into TradingView's Pine Editor by hand — usually easier to use the "Open the script" link above and copy it in the browser.

**`1-FIREFOX-SETUP-…​.xpi`** — the Firefox add-on. Same file as the Install button above; clicking it in Firefox installs it. In Chrome it just downloads something useless.

**`2-CHROME-SETUP-…​.zip`** — the Chrome extension as a file, for anyone who can't use the Web Store.
Clicking **downloads a zip and installs nothing.** Chrome can't install an extension from a file. Unzip it → `chrome://extensions` → turn on **Developer mode** (top right) → **Load unpacked** → select the unzipped **`nexus-tradingview-bridge` folder** (the one with `manifest.json` directly inside — Chrome loads the folder, not the zip). Installed this way it will **not** auto-update.

**`3.0-GUIDE-chrome.txt` · `3.1-GUIDE-firefox.txt` · `3.2-GUIDE-pine.md`** — reading, not installing. The long-form walkthroughs if the steps above aren't enough. Readable in your browser: [Chrome](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-chrome-install.txt) · [Firefox](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-firefox-install.txt) · [Pine](https://github.com/ahoward001/nexus-tv-bridge/blob/main/GUIDE-pine-indicator-setup.md)

*Ignore "Source code (zip/tar.gz)" — GitHub generates those automatically and they aren't the extension.*

---

> **On version currency:** Firefox and the zip above are always this build. **Chrome's Web Store copy can be up to ~24 hours behind** — Google reviews every submission and locks the listing while one is pending, so Store releases land in batches. If you need today's code on Chrome right now, use the `2-CHROME-SETUP` zip and the manual steps above instead of the Store link.

---

> ### ⚠️ The Pine indicator changed on Aug 11, 2026
>
> If you have not re-pasted **`nexus-strike-metrics.pine`** since **4.4.0**, do it — nothing updates it for you, on any browser. Copy it from **step 0** above, paste over the old one, **Ctrl+S**. Your saved settings survive.

## v4.4.1 — 2026-08-11

**Fixes a 14-second sync introduced in 4.3.3.** That release added a check for "can the strike table be read?" before deciding whether to reload — but the only way to read it clicks TradingView's Overview nav, which navigated your Nexus tab off the Export view. The *next* sync then found no export code and fell all the way through to opening a fresh tab: 14.7s instead of ~2s. The check broke the thing it was checking.

The check is gone. The problem it guarded against is still handled, just without side effects: if the strike read comes back empty the reload happens then, and a stale snapshot is pasted-and-labelled rather than dropped.

### From 4.4.0

**Brightness slider** — *bold ← → faded* in settings. Washes out bubbles, boxes and dotted lines together without disturbing the relative weighting that makes big levels read heavier.

**The Score column sits closer.** All three were spaced identically in bars, but Score holds `49` while GEX holds `−29.4M`, so equal spacing left more whitespace after Score. Shifted a quarter-gap right so they look even.


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

---

> ### ⚠️ The Pine indicator changed on Aug 11, 2026
>
> If you have not re-pasted **`nexus-strike-metrics.pine`** since **4.4.0**, do it — nothing updates it for you, on any browser. Copy it from the link in step 3 above, paste over the old one, **Ctrl+S**. Your saved settings survive.

## v4.4.0 — 2026-08-11

⚠️ **Re-paste the Pine script for this one** — the indicator changed. Copy it again from step 3 above; your saved settings survive.

**Brightness slider.** New *Brightness — bold ← → faded* control in settings. It washes out the whole overlay together — bubbles, boxes and dotted lines — without disturbing the relative weighting that makes big levels read heavier than small ones. It rides on top of the individual colour settings rather than replacing them, so any tuning you've already done survives.

**The Score column sits closer.** All three columns were spaced by the same number of bars, but Score holds one or two characters while OI and GEX hold things like `−29.4M` — so an identical gap left visibly more whitespace after Score. It's now shifted a quarter-gap right so the three *look* evenly spaced. Fixed rather than adjustable: it corrects an imbalance rather than expressing a preference.

### Also fixed

**Columns could be left stale while the levels updated.** The fast path skipped the reload whenever the export was fresh — but the strike table can be unreadable even when the export is fine, and the columns then silently kept old numbers. The fast path now has to deliver everything, and reloads if it can't.

**A sync that couldn't read strikes took ~9 seconds.** The reader's internal waits (~4.4s) were tuned separately and never added up, and the caller made two passes over the same tab. Reader is now bounded to ~2s, one pass, 3s cap — then it blinks, which is what actually fixes it.

**It always pastes something now.** A stale strike snapshot used to be discarded, leaving nothing; it's now used as a labelled fallback and both ages are reported — so "current levels, older columns" says so instead of looking like a clean sync.


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

## v4.3.3 — 2026-08-11

**Fixes a bug in 4.2.4–4.3.2: the columns could be left stale while the levels updated.**

The fast path skipped the reload whenever Nexus's export was fresh — but a sync writes two things, and the *strike table* can be unreadable from a tab even when the export is fine. When that happened you got current levels next to Score / OI / GEX numbers from an earlier read, and the sync still took ~9s because the strike reader retried before giving up.

The fast path now has to be able to deliver **everything**. If the strike table can't be read, that counts as stale and it reloads — which fixes it.

The extension did flag this itself (*"Strike metrics didn't update — the columns are stale"*), so it was visible rather than silent. But visible-and-wrong is still wrong.


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
