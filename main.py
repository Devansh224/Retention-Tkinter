from ui.login_ui import LoginUI
from db_connection import initialise_db
import customtkinter as ctk
# from PIL import Image
def main():
    # We import the function initialise_db here to run our databases
    initialise_db()

    # Creates a CTk root window - basically the project's MUST DOs
    root = ctk.CTk()
    root.title("Retention")
    root.geometry("1200x700")
    root.minsize(900, 600)

    # Image.open("assets/icon.png").save("assets/icon.ico")
    root.iconbitmap("assets/icon.ico") 

    '''
        Show login UI first, here pack means to load the widget to the window
        fill = "both" makes it expand in both directions
        expand = True makes it expand to fill any extra space
    '''
    LoginUI(root).pack(fill="both", expand=True)

    # Start the CTk event program
    root.mainloop()

if __name__ == "__main__":
    main()
