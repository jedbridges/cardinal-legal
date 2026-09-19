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

In Plausible, both events carry a `variant` property.

- **Hero shown** fires once per page view.
- **Download click** fires when someone taps through to the App Store, and
  also records `place`: `hero`, `subnav`, `footer` or `page`.

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

Seven are written; four run at a time. In `index.html`, `MESSAGES` holds all
of them and `LIVE` holds the ones being served.

| Name | Angle |
| --- | --- |
| `control` | The incumbent, and the only one in the HTML itself |
| `privacy` | Nobody is watching you read |
| `nodata` | No account, no ads, nothing collected |
| `ai` | Ask a question, get the verses |
| `offline` | The whole Bible, signal or not |
| `free` | Reading is free, all of it |
| `nofeed` | No feed, no streaks, no badges |

To add one, put it in `MESSAGES` and add its name to `LIVE`. Keep the same
shape: an `h1` with one `<em>` phrase, and a `lede` of one or two sentences.

Every claim in a message has to be true. These are marketing lines on a page
whose whole argument is that it does not exaggerate, and a headline is the
easiest place to accidentally promise something the app does not do.

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

**Analytics is Plausible**: cookieless, no personal data, no consent banner.
That is not a preference. This page argues that nobody is watching you read,
and it cannot make that argument over Google Analytics. Section 13 of the
privacy policy describes both the analytics and this test.

## Setup, once

The analytics tag in `index.html` ships with `PLAUSIBLE_DOMAIN_NOT_SET`.
Create the site at plausible.io, then replace that string with
`cardinalbible.app`.

Until you do, the script 404s harmlessly, every event is a no-op, and the
experiment still assigns and renders. Nothing on the page depends on
analytics loading, so a forgotten key costs you data and not a broken page.
