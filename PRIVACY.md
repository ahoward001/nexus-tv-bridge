# Privacy Policy — Nexus → TradingView Bridge

_Last updated: 2026-08-10_

**Short version: this extension collects nothing, sends nothing anywhere, and has no
servers, no analytics, and no accounts.**

## What it does with data

The extension reads the options levels shown on your **own, already-signed-in Nexus
dashboard tab** and writes them into the settings of an indicator on **your own
TradingView chart**. That data moves from one of your browser tabs to another, on
your machine. It is not copied, uploaded, or retained anywhere else.

It also reads the price shown on your TradingView chart, in order to notice when
price approaches one of your levels. That reading happens locally and is used only to
decide whether to show you a desktop notification.

## What it does not do

- **No data is transmitted to the developer or to any third party.** The extension
  has no backend. There is no server to send anything to.
- **No analytics, telemetry, tracking, or advertising identifiers** of any kind.
- **No credentials are handled.** The extension never sees, stores, or transmits your
  Nexus or TradingView password, cookies, or session tokens. It relies entirely on
  the sessions you are already signed into in your own browser.
- **No browsing history.** It only runs on `dashboard.nexusfutures.net` and
  `tradingview.com`, and cannot see any other site.
- **Nothing is sold or shared.** There is nothing collected to sell or share.

## What is stored, and where

Your **settings** — which columns to show, how many levels to draw, where the columns
sit, alert preferences and thresholds — are saved using the browser's own extension
storage.

One thing worth being explicit about: this uses your browser's built-in **settings
sync**, so if you have browser sync enabled, your settings travel between your own
signed-in browsers the same way your bookmarks do. That transfer is handled by your
browser vendor (Google or Mozilla) under their privacy policy, not by this extension,
and it contains only your display preferences — no market data, and nothing personal.
If you have browser sync turned off, the settings stay on that machine.

The extension also keeps a small amount of local state so alerts behave sensibly —
for example, the last price it saw and when a level last triggered — so it doesn't
notify you repeatedly about the same thing. That state never leaves your machine and
is discarded when you uninstall.

## Permissions, and why each one exists

| Permission | Why |
|---|---|
| `storage` | Save your display and alert preferences. |
| `scripting` | Read the levels from the Nexus page and write them into the TradingView indicator. This is the core function. |
| `notifications` | Show optional desktop alerts when price approaches a level. Off by default. |
| `alarms` | Schedule the periodic price check that drives those alerts. |
| `dashboard.nexusfutures.net` | Read your own levels from your signed-in dashboard tab. |
| `*.tradingview.com` | Write those levels into the indicator on your chart. |

## Network requests

The extension makes requests to **one** origin: `dashboard.nexusfutures.net` — the
same site you are already signed into — to read your current levels. Those requests
return page content, which is parsed as text. **No code is downloaded or executed
from any remote source**; everything that runs ships inside the extension package.

## Changes

Any change to this policy will be published in this file, with the date above
updated. The file's history is public in the repository.

## Contact

Questions: **aidan@axiumwealth.com**

This extension is an independent tool and is not affiliated with, endorsed by, or
sponsored by Nexus Futures or TradingView.
