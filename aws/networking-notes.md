
# AWS Networking Notes

## Project
Secure API Infrastructure

## AWS Region
Europe (Stockholm) — eu-north-1

## VPC

- Name: secure-api-vpc
- CIDR: 10.0.0.0/16

## Subnets

### Public subnet
- Name: secure-api-public-a
- CIDR: 10.0.1.0/24
- Purpose: Hosts resources that require public internet connectivity.

### Private subnet
- Name: secure-api-private-a
- CIDR: 10.0.2.0/24
- Purpose: Hosts resources that should not be directly accessible from the internet.

Both subnets are in the same Availability Zone.

## Internet Gateway

- Name: secure-api-igw
- Attached to the VPC.
- Provides internet connectivity to resources in the public subnet when routing and security rules permit.

## Route tables

### Public route table
- Name: secure-api-public-rt
- Associated with the public subnet.
- Default route: 0.0.0.0/0 through the Internet Gateway.

### Private route table
- Name: secure-api-private-rt
- Associated with the private subnet.
- Contains the local VPC route only.
- No NAT Gateway was created.

## Network Access Control Lists (NACLs)

NACLs operate at the subnet level and are stateless. Both inbound and outbound rules must allow the required traffic.

## Security Groups

Security groups operate at the instance/network-interface level and are stateful.

The EC2 security group allows:
- SSH (22): restricted to the administrator's IP address.
- HTTP (80): public access.
- HTTPS (443): public access.
- Port 8000 is not publicly exposed.

## NAT Gateway

A NAT Gateway allows instances in private subnets to initiate outbound internet connections.

We studied its purpose but did not create one, avoiding unnecessary AWS charges.

## Cost and security considerations

- Avoid unnecessary NAT Gateways and other billable resources.
- Restrict SSH access to trusted IP addresses.
- Keep application and database resources private where possible.
- Review AWS Billing and Cost Explorer regularly.
