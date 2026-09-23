# Security

- No secrets in source control.
- Use secure password hashing and RBAC in production.
- Verify webhook signatures.
- Enforce opt-out before every outbound message.
- Payment QR creation never marks an order paid.
- Payment verification must be explicit, idempotent and auditable.
- AI cannot verify payments, alter financial records, issue refunds, access secrets or bypass safeguards.
- Redact credentials from logs.
- Add rate limits and audit events to production endpoints.
