# Cloudflare Quick Tunnel test

## Status

A temporary Quick Tunnel was tested on 2026-11-20 against the Ubuntu API lab. No Cloudflare account, registered domain, or DNS zone was used. The tunnel provided a temporary HTTPS URL for development testing only.

## Origin and trusted host

The tunnel forwarded requests to the API on Ubuntu at `http://127.0.0.1:8000`. Uvicorn was started with a process-only trusted-host override:

```bash
ALLOWED_HOSTS='localhost,127.0.0.1,*.trycloudflare.com' uvicorn api.main:app --host 127.0.0.1 --port 8000
```

This override applied only to that Uvicorn process; it did not change `.env`.

## Start and stop the tunnel

On the Ubuntu server, with the API running, start:

```bash
cloudflared tunnel --url http://127.0.0.1:8000
```

Cloudflare prints a random `trycloudflare.com` hostname. Keep the `cloudflared` process running while testing. Press `Ctrl+C` in that terminal to stop the tunnel. The temporary hostname changes on a new run.

## Verification

- `GET /` through the temporary HTTPS URL returned `200` with the API welcome response.
- `GET /items` without an API key returned `401`, confirming that the protected endpoint still requires authentication.
- The API test suite passed all nine tests after the project was restored from backup.

No API key was included in this document. The authenticated `/items` route was not tested through the Quick Tunnel.

## Limitations

- The URL is temporary, public to anyone who has it, and has no uptime guarantee.
- Quick Tunnels are intended for development and testing, not production.
- This test does not configure custom DNS, a Cloudflare DNS zone, domain proxy settings, or a stable hostname.
- A registered domain is required for the standard Cloudflare full DNS setup. See [Quick Tunnel documentation](https://developers.cloudflare.com/tunnel/get-started/quick-tunnels/) and [Cloudflare full setup requirements](https://developers.cloudflare.com/dns/zone-setups/full-setup/setup/).
