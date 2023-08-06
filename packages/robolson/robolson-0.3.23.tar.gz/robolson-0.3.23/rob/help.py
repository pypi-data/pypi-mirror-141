import glob

from pathlib import Path

_EXCLUSIONS = ["__init__.py"]

print("Available scripts (pass -h for CLI usage):")
print("\n".join([elem for elem in glob.glob("*.py") if elem not in _EXCLUSIONS]))
