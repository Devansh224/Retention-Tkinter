import customtkinter as ctk

class Theme:
    # Colors
    BG_COLOR = "#1E1E2F"
    FG_COLOR = "#2E2E3E"
    ACCENT = "#5952DB"
    TEXT_COLOR = "#F2F2F2"
    SUBTEXT = "#A6A6A6"
    SUCCESS = "#00C896"
    ERROR = "#FF5C5C"
    HOVER_COLOR = "#5750D6"
    BUTTON_HOVER = "#50555f"

    # Fonts
    HEADER = ("Segoe UI", 24, "bold")
    SUBHEADER = ("Segoe UI", 18, "bold")
    BODY = ("Segoe UI", 13)
    SMALL = ("Segoe UI", 11)
    TITLE = ("Segoe UI", 20, "bold")
    SECTION = ("Segoe UI", 16, "bold")
    LARGE = ("Segoe UI", 15)

    @staticmethod
    def set_theme():
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

    @staticmethod
    def style_button(button):
        button.configure(
            fg_color=Theme.ACCENT,
            hover_color=Theme.HOVER_COLOR,
            text_color="white",
            corner_radius=10,
            font=Theme.BODY
        )

    @staticmethod
    def style_entry(entry):
        entry.configure(
            fg_color=Theme.FG_COLOR,
            border_color=Theme.ACCENT,
            border_width=1,
            text_color=Theme.TEXT_COLOR,
            font=Theme.BODY,
            corner_radius=8
        )

    @staticmethod
    def style_label(label, bold=False, size=13):
        label.configure(
            text_color=Theme.TEXT_COLOR,
            font=("Segoe UI", size, "bold" if bold else "normal")
        )
    
    @staticmethod
    def style_optionmenu(menu):
        menu.configure(
            fg_color=Theme.FG_COLOR,
            button_color="#3a3f4a",
            button_hover_color=Theme.BUTTON_HOVER,
            text_color="white"
        )
    def style_chapter_button(button):
        button.configure(
            fg_color="#3A3A4F",              # darker shade than FG_COLOR
            hover_color=Theme.ACCENT,        # highlight with accent on hover
            text_color=Theme.TEXT_COLOR,
            corner_radius=8,
            font=Theme.SMALL
        )

    @staticmethod
    def style_frame(frame):
        frame.configure(fg_color=Theme.FG_COLOR, corner_radius=10)
