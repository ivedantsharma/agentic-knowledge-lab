from enum import StrEnum

from pydantic import BaseModel, field_validator


class PlannerActionType(StrEnum):
    SEARCH = "search"
    STOP = "stop"


class PlannerAction(BaseModel):
    action_type: PlannerActionType
    query: str | None = None
    answer: str | None = None

    @field_validator("query", "answer")
    @classmethod
    def clean_optional_text(
        cls,
        value: str | None,
    ) -> str | None:
        if value is None:
            return None

        cleaned = value.strip()

        if not cleaned:
            raise ValueError(
                "planner action text must not be blank"
            )

        return cleaned

    def model_post_init(self, /, __context) -> None:
        if (
            self.action_type == PlannerActionType.SEARCH
            and self.query is None
        ):
            raise ValueError(
                "SEARCH action requires query"
            )

        if (
            self.action_type == PlannerActionType.STOP
            and self.answer is None
        ):
            raise ValueError(
                "STOP action requires answer"
            )
