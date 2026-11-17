
# AWS Security Groups

## Project
Secure API Infrastructure

## Security Group

- Name: secure-api-ec2-sg
- Attached to: Secure API EC2 instance
- VPC: secure-api-vpc

## Inbound Rules

| Type | Protocol | Port | Source | Purpose |
|---|---|---|---|---|
| SSH | TCP | 22 | Administrator's IP (/32) | Secure server administration |
| HTTP | TCP | 80 | 0.0.0.0/0 | Public HTTP traffic |
| HTTPS | TCP | 443 | 0.0.0.0/0 | Permits HTTPS traffic |

## Outbound Rules

The default outbound rule permits outbound traffic.

## Security Decisions

- SSH access is restricted to the administrator's IP address.
- HTTP and HTTPS are permitted by the security group.
- Application port 8000 is not publicly exposed.
- Nginx acts as a reverse proxy to the FastAPI application.
- Security groups are stateful: return traffic is automatically permitted.

## Important HTTPS Note

Port 443 is permitted by the security group, but TLS/HTTPS has not yet been configured on the server. Domain and Cloudflare configuration remain future tasks.

## Security Group vs NACL

| Feature | Security Group | NACL |
|---|---|---|
| Level | Instance/network interface | Subnet |
| Stateful | Yes | No |
| Rules | Allow only | Allow and deny |
| Return traffic | Automatically allowed | Must be explicitly allowed |
