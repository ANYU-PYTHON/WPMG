import customtkinter as ctk

root = ctk.CTk()
root.geometry('500x300')

progressbar = ctk.CTkProgressBar(root, width=200, height=8)
progressbar.place(relx=0.5, rely=0.5, anchor='center')
progressbar.set(0)

def update_progress():
    progress_value = progressbar.get()
    if progress_value < 1:
        progress_value += 0.1
        progressbar.set(progress_value)
        if progress_value >= 1:
            button.configure(text="終了")
    else:
        progress_value = 0
        progressbar.set(progress_value)
        button.configure(text="増やす")

button = ctk.CTkButton(root, text="増やす", command=update_progress)
button.place(relx=0.5, rely=0.8, anchor='center')

root.mainloop()