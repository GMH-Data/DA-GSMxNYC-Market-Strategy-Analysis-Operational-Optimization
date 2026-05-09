import json
import sys

# Set stdout to utf-8
sys.stdout.reconfigure(encoding="utf-8")


def extract_deep_dive_data(nb_path):
    with open(nb_path, "r", encoding="utf-8") as f:
        nb = json.load(f)

    for cell in nb["cells"]:
        if cell["cell_type"] == "code":
            source = "".join(cell["source"])

            # [2.2.1.2.A/B] Juno & Via
            if "[2.2.1.2.A]" in source or "[2.2.1.2.B]" in source:
                print("--- SECTION JUNO & VIA ---")
                for output in cell.get("outputs", []):
                    if output["output_type"] == "stream":
                        print("".join(output["text"]))
                    if (
                        output["output_type"] == "display_data"
                        and "text/plain" in output["data"]
                    ):
                        print("".join(output["data"]["text/plain"]))

            # [2.2.1.2.C] Fare per Mile
            if "[2.2.1.2.C]" in source:
                print("\n--- SECTION FARE PER MILE ---")
                for output in cell.get("outputs", []):
                    if output["output_type"] == "stream":
                        print("".join(output["text"]))
                    if (
                        output["output_type"] == "display_data"
                        and "text/plain" in output["data"]
                    ):
                        print("".join(output["data"]["text/plain"]))


extract_deep_dive_data("Analysis.ipynb")
