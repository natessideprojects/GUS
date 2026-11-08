# GUS Drive demo website

Website for https://gusdrive.com, hosted on Vercel from natessideprojects/GUS.

The full demo binaries belong in GitHub Releases, not Git history or the Vercel deployment. The website distinguishes North Georgia Windows/Android from DIY Windows; DIY Android is not supplied.

Edit `content/pages.json` and `content/layout.html` for page content, `public/style.css` for styling and `public/app.js` for interactions. Regenerate HTML with `python -B scripts/build.py`, run `npm run build`, then preview with `npm run dev`. Commit only the site, scripts and documentation. `releases/` and `work/` are ignored.

Release tag: `demo-2026-11-07`. Publish the four full app download files (two North Georgia Windows ZIP parts, the APK and the DIY ZIP), `SHA256SUMS.txt`, `downloads.json` and `DEMO-README.txt` together. The project owner confirmed completion of the redistribution review on November 7, 2026. The downloads are demos with known issues, not a full release. Bundled third-party license notices remain included.

Contact is shown behind the Contact page's email button; this avoids displaying the address, but is not a guarantee against address harvesting. No analytics, cookies, accounts or document-upload service is added by this static site.
