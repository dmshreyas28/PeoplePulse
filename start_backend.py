"""Backend startup script with proper Python path configuration."""
import sys
import os
from pathlib import Path

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.absolute()

# Add necessary paths to sys.path
paths_to_add = [
    str(PROJECT_ROOT),
    str(PROJECT_ROOT / "backend"),
    str(PROJECT_ROOT / "ml" / "pipeline"),
]

for path in paths_to_add:
    if path not in sys.path:
        sys.path.insert(0, path)

print("=" * 60)
print("Starting PeoplePulse Backend Server")
print("=" * 60)
print(f"Project Root: {PROJECT_ROOT}")
print(f"Python Path configured:")
for p in paths_to_add:
    print(f"  - {p}")
print("=" * 60)
print()

# Now import and run uvicorn
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "backend.app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=[str(PROJECT_ROOT / "backend")]
    )
