# Live Lotto — Pre-sale Landing Page (GitHub Pages)

Static landing page for the **Live Lotto Draw Results** app pre-sale.
Pay $9.9 once → lifetime premium code (reg. $199).

## Publish to GitHub Pages

1. Create a new repo, e.g. `live-lotto-presale`
2. Push the contents of this folder to the repo's `main` branch
3. Repo → **Settings → Pages** → Source: `Deploy from a branch` → Branch: `main` / `/(root)` → Save
4. Your page is live at `https://<username>.github.io/live-lotto-presale/`

## Before you launch — 3 things to replace

| Placeholder | Where | Replace with |
|---|---|---|
| `https://YOUR-PAYMENT-LINK` | `index.html` (pre-sale CTA button) | Your Stripe Payment Link, Gumroad, or Lemon Squeezy checkout URL for the $9.9 product |
| `support@example.com` | `index.html` (footer) | Your real support email |
| `PRESALE_END` | `index.html` (bottom script) | Your real pre-sale end date/time |

## Collecting pre-sale emails (optional)

GitHub Pages is static, so the checkout happens on your payment provider
(Stripe/Gumroad email you the buyer's address automatically — that's your
pre-sale list). If you also want a free "notify me" form, add a
[Formspree](https://formspree.io) endpoint to a form in `index.html`.

## Files

- `index.html` — the whole page (copy, styles, countdown, FAQ; logo inlined)
- `assets/css/images-a.css`, `assets/css/images-b.css` — app screenshots
  (web-optimized, embedded as data URIs so the site is fully self-contained)
