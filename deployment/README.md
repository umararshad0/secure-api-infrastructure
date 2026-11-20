# Ubuntu deployment

## Server preparation

Run `sudo deployment/setup-server.sh` to install prerequisite packages.
It does not configure the firewall, create secrets, or change Nginx or
systemd configuration.

## First deployment

1. Clone the repository as the `umar` user.
2. Create and activate a virtual environment:
   `python3 -m venv .venv`
3. Install dependencies:
   `.venv/bin/pip install -r requirements.txt`
4. Create `.env` from `.env.example`, set production values, and restrict
   access with `chmod 600 .env`.
5. Configure and verify the `secure-api` systemd service and Nginx reverse
   proxy for this server.
6. Run `deployment/deploy.sh`.

`deploy.sh` pulls `main`, installs dependencies, runs pytest, restarts the
service, and checks that systemd reports it active. It assumes the repository,
virtual environment, and service are already configured.

## Service management

- Status: `sudo systemctl status secure-api nginx --no-pager`
- Restart API: `sudo systemctl restart secure-api`
- API logs: `sudo journalctl -u secure-api -n 50 --no-pager`
- Check Nginx config: `sudo nginx -t`
- Reload Nginx: `sudo systemctl reload nginx`

## SSH hardening

Follow [`ssh-hardening.md`](ssh-hardening.md) to install an SSH public key,
verify a separate key-based login, and only then disable password and root SSH
login. Keep an existing session or VM console available until the new login is
verified.

## Backup

Run `deployment/backup.sh` to create and verify a backup under
`/home/umar/backups/`. The daily cron schedule uses `/bin/bash` and logs to
`/home/umar/backups/backup.log`; inspect it with `crontab -l`.

## Rollback

For a bad application commit, revert it on the development machine, push the
revert to `main`, then run `deployment/deploy.sh` on the server. This keeps
Git history intact and redeploys the reverted code. Check service status and
logs afterward. Do not use `git reset --hard` on the server as a routine
rollback method.

## Troubleshooting

- If deployment tests fail, fix the failure before restarting the service.
- If the service is inactive, inspect `journalctl -u secure-api`.
- If Nginx returns an error, run `sudo nginx -t` and inspect
  `/var/log/nginx/error.log`.
- For backup failures, inspect `/home/umar/backups/backup.log`.
