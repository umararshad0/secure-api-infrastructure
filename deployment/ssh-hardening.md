# SSH hardening for the Ubuntu lab VM

These steps use the non-root `umar` account. Keep the VM console or an existing
SSH session open until key-based login has been tested in a second terminal.
Do not disable password login until that test succeeds.

## 1. Create an SSH key on the Mac

In **Mac Terminal**, create an Ed25519 key if one does not already exist:

```bash
test -f ~/.ssh/id_ed25519.pub || ssh-keygen -t ed25519 -a 64 -C "umar@secure-api-vm"
```

Install the public key on the VM. This prompts for the current `umar` password;
it copies only the public key:

```bash
cat ~/.ssh/id_ed25519.pub | ssh umar@192.168.64.2 'umask 077; mkdir -p ~/.ssh; cat >> ~/.ssh/authorized_keys; chmod 700 ~/.ssh; chmod 600 ~/.ssh/authorized_keys'
```

Open a **second Mac Terminal window** and verify key login and sudo access:

```bash
ssh -o IdentitiesOnly=yes -i ~/.ssh/id_ed25519 umar@192.168.64.2
whoami
sudo -v
```

Proceed only if SSH connects without asking for the account password, `whoami`
prints `umar`, and `sudo -v` succeeds. Keep this verified session open.

## 2. Disable password and root SSH login

In the verified Ubuntu SSH session, create an SSH server drop-in:

```bash
sudo tee /etc/ssh/sshd_config.d/00-secure-api-hardening.conf >/dev/null <<'EOF'
PermitRootLogin no
PasswordAuthentication no
KbdInteractiveAuthentication no
PubkeyAuthentication yes
EOF
```

Validate the configuration before applying it, then reload SSH:

```bash
sudo sshd -t && sudo systemctl reload ssh
```

From a **third Mac Terminal window**, open a fresh key-based connection using
the command in step 1. Confirm `whoami` prints `umar` and `sudo -v` succeeds
before closing either existing session. If validation or reload fails, remove
the drop-in from the still-open session and reload SSH:

```bash
sudo rm /etc/ssh/sshd_config.d/00-secure-api-hardening.conf
sudo systemctl reload ssh
```

## Verification

From the Mac, confirm public-key authentication is accepted:

```bash
ssh -o BatchMode=yes -o IdentitiesOnly=yes -i ~/.ssh/id_ed25519 umar@192.168.64.2 'whoami'
```

Expected output is `umar`. Verify root and password authentication are disabled
on Ubuntu with:

```bash
sudo sshd -T | grep -E '^(permitrootlogin|passwordauthentication|kbdinteractiveauthentication|pubkeyauthentication) '
```

Expected settings are `permitrootlogin no`, `passwordauthentication no`,
`kbdinteractiveauthentication no`, and `pubkeyauthentication yes`. If the VM
uses another address, substitute the current address shown by `hostname -I`.
