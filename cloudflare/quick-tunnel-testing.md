# Cloudflare Quick Tunnel test

## Status

A temporary Quick Tunnel was tested on 2026-11-20 against the Ubuntu API lab. No Cloudflare account, registered domain, or DNS zone was used. The tunnel provided a temporary HTTPS URL for development testing only.

## Origin and reverse proxy

The API runs under the `secure-api.service` systemd unit on `127.0.0.1:8000`. Nginx listens on HTTP port 80 and HTTPS port 443, and proxies to Uvicorn with the upstream `Host` header set to `127.0.0.1`, which is in the API's trusted-host list.

The local HTTPS certificate is self-signed. Use `curl -k` for local HTTPS checks; the public Quick Tunnel URL uses HTTPS at Cloudflare's edge.

## Start and stop the tunnel

On the Ubuntu server, with the API running, start:

```bash
cloudflared tunnel --url http://127.0.0.1:80
```

Cloudflare prints a random `trycloudflare.com` hostname. Keep the `cloudflared` process running while testing. Press `Ctrl+C` in that terminal to stop the tunnel. The temporary hostname changes on a new run.

## Verification

- `GET /` through the temporary HTTPS URL returned `200` with the API welcome response.
- `GET /items` without an API key returned `401`, confirming that the protected endpoint still requires authentication.
- Authenticated `GET /items` through local Nginx returned `200` without printing the API key.
- Local Nginx HTTP and self-signed HTTPS checks returned `200`.
- The `secure-api` and `nginx` services were active.
- The API test suite passed all nine tests after the project was restored from backup.

No API key was included in this document. The authenticated `/items` route was not tested through the Quick Tunnel.

## Limitations

- The URL is temporary, public to anyone who has it, and has no uptime guarantee.
- Quick Tunnels are intended for development and testing, not production.
- This test does not configure custom DNS, a Cloudflare DNS zone, domain proxy settings, or a stable hostname.
- A registered domain is required for the standard Cloudflare full DNS setup. See [Quick Tunnel documentation](https://developers.cloudflare.com/tunnel/get-started/quick-tunnels/) and [Cloudflare full setup requirements](https://developers.cloudflare.com/dns/zone-setups/full-setup/setup/).
