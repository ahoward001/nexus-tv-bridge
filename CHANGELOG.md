# Version history

**MAJOR** = a whole new capability · **MINOR** = a feature within one · patch = a bug fix.

Newest first.

---

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
