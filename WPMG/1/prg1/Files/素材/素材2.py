import customtkinter as ctk

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.geometry("5000x300")
root.title("Windowsマーク風ボタン（pack版）")
"""
# --- 全体フレーム ---
frame = ctk.CTkFrame(root)
frame.pack(expand=True)
"""
# --- 上段フレーム ---
top_frame = ctk.CTkFrame(root, fg_color="transparent")
top_frame.pack(pady=5)

# --- 下段フレーム ---
bottom_frame = ctk.CTkFrame(root, fg_color="transparent")
bottom_frame.pack(pady=5)

# --- 上段ボタン（左・右） ---
btn1 = ctk.CTkButton(top_frame, text="1", width=300, height=70)
btn1.pack(side="left", padx=5)

btn2 = ctk.CTkButton(top_frame, text="2", width=300, height=70)
btn2.pack(side="left", padx=5)

# --- 下段ボタン（左・右） ---
btn3 = ctk.CTkButton(bottom_frame, text="3", width=300, height=70)
btn3.pack(side="left", padx=5)

btn4 = ctk.CTkButton(bottom_frame, text="4", width=300, height=70)
btn4.pack(side="left", padx=5)

root.mainloop()

