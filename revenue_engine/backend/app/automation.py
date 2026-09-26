from dataclasses import dataclass
from .config import settings

@dataclass
class Draft:
    channel: str
    recipient: str
    subject: str
    body: str

class OutreachPolicy:
    def __init__(self, dry_run: bool|None=None):
        self.dry_run=settings.outreach_dry_run if dry_run is None else dry_run
    def validate(self, *, opted_out: bool, recipient: str|None):
        if opted_out: raise ValueError("Lead has opted out")
        if not recipient: raise ValueError("Recipient is required")
    def send(self, draft: Draft, *, opted_out: bool):
        self.validate(opted_out=opted_out,recipient=draft.recipient)
        if self.dry_run: return {"status":"DRY_RUN","draft":draft.__dict__}
        # Provider adapters should be injected here; no provider is called implicitly.
        raise RuntimeError("No outreach provider configured")

class AIActionPolicy:
    FORBIDDEN={"verify_payment","modify_financial_record","refund","change_security","bypass_opt_out","access_secret"}
    def allow(self, action: str):
        if action in self.FORBIDDEN: raise PermissionError(f"AI action blocked: {action}")
        return True
