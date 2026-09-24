from __future__ import annotations

import argparse
import importlib.util
import shutil
import sys
from pathlib import Path


CASE = Path(__file__).resolve().parents[1]
FIXTURE = CASE / "fixture"
INSTRUCTIONS = CASE / "reviewer" / "REVIEW-INSTRUCTIONS.md"
RESPONSE = CASE / "reviewer" / "review-response.md"


def load_evidence_module():
    path = FIXTURE / "generate_evidence.py"
    spec = importlib.util.spec_from_file_location("case001_generate_evidence", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load evidence generator")
    module = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(FIXTURE))
    try:
        spec.loader.exec_module(module)
    finally:
        sys.path.pop(0)
    return module


def build(destination: Path) -> Path:
    if destination.exists():
        shutil.rmtree(destination)
    destination.mkdir(parents=True)

    shutil.copy2(CASE / "prompt.md", destination / "prompt.md")
    shutil.copytree(FIXTURE / "makor_fixture", destination / "fixture" / "makor_fixture")
    shutil.copytree(FIXTURE / "tests", destination / "fixture" / "tests")
    shutil.copy2(INSTRUCTIONS, destination / "REVIEW-INSTRUCTIONS.md")
    shutil.copy2(RESPONSE, destination / "review-response.md")

    module = load_evidence_module()
    system = module.build_incident()

    # write_bundle currently writes under the source fixture; copy the generated
    # result into the blinded bundle, then remove the source-side generated dir.
    source_evidence = module.write_bundle(system)
    shutil.copytree(source_evidence, destination / "evidence")
    shutil.rmtree(source_evidence)

    forbidden = [
        "private",
        "reference_solution",
        "oracle",
        "counterfactual",
        "SCORING-WALKTHROUGH",
        "HUMAN-WALKTHROUGH",
    ]
    lowered = [str(path.relative_to(destination)).lower() for path in destination.rglob("*")]
    for token in forbidden:
        if any(token.lower() in item for item in lowered):
            raise RuntimeError(f"forbidden reviewer-bundle path leaked: {token}")

    return destination


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "destination",
        nargs="?",
        default="/tmp/makorbench-case001-reviewer",
    )
    args = parser.parse_args()
    path = build(Path(args.destination))
    print(path)


if __name__ == "__main__":
    main()
