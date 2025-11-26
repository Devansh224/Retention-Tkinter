import customtkinter as ctk

class Theme:
    # Modern Dark Colors
    BG_COLOR = "#121212"       # true dark background
    FG_COLOR = "#1E1E1E"       # surface panels/cards
    # ACCENT = "#306ED8"         # vibrant modern blue
    ACCENT = "#4F30D8"         # vibrant modern blue
    ACCENT_LIGHT = "#6370FF"   # lighter accent for highlights
    TEXT_COLOR = "#E5E7EB"     # soft off-white text
    SUBTEXT = "#9CA3AF"        # muted gray for secondary info
    SUCCESS = "#22C55E"        # modern green
    ERROR = "#EF4444"          # crisp red
    # HOVER_COLOR = "#2858DB"    # brighter blue hover
    HOVER_COLOR = "#441FCA"    # brighter blue hover
    BUTTON_HOVER = "#374151"   # subtle gray hover for option menus

    # Fonts (modern system look)
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
            text_color=Theme.TEXT_COLOR,
            corner_radius=10,
            font=Theme.BODY
        )

    @staticmethod
    def style_entry(entry):
        entry.configure(
            fg_color=Theme.FG_COLOR,
            border_color=Theme.ACCENT,
            border_width=0,  # flat until focus
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
            button_color="#2D2D2D",
            button_hover_color=Theme.BUTTON_HOVER,
            text_color=Theme.TEXT_COLOR
        )

    @staticmethod
    def style_chapter_button(button):
        button.configure(
            fg_color="#2A2A2A",              # darker shade for chapter buttons
            hover_color=Theme.ACCENT,        # highlight with accent on hover
            text_color=Theme.TEXT_COLOR,
            corner_radius=8,
            font=Theme.SMALL
        )

    @staticmethod
    def style_frame(frame):
        frame.configure(
            fg_color=Theme.FG_COLOR,
            corner_radius=12
        )