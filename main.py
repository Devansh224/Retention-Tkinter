from ui.login_ui import LoginUI
from db_connection import initialise_db
import customtkinter as ctk
from PIL import Image
def main():
    initialise_db()

    root = ctk.CTk()
    root.title("Retention")
    root.geometry("1200x700")
    root.minsize(900, 600)

    Image.open("assets/icon.png").save("assets/icon.ico")
    root.iconbitmap("assets/icon.ico") 

    # mount login frame inside root
    LoginUI(root).pack(fill="both", expand=True)

    root.mainloop()

if __name__ == "__main__":
    main()
