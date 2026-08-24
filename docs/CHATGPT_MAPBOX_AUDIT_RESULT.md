# Mapbox audit result — the dots are DOM markers, and AT&T is refusing to send data

The evidence-only audit you asked for has run. Two findings, both from artifacts,
not inference. No classifier change was made.

## Repo, so you can read the raw files yourself

```
https://github.com/patricksiado-prog/Go-High-Level-MCP-2026-Complete
branch: claude/optimus-map-tools-setup-6dcl6o
```

NOT `optimus-map-tools` — that repo holds `fiber_hunter.py` v5.27, a pixel-based
tool that is **not running**. An earlier review lost time on it.

| file | contents |
|---|---|
| `optimus/_feed/mapbox_features_dump.json` | 79 DOM markers with pixel positions and computed colour |
| `optimus/_feed/mapbox_style_dump.json` | proves no Mapbox Map object exists |
| `optimus/_feed/heartbeat.json` | live phase trail |
| `optimus/_feed/20260823-*.json` | per-run reports: stage counters, capture truth, zero-lead bodies |
| `optimus/precise_fiber_hunter.py` | the running hunter |
| `optimus/decode_gold.py`, `wire_diff.py`, `build_codes.json` | decoder, diff tool, code table |

BRAIN notes: `patricksiado-prog/optimus-map-tools`, branch
`claude/new-session-8z4pyb`, `BRAIN.md` sections 22.20–22.26.

---

## FINDING 1 — `queryRenderedFeatures()` could never have worked

```
map object captured : False
style layers        : 0
rendered features   : 0
DOM markers         : 255 present (80 captured)
error               : no mapboxgl.Map object found
```

AT&T uses `mapboxgl.Marker` — DOM elements — and never exposes the `Map`
instance. There is no style to read, no `circle-color` expression, no filter.
Every diagnostic built on the Mapbox query path was aimed at an abstraction this
page does not expose.

**Ground truth from one populated Devonwood viewport:**

```
rgb(65, 166, 0)      60   GREEN
rgb(137, 137, 137)   11   GREY
rgb(255, 176, 0)      8   GOLD
rgba(0, 0, 0, 0)      1   (the user's own location pin)
```

**The markers carry NO usable state:**

```html
<div class="address-marker mapboxgl-marker mapboxgl-marker-anchor-center"
     aria-label="Map marker" role="button" tabindex="0" aria-expanded="false"
     style="background: rgb(255, 176, 0);
            transform: translate(374px, 390px) translate(-50%,-50%) translate(0,0);">
```

- no `data-*` attributes on any marker
- no React props on the DOM node
- no `lngLat` on the element
- all 79 share ONE class name

The colour is written straight to `background-color` by AT&T's JS. The DOM
cannot tell us which backend property drove it.

**But the join is still solvable.** Each marker carries a pixel position, and
backend records carry lat/lng. At neighbourhood scale Mercator is locally
affine, so with ~79 points on each side the lat/lng → pixel transform can be fit
by least squares. **The residual is the proof**: if the two sets correspond the
fit snaps to near-zero; if they don't, it blows up. That gives a record-level
pairing, not an aggregate count match — which is the bar you correctly set.

---

## FINDING 2 — this is why nothing parses, and it is not a parser bug

From the same run's console:

```
!! WHY THIS VIEW CAPTURED NOTHING:
!! VALID JSON but no 'content' list.
!! Top-level keys: errors, isSuspended, success
```

Stage counters for that run:

```
AT&T REPLIES (200 JSON)   79
GREEN classified           0
GOLD classified            0
GREY classified            0
UNKNOWN classified         0
AUTH_EXPIRED replies       4
PARSE_ERROR replies        3
VALID_ZERO cells           1
FIRST DROP: CLASSIFIED
```

**79 valid JSON replies, none containing a `content` array.** AT&T answers
200 OK and declines to send addresses. There is nothing to parse.

`isSuspended` is a TOP-LEVEL key — it describes the session or the account
making the request, not an individual address.

Caveat stated plainly: **the key name is confirmed, the value is not.** The full
body publishes with the run report; until then this is a strong reading, not a
proven fact.

If `isSuspended: true`, then the parser, the classifier and the Mapbox path were
never the problem, and no rebuild could have fixed it — it is an account-side
block that needs AT&T rather than a commit.

---

## What was NOT changed

- the GREEN predicate — untouched throughout
- gold/grey classification — an undecodable customer is still written as
  UNKNOWN and never promoted (`OPTIMUS_UNKNOWN_CUSTOMER` defaults to `unknown`)
- `build_codes.json` — no guessed mapping added

## The one question worth answering now

Have you seen `isSuspended` in AT&T's dealer/serviceability API? Does it mean
the dealer account's map access is suspended, a rate limit, or something
per-request? That determines whether this is an AT&T account problem or a
request-shape problem — and it is the only thing standing between here and
working capture.
