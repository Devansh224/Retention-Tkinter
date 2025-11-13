from ui.login_ui import LoginUI
from db_connection import initialise_db
import customtkinter as ctk

def main():
    initialise_db()

    root = ctk.CTk()
    root.title("Retention")
    root.geometry("1200x700")
    root.minsize(900, 600)

    # mount login frame inside root
    LoginUI(root).pack(fill="both", expand=True)

    root.mainloop()

if __name__ == "__main__":
    main()
