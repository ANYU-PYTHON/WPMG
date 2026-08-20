from pathlib import Path
import pickle
from datetime import datetime
def all_prg(usernum, num=None):
    base_dir = Path(__file__).resolve().parent
    target_path = base_dir / f"WPMG/{usernum}/.wpmginfo"

    with open(target_path, "rb") as f:
        loaded_data = pickle.load(f)

    result = [
        [
            name,
            datetime.strptime(data["lastdate"], "%Y%m%d.%H%M").strftime("%Y/%m/%d.%H:%M")
        ]
        for name, data in sorted(
            loaded_data.items(),
            key=lambda x: x[1]["lastdate"],
            reverse=True
        )
    ]

    if num:
        return result
    else:
        return result[:3]

print(all_prg(1))