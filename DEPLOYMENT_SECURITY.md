# Deployment Security Checklist

This site is currently a static personal website. The production security posture should be enforced mostly at the hosting/CDN layer.

Replace `https://your-domain.com` with the final production domain before deployment.

## Required HTTPS

- Serve the site only over HTTPS.
- Redirect HTTP to HTTPS.
- Enable HSTS after the domain is stable:

```http
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
```

Do not enable `preload` until you are sure every subdomain supports HTTPS.

## Recommended Security Headers

```http
Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.tailwindcss.com https://unpkg.com https://cdn.jsdelivr.net; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data: https://your-domain.com; media-src 'self' https://stream.mux.com https://d8j0ntlcm91z4.cloudfront.net; connect-src 'self' https://stream.mux.com https://d8j0ntlcm91z4.cloudfront.net; frame-ancestors 'none'; base-uri 'self'; form-action 'self'; upgrade-insecure-requests
X-Content-Type-Options: nosniff
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=(), usb=(), interest-cohort=()
```

Important: the current site uses inline scripts, Tailwind CDN, Babel standalone, React UMD, Framer Motion UMD, and hls.js CDN. This requires a looser CSP than a bundled production build. A future Vite build can remove most `unsafe-inline` requirements.

## Static Asset Cache Policy

HTML:

```http
Cache-Control: no-cache
```

Versioned images, videos, fonts, and PDFs:

```http
Cache-Control: public, max-age=31536000, immutable
```

If files are not fingerprinted, use a shorter cache:

```http
Cache-Control: public, max-age=86400
```

## Platform Notes

### Cloudflare Pages

- Add the custom domain through Cloudflare Pages dashboard, not only by manually creating DNS records.
- Configure redirects and headers with `_redirects` and `_headers` if the site is deployed through Pages.
- Enable Web Analytics if lightweight traffic monitoring is needed.

### Vercel

- Configure security headers in `vercel.json`.
- Keep static files in the deployment root or `public` directory after migration.

### Aliyun or Tencent Cloud Static Hosting

- If the site is hosted on mainland China infrastructure, complete ICP filing before public access.
- Configure HTTPS certificate, CDN cache rules, and security headers at CDN level.

## Supply Chain Notes

Current external runtime dependencies:

- Tailwind CDN
- Google Fonts
- React UMD from unpkg
- ReactDOM UMD from unpkg
- Babel standalone from unpkg
- Framer Motion UMD from unpkg
- hls.js from jsDelivr
- Remote videos from Mux and CloudFront

Before long-term production operation, migrate to a build process so dependencies are pinned, bundled, and audited.

## Pre-Launch Checklist

- Replace all `https://your-domain.com` placeholders.
- Verify `robots.txt`, `sitemap.xml`, `security.txt`, and `llms.txt` are reachable from the domain root.
- Validate structured data with search engine rich result tools.
- Submit sitemap to search platforms.
- Confirm mobile navigation works after CDN caching is enabled.
- Confirm remote background videos have acceptable fallback behavior.
