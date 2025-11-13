import customtkinter as ctk
from PIL import Image
from ui.theme import Theme
from auth import register_user

class RegisterUI(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        Theme.set_theme()
        # self.title("Retention - Register")
        
        # self.geometry("1200x700")
        # self.minsize(900, 600)

        self.grid_columnconfigure(0, weight=3)   # banner ~65–70%
        self.grid_columnconfigure(1, weight=2)   # form ~30–35%
        self.grid_rowconfigure(0, weight=1)

        # Banner
        banner_img = Image.open("assets/banner.jpg").resize((700, 700))
        banner = ctk.CTkImage(light_image=banner_img, dark_image=banner_img, size=(700, 700))
        ctk.CTkLabel(self, image=banner, text="").grid(row=0, column=0, sticky="nsew")

        # Right form card
        form = ctk.CTkFrame(self, width=400, corner_radius=12)
        form.grid(row=0, column=1, sticky="nsew", padx=40, pady=40)
        form.grid_propagate(False)
        form.grid_columnconfigure(0, weight=1)
        form.grid_rowconfigure(0, weight=1)
        form.grid_rowconfigure(9, weight=1)

        header = ctk.CTkLabel(form, text="Create Account")
        Theme.style_label(header, bold=True, size=26)
        header.grid(row=1, column=0, pady=(0, 50))

        self.username = ctk.CTkEntry(form, placeholder_text="Username")
        Theme.style_entry(self.username)
        self.username.grid(row=2, column=0, padx=20, pady=(0, 25), sticky="ew")

        self.email = ctk.CTkEntry(form, placeholder_text="Email (optional)")
        Theme.style_entry(self.email)
        self.email.grid(row=3, column=0, padx=20, pady=(0, 25), sticky="ew")

        self.password = ctk.CTkEntry(form, placeholder_text="Password", show="•")
        Theme.style_entry(self.password)
        self.password.grid(row=4, column=0, padx=20, pady=(0, 25), sticky="ew")

        self.confirm = ctk.CTkEntry(form, placeholder_text="Confirm Password", show="•")
        Theme.style_entry(self.confirm)
        self.confirm.grid(row=5, column=0, padx=20, pady=(0, 35), sticky="ew")

        self.status = ctk.CTkLabel(form, text="", font=Theme.SMALL, text_color=Theme.ERROR)
        self.status.grid(row=6, column=0)

        register_btn = ctk.CTkButton(form, text="Register", command=self.on_register)
        Theme.style_button(register_btn)
        register_btn.grid(row=7, column=0, padx=20, pady=(0, 35), sticky="ew")

        signin_btn = ctk.CTkButton(form, text="Back to Login", fg_color="transparent",
                                   text_color=Theme.ACCENT, hover_color=Theme.FG_COLOR,
                                   command=self.close)
        signin_btn.grid(row=8, column=0, pady=(30, 0))

    def on_register(self):
        u = self.username.get().strip()
        e = self.email.get().strip() or None
        p = self.password.get()
        c = self.confirm.get()

        if not u or not p:
            self.status.configure(text="Username and password required.", text_color=Theme.ERROR)
            return
        if p != c:
            self.status.configure(text="Passwords do not match.", text_color=Theme.ERROR)
            return
        if len(p) < 6:
            self.status.configure(text="Use at least 6 characters for password.", text_color=Theme.ERROR)
            return

        ok, msg = register_user(u, p, e)
        if ok:
            self.status.configure(text=msg, text_color=Theme.SUCCESS)
            # Optional: auto-return to login after success
            # self.after(800, self.close)
        else:
            self.status.configure(text=msg, text_color=Theme.ERROR)

    def close(self):
        from ui.login_ui import LoginUI
        self.pack_forget()
        login_frame = LoginUI(self.parent)
        login_frame.pack(fill="both", expand=True)
