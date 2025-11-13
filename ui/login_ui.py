import customtkinter as ctk
from PIL import Image
from ui.theme import Theme
from ui.register_ui import RegisterUI
from auth import authenticate_user
from ui.dashboard_ui import DashboardUI

class LoginUI(ctk.CTkFrame):
    def __init__(self, parent, theme=None):
        super().__init__(parent)
        Theme.set_theme()
        self.theme = theme or Theme

        # Grid: banner heavier than form
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
        form.grid_rowconfigure(7, weight=1)

        header = ctk.CTkLabel(form, text="Welcome Back")
        Theme.style_label(header, bold=True, size=26)
        header.grid(row=1, column=0, pady=(0, 50))

        self.username = ctk.CTkEntry(form, placeholder_text="Username")
        Theme.style_entry(self.username)
        self.username.grid(row=2, column=0, padx=20, pady=(0, 25), sticky="ew")

        self.password = ctk.CTkEntry(form, placeholder_text="Password", show="•")
        Theme.style_entry(self.password)
        self.password.grid(row=3, column=0, padx=20, pady=(0, 25), sticky="ew")

        login_btn = ctk.CTkButton(form, text="Login", command=self.on_login)
        Theme.style_button(login_btn)
        login_btn.grid(row=4, column=0, padx=20, pady=(0, 35), sticky="ew")

        self.status = ctk.CTkLabel(form, text="", font=Theme.SMALL, text_color=Theme.ERROR)
        self.status.grid(row=5, column=0)

        register_btn = ctk.CTkButton(form, text="Create Account", fg_color="transparent",
                                     text_color=Theme.ACCENT, hover_color=Theme.FG_COLOR,
                                     command=self.open_register)
        register_btn.grid(row=6, column=0, pady=(30, 0))

    def on_login(self):
        u, p = self.username.get().strip(), self.password.get()
        if not u or not p:
            self.status.configure(text="Please enter username and password.", text_color=Theme.ERROR)
            return

        ok, result = authenticate_user(u, p)
        if ok:
            self.status.configure(text="Login successful!", text_color=Theme.SUCCESS)

            # remove login widgets
            for w in self.winfo_children():
                w.destroy()

            # mount dashboard inside the same window
            dashboard = DashboardUI(self, result)  # theme defaults
            dashboard.pack(fill="both", expand=True)
        else:
            self.status.configure(text=result, text_color=Theme.ERROR)

    def open_register(self):
        self.pack_forget()  # hide login frame
        register_frame = RegisterUI(self.master)
        register_frame.pack(fill="both", expand=True)







