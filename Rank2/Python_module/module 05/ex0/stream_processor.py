from abc import ABC, abstractmethod
from typing import Any, List


class DataProcessor(ABC):
    """Abstract base class for all data processors."""

    @abstractmethod
    def process(self, data: Any) -> str:
        pass

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    def format_output(self, result: str) -> str:
        """Format the output string."""
        return f"Output: {result}"


class NumericProcessor(DataProcessor):
    """
    This processor handles numeric lists by calculating the sum and average
    of the values. It validates that the data can be summed and divided.
    """
    def validate(self, data: Any) -> bool:
        """
        Checks if the data is a non-empty collection of numbers by attempting
        to sum the values and divide by the length.
        _ instead of "avg" because there is no usage after
        Return True if data can be summed and divided (non-empty numbers),
        False otherwise (TypeError(input like ABC)
        or ZeroDivisionError(input no data))
        """
        try:
            total = sum(data)
            _ = total / len(data)
            return True
        except (TypeError, ZeroDivisionError):
            return False

    def process(self, data: Any) -> str:
        """
        Calculates the sum and average of the numeric values in the input data.
        """
        try:
            total = sum(data)
            avg = total / len(data)
            return (
                f"Processed {len(data)} numeric values, "
                f"sum={total}, avg={avg}"
            )
        except (TypeError, ZeroDivisionError):
            return "[ERROR] Numeric processing failed: invalid data"

    def format_output(self, result: str) -> str:
        """Format the output string."""
        base = super().format_output(result)
        return f"[NUMERIC] {base}"


class TextProcessor(DataProcessor):
    """Processes text string data."""
    def validate(self, data: Any) -> bool:
        """Validate if data is a string."""
        try:
            _ = data.split()
            return True
        except AttributeError:
            return False

    def process(self, data: Any) -> str:
        """Process text and return character and word count."""
        try:
            chars = len(data)
            words = len(data.split())
            return f"Processed text: {chars} characters, {words} words"
        except AttributeError:
            return "[ERROR] Text processing failed: invalid data"

    def format_output(self, result: str) -> str:
        """Format output with text prefix."""
        base = super().format_output(result)
        return f"[TEXT] {base}"


class LogProcessor(DataProcessor):
    """Processes log entry strings."""
    def validate(self, data: Any) -> bool:
        """
        Validate if data can be processed as a log entry.
        Checks if the data contains a colon (":") separator.
        """
        try:
            return ":" in data
        except TypeError:
            return False

    def process(self, data: Any) -> str:
        """
        Process log entry and detect log level.
        Splits the data at the first colon to extract level and message.
        level befor :,  _ is :, message after :
        """
        try:
            level, _, message = data.partition(":")
            level = level.strip()
            message = message.strip()
            if level == "ERROR":
                return f"[ALERT] ERROR level detected: {message}"
            return f"[{level}] {level} level detected: {message}"
        except (TypeError, AttributeError):
            return "[ERROR] Log processing failed: invalid data"

    def format_output(self, result: str) -> str:
        """
        Format the output with log processor identifier.
        Adds a [LOG] prefix to the base formatted output.
        """
        base = super().format_output(result)
        return f"[LOG] {base}"


def main() -> None:
    print("=== CODE NEXUS - DATA PROCESSOR FOUNDATION ===")

    print("\nInitializing Numeric Processor...")
    np = NumericProcessor()
    data1 = [1, 2, 3, 4, 5]
    print(f"Processing data: {data1}")
    if np.validate(data1):
        print("Validation: Numeric data verified")
        result = np.process(data1)
        print(np.format_output(result))
    print()

    print("Initializing Text Processor...")
    tp = TextProcessor()
    data2 = "Hello Nexus World"
    print(f'Processing data: "{data2}"')
    if tp.validate(data2):
        print("Validation: Text data verified")
        result = tp.process(data2)
        print(tp.format_output(result))
    print()

    print("Initializing Log Processor...")
    lp = LogProcessor()
    data3 = "ERROR: Connection timeout"
    print(f'Processing data: "{data3}"')
    if lp.validate(data3):
        print("Validation: Log entry verified")
        result = lp.process(data3)
        print(lp.format_output(result))
    print()

    print("=== Polymorphic Processing Demo ===")

    print("Processing multiple data types through same interface...")
    processors: List[DataProcessor] = [
        NumericProcessor(),
        TextProcessor(),
        LogProcessor(),
    ]

    test_data: List[Any] = [
        [1, 2, 3],
        "Hello World",
        "INFO: System ready",
    ]

    for i in range(len(processors)):
        result = processors[i].process(test_data[i])
        print(f"Result {i + 1}: {result}")

    print("Foundation systems online. Nexus ready for advanced streams.")


if __name__ == "__main__":
    main()
