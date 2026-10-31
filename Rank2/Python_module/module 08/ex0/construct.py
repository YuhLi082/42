import sys
import os
import site


def main() -> None:
    in_venv = sys.prefix != sys.base_prefix

    if not in_venv:
        print("MATRIX STATUS: You're still plugged in")
        print(f"Current Python: {sys.executable}")
        print("Virtual Environment: None detected")
        print("\nWARNING: You're in the global environment! "
              "The machines can see everything you install.")
        print("\nTo enter the construct, run:")
        print("\n  python3 -m venv matrix_env")
        if os.name == "nt":
            print("  matrix_env\\Scripts\\activate")
        else:
            print("  source matrix_env/bin/activate")
        print("\nThen run this program again.")

    else:
        print("MATRIX STATUS: Welcome to the construct")
        print(f"Current Python:  {sys.executable}")
        venv_path = os.environ.get("VIRTUAL_ENV", "Unknown")
        print(f"Virtual Environment: {os.path.basename(venv_path)}")
        print(f"Environment Path: {venv_path}")
        print("\nSUCCESS: You're in an isolated environment! "
              "Safe to install packages without affecting the global system.")
        print("\nPackage installation path:")
        try:
            paths = site.getsitepackages()
            if paths:
                for path in paths:
                    print(f"  {path}")
        except AttributeError:
            user_site = site.getusersitepackages()
            if user_site:
                print(f"  {user_site}")


if __name__ == "__main__":
    main()
