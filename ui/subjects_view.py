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

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._build_ui()

    def _build_ui(self):
        title = ctk.CTkLabel(self, text="Subjects")
        self.theme.style_label(title, bold=True, size=22)
        title.grid(row=0, column=0, padx=20, pady=(18, 8), sticky="n")

        subj_row = ctk.CTkFrame(self, fg_color="transparent")
        subj_row.grid(row=1, column=0, sticky="ew", padx=20, pady=(8, 12))
        subj_row.grid_columnconfigure(0, weight=1)

        self.subject_entry = ctk.CTkEntry(subj_row, placeholder_text="New subject name")
        self.theme.style_entry(self.subject_entry)
        self.subject_entry.grid(row=0, column=0, sticky="ew")
        self.subject_entry.bind("<Return>", lambda e: self._add_subject())

        add_subj_btn = ctk.CTkButton(subj_row, text="➕", width=40, command=self._add_subject)
        self.theme.style_button(add_subj_btn)
        add_subj_btn.grid(row=0, column=1, padx=(6,0))

        self.list_frame = ctk.CTkScrollableFrame(self, corner_radius=10, fg_color=self.theme.FG_COLOR)
        self.list_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.list_frame.grid_columnconfigure(0, weight=1)

        self.refresh()

    def refresh(self):
        for w in self.list_frame.winfo_children():
            w.destroy()

        subjects = get_subjects(self.user_id)
        self.subject_map = {sname: sid for sid, sname in subjects}  # ✅ FIX: rebuild subject map

        if not subjects:
            lbl = ctk.CTkLabel(self.list_frame, text="No subjects yet.")
            self.theme.style_label(lbl, size=13)
            lbl.configure(text_color=self.theme.SUBTEXT)
            lbl.grid(row=0, column=0, padx=12, pady=8, sticky="w")
            return

        row = 0
        for sid, sname in subjects:
            card = ctk.CTkFrame(self.list_frame, corner_radius=10, fg_color=self.theme.BG_COLOR)
            card.grid(row=row, column=0, sticky="ew", padx=12, pady=8)
            card.grid_columnconfigure(0, weight=1)
            row += 1

            header = ctk.CTkFrame(card, fg_color="transparent")
            header.grid(row=0, column=0, sticky="ew", padx=10, pady=(6,4))
            header.grid_columnconfigure(0, weight=1)

            subj_lbl = ctk.CTkLabel(header, text=sname)
            self.theme.style_label(subj_lbl, bold=True, size=18)
            subj_lbl.grid(row=0, column=0, sticky="w")

            def on_delete_subject(sid=sid):
                delete_subject(self.user_id, sid)
                self.refresh()

            del_btn = ctk.CTkButton(header, text="🗑", width=40, command=on_delete_subject)
            self.theme.style_button(del_btn)
            del_btn.configure(fg_color=self.theme.ERROR, hover_color="#aa0000")
            del_btn.grid(row=0, column=1, padx=6)

            chap_row = ctk.CTkFrame(card, fg_color="transparent")
            chap_row.grid(row=1, column=0, sticky="ew", padx=10, pady=(4,4))
            chap_row.grid_columnconfigure(0, weight=1)

            chap_entry = ctk.CTkEntry(chap_row, placeholder_text="New chapter")
            self.theme.style_entry(chap_entry)
            chap_entry.grid(row=0, column=0, sticky="ew")
            chap_entry.bind("<Return>", lambda e, sid=sid, entry=chap_entry: self._add_chapter(sid, entry))

            add_chap_btn = ctk.CTkButton(chap_row, text="➕", width=40,
                                         command=lambda sid=sid, entry=chap_entry: self._add_chapter(sid, entry))
            self.theme.style_button(add_chap_btn)
            add_chap_btn.grid(row=0, column=1, padx=(6,0))

            chap_list = ctk.CTkFrame(card, fg_color="transparent")
            chap_list.grid(row=2, column=0, sticky="ew", padx=10, pady=(0,6))
            chap_list.grid_columnconfigure(0, weight=1)

            for cid, cname in get_chapters(self.user_id, sid):
                row_chap = ctk.CTkFrame(chap_list, fg_color="transparent")
                row_chap.pack(fill="x", pady=2)

                chap_btn = ctk.CTkButton(
                    row_chap,
                    text=f"📖 {cname}",
                    fg_color=self.theme.FG_COLOR,
                    command=lambda sid=sid, cid=cid: self._open_chap_flashcards(sid, cid)
                )
                self.theme.style_chapter_button(chap_btn)
                chap_btn.pack(side="left", fill="x", expand=True)

                def on_delete_chapter(cid=cid, sid=sid):
                    delete_chapter(self.user_id, sid, cid)
                    self.refresh()

                del_chap_btn = ctk.CTkButton(row_chap, text="🗑", width=40, command=on_delete_chapter)
                self.theme.style_button(del_chap_btn)
                del_chap_btn.configure(fg_color=self.theme.ERROR, hover_color="#aa0000")
                del_chap_btn.pack(side="right", padx=6)

    def _add_subject(self):
        name = (self.subject_entry.get() or "").strip()
        if not name:
            return
        add_subject(self.user_id, name)
        self.subject_entry.delete(0, "end")
        self.refresh()

    def _add_chapter(self, sid, entry):
        name = (entry.get() or "").strip()
        if not name:
            return
        add_chapter(self.user_id, sid, name)
        entry.delete(0, "end")
        self.refresh()

    def _open_chap_flashcards(self, sid, cid):
        if self.on_open_flashcards:
            self.on_open_flashcards(sid, cid)

