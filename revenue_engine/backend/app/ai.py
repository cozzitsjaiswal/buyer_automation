from .automation import AIActionPolicy

class AIService:
    """Provider-neutral AI boundary. Models may classify/draft/recommend, never settle money."""
    def __init__(self, provider=None):
        self.provider=provider
        self.policy=AIActionPolicy()
    def classify(self, text: str):
        if not text.strip(): return {"intent":"unknown","confidence":0}
        return {"intent":"general_inquiry","confidence":0.5}
    def draft_reply(self, context: str):
        self.policy.allow("draft_reply")
        return "Thanks for reaching out. We can review your business's digital presence and share the relevant package details."
    def recommend_package(self, digital_presence_score: int):
        return "growth_suite" if digital_presence_score < 50 else "digital_identity"
