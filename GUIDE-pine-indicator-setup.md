# Setting up the "Nexus Strike Metrics" indicator

The extension needs **two** indicators on your TradingView chart:

| Indicator | Where it comes from | What it draws |
|---|---|---|
| **Nexus Futures** (V3, V4.x — any version) | Nexus, invite-only | Nexus's own curated walls |
| **Nexus Strike Metrics** | `nexus-strike-metrics.pine` in this folder | The per-strike Score / OI / GEX columns ("strike metrics") |

You already have the first one if you're a Nexus subscriber. The second is the
Pine script included here, and you add it **once** — after that the extension
keeps it fed automatically.

> **The extension cannot install this for you.** Chrome extensions can't create
> TradingView indicators. It's a 2-minute, one-time copy-paste.

---

## Option A — do it by hand (2 minutes)

1. Open your TradingView chart.
2. Open **`nexus-strike-metrics.pine`** (in this folder) in any text editor.
   Select all (**Ctrl+A**) and copy (**Ctrl+C**). *(Mac: ⌘A / ⌘C.)*
3. Open the **Pine Editor**. On current TradingView it is *not* in the bottom
   toolbar — click the **grid/apps icon at the bottom-right of the chart** (the 3×3
   dots) and choose **Pine Editor** under *PRODUCTS*. (Star it there to keep it
   handy.)

   *Already have the indicator on the chart?* The quicker way back to its code is
   the **`{ }` brackets icon** on the indicator's row in the chart legend — it opens
   that script's source straight in the editor. That's the route to use when you're
   re-pasting an updated version.
4. Click into the code area, select all (**Ctrl+A**), and **paste** (**Ctrl+V**).
   This replaces the default template — that's correct.
5. Press **Ctrl+S** (⌘S on Mac) to save the script. Name it **Nexus Strike Metrics**
   if it asks.
6. Click **"Add to chart"** — **exactly once.**
7. Click the chart, then press **Ctrl+S** again to save the **layout**.
   *(Two different saves: step 5 saves the script, step 7 saves the chart.
   Skip step 7 and it disappears when you reload.)*
8. Click the extension's floating button to sync. The columns fill in.

### Things that will bite you

- **Click "Add to chart" only once.** Each click adds *another* copy. The
  extension writes to whichever it finds first, so a duplicate makes the visible
  one look frozen. To remove an extra: **click its legend title, then press
  Delete.** TradingView's legend Remove button ignores programmatic clicks, and
  the hover-X is fiddly — the title-then-Delete route is the reliable one.
- **Don't click "Publish script."** That shares it publicly. You want Ctrl+S.
- **Two saves are required** (script *and* layout). This is the #1 reason
  people say "it vanished after I refreshed."
- If the editor shows a banner saying *"This is a historical version"*, you're
  viewing an old snapshot and it's **read-only** — pastes silently do nothing.
  Click the script-name dropdown and pick the current version first.

---

## Option B — have an AI assistant do it

If you use ChatGPT, Claude, or any assistant that can drive your browser, paste the
prompt below. Everything it needs is in it — it doesn't matter which one you use.

```text
I need you to install a TradingView Pine indicator for me. Please do it
yourself rather than giving me instructions.

THE FILE: nexus-strike-metrics.pine, in the nexus-tradingview-bridge folder I
was sent. Read it and use its full contents verbatim — do not rewrite,
summarize, shorten, or "improve" it. It must be pasted exactly as-is.

WHAT TO DO, in order:
1. Open my TradingView chart. Make sure the tab is actually visible/foreground
   — TradingView does not render its legend or Pine editor on a hidden tab, so
   anything you try on a background tab will silently fail.
2. Open the Pine Editor (the "Pine" button in the bottom toolbar).
3. If a banner says "This is a historical version of the script," you are in a
   READ-ONLY view and pastes will do nothing. Get out of that view first
   (script-name dropdown -> current version).
4. Select all in the editor and replace everything with the file's contents.
5. Save the SCRIPT (Ctrl+S, or Cmd+S on Mac). Confirm the editor shows "Saved" and that
   there are no red compile errors.
6. Click "Add to chart" EXACTLY ONCE. Do not click it twice — each click adds
   a duplicate indicator, and duplicates cause levels to appear not to update.
   Do NOT click "Publish script" at any point.
7. Verify the chart legend now lists BOTH:
      - "Nexus Strike Metrics"
      - "Nexus Futures" (some version — V3, V4.1, etc.)
   If "Nexus Futures" is missing, STOP and tell me. Do not save the layout,
   because saving without it would erase it from my saved chart.
8. Once both are present, save the LAYOUT (click the chart, Ctrl+S, or the
   Save button next to the layout name). This is a SEPARATE save from step 5 —
   skipping it means the indicator disappears on reload.
9. Tell me it's done and to click the extension's floating button to sync.

IF YOU END UP WITH A DUPLICATE: do not try to click the legend's Remove/hide
button -- TradingView rejects synthetic clicks on it. Click the duplicate's
legend TITLE to select it, then press the Delete key. Verify exactly one
"Nexus Strike Metrics" remains before saving the layout.

DO NOT: edit the Pine source, change my other indicators' settings, delete
anything from my chart, or save the layout if anything is missing.
```

---

## After setup

Click the extension's floating button on the chart. It reads Nexus, writes the
levels into the indicator, and the Score / OI / GEX columns appear to the right
of price. From then on every sync refreshes them automatically.

Colors are all adjustable in the indicator's **Settings → Colors** — the score
ramp, the OI/GEX green/red scales, header colors, and how faint small values
get. Nothing there affects the data, only how it looks.
