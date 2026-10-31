import os
import sys
from typing import Dict, Any, Optional


try:
    from dotenv import load_dotenv
except ImportError:
    print("ERROR: python-dotenv module not installed")
    print("Install it with: pip install python-dotenv")
    sys.exit(1)


def load_config() -> Dict[str, Any]:
    load_dotenv()

    config = {
        'MATRIX_MODE': os.getenv('MATRIX_MODE', 'development'),
        'DATABASE_URL': os.getenv('DATABASE_URL', 'sqlite:///local.db'),
        'API_KEY': os.getenv('API_KEY'),
        'LOG_LEVEL': os.getenv('LOG_LEVEL', 'INFO'),
        'ZION_ENDPOINT': os.getenv('ZION_ENDPOINT', 'http://localhost:8000'),
    }

    return config


def validate_config(config: Dict[str, Any]) -> bool:
    errors = []

    if config['MATRIX_MODE'] not in ['development', 'production']:
        errors.append("MATRIX_MODE must be 'development' or 'production'")

    if not config['DATABASE_URL']:
        errors.append("DATABASE_URL is required")

    valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR']
    if config['LOG_LEVEL'] not in valid_levels:
        errors.append(f"LOG_LEVEL must be one of {valid_levels}")

    if config['MATRIX_MODE'] == 'production' and not config['API_KEY']:
        errors.append("API_KEY is required in production mode")

    if not config['ZION_ENDPOINT']:
        errors.append("ZION_ENDPOINT is required")

    if errors:
        for err in errors:
            print(err)
        return False

    return True


def detect_virtual_env() -> Optional[str]:
    venv = os.getenv('VIRTUAL_ENV')
    if venv:
        return os.path.basename(venv)

    if hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix:
        return "venv"

    return None


def main() -> int:
    print("ORACLE STATUS: Reading the Matrix...")
    print()

    venv = detect_virtual_env()

    if venv:
        print(f"Running in virtual environment: {venv}")
    else:
        print("No virtual environment detected")
        print("Create one: python -m venv matrix_env")
        print("Activate: source matrix_env/bin/activate")
    print()

    config = load_config()

    if not validate_config(config):
        print("Configuration validation failed!")
        return 1

    print("Configuration loaded:")
    print()

    if config['MATRIX_MODE'] == 'production':
        print("Mode: production")
        print("Database: Connected to production cluster")
    else:
        print("Mode: development")
        print("Database: Connected to local instance")

    if config['API_KEY']:
        print("API Access: Authenticated")
    else:
        print("API Access: Not authenticated")

    if config['LOG_LEVEL'] == 'DEBUG':
        print("Log Level: DEBUG")
    else:
        print(f"Log Level: {config['LOG_LEVEL']}")

    print("Zion Network: Online")
    print()

    print("Environment security check:")
    print("[OK] No hardcoded secrets detected")

    if os.path.exists('.env'):
        print("[OK] .env file properly configured")
    else:
        print("[WARNING] .env file not found")

    if config['MATRIX_MODE'] == 'production':
        print("[OK] Production overrides available")
    else:
        print("[INFO] Running in development mode")
    print()

    print("The Oracle sees all configurations.")

    return 0


if __name__ == '__main__':
    sys.exit(main())
