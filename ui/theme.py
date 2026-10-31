"""
theme.py: Hệ thống giao diện Clean Light phong cách tối giản, hiện đại cho Git Diff Tool.
"""

import tkinter as tk
from tkinter import ttk


class CleanLightTheme:
    """Bảng màu và cấu hình giao diện Clean Light"""

    # Màu nền
    BG_MAIN = "#f8fafc"       # Slate 50
    BG_CARD = "#ffffff"       # Trắng tinh khiết
    BG_CARD_SUBTLE = "#f1f5f9" # Slate 100
    BG_ACTIVE = "#e2e8f0"     # Slate 200

    # Đường viền
    BORDER_COLOR = "#e2e8f0"  # Slate 200
    BORDER_FOCUS = "#3b82f6"  # Blue 500

    # Màu chủ đạo (Accent / Primary)
    PRIMARY = "#2563eb"       # Blue 600
    PRIMARY_HOVER = "#1d4ed8" # Blue 700
    PRIMARY_ACTIVE = "#1e40af"# Blue 800
    PRIMARY_FG = "#ffffff"

    # Nút phụ (Secondary)
    BTN_SEC_BG = "#f1f5f9"
    BTN_SEC_FG = "#334155"
    BTN_SEC_BORDER = "#cbd5e1"

    # Màu văn bản
    TEXT_MAIN = "#0f172a"     # Slate 900
    TEXT_MUTED = "#475569"    # Slate 600
    TEXT_LIGHT = "#94a3b8"    # Slate 400

    # Trạng thái Diff
    DIFF_ADD_FG = "#15803d"   # Green 700
    DIFF_ADD_BG = "#f0fdf4"   # Green 50
    DIFF_DEL_FG = "#b91c1c"   # Red 700
    DIFF_DEL_BG = "#fef2f2"   # Red 50
    DIFF_MOD_FG = "#b45309"   # Amber 700
    DIFF_MOD_BG = "#fffbeb"   # Amber 50
    DIFF_HUNK_FG = "#4338ca"  # Indigo 700
    DIFF_HUNK_BG = "#eef2ff"  # Indigo 50

    # Phông chữ chuẩn hiện đại
    FONT_FAMILY = "Segoe UI"
    FONT_MONO = "Consolas"

    @classmethod
    def apply(cls, root: tk.Tk) -> ttk.Style:
        """Áp dụng style cho toàn bộ cửa sổ ứng dụng"""
        root.configure(bg=cls.BG_MAIN)

        style = ttk.Style(root)
        # Sử dụng theme 'clam' làm nền tảng vì hỗ trợ tùy biến màu sắc sâu nhất
        try:
            style.theme_use("clam")
        except Exception:
            pass

        # Cấu hình TFrame
        style.configure("TFrame", background=cls.BG_MAIN)
        style.configure("Card.TFrame", background=cls.BG_CARD, relief="flat")
        style.configure("SubCard.TFrame", background=cls.BG_CARD_SUBTLE, relief="flat")

        # Cấu hình TLabel
        style.configure(
            "TLabel",
            background=cls.BG_MAIN,
            foreground=cls.TEXT_MAIN,
            font=(cls.FONT_FAMILY, 9),
        )
        style.configure(
            "Card.TLabel",
            background=cls.BG_CARD,
            foreground=cls.TEXT_MAIN,
            font=(cls.FONT_FAMILY, 9),
        )
        style.configure(
            "Title.TLabel",
            background=cls.BG_MAIN,
            foreground=cls.TEXT_MAIN,
            font=(cls.FONT_FAMILY, 14, "bold"),
        )
        style.configure(
            "Section.TLabel",
            background=cls.BG_CARD,
            foreground=cls.TEXT_MAIN,
            font=(cls.FONT_FAMILY, 10, "bold"),
        )
        style.configure(
            "Muted.TLabel",
            background=cls.BG_CARD,
            foreground=cls.TEXT_MUTED,
            font=(cls.FONT_FAMILY, 9),
        )
        style.configure(
            "Status.TLabel",
            background=cls.BG_MAIN,
            foreground=cls.PRIMARY,
            font=(cls.FONT_FAMILY, 9, "bold"),
        )

        # Cấu hình TButton tiêu chuẩn
        style.configure(
            "TButton",
            font=(cls.FONT_FAMILY, 9, "bold"),
            background=cls.BTN_SEC_BG,
            foreground=cls.BTN_SEC_FG,
            borderwidth=1,
            focuscolor="none",
            padding=(10, 5),
        )
        style.map(
            "TButton",
            background=[("pressed", cls.BG_ACTIVE), ("active", "#e2e8f0")],
            foreground=[("disabled", cls.TEXT_LIGHT)],
        )

        # Cấu hình Primary.TButton (Nút nhấn hành động chính)
        style.configure(
            "Primary.TButton",
            font=(cls.FONT_FAMILY, 10, "bold"),
            background=cls.PRIMARY,
            foreground=cls.PRIMARY_FG,
            borderwidth=0,
            focuscolor="none",
            padding=(14, 7),
        )
        style.map(
            "Primary.TButton",
            background=[("pressed", cls.PRIMARY_ACTIVE), ("active", cls.PRIMARY_HOVER)],
            foreground=[("disabled", "#cbd5e1")],
        )

        # Cấu hình TEntry
        style.configure(
            "TEntry",
            font=(cls.FONT_FAMILY, 9),
            fieldbackground=cls.BG_CARD,
            foreground=cls.TEXT_MAIN,
            bordercolor=cls.BORDER_COLOR,
            lightcolor=cls.BORDER_COLOR,
            darkcolor=cls.BORDER_COLOR,
            padding=5,
        )

        # Cấu hình TCombobox
        style.configure(
            "TCombobox",
            font=(cls.FONT_FAMILY, 9),
            fieldbackground=cls.BG_CARD,
            background=cls.BG_CARD_SUBTLE,
            foreground=cls.TEXT_MAIN,
            bordercolor=cls.BORDER_COLOR,
            padding=4,
        )

        # Cấu hình TRadiobutton
        style.configure(
            "TRadiobutton",
            background=cls.BG_CARD,
            foreground=cls.TEXT_MAIN,
            font=(cls.FONT_FAMILY, 9),
        )

        # Cấu hình TCheckbutton
        style.configure(
            "TCheckbutton",
            background=cls.BG_CARD,
            foreground=cls.TEXT_MAIN,
            font=(cls.FONT_FAMILY, 9),
        )

        # Cấu hình Notebook (Tab)
        style.configure(
            "TNotebook",
            background=cls.BG_MAIN,
            borderwidth=0,
        )
        style.configure(
            "TNotebook.Tab",
            font=(cls.FONT_FAMILY, 9, "bold"),
            padding=(14, 6),
            background=cls.BG_CARD_SUBTLE,
            foreground=cls.TEXT_MUTED,
            borderwidth=0,
        )
        style.map(
            "TNotebook.Tab",
            background=[("selected", cls.BG_CARD)],
            foreground=[("selected", cls.PRIMARY)],
        )

        # Cấu hình Treeview (Danh sách file thay đổi)
        style.configure(
            "Treeview",
            font=(cls.FONT_FAMILY, 9),
            background=cls.BG_CARD,
            fieldbackground=cls.BG_CARD,
            foreground=cls.TEXT_MAIN,
            rowheight=24,
            borderwidth=1,
            relief="solid",
        )
        style.configure(
            "Treeview.Heading",
            font=(cls.FONT_FAMILY, 9, "bold"),
            background=cls.BG_CARD_SUBTLE,
            foreground=cls.TEXT_MAIN,
            relief="flat",
            padding=(6, 4),
        )
        style.map(
            "Treeview",
            background=[("selected", "#dbeafe")],
            foreground=[("selected", cls.TEXT_MAIN)],
        )

        # Cấu hình TProgressbar
        style.configure(
            "Horizontal.TProgressbar",
            troughcolor=cls.BG_CARD_SUBTLE,
            background=cls.PRIMARY,
            bordercolor=cls.BORDER_COLOR,
            lightcolor=cls.PRIMARY,
            darkcolor=cls.PRIMARY,
            thickness=6,
        )

        return style
