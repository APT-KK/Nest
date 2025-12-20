"""Project service for handling AI queries with intent routing."""

import logging

from backend.apps.ai.core.dtos import AIQueryDTO, AIResponseDTO, ProjectPublicDTO, RouterIntentDTO
from backend.apps.ai.router.intent import IntentRouter

logger = logging.getLogger(__name__)


# Ensure the class name is exactly 'ProjectService' (Case Sensitive)
class ProjectService:
    """Layer 2: Project Service.

    Role: Deterministic Source of Truth for Project Data.
    """

    def __init__(self):
        """Initialize ProjectService with Intent Router and thresholds."""
        # Initialized Intent Router
        self.router = IntentRouter()

        # Thresholds
        self.CONFIDENCE_THRESHOLD = 0.65
        self.FAIL_OPEN_TIMEOUT = 0.05  # 50ms

    async def process_query(self, query: AIQueryDTO) -> AIResponseDTO:
        """Orchestrate flow: Router -> Static Service OR Hybrid Retrieval."""
        intent_label = "dynamic"  # Default fail-open state
        confidence = 0.0

        # Router Intent Processing(With Fail-Open Circuit Breaker)
        try:
            router_result = self.router.get_intent(query.text)
            intent_label = router_result.get("intent", "dynamic").lower()
            confidence = router_result.get("confidence", 0.0)

            logger.info("Router Prediction: %s(%s)", intent_label, confidence)
        except Exception:  # noqa: BLE001 - Intentional fail-open policy
            logger.exception("Router Failed(Fail-Open Triggered)")
            intent_label = "dynamic"

        if confidence < self.CONFIDENCE_THRESHOLD and intent_label != "dynamic":
            return AIResponseDTO(
                answer=(
                    "I'm not sure if you want a specific fact or a general explanation. "
                    "Can you clarify?"
                ),
                source="system",
                intent=RouterIntentDTO(label=intent_label, confidence=confidence),
            )

        # Static Service Handling
        if intent_label == "static":
            # Call your deteministic lookup logic
            project_data = await self._fetch_static_project_data(query.text)

            if project_data:
                return AIResponseDTO(
                    answer=self._format_project_response(project_data),
                    source="static_lookup",
                    intent=RouterIntentDTO(label="static", confidence=confidence),
                    show_manual_search_btn=True,  # Escape Hatch
                )
            logger.info("Static lookup returned null. Failling back to Layer 3.")

        # Hybrid Retrieval Handling (Layer 3)
        return await self._execute_hybrid_retrieval(query.text)

    # Helper function
    async def _fetch_static_project_data(self, key: str) -> ProjectPublicDTO | None:
        """Fetch static project data by key."""
        # TODO(@user): Implement actual data retrieval logic
        # Return None if not found
        return None

    def _format_project_response(self, data: ProjectPublicDTO) -> str:
        """Format project data into a readable response string."""
        return (
            f"**{data.name}**: {data.description}\n"
            f"Maintainers: {','.join(data.maintainers) if data.maintainers else 'None'}"
        )

    async def _execute_hybrid_retrieval(self, text: str) -> AIResponseDTO:
        """Execute hybrid retrieval using RAG."""
        # Connection to Agent/LLM logic
        return AIResponseDTO(
            answer="[Generated Answer From Hybrid RAG]",
            source="hybrid_rag",
        )
