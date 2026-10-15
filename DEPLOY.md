# Deploy and DNS checklist

Host: **Cloudflare Pages** (free, fast in India, and DNS, email forwarding and the registrar all live in the same dashboard).

## 1. Buy the domain (5 minutes, phone OK)
1. Go to dash.cloudflare.com, sign up or log in.
2. Domain Registration > Register Domains > search `dromgurram.com` > buy (at cost, about USD 10 a year).
3. If you buy elsewhere (GoDaddy, Namecheap, Hostinger): add the site to Cloudflare (Websites > Add a site > Free plan) and change the nameservers at your registrar to the two Cloudflare gives you.

## 2. Create the Pages project
1. Cloudflare dashboard > Workers & Pages > Create > Pages > Upload assets.
2. Project name: `dromgurram`. Upload anything (it gets replaced by the first real deploy).
3. Custom domains > Set up a custom domain > `dromgurram.com`. Add `www.dromgurram.com` too.
4. Cloudflare creates these DNS records itself. Check they exist under DNS > Records:

| Type | Name | Content | Proxy |
|---|---|---|---|
| CNAME | dromgurram.com (@) | dromgurram.pages.dev | Proxied |
| CNAME | www | dromgurram.pages.dev | Proxied |

5. Rules > Redirect Rules > "Redirect from WWW to root" template, so there is one canonical address.

## 3. Let GitHub deploy it
1. Cloudflare > My Profile > API Tokens > Create Token > template "Edit Cloudflare Workers" (covers Pages). Copy the token.
2. Copy your Account ID from the Workers & Pages overview page (right side).
3. GitHub > theantideather/alienables.xyz > Settings > Secrets and variables > Actions > New repository secret:
   - `CLOUDFLARE_API_TOKEN` = the token
   - `CLOUDFLARE_ACCOUNT_ID` = the account ID
4. Every push to `main` that touches `site/` now builds, checks, deploys, and pings IndexNow.

## 4. Email: hello@dromgurram.com (free)
1. Cloudflare > dromgurram.com > Email > Email Routing > Enable. It adds the MX and TXT records itself.
2. Custom address `hello` > forward to your Gmail. Confirm the verification email.
3. Tell me it works, and I'll put it on /contact and /press.

## 5. After it's live
Search Console and Bing Webmaster Tools steps are in Phase 4 of PLAN.md. The TXT record Google gives you for verification goes in DNS > Records > Add > Type TXT, Name @.
