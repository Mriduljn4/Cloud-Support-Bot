# TLS Certificate Expiry Runbook

## Trigger
Start this procedure when a certificate expiry alert fires with fewer than 14 days remaining, when clients report SSL handshake failures or browser security warnings, or when an automated renewal job shows a failure status.

## Response procedure
1. Confirm which certificate is affected and where it is in use. A single domain may have certificates in multiple locations: the ingress controller, the load balancer listener, a CDN origin, and internal service-to-service mTLS. Resolving one location without checking the others leaves the incident partially open.
2. Check whether automated renewal is configured and why it did not run. For Let's Encrypt certificates managed by cert-manager, inspect the `Certificate` and `CertificateRequest` Kubernetes resources for error conditions. For certificates managed outside the cluster, check the renewal job logs.
3. If automated renewal failed due to a DNS-01 or HTTP-01 challenge error, verify that the challenge solver has the correct permissions and that the expected DNS record or HTTP path is reachable from the validation server.
4. If the certificate has already expired and clients are receiving errors, prioritise getting a valid certificate deployed over diagnosing the root cause of the renewal failure.
5. After issuing a new certificate, verify that the serving endpoint is presenting the new certificate before closing the incident: `openssl s_client -connect <hostname>:443 -servername <hostname>` should show a `notAfter` date in the future.
6. Confirm that the renewed certificate covers all required subject alternative names (SANs). A certificate that is valid but missing a subdomain will produce errors for that specific subdomain only.
7. Review and fix the renewal automation to prevent recurrence. A successful emergency renewal does not close the problem if the automated process remains broken.

## Safety note
Do not delete a certificate secret from Kubernetes to force re-issuance unless you have confirmed the renewal process will succeed. Deleting a secret removes the current certificate immediately and leaves the service with no certificate until issuance completes.

## Escalation
Escalate to the platform team if cert-manager is not reconciling resources or if the ACME issuer account shows an error that requires re-registration. Escalate to the security team if the certificate was revoked rather than expired.
