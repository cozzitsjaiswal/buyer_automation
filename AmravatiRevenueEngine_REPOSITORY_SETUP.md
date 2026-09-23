# Amravati Revenue Engine — Repository Setup

This repository plan is ready to be used for a fresh repository. The connected GitHub integration can create files, branches, commits, workflows, tests, and release configuration, but it cannot create a brand-new GitHub repository because the available connector does not expose repository-creation/administration APIs.

Recommended new repository name: `amravati-revenue-engine`

## Target contents
- FastAPI backend
- React frontend
- PostgreSQL + Redis
- Background workers
- AI abstraction layer
- Email/WhatsApp outreach adapters
- UPI QR/deep-link order flow with explicit payment verification
- PDF invoices via ReportLab
- Telegram telemetry
- Authentication/RBAC and audit logs
- Docker Compose
- GitHub Actions CI/CD
- Windows desktop/EXE packaging
- Complete installation and deployment guides
- Demo mode with dry-run outreach

## Windows EXE
Use PyInstaller for a desktop launcher/backend bundle and a Windows installer workflow. The EXE must read configuration from `.env`, default to demo/dry-run mode, never embed secrets, and provide a local browser dashboard.

## Safety-critical rules
1. QR generation never equals payment success.
2. Payment verification must be explicit and auditable.
3. Opted-out leads must never receive outreach.
4. AI cannot verify payments or change financial records.
5. No credentials in source control.
6. No fabricated lead or payment data.
