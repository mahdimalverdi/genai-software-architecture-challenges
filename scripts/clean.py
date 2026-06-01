from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
BUILD_DIR = ROOT / "build"

if BUILD_DIR.exists():
    shutil.rmtree(BUILD_DIR)
