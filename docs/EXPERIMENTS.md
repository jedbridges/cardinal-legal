# Testing the hero message

The top of the landing page shows one of several messages, chosen at random
per visitor and remembered. Two numbers decide which one is best: how many
people saw it, and how many of those clicked through to the App Store.

Everything lives in `index.html`. Search for `HERO MESSAGE EXPERIMENT`.

## Before anything else: what this can and cannot tell you

**It measures clicks, not installs.** Apple does not hand a website the
outcome of a tap on an App Store link. The click-through rate is a proxy. A
winner found here should be confirmed against downloads in App Store Connect
before you believe it completely.

**It needs more traffic than people expect.** This is the part that decides
whether the whole exercise is worth doing, so here is the arithmetic rather
than a reassurance. Assuming roughly one visitor in eight clicks through:

| To be confident a message is | Visitors needed, per message |
| --- | --- |
| 10% better | 12,000 |
| 25% better | 2,000 |
| 50% better | 560 |
| twice as good | 160 |

Multiply by the number of messages running. Four messages chasing a 50%
difference is about 2,200 visitors; at 30 visitors a day that is ten weeks.
The same four chasing a 10% difference is 48,000 visitors, which is never.

Two things follow from that table, and they are the whole method:

1. **Run few messages at once.** Four is the current setting and is already
   generous. Two finishes twice as fast.
2. **Only look for large differences.** A small-site test can find "this
   message is much better". It cannot find "this message is slightly
   better", and a number that wobbles above and below the others for a month
   is telling you the messages are equivalent, not that you need more time.

If a round ends with no clear winner, that is a real result. It means the
headline is not what is holding the page back, and the next thing to test is
something else.

## Running a round

1. Open `index.html` and find `LIVE` near the top.
2. Set it to the names you want running, e.g. `['control', 'nodata', 'free']`.
3. Commit and push. Pages redeploys on its own.

Anyone already assigned to a message you removed is reassigned on their next
visit, which is correct: a retired message should stop being served.

Always keep `control` in the list. It is the message the page is wearing
today, and without it a round tells you which challenger beat the others but
not whether any of them beat what you already had.

## Reading the results

Both signals carry a `variant` parameter.

- **`web.hero_shown`** fires once per page view.
- **`web.download_clicked`** fires when someone taps through to the App
  Store, and also carries `place`: `hero`, `subnav`, `footer` or `page`.

Names follow the app's own convention from `AnalyticsEvent.swift`: dotted,
lowercase, underscores inside a word. The `web.` prefix keeps the site's
signals separable from the app's at a glance.

In TelemetryDeck, build one insight counting `web.hero_shown` grouped by
`variant`, and another counting `web.download_clicked` grouped the same way.
The click-through rate is the second divided by the first.

Click-through rate for a message is its `Download click` count divided by its
`Hero shown` count. Compare those rates, not the raw click counts: an unlucky
split can hand one message more traffic than another.

Before calling a winner, check the table above. If the leader has fewer
visitors than the row you are aiming at, you do not have an answer yet, no
matter how large the gap looks. Gaps are largest early, when they mean least.

`place` is worth reading on its own. If most conversions come from the sticky
bar rather than the hero, the hero message matters less than this test
assumes, and the bar is where the work should go.

## The messages

Eleven are written; four run at a time. In `index.html`, `MESSAGES` holds
all of them and `LIVE` holds the ones being served.

| Name | Angle | Running |
| --- | --- | --- |
| `control` | The incumbent, and the only one in the HTML itself | yes |
| `ai` | Ask a question, every answer shows its verses | yes |
| `ai-grounded` | It quotes the text, not its memory of it | yes |
| `ai-path` | Say what you are going through, it builds the plan | yes |
| `ai-free` | The biggest questions, answered in full, free | parked |
| `ai-private` | A Bible AI that never reads your notes | parked |
| `privacy` | Nobody is watching you read | parked |
| `nodata` | No account, no ads, nothing collected | parked |
| `offline` | The whole Bible, signal or not | parked |
| `free` | Reading is free, all of it | parked |
| `nofeed` | No feed, no streaks, no badges | parked |

The current round tests one hypothesis: that the AI is the reason to
download. Three framings of it against the incumbent, chosen to be as
unalike as possible, because two similar messages split the traffic and
answer nothing.

