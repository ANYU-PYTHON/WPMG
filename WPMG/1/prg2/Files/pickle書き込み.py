import pickle
from pathlib import Path
from argon2 import PasswordHasher
# ユーザー認証Argon2へ切り替え
ph = PasswordHasher()
base_dir = Path(__file__).resolve().parent
target_path = base_dir / "WPMG/1/.wpmginfo"
print(target_path)
#data={'プロジェクト WPMG': {'lastdate': '20260725.2130', 'makedate': '20260725.2100'}, "プロジェクト1": {"lastdate": "20260724.2000", "makedate": "20260724.1900"}}

data = {'prg1': {'lastdate': '20260725.2130', 'makedate': '20260725.2100'}, 'prg2': {'lastdate': '20260724.2000', 'makedate': '20260724.1900'}, 'prg3': {'lastdate': '20260725.2200', 'makedate': '20260724.1859'}, "prg4": {'lastdate': '20260725.2200', 'makedate': '20260724.1859'}}
with open(target_path, "wb") as f:
    pickle.dump(data, f)
    #loaded_data = pickle.load(f)
    #f.write(ph.hash("test"))
#print(loaded_data)