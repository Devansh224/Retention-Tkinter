import customtkinter as ctk
from ui.home_view import HomeView
from ui.flashcards_view import FlashcardsView
from ui.subjects_view import SubjectsView
from ui.tasks_view import TasksView  
from ui.theme import Theme

class DashboardUI(ctk.CTkFrame):
    def __init__(self, parent, user, theme=None):
        super().__init__(parent)
        self.user = user
        self.theme = theme or Theme

        # Layout: nav + main
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)  # sidebar
        self.grid_columnconfigure(1, weight=1)  # main content

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, fg_color=self.theme.FG_COLOR, corner_radius=0, width=200)
        self.sidebar.grid(row=0, column=0, sticky="ns")
        self.sidebar.grid_rowconfigure(99, weight=1)

        # Header container
        header_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=20, pady=(20,10), sticky="w")

        logo_lbl = ctk.CTkLabel(header_frame, text="📖")
        self.theme.style_label(logo_lbl, bold=True, size=16)
        logo_lbl.pack(side="left")

        title_lbl = ctk.CTkLabel(header_frame, text="Retention")
        self.theme.style_label(title_lbl, bold=True, size=22)
        title_lbl.pack(side="left", padx=(6,0))

        # User info
        user_lbl = ctk.CTkLabel(self.sidebar, text=f"👤 {self.user['username']}")
        self.theme.style_label(user_lbl, size=14)
        user_lbl.configure(text_color=self.theme.SUBTEXT)
        user_lbl.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="w")

        # Navigation buttons
        self.home_btn = self._make_nav_button("🏠 Home", 2, self.show_home, active=True)
        self.btn_subjects = self._make_nav_button("📚 Subjects", 3, self.show_subjects)
        self.btn_flashcards = self._make_nav_button("📝 Flashcards", 4, self.show_flashcards)
        self.btn_tasks = self._make_nav_button("✅ Tasks", 5, self.show_tasks)

        # Divider before logout
        ctk.CTkFrame(self.sidebar, height=1, fg_color=self.theme.SUBTEXT).grid(
            row=98, column=0, sticky="ew", padx=12, pady=12
        )

        # Logout
        btn_logout = ctk.CTkButton(self.sidebar, text="🔖 Logout", command=self.logout, corner_radius=10)
        self.theme.style_button(btn_logout)
        btn_logout.configure(fg_color=self.theme.ERROR, hover_color="#aa0000")
        btn_logout.grid(row=100, column=0, padx=12, pady=(0, 20), sticky="ew")

        # Main content
        self.main_frame = ctk.CTkFrame(self, fg_color=self.theme.BG_COLOR)
        self.main_frame.grid(row=0, column=1, sticky="nsew")

        self.show_home()

    def _make_nav_button(self, text, row, command, active=False):
        """Helper to create polished nav buttons with hover + active highlight."""
        btn = ctk.CTkButton(self.sidebar, text=text, command=command, corner_radius=10)
        self.theme.style_button(btn)
        btn.configure(
            fg_color=self.theme.ACCENT if active else self.theme.FG_COLOR,
            hover_color=self.theme.HOVER_COLOR
        )
        btn.grid(row=row, column=0, padx=12, pady=6, sticky="ew")
        return btn

    def clear_main(self):
        for w in self.main_frame.winfo_children():
            w.destroy()

    def _set_active(self, active_btn):
        """Highlight the active nav button."""
        for btn in [self.home_btn, self.btn_subjects, self.btn_flashcards, self.btn_tasks]:
            btn.configure(fg_color=self.theme.FG_COLOR)
        active_btn.configure(fg_color=self.theme.ACCENT)

    def show_home(self):
        self.clear_main()
        self._set_active(self.home_btn)
        HomeView(
            self.main_frame,
            self.user["id"],
            self.theme,
            username=self.user["username"],
            on_subjects=self.show_subjects,
            on_tasks=self.show_tasks,
            on_flashcards=self.show_flashcards
        ).pack(fill="both", expand=True)

    def show_subjects(self):
        self.clear_main()
        self._set_active(self.btn_subjects)
        SubjectsView(
            self.main_frame,
            self.user["id"],
            self.theme,
            on_open_flashcards=self.show_flashcards
        ).pack(fill="both", expand=True)

    def show_flashcards(self, subject_id=None, chapter_id=None):
        self.clear_main()
        self._set_active(self.btn_flashcards)
        FlashcardsView(
            self.main_frame,
            self.user["id"],
            self.theme,
            subject_id=subject_id,
            chapter_id=chapter_id
        ).pack(fill="both", expand=True)

    def show_tasks(self):
        self.clear_main()
        self._set_active(self.btn_tasks)
        TasksView(self.main_frame, self.user["id"], self.theme).pack(fill="both", expand=True)
    
    def logout(self):
        self.destroy()
        from ui.login_ui import LoginUI
        LoginUI(self.master).pack(fill="both", expand=True)
