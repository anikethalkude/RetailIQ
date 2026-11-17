
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

scripts = [
    "prepare_data",
    "load_to_postgres",
    "explore_demand",
    "forecast_demand",
    "generate_forecast",
    "visualize_forecast",
    "load_forecast_to_postgres",
    "generate_business_insights",
    "load_business_insights_to_postgres"
]

print("\n===================================")
print("       RETAILIQ PIPELINE")
print("===================================\n")

for index, script in enumerate(scripts, start=1):

    print(f"\nSTEP {index}/{len(scripts)}: Running {script}.py")
    print("-----------------------------------", flush=True)

    try:
        subprocess.run(
            [sys.executable, "-m", f"src.{script}"],
            cwd=ROOT,
            check=True
        )

        print(f"SUCCESS: {script}.py", flush=True)

    except subprocess.CalledProcessError as error:
        print(f"\nPIPELINE FAILED at: {script}.py")
        print(f"Exit code: {error.returncode}")
        sys.exit(error.returncode)

print("\n===================================")
print(" RETAILIQ PIPELINE COMPLETED!")
print("===================================")
