import customtkinter as ctk
from flashcards import add_flashcard, get_flashcards, get_due_flashcards, update_flashcard_review, delete_flashcard
from db_connection import create_connection
from subjects import get_subjects
from chapters import get_chapters
from datetime import timedelta

class FlashcardsView(ctk.CTkFrame):
    def __init__(self, parent, user_id, theme, subject_id=None, chapter_id=None):
        super().__init__(parent, fg_color=theme.BG_COLOR)
        self.user_id = user_id
        self.theme = theme
        self.subject_id = subject_id
        self.chapter_id = chapter_id
        self.flashcards = get_flashcards(user_id, subject_id, chapter_id)
        print("Fetched flashcards:", len(self.flashcards), "cards")

        # ---------------- DASHBOARD HEADER ----------------
        header = ctk.CTkFrame(self, corner_radius=10, fg_color=theme.FG_COLOR)
        header.pack(fill="x", padx=20, pady=(20,10))

        ctk.CTkLabel(header, text="Flashcards Dashboard",
                     font=theme.TITLE).pack(side="left", padx=10)

        self.practice_btn = ctk.CTkButton(
            header,
            text="Practice Today's Cards (0)",
            command=lambda: self._switch_to_review()
        )
        self.theme.style_button(self.practice_btn)
        self.practice_btn.pack(side="right", padx=10, pady=10)

        # ---------------- SUMMARY PANELS ----------------
        summary_frame = ctk.CTkFrame(self, corner_radius=10, fg_color=theme.FG_COLOR)
        summary_frame.pack(fill="x", padx=20, pady=(0,20))

        # Left summary
        self.left_panel = ctk.CTkFrame(summary_frame, fg_color="transparent")
        self.left_panel.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.streak_label = ctk.CTkLabel(self.left_panel, text="Streak: 0 days", 
                                         font=theme.BODY, text_color=theme.TEXT_COLOR)
        self.streak_label.pack(anchor="w", pady=4)

        self.cards_today_label = ctk.CTkLabel(self.left_panel, text="Cards studied today: 0", 
                                              font=theme.BODY, text_color=theme.TEXT_COLOR)
        self.cards_today_label.pack(anchor="w", pady=4)

        # Right summary
        self.right_panel = ctk.CTkFrame(summary_frame, fg_color="transparent")
        self.right_panel.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.performance_labels = {}

        # ---------------- TABVIEW ----------------
        self.tabs = ctk.CTkTabview(
            self,
            fg_color=self.theme.FG_COLOR,   # background of the tabview
            corner_radius=8
        )
        self.tabs.pack(fill="both", expand=True, padx=20, pady=20)

        # Style the tab buttons (active vs inactive)
        self.tabs._segmented_button.configure(
            corner_radius=8,
            fg_color=self.theme.FG_COLOR,          # inactive tab background
            selected_color=self.theme.ACCENT,      # active tab background (bluish accent)
            selected_hover_color=self.theme.HOVER_COLOR,  # hover on active tab
            unselected_color=self.theme.FG_COLOR,  # inactive tab background
            unselected_hover_color="#2a2a2a",      # hover on inactive tab
            text_color=self.theme.TEXT_COLOR       # text color for all tabs
        )

        # Add tabs
        self.create_tab = self.tabs.add("➕ Create")
        self.review_tab = self.tabs.add("📖 Review")

        # Make tab content match background
        self.create_tab.configure(fg_color=self.theme.BG_COLOR)
        self.review_tab.configure(fg_color=self.theme.BG_COLOR)

        self.tabs.pack(fill="both", expand=True, padx=20, pady=20)  # make sure it shows up


        self._build_create_tab()
        self._build_review_tab()

        self._update_dashboard()

    def _switch_to_review(self):
        self.tabs.set("📖 Review")
        self._load_next_card()

    def _update_dashboard(self):
        conn = create_connection(); cur = conn.cursor()

        due_cards = get_due_flashcards(self.user_id, self.subject_id, self.chapter_id)
        self.practice_btn.configure(text=f"Practice Today's Cards ({len(due_cards)})")

        cur.execute("""
            SELECT COUNT(*) FROM flashcards
            WHERE user_id=%s AND DATE(updated_at)=CURDATE()
        """, (self.user_id,))
        studied_today = cur.fetchone()[0]
        self.cards_today_label.configure(text=f"Cards studied today: {studied_today}")

        cur.execute("""
            SELECT s.name
            FROM subjects s
            JOIN flashcards f ON f.subject_id = s.id
            WHERE f.user_id=%s AND DATE(f.updated_at)=CURDATE()
            GROUP BY s.name
        """, (self.user_id,))
        subjects_today = [row[0] for row in cur.fetchall()]
        cur.close(); conn.close()

        subjects_text = ", ".join(subjects_today) if subjects_today else "None yet"
        self.streak_label.configure(text="Streak: 0 days")

        for widget in self.right_panel.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.right_panel, text="Subjects Studied Today",
                    font=self.theme.SECTION, text_color=self.theme.TEXT_COLOR).pack(anchor="w", pady=(0,6))
        ctk.CTkLabel(self.right_panel, text=subjects_text,
                    font=self.theme.BODY, text_color=self.theme.TEXT_COLOR).pack(anchor="w", pady=2)

    def _format_interval(self, outcome: str) -> str:
        intervals = {
            "forgot": timedelta(days=1),
            "partial": timedelta(days=2),
            "effort": timedelta(days=3),
            "easy": timedelta(days=5),
            "skip": timedelta(hours=1)
        }
        interval = intervals.get(outcome)
        if not interval:
            return ""
        # Format nicely
        if interval.days > 0:
            return f"{interval.days}d"
        else:
            hours = interval.seconds // 3600
            minutes = (interval.seconds % 3600) // 60
            if hours > 0:
                return f"{hours}h"
            else:
                return f"{minutes}m"

    
    
    # ---------------- CREATE TAB ----------------
    def _build_create_tab(self):
        # Wrap entire tab in a scrollable frame
        create_scroll = ctk.CTkScrollableFrame(self.create_tab, fg_color="transparent")
        create_scroll.pack(fill="both", expand=True)

        subjects = get_subjects(self.user_id)
        subject_names = [s[1] for s in subjects]
        self.subject_map = {s[1]: s[0] for s in subjects}

        self.subject_dropdown = ctk.CTkOptionMenu(
            create_scroll,
            values=subject_names,
            command=self._on_subject_change
        )
        self.theme.style_optionmenu(self.subject_dropdown)
        self.subject_dropdown.pack(fill="x", padx=20, pady=(20, 10))

        self.chapter_dropdown = ctk.CTkOptionMenu(
            create_scroll,
            values=["(none)"],
            command=self._on_chapter_change
        )
        self.theme.style_optionmenu(self.chapter_dropdown)
        self.chapter_dropdown.pack(fill="x", padx=20, pady=(0, 10))

        self.cards_frame = ctk.CTkScrollableFrame(
            create_scroll, corner_radius=8, fg_color=self.theme.FG_COLOR
        )
        self.cards_frame.pack(fill="both", expand=True, padx=20, pady=10)

        if self.subject_id:
            for name, sid in self.subject_map.items():
                if sid == self.subject_id:
                    self.subject_dropdown.set(name)
                    self._on_subject_change(name)
                    if self.chapter_id:
                        chapters = get_chapters(self.user_id, self.subject_id)
                        for cid, cname in chapters:
                            if cid == self.chapter_id:
                                self.chapter_dropdown.set(cname)
                                break
                    break

        self.front_entry = ctk.CTkEntry(create_scroll, placeholder_text="Front (Question)")
        self.theme.style_entry(self.front_entry)
        self.front_entry.pack(fill="x", padx=20, pady=(10, 6))

        self.back_entry = ctk.CTkEntry(create_scroll, placeholder_text="Back (Answer)")
        self.theme.style_entry(self.back_entry)
        self.back_entry.pack(fill="x", padx=20, pady=(0, 6))

        self.tags_entry = ctk.CTkEntry(create_scroll, placeholder_text="Tags (optional)")
        self.theme.style_entry(self.tags_entry)
        self.tags_entry.pack(fill="x", padx=20, pady=(0, 10))

        def on_add():
            subj_choice = self.subject_dropdown.get()
            chap_choice = self.chapter_dropdown.get()
            subject_id = self.subject_map.get(subj_choice)
            chapter_id = None
            if chap_choice != "(none)":
                chapters = get_chapters(self.user_id, subject_id)
                for cid, cname in chapters:
                    if cname == chap_choice:
                        chapter_id = cid
                        break

            front, back, tags = self.front_entry.get(), self.back_entry.get(), self.tags_entry.get()
            if not front or not back:
                return
            add_flashcard(self.user_id, subject_id, chapter_id, front, back, tags)

            self.front_entry.delete(0, "end")
            self.back_entry.delete(0, "end")
            self.tags_entry.delete(0, "end")

            self._refresh_flashcards(subject_id, chapter_id)
            self._load_next_card()

        add_btn = ctk.CTkButton(create_scroll, text="Save Flashcard", command=on_add)
        self.theme.style_button(add_btn)
        add_btn.pack(pady=20)

        self._refresh_flashcards(self.subject_id, self.chapter_id)

    # ...existing code...
        
    def _delete_flashcard(self, card_id):
        delete_flashcard(card_id)
        self._refresh_flashcards(self.subject_id, self.chapter_id)
        self._update_dashboard()
        
    def _refresh_flashcards(self, subject_id=None, chapter_id=None):
        for w in self.cards_frame.winfo_children():
            w.destroy()

        cards = get_flashcards(self.user_id, subject_id or self.subject_id, chapter_id or self.chapter_id)
        if not cards:
            ctk.CTkLabel(self.cards_frame, text="No flashcards yet.", 
                        text_color=self.theme.SUBTEXT, font=self.theme.BODY).pack(pady=10)
            return

        for cid, front, back, next_date, tags in cards:
            card = ctk.CTkFrame(self.cards_frame, corner_radius=6, fg_color=self.theme.BG_COLOR)
            card.pack(fill="x", padx=10, pady=6)

            ctk.CTkLabel(card, text=f"Q: {front}", font=self.theme.SUBHEADER,
                        text_color=self.theme.TEXT_COLOR).pack(anchor="w", padx=10, pady=(4,0))
            ctk.CTkLabel(card, text=f"A: {back}", font=self.theme.BODY,
                        text_color=self.theme.TEXT_COLOR).pack(anchor="w", padx=10, pady=(0,4)) 
            tag_text = tags if tags else "No Tags"
            ctk.CTkLabel(card, text=f"🏷 {tag_text}", font=self.theme.SMALL,
                 text_color=self.theme.SUBTEXT).pack(anchor="w", padx=10, pady=(0,4))
            ctk.CTkLabel(card, text=f"Next Review: {next_date}", font=self.theme.SMALL, 
                        text_color=self.theme.SUBTEXT).pack(anchor="w", padx=10, pady=(0,4))
        
            del_btn = ctk.CTkButton(card, text="🗑 Delete", command=lambda id=cid: self._delete_flashcard(id))
            self.theme.style_button(del_btn)
            del_btn.pack(side="right", padx=10, pady=4)

    def _on_subject_change(self, selected_name: str):
        self.subject_id = self.subject_map.get(selected_name)
        chapters = get_chapters(self.user_id, self.subject_id) if self.subject_id else []
        if chapters:
            self.chapter_dropdown.configure(values=[c[1] for c in chapters])
            # If we already have a chapter_id, set it; else default to "(none)"
            if self.chapter_id:
                for cid, cname in chapters:
                    if cid == self.chapter_id:
                        self.chapter_dropdown.set(cname)
                        break
            else:
                self.chapter_dropdown.set("(none)")
        else:
            self.chapter_dropdown.configure(values=["(none)"])
            self.chapter_dropdown.set("(none)")
            self.chapter_id = None

        self._refresh_flashcards(self.subject_id, self.chapter_id)
        self._update_dashboard()


    def _on_chapter_change(self, selected_name: str):
        if not self.subject_id:
            self.chapter_id = None
        else:
            chapters = get_chapters(self.user_id, self.subject_id)
            self.chapter_id = None
            for cid, cname in chapters:
                if cname == selected_name:
                    self.chapter_id = cid
                    break

        self._refresh_flashcards(self.subject_id, self.chapter_id)
        self._update_dashboard()

    # ...existing code...

    # ---------------- REVIEW TAB ----------------
    def _build_review_tab(self):
        stats_frame = ctk.CTkFrame(self.review_tab, fg_color=self.theme.FG_COLOR, corner_radius=10)
        stats_frame.pack(fill="x", padx=20, pady=(20,10))

        # Get subjects for dropdown
        subjects = get_subjects(self.user_id)
        subject_names = [s[1] for s in subjects]
        self.subject_map = {s[1]: s[0] for s in subjects}

        # Current due cards count
        due_cards = get_due_flashcards(self.user_id, self.subject_id, self.chapter_id)
        total_due = len(due_cards)

        subj_name = "All Subjects"
        if self.subject_id:
            subj_name = next((s[1] for s in subjects if s[0] == self.subject_id), subj_name)

        # Stats labels
        self.due_today_label = ctk.CTkLabel(
            stats_frame,
            text=f"📊 Due Today: {total_due}",
            font=self.theme.SECTION,
            text_color=self.theme.TEXT_COLOR
        )
        self.due_today_label.pack(side="left", padx=10, pady=10)

        # Subject filter dropdown
        self.review_subject_dropdown = ctk.CTkOptionMenu(
            stats_frame,
            values=["All Subjects"] + subject_names,
            command=self._on_review_subject_change
        )
        self.theme.style_optionmenu(self.review_subject_dropdown)
        self.review_subject_dropdown.pack(side="right", padx=10, pady=10)

        # Default selection
        if self.subject_id:
            for name, sid in self.subject_map.items():
                if sid == self.subject_id:
                    self.review_subject_dropdown.set(name)
                    break
        else:
            self.review_subject_dropdown.set("All Subjects")

        # Review frame
        self.review_frame = ctk.CTkFrame(self.review_tab, corner_radius=8, fg_color=self.theme.FG_COLOR)
        self.review_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Buttons frame
        btn_frame = ctk.CTkFrame(self.review_tab, fg_color="transparent")
        btn_frame.pack(pady=20)

        # Outcome intervals
        intervals = {
            "forgot": timedelta(days=1),
            "partial": timedelta(days=2),
            "effort": timedelta(days=3),
            "easy": timedelta(days=5),
            "skip": timedelta(hours=1)
        }

        outcomes = [
            ("❌ Forgot", "forgot"),
            ("🤔 Partial", "partial"),
            ("💪 Effort", "effort"),
            ("✅ Easy", "easy"),
            ("⏭ Skip", "skip"),
        ]

        for text, outcome in outcomes:
            interval = intervals[outcome]
            if interval.days > 0:
                interval_text = f"{interval.days}d"
            else:
                hours = interval.seconds // 3600
                minutes = (interval.seconds % 3600) // 60
                interval_text = f"{hours}h" if hours else f"{minutes}m"

            btn = ctk.CTkButton(
                btn_frame,
                text=f"{text} ({interval_text})",
                command=lambda o=outcome: self._handle_review(o)
            )
            self.theme.style_button(btn)
            btn.pack(side="left", padx=6)

        self._load_next_card()

    def _load_next_card(self):
        if self.subject_id:
            due = get_due_flashcards(self.user_id, self.subject_id, self.chapter_id)
        else:
            due = get_due_flashcards(self.user_id)

        for w in self.review_frame.winfo_children():
            w.destroy()

        if not due:
            self.current_card = None
            ctk.CTkLabel(self.review_frame, text="No cards due",
                        font=self.theme.SUBHEADER, text_color=self.theme.TEXT_COLOR, 
                        wraplength=600, justify="center").pack(pady=40)
        else:
            self.current_card = due[0]
            card_id, front, back, next_date = self.current_card[:4]
            subject_name = self.current_card[4] if len(self.current_card) > 4 else None
            chapter_name = self.current_card[5] if len(self.current_card) > 5 else None
            tags = self.current_card[6] if len(self.current_card) > 6 else None

            if subject_name:
                ctk.CTkLabel(self.review_frame, text=subject_name,
                            font=self.theme.TITLE, text_color=self.theme.TEXT_COLOR).pack(anchor="w", padx=10, pady=(6,0))
            if chapter_name:
                ctk.CTkLabel(self.review_frame, text=f"📄 {chapter_name}",
                            font=self.theme.SECTION, text_color=self.theme.TEXT_COLOR).pack(anchor="w", padx=10, pady=(0,6))
            if tags:
                ctk.CTkLabel(self.review_frame, text=f"• {tags}",
                            font=self.theme.BODY, text_color=self.theme.SUBTEXT).pack(anchor="w", padx=20, pady=(0,6))

            ctk.CTkLabel(self.review_frame, text=front,
                        font=self.theme.SUBHEADER, text_color=self.theme.TEXT_COLOR,
                        justify="center").pack(expand=True, pady=(10,6))

            back_label = ctk.CTkLabel(self.review_frame, text=back,
                                    font=self.theme.LARGE, text_color=self.theme.TEXT_COLOR,
                                    justify="center")

            def reveal():
                back_label.pack(expand=True, pady=(0,6))

            reveal_btn = ctk.CTkButton(self.review_frame, text="Show Answer", command=reveal)
            self.theme.style_button(reveal_btn)
            reveal_btn.pack(pady=10)

    def _handle_review(self, outcome):
        if not self.current_card:
            return
        card_id = self.current_card[0]
        update_flashcard_review(card_id, outcome)

        self._load_next_card()
        self._update_dashboard()
        self._update_due_today()
    def _on_review_subject_change(self, selected_name: str):
        if selected_name == "All Subjects":
            self.subject_id = None
            self.chapter_id = None
        else:
            self.subject_id = self.subject_map.get(selected_name)
            self.chapter_id = None  # reset chapter filter when subject changes
        self._load_next_card()
        self._update_dashboard()
    def _update_due_today(self):
        due_cards = get_due_flashcards(self.user_id, self.subject_id, self.chapter_id)
        total_due = len(due_cards)
        self.due_today_label.configure(text=f"📊 Due Today: {total_due}")

