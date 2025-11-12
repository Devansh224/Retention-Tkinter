from ui.login_ui import LoginUI
from db_connection import initialise_db

def main():
    initialise_db()
    app = LoginUI()
    app.mainloop()

if __name__ == "__main__":
    main()
