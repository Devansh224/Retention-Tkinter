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
        self.sidebar = ctk.CTkFrame(self, fg_color=self.theme.FG_COLOR, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="ns")
        self.sidebar.grid_rowconfigure(99, weight=1)  # spacer

        # Header container
        header_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=20, pady=(20,10), sticky="w")

        logo_lbl = ctk.CTkLabel(header_frame, text="📖")
        self.theme.style_label(logo_lbl, bold=True, size=15)
        logo_lbl.pack(side="left")

        title_lbl = ctk.CTkLabel(header_frame, text="Retention")
        self.theme.style_label(title_lbl, bold=True, size=20)
        title_lbl.pack(side="left", padx=(6,0))

        # User info
        user_lbl = ctk.CTkLabel(self.sidebar, text=f"👤 {self.user['username']}")
        self.theme.style_label(user_lbl, size=14)
        user_lbl.configure(text_color=self.theme.SUBTEXT)
        user_lbl.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="w")

        # Navigation buttons
        home_btn = ctk.CTkButton(self.sidebar, text="🏠 Home", command=self.show_home)
        self.theme.style_button(home_btn)
        home_btn.grid(row=2, column=0, padx=12, pady=(0, 6), sticky="ew")

        btn_subjects = ctk.CTkButton(self.sidebar, text="📚 Subjects", command=self.show_subjects)
        self.theme.style_button(btn_subjects)
        btn_subjects.grid(row=3, column=0, padx=12, pady=6, sticky="ew")

        btn_flashcards = ctk.CTkButton(self.sidebar, text="📝 Flashcards", command=self.show_flashcards)
        self.theme.style_button(btn_flashcards)
        btn_flashcards.grid(row=4, column=0, padx=12, pady=6, sticky="ew")

        btn_tasks = ctk.CTkButton(self.sidebar, text="✅ Tasks", command=self.show_tasks)
        self.theme.style_button(btn_tasks)
        btn_tasks.grid(row=5, column=0, padx=12, pady=6, sticky="ew")

        # Spacer row
        ctk.CTkLabel(self.sidebar, text="").grid(row=99, column=0)

        # Footer
        btn_logout = ctk.CTkButton(self.sidebar, text="🚪 Logout", command=self.logout)
        self.theme.style_button(btn_logout)
        btn_logout.configure(fg_color=self.theme.ERROR, hover_color="#aa0000")
        btn_logout.grid(row=100, column=0, padx=12, pady=(0, 20), sticky="ew")


        # Main content
        self.main_frame = ctk.CTkFrame(self, fg_color=self.theme.BG_COLOR)
        self.main_frame.grid(row=0, column=1, sticky="nsew")

        self.show_home()

    def clear_main(self):
        for w in self.main_frame.winfo_children():
            w.destroy()

    def show_home(self):
        self.clear_main()
        HomeView(self.main_frame, self.user["id"], self.theme, username=self.user["username"], on_subjects=self.show_subjects, on_tasks=self.show_tasks, on_flashcards=self.show_flashcards).pack(fill="both", expand=True)

    def show_subjects(self):
        self.clear_main()
        SubjectsView(self.main_frame, self.user["id"], self.theme,
                     on_open_flashcards=self.show_flashcards).pack(fill="both", expand=True)

    def show_flashcards(self, subject_id=None, chapter_id=None):
        self.clear_main()
        FlashcardsView(self.main_frame, self.user["id"], self.theme,
                       subject_id=subject_id, chapter_id=chapter_id).pack(fill="both", expand=True)

    def show_tasks(self):
        self.clear_main()
        TasksView(self.main_frame, self.user["id"], self.theme).pack(fill="both", expand=True)
    
    def logout(self):
        self.destroy()
        from ui.login_ui import LoginUI
        LoginUI(self.master).pack(fill="both", expand=True)

