import importlib
import sys


def main() -> None:
    print("LOADING STATUS: Loading programs...")
    print()
    print("Checking dependencies")

    diction = {
        "pandas": "Data manipulation ready",
        "numpy": "Numerical computation ready",
        "requests": "Network access ready",
        "matplotlib": "Visualization ready"
    }

    for name, description in diction.items():
        try:
            module = importlib.import_module(name)
            version = getattr(module, '__version__', 'Unknown')
            print(f"[OK] {name} ({version}) - {description}")
        except ImportError:
            print(f"Missing dependency: {name}")
            print(f"Please install it using 'pip install {name}'")
            sys.exit(1)
        except Exception as e:
            print(f"Error loading {name}: {e}")
            sys.exit(1)

    print()
    compare_managers()
    create_matrix()


def compare_managers() -> None:
    print("Dependency Management Comparison:")
    print("----------------------------------")
    print("pip (requirements.txt):")
    print("  Install : pip install -r requirements.txt")
    print("  pandas  >= 2.2, < 3.0")
    print("  numpy   >= 1.24, < 2.0")
    print("  matplot >= 3.7, < 4.0")
    print("  requests== 2.31.0")
    print("  Pros    : simple, built-in, universally supported")
    print("  Cons    : no lock file by default, no env management")
    print()
    print("Poetry (pyproject.toml):")
    print("  Install : poetry install")
    print("  pandas  ^2.0")
    print("  numpy   ^1.24")
    print("  matplot ^3.7")
    print("  requests^2.28")
    print("  Pros    : lock file, env management, build/publish tools")
    print("  Cons    : extra install required, slower resolution")
    print()


def create_matrix() -> None:
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt

    print("Analyzing Matrix data...")
    data = np.random.standard_normal(1000)
    print("Processing 1000 data points...")

    df = pd.DataFrame(data, columns=['Signal'])
    df['Moving_Average'] = df['Signal'].rolling(window=10).mean()

    plt.figure(figsize=(10, 6))
    plt.plot(data, alpha=0.5, label='Raw Signal')
    plt.plot(df['Moving_Average'], color='red', linewidth=2, label='Filtered')
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.legend()
    plt.grid(True, alpha=0.3)

    print("Generating visualization...")
    print()

    plt.title("Matrix Analysis")
    plt.savefig("matrix_analysis.png", dpi=100, bbox_inches="tight")
    plt.close()

    print("Analysis complete!")
    print("Results saved to: matrix_analysis.png")


if __name__ == "__main__":
    main()