- `ai` is **capability**: it can answer.
- `ai-grounded` is **trust**: it will not invent a verse.
- `ai-path` is **personalisation**: it makes something for you.

If all three lose to `control`, AI is not the reason people download, and
that is worth knowing in one round rather than six.

### On the grounded claim

`ai-grounded` is the one no generic AI Bible app can copy, so it is worth
saying exactly what backs it. From `AskAboutView.swift` in the app:

> when a question names a passage, Cardinal sends that passage's exact text
> so the wording is the text and not a memory of it

Licensed translations never leave the device, so with one selected Ask quotes
the nearest public-domain edition rather than the licensed wording. Custom
paths verify every reference against the bundled Bible before you see it, and
a scanned photo only surfaces references that resolve to a real verse.

Do not stretch this into "the AI cannot be wrong". It can be wrong about
interpretation. What it does not do is misquote the text or cite a verse that
does not exist.

### Writing another one

Put it in `MESSAGES` and add its name to `LIVE`. Keep the same shape: an `h1`
carrying one `<em>` phrase, and a `lede` of one or two sentences.

Every claim in a message has to be true. These are marketing lines on a page
whose whole argument is that it does not exaggerate, and a headline is the
easiest place to accidentally promise something the app does not do. Two that
were considered and rejected for exactly that reason: "the AI runs on your
phone", which is true of custom paths and photo scanning but not of Ask, and
"AI that never sees what you are reading", when asking about a passage sends
that passage.

## How it works, and why it is built this way

**The control is in the HTML.** Crawlers, readers with JavaScript off, and
anyone opening view-source get the real headline rather than a placeholder.
Only the other messages are swapped in.

**The swap is synchronous and next to the element.** Parsing stops at that
script, the text changes, and the browser paints once. A swap that waits on a
flag service paints the old headline first, and then the test is partly
measuring its own flicker.

**Assignment happens in the head**, before anything renders, and is stored as
one word in `localStorage`. No cookie, no identifier, no network call. If
storage is unavailable the visitor is simply reassigned each time, which
costs a little precision and breaks nothing.

**Analytics is TelemetryDeck**, which the app already reports to. That is
the reason to prefer it over a web analytics tool: the site introduces no
new company into the handling of anything, so section 13 of the privacy
policy names one processor rather than two. On a site whose argument is that
nobody is watching you read, that is worth more than a nicer funnel chart.

The cost is that TelemetryDeck is built for apps. It will not hand you a
conversion rate; you build two insights and divide. `track()` is
provider-agnostic, so if that becomes annoying, Umami and Plausible are one
commented-out script tag away.

The tag is `defer`, which keeps it off the critical path and guarantees it
has executed before `DOMContentLoaded`. That is what lets the events fire
without a queue: Umami has none of its own, so an event sent while the page
is still parsing is simply lost. The impression waits for
`DOMContentLoaded`; clicks happen long after.

## Setup, once

The tag in `index.html` ships with `TELEMETRYDECK_APP_ID_NOT_SET`.

**Create a separate TelemetryDeck app for the website. Do not reuse the iOS
app's ID.** Web visitors and app users in one bucket means every app metric
quietly counts people who only ever read a web page, and that is not a
mistake you notice, it is one you act on.

Then replace that string with the new app's ID.

### Checking it actually works

Load the site with `?debug=analytics` and open the browser console. It
prints which provider it found and what it sent:

```
[analytics] via telemetrydeck web.hero_shown {variant: 'ai-grounded'}
[analytics] variant=ai-grounded | provider=telemetrydeck
```

If it says `NO PROVIDER FOUND`, the app ID is still unset, the script is
blocked, or an ad blocker ate it. Worth doing once after setup: silent
analytics that records nothing looks exactly like analytics that works
until you go looking for the data weeks later.

The adapter finds the SDK by looking for a `signal` function on `td`,
`TelemetryDeck` or `telemetrydeck`, rather than hardcoding one. That is
deliberate: this was written somewhere their CDN and docs were unreachable,
so the integration detects the API instead of assuming it.

Until you do, the script 404s harmlessly, every event is a no-op, and the
experiment still assigns and renders. Nothing on the page depends on
analytics loading, so a forgotten key costs you data and not a broken page.
