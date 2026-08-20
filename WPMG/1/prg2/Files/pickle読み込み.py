import pickle
from pathlib import Path
base_dir = Path(__file__).resolve().parent
target_path = base_dir / "WPMG/1/.wpmginfo"
print(target_path)


with open(target_path, "rb") as f:
    loaded_data = pickle.load(f)

print(loaded_data)