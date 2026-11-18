#!/usr/bin/env bash
set -Eeuo pipefail

if [[ "$EUID" -ne 0 ]]; then
  echo "Run with sudo: sudo $0" >&2
  exit 1
fi

if ! grep -qi ubuntu /etc/os-release; then
  echo "This script is intended for Ubuntu Server." >&2
  exit 1
fi

export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y git nginx python3 python3-venv python3-pip fail2ban ufw

echo "Prerequisite packages installed."
echo "Review UFW rules and SSH access before enabling or changing the firewall."
