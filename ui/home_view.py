import customtkinter as ctk
from ui.theme import Theme
from subjects import get_subjects
from chapters import get_chapters
from tasks import get_tasks
from flashcards import get_due_flashcards
import random

def load_tips():
    with open("tips.txt", "r", encoding="utf-8") as f:
        tips = [line.strip() for line in f if line.strip()]
    return tips

class HomeView(ctk.CTkFrame):
    def __init__(self, parent, user_id, theme=None, username="User",
                 on_subjects=None, on_tasks=None, on_flashcards=None):
        super().__init__(parent, fg_color=(theme or Theme).BG_COLOR)
        self.user_id = user_id
        self.theme = theme or Theme
        self.username = username
        self.on_subjects = on_subjects
        self.on_tasks = on_tasks
        self.on_flashcards = on_flashcards

        self.grid_rowconfigure(7, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._build_ui()

    def _build_ui(self):
        # ---- Greeting Header ----
        header = ctk.CTkLabel(self, text=f"👋 Welcome back, {self.username}!")
        self.theme.style_label(header, bold=True, size=24)
        header.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        subheader = ctk.CTkLabel(self, text="Here’s a quick look at your progress today:")
        self.theme.style_label(subheader, size=14)
        subheader.configure(text_color=self.theme.SUBTEXT)
        subheader.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="w")

        # ---- Stats Panel ----
        stats_frame = ctk.CTkFrame(self, corner_radius=12, fg_color=self.theme.FG_COLOR)
        stats_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="ew")
        stats_frame.grid_columnconfigure((0,1,2,3), weight=1)

        subjects = get_subjects(self.user_id)
        chapters = sum(len(get_chapters(self.user_id, sid)) for sid, _ in subjects)
        tasks = get_tasks(self.user_id, only_pending=True)
        flashcards_due = get_due_flashcards(self.user_id)

        stats = [
            ("📚 Subjects", len(subjects)),
            ("📖 Chapters", chapters),
            ("✅ Pending Tasks", len(tasks)),
            ("🃏 Flashcards Due", len(flashcards_due)),
        ]

        for i, (label, value) in enumerate(stats):
            stat_card = ctk.CTkFrame(stats_frame, corner_radius=8, fg_color=self.theme.BG_COLOR)
            stat_card.grid(row=0, column=i, padx=10, pady=10, sticky="nsew")

            lbl = ctk.CTkLabel(stat_card, text=label)
            self.theme.style_label(lbl, bold=True, size=14)
            lbl.pack(pady=(8,2))

            val_lbl = ctk.CTkLabel(stat_card, text=str(value))
            self.theme.style_label(val_lbl, bold=True, size=20)
            val_lbl.pack(pady=(0,8))

        # ---- Navigation Shortcuts ----
        nav_frame = ctk.CTkFrame(self, corner_radius=12, fg_color=self.theme.FG_COLOR)
        nav_frame.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="nsew")
        nav_frame.grid_columnconfigure((0,1,2), weight=1)

        subj_btn = ctk.CTkButton(nav_frame, text="📚 Go to Subjects",
                                 command=self.on_subjects)
        self.theme.style_button(subj_btn)
        subj_btn.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

        task_btn = ctk.CTkButton(nav_frame, text="✅ View Tasks",
                                 command=self.on_tasks)
        self.theme.style_button(task_btn)
        task_btn.grid(row=0, column=1, padx=20, pady=20, sticky="ew")

        flash_btn = ctk.CTkButton(nav_frame, text="🃏 Practice Flashcards",
                                  command=self.on_flashcards)
        self.theme.style_button(flash_btn)
        flash_btn.grid(row=0, column=2, padx=20, pady=20, sticky="ew")

        # ---- Daily Inspiration ----
        inspiration_frame = ctk.CTkFrame(self, corner_radius=12, fg_color=self.theme.FG_COLOR)
        inspiration_frame.grid(row=4, column=0, padx=20, pady=(0, 20), sticky="ew")

        tips = load_tips()

        inspo_lbl = ctk.CTkLabel(inspiration_frame,
                                 text=random.choice(tips),
                                 font=self.theme.BODY,
                                 text_color=self.theme.SUBTEXT)
        inspo_lbl.pack(padx=12, pady=12, anchor="w")

        # ---- Recent Tasks ----
        activity_frame = ctk.CTkFrame(self, corner_radius=12, fg_color=self.theme.FG_COLOR)
        activity_frame.grid(row=5, column=0, padx=20, pady=(0, 20), sticky="nsew")
        activity_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(activity_frame, text="🕒 Recent Tasks",
                     font=self.theme.SECTION, text_color=self.theme.TEXT_COLOR).grid(
            row=0, column=0, padx=12, pady=(12,6), sticky="w"
        )

        tasks_all = get_tasks(self.user_id)
        if not tasks_all:
            ctk.CTkLabel(activity_frame, text="No tasks yet.",
                        font=self.theme.BODY, text_color=self.theme.SUBTEXT).grid(
                row=1, column=0, padx=12, pady=6, sticky="w"
            )
        else:
            for i, task in enumerate(tasks_all[:3]):
                title = task["title"]
                completed = task["completed"]
                subj = task.get("subject_name") or "—"
                chap = task.get("chapter_name") or "—"

                # Build display text
                status_icon = "✔" if completed else "⏳"
                text = f"{status_icon} {title} | {subj}: {chap}"

                lbl = ctk.CTkLabel(activity_frame, text=text,
                                font=self.theme.BODY, text_color=self.theme.SUBTEXT)
                lbl.grid(row=i+1, column=0, padx=12, pady=2, sticky="w")


        # ---- Flashcards Due ----
        flash_frame = ctk.CTkFrame(self, corner_radius=12, fg_color=self.theme.FG_COLOR)
        flash_frame.grid(row=6, column=0, padx=20, pady=(0, 20), sticky="nsew")
        flash_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(flash_frame, text="🃏 Flashcards Due",
                     font=self.theme.SECTION, text_color=self.theme.TEXT_COLOR).grid(
            row=0, column=0, padx=12, pady=(12,6), sticky="w"
        )

        if not flashcards_due:
            ctk.CTkLabel(flash_frame, text="No flashcards due right now.",
                         font=self.theme.BODY, text_color=self.theme.SUBTEXT).grid(
                row=1, column=0, padx=12, pady=6, sticky="w"
            )
        else:
            for i, card in enumerate(flashcards_due[:3]):
                cid, front, back, next_date = card
                text = f"⏳ {front} (due {next_date})"
                lbl = ctk.CTkLabel(flash_frame, text=text,
                                   font=self.theme.BODY, text_color=self.theme.SUBTEXT)
                lbl.grid(row=i+1, column=0, padx=12, pady=2, sticky="w")
