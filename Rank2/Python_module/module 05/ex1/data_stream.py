from abc import ABC, abstractmethod
from typing import Any, List, Dict, Union, Optional


class DataStream(ABC):
    """Abstract base class for all data streams."""
    def __init__(self, stream_id: str) -> None:
        """Initialize the data stream with a unique stream ID."""
        self.stream_id = stream_id

    @abstractmethod
    def process_batch(self, data_batch: List[Any]) -> str:
        """Process a batch of data and return a result string."""
        pass

    def filter_data(self, data_batch: List[Any],
                    criteria: Optional[str] = None) -> List[Any]:
        """Filter data batch based on criteria.
        Returns all data if no criteria given."""
        if criteria is None:
            return data_batch
        return [d for d in data_batch if criteria in str(d)]

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        """Return basic stream statistics including stream ID."""
        return {"stream_id": self.stream_id}


class SensorStream(DataStream):
    """Handles environmental sensor data."""
    def __init__(self, stream_id: str) -> None:
        """Initialize sensor stream with stream ID."""
        super().__init__(stream_id)

    def process_batch(self, data_batch: List[Any]) -> str:
        """Process sensor data batch and return reading count."""
        try:
            if not isinstance(data_batch, list):
                raise TypeError("data_batch must be a list")

            count = len(data_batch)
            temps = []

            for d in data_batch:
                key, _, value = str(d).partition(":")
                if key == "temp":
                    temps.append(float(value))
            if temps:
                avg_temp = sum(temps) / len(temps)
                return (
                    f"Sensor analysis: {count} "
                    f"readings processed, avg temp: {avg_temp}°C"
                )
            return f"Sensor analysis: {count} readings processed"

        except (TypeError, ValueError) as e:
            return f"Error: {e}"

    def filter_data(self, data_batch: List[Any],
                    criteria: Optional[str] = None) -> List[Any]:
        """Filter data: if criteria provided,
        return only items containing criteria."""
        if criteria is None:
            return data_batch
        return [d for d in data_batch if isinstance(d, str) and criteria in d]

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        """Return sensor stream statistics including stream type."""
        stats = super().get_stats()
        stats["type"] = "Environmental Data"
        return stats


class TransactionStream(DataStream):
    """Handles financial transaction data."""
    def __init__(self, stream_id: str) -> None:
        """Initialize transaction stream with stream ID."""
        super().__init__(stream_id)

    def process_batch(self, data_batch: List[Any]) -> str:
        """Process transaction batch and
        return operation count and net flow."""
        try:
            if not isinstance(data_batch, list):
                raise TypeError("data_batch must be a list")

            count = len(data_batch)
            net = 0
            for d in data_batch:
                action, _, value = str(d).partition(":")
                if action == "buy":
                    net += int(value)
                elif action == "sell":
                    net -= int(value)
            sign = "+" if net >= 0 else ""
            return (
                f"Transaction analysis: {count} operations, "
                f"net flow: {sign}{net} units"
            )
        except (TypeError, ValueError) as e:
            return f"Error: {e}"

    def filter_data(self, data_batch: List[Any],
                    criteria: Optional[str] = None) -> List[Any]:
        """Filter transaction data by criteria using isinstance check."""
        if criteria is None:
            return data_batch
        return [d for d in data_batch if isinstance(d, str) and criteria in d]

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        """Return transaction stream statistics including stream type."""
        stats = super().get_stats()
        stats["type"] = "Financial Data"
        return stats


class EventStream(DataStream):
    """Handles System Events data."""
    def __init__(self, stream_id: str) -> None:
        """Initialize event stream with stream ID."""
        super().__init__(stream_id)

    def process_batch(self, data_batch: List[Any]) -> str:
        """Process event batch and return event count and error count."""
        try:
            if not isinstance(data_batch, list):
                raise TypeError("data_batch must be a list")

            count = len(data_batch)
            errors = 0
            for d in data_batch:
                if isinstance(d, str) and d.lower() == "error":
                    errors += 1
            return f"Event analysis: {count} events, {errors} error detected"
        except TypeError as e:
            return f"Error: {e}"

    def filter_data(self, data_batch: List[Any],
                    criteria: Optional[str] = None) -> List[Any]:
        """Filter System Events data by criteria using isinstance check."""
        if criteria is None:
            return data_batch
        return [d for d in data_batch if isinstance(d, str) and criteria in d]

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        """Return Event stream statistics including stream type."""
        stats = super().get_stats()
        stats["type"] = "System Events"
        return stats


class StreamProcessor:
    """Manages multiple streams polymorphically."""
    def __init__(self) -> None:
        """Initialize stream processor with empty stream list."""
        self.streams: List[DataStream] = []

    def add_stream(self, stream: DataStream) -> None:
        """Add stream in list"""
        self.streams.append(stream)

    def process_all(self, batches: List[List[Any]]) -> List[str]:
        """Process all streams with their respective batches."""
        results: List[str] = []
        for i in range(len(self.streams)):
            try:
                result = self.streams[i].process_batch(batches[i])
                results.append(result)
            except Exception as e:
                results.append(f"Error: {e}")
        return results


if __name__ == "__main__":
    print("=== CODE NEXUS - POLYMORPHIC STREAM SYSTEM ===")

    print("\nInitializing Sensor Stream...")
    sensor = SensorStream("SENSOR_001")
    stats = sensor.get_stats()
    print(f"Stream ID: {stats['stream_id']}, Type: {stats['type']}")
    batch1: List[Any] = ["temp:22.5", "humidity:65", "pressure:1013"]
    print(f"Processing sensor batch: {batch1}")
    print(sensor.process_batch(batch1))

    print("\nInitializing Transaction Stream...")
    trans = TransactionStream("TRANS_001")
    stats = trans.get_stats()
    print(f"Stream ID: {stats['stream_id']}, Type: {stats['type']}")
    batch2: List[Any] = ["buy:100", "sell:150", "buy:75"]
    print(f"Processing transaction batch: {batch2}")
    print(trans.process_batch(batch2))

    print("\nInitializing Event Stream...")
    event = EventStream("EVENT_001")
    stats = event.get_stats()
    print(f"Stream ID: {stats['stream_id']}, Type: {stats['type']}")
    batch3: List[Any] = ["login", "error", "logout"]
    print(f"Processing event batch: {batch3}")
    print(event.process_batch(batch3))

    print("\n=== Polymorphic Stream Processing ===")
    print("Processing mixed stream types through unified interface...")

    sp = StreamProcessor()
    sp.add_stream(SensorStream("S2"))
    sp.add_stream(TransactionStream("T2"))
    sp.add_stream(EventStream("E2"))

    mixed_batches: List[List[Any]] = [
        ["temp:20", "humidity:70"],
        ["buy:500", "sell:200", "buy:800", "sell:100"],
        ["login", "access", "logout"],
    ]

    print("\nBatch 1 Results:")
    results = sp.process_all(mixed_batches)
    for i in range(len(results)):
        print(f"- {results[i]}")

    print("\nStream filtering active: High-priority data only")
    filtered_sensor = sensor.filter_data(batch1, criteria="temp")
    filtered_trans = trans.filter_data(batch2, criteria="sell")
    print(f"Filtered results: {len(filtered_sensor)} critical sensor alerts, "
          f"{len(filtered_trans)} large transaction")

    print("\nAll streams processed successfully. Nexus throughput optimal.")
