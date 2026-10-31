from datetime import datetime
from typing import List
from enum import Enum
from pydantic import BaseModel, Field, ValidationError, model_validator


class Rank(str, Enum):
    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(..., min_length=3, max_length=10)
    name: str = Field(..., min_length=2, max_length=50)
    rank: Rank
    age: int = Field(..., ge=18, le=80)
    specialization: str = Field(..., min_length=3, max_length=30)
    years_experience: int = Field(..., ge=0, le=50)
    is_active: bool = Field(default=True)


class SpaceMission(BaseModel):
    mission_id: str = Field(..., min_length=5, max_length=15)
    mission_name: str = Field(..., min_length=3, max_length=100)
    destination: str = Field(..., min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(..., ge=1, le=3650)
    crew: List[CrewMember] = Field(..., min_length=1, max_length=12)
    mission_status: str = Field(default="planned")
    budget_millions: float = Field(..., ge=1.0, le=10000.0)

    @model_validator(mode='after')
    def check_rules(self):
        if not self.mission_id.startswith('M'):
            raise ValueError('ID must start with M')
        if not any(m.rank in (Rank.COMMANDER, Rank.CAPTAIN)
                   for m in self.crew):
            raise ValueError('Must have Commander or Captain')
        if any(not m.is_active for m in self.crew):
            raise ValueError('All crew must be active')
        if self.duration_days > 365:
            exp = sum(1 for m in self.crew if m.years_experience >= 5)
            if exp / len(self.crew) < 0.5:
                raise ValueError('Long mission needs 50% experienced crew')
        return self


def main() -> None:
    c1 = CrewMember(
        member_id="C01",
        name="John",
        rank=Rank.COMMANDER,
        age=45,
        specialization="Pilot",
        years_experience=20
    )
    c2 = CrewMember(
        member_id="C02",
        name="Jane",
        rank=Rank.OFFICER,
        age=35,
        specialization="Engineer",
        years_experience=10
    )
    c3 = CrewMember(
        member_id="C03",
        name="Nick",
        rank=Rank.OFFICER,
        age=25,
        specialization="Engineer",
        years_experience=2
    )
    c4 = CrewMember(
        member_id="C04",
        name="Jack",
        rank=Rank.CADET,
        age=22,
        specialization="Science",
        years_experience=1
    )
    mission = SpaceMission(
        mission_id="M0001",
        mission_name="Mars Mission",
        destination="Mars",
        launch_date=datetime.now(),
        duration_days=100,
        crew=[c1, c2],
        budget_millions=100.0
    )
    print("Valid mission:", mission.mission_id)

    try:
        SpaceMission(
            mission_id="M0002",
            mission_name="Bad Mission",
            destination="Moon",
            launch_date=datetime.now(),
            duration_days=100,
            crew=[c3, c4],
            budget_millions=100.0
        )
    except ValidationError as e:
        print("Validation error:")
        for error in e.errors():
            print(f"  - {error['msg']}")


if __name__ == "__main__":
    main()
