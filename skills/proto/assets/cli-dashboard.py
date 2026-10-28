"""SpecFlow CLI prototype template.

All scenarios are synthetic UI/flow demonstrations: this program does not read
files, call a model, inspect hardware, or execute destructive operations.
"""

import argparse
import sys
import time


class Colors:
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"


def print_banner() -> None:
    print(f"{Colors.HEADER}{'=' * 58}{Colors.ENDC}")
    print(f"{Colors.BOLD}SpecFlow CLI Prototype — SIMULATION ONLY{Colors.ENDC}")
    print("No files, model endpoints, hardware, or production services are accessed.\n")


def simulate_progress(label: str, duration: float = 0.4) -> None:
    """Animate a demo progress bar; it is not measured task progress."""
    steps = 10
    print(f"{Colors.BLUE}[SIMULATED]{Colors.ENDC} {label}")
    for step in range(steps + 1):
        percent = int(step / steps * 100)
        bar = "█" * step + "-" * (steps - step)
        sys.stdout.write(f"\r  |{Colors.CYAN}{bar}{Colors.ENDC}| {percent}%")
        sys.stdout.flush()
        time.sleep(duration / steps)
    print("\n")


def run_scenario(scenario: str) -> int:
    print_banner()

    if scenario == "happy":
        print(f"{Colors.GREEN}[SCENARIO] Synthetic extraction example{Colors.ENDC}")
        print("Input: fictional incident summary; confidence values below are illustrative only.")
        simulate_progress("Simulating parse and review steps")
        print("Example output: component=Inference Worker | evidence=synthetic fixture")
        print("SIMULATED SUCCESS — exit code 0")
        return 0

    if scenario == "confirm":
        print(f"{Colors.WARNING}[DEMO STATE] AWAITING_CONFIRM{Colors.ENDC}")
        print("A hypothetical destructive request needs a human decision.")
        print("This prototype will not execute the requested action.")
        choice = input("Simulate approval? [y/N]: ").strip().lower()
        if choice == "y":
            print("Approval state simulated; no data or external system was changed.")
            return 0
        print("Demo cancelled. Exit code 3")
        return 3

    print(f"{Colors.WARNING}[DEMO STATE] FALLBACK_ERROR{Colors.ENDC}")
    print("A preset failure path is being displayed; no resource exhaustion was measured.")
    print("SIMULATED FALLBACK — exit code 2")
    return 2


def main() -> int:
    parser = argparse.ArgumentParser(description="CLI workflow prototype (simulation only)")
    parser.add_argument(
        "--scenario",
        choices=["happy", "confirm", "fallback"],
        default="happy",
        help="Synthetic scenario to display",
    )
    args = parser.parse_args()
    try:
        return run_scenario(args.scenario)
    except KeyboardInterrupt:
        print("\nDemo interrupted. Exit code 130")
        return 130


if __name__ == "__main__":
    sys.exit(main())
