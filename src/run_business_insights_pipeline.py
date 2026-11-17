
from pathlib import Path
import subprocess
import sys

# RetailIQ project directory
ROOT = Path(__file__).resolve().parents[1]

# Scripts to execute in order
scripts = [
    "src/generate_business_insights.py",
    "src/load_business_insights_to_postgres.py"
]

print("=" * 55)
print("RETAILIQ - BUSINESS INSIGHTS AUTOMATION")
print("=" * 55)

for script in scripts:

    script_path = ROOT / script

    print(f"\nRunning: {script}")

    if not script_path.exists():
        raise FileNotFoundError(
            f"Script not found: {script_path}"
        )

    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=ROOT
    )

    if result.returncode != 0:
        print(f"\nPipeline stopped. Failed: {script}")
        sys.exit(result.returncode)

    print(f"Completed successfully: {script}")

print("\n" + "=" * 55)
print("RETAILIQ BUSINESS INSIGHTS PIPELINE COMPLETED!")
print("=" * 55)
