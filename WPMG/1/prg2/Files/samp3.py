from argon2 import PasswordHasher
# ユーザー認証Argon2へ切り替え
ph = PasswordHasher()
pw1 = "test"
pw2 = "test"
pw = ph.hash(f"a24d{pw1};?HASH!!uiher853976{pw2}")
with open("admin.pw", "w") as f:
    f.write(pw)