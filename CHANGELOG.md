# Version history

**MAJOR** = a whole new capability · **MINOR** = a feature within one · patch = a bug fix.

Newest first.

---

## v4.5.2 — 2026-08-12

## Read this first

**1. Install (Firefox).** Open this page **in Firefox**, then under **Assets** click
**`1-FIREFOX-SETUP-nexus-tv-bridge-v4.5.2.xpi`** → **Add**. Ignore "Source code" — that's not the extension.

**2. Grant host permissions — or nothing works.** Firefox treats them as optional:
`about:addons` → Nexus → TradingView Bridge → **Permissions** → enable
**dashboard.nexusfutures.net** and **tradingview.com**.

**3. Turn on automatic updates.** `about:addons` → Nexus → TradingView Bridge → the
**...** menu → **Allow Automatic Updates** on. Firefox then checks daily and you never
repeat step 1.

**4. Pine indicator:** [nexus-strike-metrics.pine](https://github.com/ahoward001/nexus-tv-bridge/blob/main/nexus-strike-metrics.pine)
— copy it into TradingView's Pine Editor, Ctrl+S, Add to chart once, then Ctrl+S again to save the layout.
It is NOT part of the extension and never auto-updates.

Requires Firefox 128+.

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
