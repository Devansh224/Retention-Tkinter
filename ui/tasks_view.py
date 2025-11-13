import customtkinter as ctk
from ui.theme import Theme
from tasks import add_task, get_tasks, mark_task_done, delete_task
from subjects import get_subjects
from chapters import get_chapters

class TasksView(ctk.CTkFrame):
    def __init__(self, parent, user_id, theme=None):
        super().__init__(parent, fg_color=(theme or Theme).BG_COLOR)
        self.user_id = user_id
        self.theme = theme or Theme

        self.grid_rowconfigure(6, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._build_ui()

    def _build_ui(self):
        # Title
        title = ctk.CTkLabel(self, text="Tasks")
        self.theme.style_label(title, bold=True, size=22)
        title.grid(row=0, column=0, padx=20, pady=(18, 8), sticky="n")

        # Task title entry
        self.task_entry = ctk.CTkEntry(self, placeholder_text="Task title")
        self.theme.style_entry(self.task_entry)
        self.task_entry.grid(row=1, column=0, padx=20, pady=(4, 2), sticky="ew")

        # Description entry
        self.desc_entry = ctk.CTkEntry(self, placeholder_text="Description (optional)")
        self.theme.style_entry(self.desc_entry)
        self.desc_entry.grid(row=2, column=0, padx=20, pady=(2, 2), sticky="ew")

        # Subject dropdown
        subjects = get_subjects(self.user_id)
        self.subject_map = {sname: sid for sid, sname in subjects}
        self.subject_var = ctk.StringVar(value="Select Subject")
        self.subject_dropdown = ctk.CTkOptionMenu(self, variable=self.subject_var,
                                                 values=list(self.subject_map.keys()),
                                                 command=self._on_subject_change)
        self.theme.style_optionmenu(self.subject_dropdown)   # theme styling
        self.subject_dropdown.grid(row=3, column=0, padx=20, pady=(2,2), sticky="ew")

        # Chapter dropdown
        self.chapter_var = ctk.StringVar(value="Select Chapter")
        self.chapter_dropdown = ctk.CTkOptionMenu(self, variable=self.chapter_var, values=[])
        self.theme.style_optionmenu(self.chapter_dropdown)   # theme styling
        self.chapter_dropdown.grid(row=4, column=0, padx=20, pady=(2,2), sticky="ew")

        # Add button
        add_btn = ctk.CTkButton(self, text="➕ Add Task", command=self._add_task)
        self.theme.style_button(add_btn)
        add_btn.grid(row=5, column=0, padx=20, pady=(4, 8), sticky="ew")

        # Task list
        self.list_frame = ctk.CTkScrollableFrame(self, corner_radius=10, fg_color=self.theme.FG_COLOR)
        self.list_frame.grid(row=6, column=0, padx=20, pady=(0, 12), sticky="nsew")
        self.list_frame.grid_columnconfigure(0, weight=1)

        self.refresh()

    def _on_subject_change(self, subject_name):
        sid = self.subject_map.get(subject_name)
        if not sid: return
        chapters = get_chapters(self.user_id, sid)
        self.chapter_map = {cname: cid for cid, cname in chapters}
        self.chapter_dropdown.configure(values=list(self.chapter_map.keys()))
        self.chapter_var.set("Select Chapter")

    def _add_task(self):
        title = (self.task_entry.get() or "").strip()
        if not title: return
        desc = (self.desc_entry.get() or "").strip() or None

        subject_id = self.subject_map.get(self.subject_var.get())
        chapter_id = None
        if hasattr(self, "chapter_map"):
            chapter_id = self.chapter_map.get(self.chapter_var.get())

        add_task(self.user_id, title, description=desc, subject_id=subject_id, chapter_id=chapter_id)

        self.task_entry.delete(0, "end")
        self.desc_entry.delete(0, "end")
        self.refresh()

    def refresh(self):
        for w in self.list_frame.winfo_children():
            w.destroy()

        tasks = get_tasks(self.user_id)
        if not tasks:
            lbl = ctk.CTkLabel(self.list_frame, text="No tasks yet.")
            self.theme.style_label(lbl, size=13)
            lbl.configure(text_color=self.theme.SUBTEXT)
            lbl.grid(row=0, column=0, padx=12, pady=6, sticky="w")
            return

        row = 0
        for task in tasks:
            card = ctk.CTkFrame(self.list_frame, corner_radius=8, fg_color=self.theme.BG_COLOR)
            card.grid(row=row, column=0, sticky="ew", padx=12, pady=4)
            card.grid_columnconfigure(0, weight=1)
            row += 1

            # Title
            lbl = ctk.CTkLabel(card, text=task["title"])
            self.theme.style_label(lbl, size=14)
            lbl.grid(row=0, column=0, sticky="w", padx=10, pady=(4,0))

            # Info line
            info_parts = []
            if task["subject_name"]: info_parts.append(task["subject_name"])
            if task["chapter_name"]: info_parts.append(task["chapter_name"])
            if task["description"]: info_parts.append(task["description"])

            if info_parts:
                info_lbl = ctk.CTkLabel(card, text=" | ".join(info_parts), text_color=self.theme.SUBTEXT)
                self.theme.style_label(info_lbl, size=12)
                info_lbl.grid(row=1, column=0, sticky="w", padx=10, pady=(0,4))

            # Actions
            if task["completed"]:
                status_lbl = ctk.CTkLabel(card, text="✔ Done", text_color=self.theme.SUCCESS)
                status_lbl.grid(row=0, column=1, rowspan=2, sticky="e", padx=10)
            else:
                done_btn = ctk.CTkButton(card, text="✔", width=40,
                                        command=lambda t=task["id"]: self._mark_done(t))
                self.theme.style_button(done_btn)
                done_btn.grid(row=0, column=1, sticky="e", padx=6)

                del_btn = ctk.CTkButton(card, text="🗑", width=40,
                                        command=lambda t=task["id"]: self._delete_task(t))
                self.theme.style_button(del_btn)
                del_btn.configure(fg_color=self.theme.ERROR, hover_color="#aa0000")
                del_btn.grid(row=1, column=1, sticky="e", padx=6)

    def _mark_done(self, task_id):
        mark_task_done(task_id)
        self.refresh()

    def _delete_task(self, task_id):
        delete_task(task_id)
        self.refresh()
