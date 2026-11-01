import customtkinter as ctk
from tkinter import messagebox

import os
import sys

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from database.db_config import create_connection
from modules.applications import open_applications
from modules.records import open_records, open_reports


def get_dashboard_counts():

    connection = create_connection()

    if connection is None:
        return 0, 0, 0

    cursor = None

    try:
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM students")
        students = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM companies")
        companies = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM placement_drives")
        drives = cursor.fetchone()[0]

        return students, companies, drives

    except Exception as error:
        print("Dashboard Error:", error)
        return 0, 0, 0

    finally:
        if cursor:
            cursor.close()
        connection.close()


def open_dashboard():

    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    dashboard = ctk.CTk()
    dashboard.title("College Placement Management System")
    dashboard.geometry("1200x750")
    dashboard.minsize(1000, 650)
    dashboard.configure(fg_color="#F3F6FA")

    navy = "#172554"
    blue = "#2563EB"
    muted = "#64748B"

    dashboard.grid_columnconfigure(1, weight=1)
    dashboard.grid_rowconfigure(0, weight=1)

    # ---------------- SIDEBAR ----------------

    sidebar = ctk.CTkFrame(
        dashboard,
        width=235,
        corner_radius=0,
        fg_color=navy
    )

    sidebar.grid(row=0, column=0, sticky="nsew")
    sidebar.grid_propagate(False)

    ctk.CTkLabel(
        sidebar,
        text="CAMPUS\nPLACEMENT",
        font=("Arial", 25, "bold"),
        text_color="white",
        justify="left"
    ).pack(anchor="w", padx=25, pady=(40, 8))

    ctk.CTkLabel(
        sidebar,
        text="MANAGEMENT SYSTEM",
        font=("Arial", 10, "bold"),
        text_color="#93C5FD"
    ).pack(anchor="w", padx=27, pady=(0, 40))

    # ---------------- MAIN CONTENT ----------------

    content = ctk.CTkFrame(
        dashboard,
        fg_color="#F3F6FA",
        corner_radius=0
    )

    content.grid(row=0, column=1, sticky="nsew")
    content.grid_columnconfigure(0, weight=1)
    content.grid_rowconfigure(1, weight=1)

    header = ctk.CTkFrame(
        content,
        fg_color="white",
        corner_radius=0,
        height=75
    )

    header.grid(row=0, column=0, sticky="ew")
    header.grid_columnconfigure(0, weight=1)
    header.grid_propagate(False)

    page_title = ctk.CTkLabel(
        header,
        text="Dashboard",
        font=("Arial", 24, "bold"),
        text_color=navy
    )

    page_title.grid(
        row=0, column=0,
        sticky="w", padx=30, pady=20
    )

    ctk.CTkLabel(
        header,
        text="ADMIN",
        font=("Arial", 12, "bold"),
        text_color=blue
    ).grid(row=0, column=1, padx=30)

    body = ctk.CTkScrollableFrame(
        content,
        fg_color="#F3F6FA",
        corner_radius=0
    )

    body.grid(
        row=1, column=0,
        sticky="nsew", padx=25, pady=20
    )

    body.grid_columnconfigure((0, 1, 2), weight=1)

    # ---------------- PAGE MANAGEMENT ----------------

    def clear_body():
        for widget in body.winfo_children():
            widget.destroy()

    def set_page_title(title):
        page_title.configure(text=title)

    # ---------------- DASHBOARD PAGE ----------------

    def show_dashboard():

        clear_body()
        set_page_title("Dashboard")

        ctk.CTkLabel(
            body,
            text="Welcome back, Administrator!",
            font=("Arial", 25, "bold"),
            text_color=navy
        ).grid(
            row=0, column=0,
            columnspan=3, sticky="w",
            pady=(10, 5)
        )

        ctk.CTkLabel(
            body,
            text="Here's an overview of your college placement activities.",
            font=("Arial", 13),
            text_color=muted
        ).grid(
            row=1, column=0,
            columnspan=3, sticky="w",
            pady=(0, 25)
        )

        students, companies, drives = get_dashboard_counts()

        statistics = [
            ("TOTAL STUDENTS", students, "#2563EB"),
            ("COMPANIES", companies, "#0F766E"),
            ("PLACEMENT DRIVES", drives, "#C2410C")
        ]

        for index, (title, value, accent) in enumerate(statistics):

            card = ctk.CTkFrame(
                body,
                fg_color="white",
                corner_radius=15,
                border_width=1,
                border_color="#E5EAF2"
            )

            card.grid(
                row=2,
                column=index,
                sticky="nsew",
                padx=8,
                pady=8
            )

            ctk.CTkLabel(
                card,
                text=title,
                font=("Arial", 12, "bold"),
                text_color=muted
            ).pack(anchor="w", padx=20, pady=(20, 10))

            ctk.CTkLabel(
                card,
                text=str(value),
                font=("Arial", 34, "bold"),
                text_color=navy
            ).pack(anchor="w", padx=20, pady=5)

            ctk.CTkLabel(
                card,
                text="Live database records",
                font=("Arial", 11),
                text_color=accent
            ).pack(anchor="w", padx=20, pady=(0, 20))

        info = ctk.CTkFrame(
            body,
            fg_color="white",
            corner_radius=15
        )

        info.grid(
            row=3, column=0,
            columnspan=3, sticky="ew",
            padx=8, pady=25
        )

        ctk.CTkLabel(
            info,
            text="Placement Management",
            font=("Arial", 20, "bold"),
            text_color=navy
        ).pack(anchor="w", padx=25, pady=(25, 10))

        ctk.CTkLabel(
            info,
            text=(
                "Manage students, companies, placement drives and "
                "applications.\n"
                "All records are connected to your MySQL database."
            ),
            font=("Arial", 14),
            text_color=muted,
            justify="left"
        ).pack(anchor="w", padx=25, pady=(0, 25))

        ctk.CTkButton(
            body,
            text="↻ Refresh Dashboard",
            fg_color=blue,
            command=show_dashboard
        ).grid(
            row=4, column=0,
            columnspan=3, pady=15
        )

    # ---------------- NAVIGATION ----------------

    navigation = [
        ("Dashboard", show_dashboard),
        (
            "Students",
            lambda: open_records(dashboard, "students")
        ),
        (
            "Companies",
            lambda: open_records(dashboard, "companies")
        ),
        (
            "Placement Drives",
            lambda: open_records(dashboard, "placement_drives")
        ),
        (
            "Applications",
            lambda: open_applications(dashboard)
        ),
        (
            "Reports",
            lambda: open_reports(dashboard)
        )
    ]

    def sidebar_item(text, command, active=False):

        button = ctk.CTkButton(
            sidebar,
            text="  " + text,
            height=45,
            corner_radius=8,
            anchor="w",
            font=("Arial", 14),
            fg_color="#334A78" if active else "transparent",
            hover_color="#334A78",
            text_color="white",
            command=command
        )

        button.pack(
            fill="x",
            padx=15,
            pady=5
        )

    for title, command in navigation:
        sidebar_item(
            title,
            command,
            active=(title == "Dashboard")
        )

    ctk.CTkLabel(
        sidebar,
        text="ADMIN PANEL  |  2026",
        font=("Arial", 10),
        text_color="#93A9D0"
    ).pack(side="bottom", pady=25)

    show_dashboard()

    dashboard.mainloop()


if __name__ == "__main__":
    open_dashboard()