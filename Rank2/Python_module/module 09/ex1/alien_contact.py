from datetime import datetime
from typing import Optional
from enum import Enum
from pydantic import BaseModel, Field, ValidationError, model_validator


class ContactType(str, Enum):
    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(..., min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(..., min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(..., ge=0.0, le=10.0)
    duration_minutes: int = Field(..., ge=1, le=1440)
    witness_count: int = Field(..., ge=1, le=100)
    message_received: Optional[str] = Field(default=None, max_length=500)
    is_verified: bool = Field(default=False)

    @model_validator(mode='after')
    def check_rules(self):
        if not self.contact_id.startswith('AC'):
            raise ValueError('ID must start with AC')
        if self.contact_type == ContactType.PHYSICAL \
                and not self.is_verified:
            raise ValueError('Physical contact must be verified')
        if self.contact_type == ContactType.TELEPATHIC \
                and self.witness_count < 3:
            raise ValueError('Telepathic needs at least 3 witnesses')
        if self.signal_strength > 7.0 and self.message_received is None:
            raise ValueError('Strong signal needs a message')
        return self


def main() -> None:
    c = AlienContact(
        contact_id="AC001",
        timestamp=datetime.now(),
        location="Earth",
        contact_type=ContactType.RADIO,
        signal_strength=5.0,
        duration_minutes=10,
        witness_count=2
    )
    print("Valid:", c.contact_id)

    try:
        AlienContact(
            contact_id="BAD01",
            timestamp=datetime.now(),
            location="Earth",
            contact_type=ContactType.RADIO,
            signal_strength=8.0,
            duration_minutes=10,
            witness_count=1
        )
    except ValidationError as e:
        print("Validation error: ")
        for error in e.errors():
            print(f"  - {error['msg']}")


if __name__ == "__main__":
    main()
