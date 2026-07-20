"""Shim so the synced studio modules (synastry.py, electional.py) find the
engines under their expected `engines` module name. Serverless-local, no
orchestrator paths."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import compute_sky as cs        # noqa: E402
import compute_factsheet as cf  # noqa: E402
import gen_wheel                # noqa: E402
