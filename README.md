# secure-api-infrastructure
A hands-on DevOps project covering secure API development, AWS networking, Linux administration, and Cloudflare deployment.
## HTTPS Configuration

The API is deployed behind Nginx, which acts as a reverse proxy to FastAPI.

HTTPS is configured using a self-signed SSL certificate generated with OpenSSL.

### SSL Certificate

- Certificate: `/etc/nginx/ssl/secure-api.crt`
- Private key: `/etc/nginx/ssl/secure-api.key`
- Certificate validity: 365 days
- Certificate type: Self-signed RSA 2048-bit

### Nginx Configuration

- HTTP listens on port 80.
- HTTPS listens on port 443.
- Nginx forwards requests to FastAPI at `127.0.0.1:8000`.
- Maximum request body size: 1 MB.

### HTTPS Testing

Test the API:

    curl -k https://192.168.64.2/

Test API authentication:

    curl -k -i https://192.168.64.2/items

The protected endpoint should return HTTP 401 when no API key is supplied.

### Security Note

The self-signed certificate is intended for local development and testing inside the UTM Ubuntu virtual machine.

The `-k` option in curl disables certificate verification. Production deployments should use a trusted certificate authority, such as Let's Encrypt.

Never commit private SSL keys or API secrets to GitHub.


## Automated Deployment

The project includes a deployment script that automates the deployment process on the Ubuntu server.

Run:

```bash
./deployment/deploy.sh
