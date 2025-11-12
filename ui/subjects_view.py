import customtkinter as ctk
from subjects import get_subjects, add_subject, delete_subject
from chapters import get_chapters, add_chapter, delete_chapter
from ui.theme import Theme

class SubjectsView(ctk.CTkFrame):
    def __init__(self, parent, user_id, theme, on_open_flashcards=None):
        super().__init__(parent, fg_color=theme.BG_COLOR)
        self.user_id = user_id
        self.theme = theme
        self.on_open_flashcards = on_open_flashcards

        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._build_ui()

    def _build_ui(self):
        # Title
        title = ctk.CTkLabel(self, text="Subjects")
        self.theme.style_label(title, bold=True, size=22)
        title.grid(row=0, column=0, padx=20, pady=(18, 8), sticky="n")

        # Subject entry
        subject_entry = ctk.CTkEntry(self, placeholder_text="New subject name")
        self.theme.style_entry(subject_entry)
        subject_entry.grid(row=1, column=0, padx=20, pady=(8, 4), sticky="ew")

        def on_add_subject():
            name = (subject_entry.get() or "").strip()
            if not name: return
            add_subject(self.user_id, name)
            self.refresh()

        add_btn = ctk.CTkButton(self, text="➕ Add Subject", command=on_add_subject)
        self.theme.style_button(add_btn)
        add_btn.grid(row=2, column=0, padx=20, pady=(0, 12), sticky="ew")

        # List frame
        self.list_frame = ctk.CTkScrollableFrame(self, corner_radius=10, fg_color=self.theme.FG_COLOR)
        self.list_frame.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.list_frame.grid_columnconfigure(0, weight=1)

        self.refresh()

    def refresh(self):
        for w in self.list_frame.winfo_children():
            w.destroy()

        subjects = get_subjects(self.user_id)
        if not subjects:
            lbl = ctk.CTkLabel(self.list_frame, text="No subjects yet.")
            self.theme.style_label(lbl, size=13)
            lbl.configure(text_color=self.theme.SUBTEXT)
            lbl.grid(row=0, column=0, padx=12, pady=8, sticky="w")
            return

        row = 0
        for sid, sname in subjects:
            card = ctk.CTkFrame(self.list_frame, corner_radius=8, fg_color=self.theme.BG_COLOR)
            card.grid(row=row, column=0, sticky="ew", padx=12, pady=6)
            row += 1

            subj_lbl = ctk.CTkLabel(card, text=sname)
            self.theme.style_label(subj_lbl, bold=True, size=18)
            subj_lbl.pack(side="left", padx=10, pady=6)

            def on_delete_subject(sid=sid):
                delete_subject(self.user_id, sid)
                self.refresh()

            del_btn = ctk.CTkButton(card, text="🗑", width=40, command=on_delete_subject)
            self.theme.style_button(del_btn)
            del_btn.configure(fg_color=self.theme.ERROR, hover_color="#aa0000")
            del_btn.pack(side="right", padx=10)

            chap_entry = ctk.CTkEntry(card, placeholder_text="New chapter")
            self.theme.style_entry(chap_entry)
            chap_entry.pack(fill="x", padx=10, pady=(0, 4))

            def on_add_chapter(sid=sid):
                name = (chap_entry.get() or "").strip()
                if not name: return
                add_chapter(self.user_id, sid, name)
                self.refresh()

            chap_btn = ctk.CTkButton(card, text="➕ Add Chapter", command=on_add_chapter)
            self.theme.style_button(chap_btn)
            chap_btn.pack(fill="x", padx=10, pady=(0, 6))

            # 🔥 FIX: loop chapters INSIDE subject loop
            for cid, cname in get_chapters(self.user_id, sid):
                row_chap = ctk.CTkFrame(card, fg_color="transparent")
                row_chap.pack(fill="x", padx=10, pady=2)

                # Chapter button (open flashcards)
                chap_btn = ctk.CTkButton(
                    row_chap,
                    text=f"📖 {cname}",
                    fg_color=self.theme.FG_COLOR,
                    command=lambda sid=sid, cid=cid: self._open_chap_flashcards(sid, cid)
                )
                self.theme.style_chapter_button(chap_btn)
                chap_btn.pack(side="left", fill="x", expand=True)

                # Chapter delete button
                def on_delete_chapter(cid=cid, sid=sid):
                    delete_chapter(self.user_id, sid, cid)
                    self.refresh()

                del_chap_btn = ctk.CTkButton(row_chap, text="🗑", width=40, command=on_delete_chapter)
                self.theme.style_button(del_chap_btn)
                del_chap_btn.configure(fg_color=self.theme.ERROR, hover_color="#aa0000")
                del_chap_btn.pack(side="right", padx=6)

    # ---- HELPER FUNCTION ----
    def _open_chap_flashcards(self, sid, cid):
        if self.on_open_flashcards:
            self.on_open_flashcards(sid, cid)

