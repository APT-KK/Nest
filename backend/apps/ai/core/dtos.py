"""Data Transfer Objects (DTOs) for AI service communication."""

from pydantic import BaseModel


class AIQueryDTO(BaseModel):
    """Represent a query sent to the AI service."""

    text: str
    project_id: str


# LAYER 1: Router DTOs
class RouterIntentDTO(BaseModel):
    """Represent an intent for the AI Router."""

    label: str  # 'static' or 'dynamic'
    confidence: float


class ProjectPublicDTO(BaseModel):
    """Security Contract: Defines exactly what data is safe to expose.

    Mitigates OWASP LLM01 - Data Exposure, by preventing sensitive data leakage.
    """

    name: str
    maintainers: list[str]
    url: dict[str, str]  # URL with validation {"repo":}
    description: str

    # Strict mode: no extra fields
    class Config:
        """Pydantic configuration for strict validation."""

        extra = "ignore"


# Unified Response DTO
class AIResponseDTO(BaseModel):
    """Represent a response from the AI service."""

    answer: str
    source: str  # "cache", "statuc_lookup"
    intent: RouterIntentDTO | None = None
    show_manual_search_btn: bool = False  # The Escape Hatch for the AI
