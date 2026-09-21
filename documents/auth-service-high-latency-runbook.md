# Auth Service High Latency Runbook

## Trigger
Start this procedure when auth service p99 latency exceeds 500ms, when token validation errors begin appearing in downstream services, or when login and session refresh success rates drop below 99.5%.

## Service overview
The Auth Service handles login, token issuance, token validation, and session refresh for all internal and customer-facing applications. It reads from a PostgreSQL user database, caches session tokens in Redis, and calls an external identity provider for federated login flows. Degradation in any of these affects all services that validate tokens on every request.

## Response procedure
1. Determine whether latency is elevated across all auth endpoints or confined to a specific operation. Login failures that involve the external identity provider are isolated from token validation failures that involve Redis. Narrow the scope before investigating.
2. Check Redis cache hit rate for token validation. If the hit rate has dropped, token validation is falling through to the database on every request, which significantly increases latency and database load simultaneously.
3. Check the external identity provider status if federated login latency is elevated. Provider-side degradation cannot be resolved internally; confirm whether the provider has a status page incident before spending time investigating internal components.
4. Review recent changes to token expiry settings, signing key configuration, or session schema. Auth service latency increases are often caused by configuration changes that alter the processing path for every request.
5. Check for a login retry storm. A client that retries failed logins aggressively can amplify load on the auth service rapidly. Look for unusual request rates from a small number of source IPs or client versions.
6. If latency is caused by database query slowness, check for missing indexes on user lookup queries and confirm that connection pool exhaustion is not occurring.
7. Do not increase token expiry times to reduce validation frequency as an emergency measure without security team sign-off. Longer-lived tokens increase the exposure window for compromised credentials.

## Safety note
Do not disable token signature validation or skip expiry checks to reduce latency during an incident. These controls exist to prevent session hijacking and cannot be bypassed without creating a security vulnerability.

## Escalation
Escalate to the security team if the latency spike is accompanied by an unusual volume of authentication failures from unfamiliar IP ranges, which may indicate a credential-stuffing attack rather than a service issue.
