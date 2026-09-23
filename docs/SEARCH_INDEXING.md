# Getting this site found

Audited 2026-09-23. The pages were published 2026-09-19, so most of what
follows is "nobody has asked a search engine to look yet" rather than
anything broken.

## What the audit found

Clean: no `noindex` anywhere, no `X-Robots-Tag` header, correct self-referencing
canonicals on all seven pages, every landing page reachable from the home page
and from every sibling, all 200s, `robots.txt` allowing every search and
answer-engine crawler by name, a valid sitemap, `FAQPage` + `Organization` +
`Review` JSON-LD, and `/llms.txt` with `/llms-full.txt`.

Not clean, and both are certificate problems rather than content problems:

1. **HTTPS is not enforced.** `http://cardinalbible.app/` answers `200`
   instead of redirecting to `https://`. Every page therefore exists at two
   addresses. The canonical tags stop this becoming a duplicate-content
   problem, but it wastes crawl and it is one checkbox.
2. **`https://www.cardinalbible.app/` is broken.** The `www` CNAME resolves to
   `jedbridges.github.io`, but the served certificate is `*.github.io`, which
   does not match, so a browser shows a full-page security warning. Over plain
   `http` it correctly `301`s to the apex. Since browsers now try HTTPS first,
   anyone typing `www.cardinalbible.app` is likely to hit the warning.

Both have the same cause. The Pages certificate is stuck:

```
https_enforced: False
https_certificate.state: dns_changed
https_certificate.domains: ['cardinalbible.app']
```

`dns_changed` means GitHub noticed a DNS change and is re-requesting a
certificate, and it has been in that state since at least 2026-09-18. While it
is stuck, the API refuses to turn on enforcement: `PUT /repos/.../pages` with
`{"https_enforced": true}` returns `404 The certificate has not finished being
issued`. The DNS itself is right: the four apex A records
(`185.199.108-111.153`), no conflicting records, and no CAA record blocking
Let's Encrypt.

**The fix is to unstick the certificate.** In the repo's Settings > Pages,
clear the custom domain, save, then type `cardinalbible.app` back in and save.
That forces a fresh certificate request covering the apex and `www`. Wait for
"Enforce HTTPS" to stop being greyed out, then tick it. The site is briefly
unreachable on the custom domain in between, which is why this is not scripted.

## Google and Bing still need an account

Neither can be done from a checkout, because both want a signed-in human.

**Google Search Console.** Add a *domain* property (`cardinalbible.app`), not a
URL-prefix one. A domain property covers `http`, `https` and `www` in one go,
which matters here given the two problems above. It verifies by DNS TXT record,
added at GoDaddy, where the nameservers already are (`ns01/ns02.domaincontrol.com`).
Then submit `https://cardinalbible.app/sitemap.xml` under Sitemaps, and use
URL Inspection > Request Indexing once on each of the five landing pages.
Google is the only one of these that cannot be hurried any other way.

**Bing Webmaster Tools.** Offers "Import from Google Search Console", which is
the whole job once Google is verified. Do Google first.

Nothing in the site's HTML needs a verification meta tag if you verify by DNS,
which is why none was added.

## IndexNow needs nobody

Bing, Yandex, Seznam and Naver accept URL submissions with no account. The key
is proved by serving it at the site root:

```
267de0147f1d471bb1998f9a47dcf79f.txt
```

That file must stay published. To submit:

```
python3 scripts/submit-indexnow.py              # everything in sitemap.xml
python3 scripts/submit-indexnow.py /quiet-time/ # just these
```

It refuses to submit unless the key file is actually live, so running it before
a push fails loudly instead of silently having every URL rejected. Run it when a
page is new or materially rewritten, not on a schedule: resubmitting unchanged
URLs is the one thing the protocol asks you not to do.

Google does not participate in IndexNow. There is no way around Search Console
for Google.

## Do not expect search to be the channel

Worth writing down so it is not relitigated. People looking for a Bible app
search the App Store, not Google, and the head terms belong to YouVersion and
BibleGateway, which cannot be outranked. This work is worth doing because it is
cheap and because an unindexed site cannot correct anything, not because search
is going to move installs.

The measurable version of that claim: assistants asked about Cardinal today
answer from the App Store listing and from third-party directories, and get it
wrong, confidently listing the NIV and the ESV as available translations. The
site is the only channel that can fix that, and it has to be in the index first.

## Where answer engines actually read Cardinal

Not here. Asked "distraction-free Bible app, no streaks", an assistant returned
Cardinal's own positioning almost verbatim and did not name the app, because it
was reading [faith.tools](https://faith.tools/bible), where Cardinal is entry 97
of about 100. Cardinal is also reviewed at position 8 on
[learnofchrist.com](https://learnofchrist.com/directory/best-bible-apps).

Those directories, not `/llms.txt`, are what assistants cite for this category.
Getting onto more of them is the highest-value AEO work available, and it is
email and forms rather than code. `docs/DIRECTORY_LISTINGS.md` tracks it.
