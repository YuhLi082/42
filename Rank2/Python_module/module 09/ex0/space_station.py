from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ValidationError


class SpaceStation(BaseModel):
    station_id: str = Field(..., min_length=3, max_length=10)
    name: str = Field(..., min_length=1, max_length=50)
    crew_size: int = Field(..., ge=1, le=20)
    power_level: float = Field(..., ge=0.0, le=100.0)
    oxygen_level: float = Field(..., ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = Field(default=True)
    notes: Optional[str] = Field(default=None, max_length=200)


def main() -> None:
    station = SpaceStation(
        station_id="LYH001",
        name="Li's Space Station",
        crew_size=6,
        power_level=85.5,
        oxygen_level=92.3,
        last_maintenance=datetime(2025, 1, 15, 10, 30, 0)
    )

    print("Valid station created:")
    print(f"  ID: {station.station_id}")
    print(f"  Name: {station.name}")
    print(f"  Crew: {station.crew_size}")
    print(f"  Power: {station.power_level}%")
    print(f"  Oxygen: {station.oxygen_level}%")
    print(f"  Status: "
          f"{'Operational' if station.is_operational else 'Non-operational'}")

    print("\nTrying invalid station (crew_size=25):")
    try:
        SpaceStation(
            station_id="01",
            name="Bad Station",
            crew_size=25,
            power_level=101.0,
            oxygen_level=101.0,
            last_maintenance=datetime.now()
        )
    except ValidationError as e:
        print("Validation error:")
        for error in e.errors():
            print(f"  - {error['msg']}")


if __name__ == "__main__":
    main()
