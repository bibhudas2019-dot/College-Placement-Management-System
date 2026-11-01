import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox

from database.db_config import create_connection


def open_applications(parent=None):
    if parent:
        window = ctk.CTkToplevel(parent)
    else:
        window = ctk.CTk()

    window.title("Applications Management | Campus Connect")
    window.geometry("1150x700")
    window.minsize(900, 600)
    window.configure(fg_color="#F3F6FA")

    window.grid_columnconfigure(0, weight=1)
    window.grid_rowconfigure(1, weight=1)

    # Header
    header = ctk.CTkFrame(
        window, fg_color="#14243A", corner_radius=0, height=105
    )
    header.grid(row=0, column=0, sticky="ew")
    header.grid_columnconfigure(0, weight=1)

    ctk.CTkLabel(
        header,
        text="APPLICATION MANAGEMENT",
        font=("Arial", 25, "bold"),
        text_color="white"
    ).grid(row=0, column=0, padx=30, pady=(22, 3), sticky="w")

    ctk.CTkLabel(
        header,
        text="View and monitor student placement applications",
        font=("Arial", 13),
        text_color="#B8C7D9"
    ).grid(row=1, column=0, padx=30, pady=(0, 18), sticky="w")

    # Main content
    content = ctk.CTkFrame(window, fg_color="transparent")
    content.grid(row=1, column=0, sticky="nsew", padx=25, pady=20)
    content.grid_columnconfigure(0, weight=1)
    content.grid_rowconfigure(2, weight=1)

    # Summary card
    summary = ctk.CTkFrame(
        content, fg_color="white", corner_radius=12
    )
    summary.grid(row=0, column=0, sticky="ew", pady=(0, 18))
    summary.grid_columnconfigure((0, 1), weight=1)

    total_label = ctk.CTkLabel(
        summary,
        text="TOTAL APPLICATIONS\n0",
        font=("Arial", 17, "bold"),
        text_color="#14243A",
        justify="left"
    )
    total_label.grid(row=0, column=0, padx=25, pady=18, sticky="w")

    status_label = ctk.CTkLabel(
        summary,
        text="APPLICATION STATUS\nLoading...",
        font=("Arial", 15, "bold"),
        text_color="#168B83",
        justify="left"
    )
    status_label.grid(row=0, column=1, padx=25, pady=18, sticky="w")

    # Toolbar
    toolbar = ctk.CTkFrame(content, fg_color="transparent")
    toolbar.grid(row=1, column=0, sticky="ew", pady=(0, 12))
    toolbar.grid_columnconfigure(0, weight=1)

    ctk.CTkLabel(
        toolbar,
        text="All Applications",
        font=("Arial", 19, "bold"),
        text_color="#14243A"
    ).grid(row=0, column=0, sticky="w")

    # Table container
    table_frame = ctk.CTkFrame(
        content, fg_color="white", corner_radius=12
    )
    table_frame.grid(row=2, column=0, sticky="nsew")
    table_frame.grid_columnconfigure(0, weight=1)
    table_frame.grid_rowconfigure(0, weight=1)

    columns = (
        "ID", "Student", "Company", "Job Role",
        "Date", "Status"
    )

    table = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings"
    )

    widths = {
        "ID": 65,
        "Student": 190,
        "Company": 170,
        "Job Role": 180,
        "Date": 120,
        "Status": 130
    }

    for column in columns:
        table.heading(column, text=column)
        table.column(
            column,
            width=widths[column],
            anchor="center"
        )

    style = ttk.Style()
    style.theme_use("clam")
    style.configure(
        "Treeview",
        background="white",
        foreground="#26364A",
        rowheight=38,
        fieldbackground="white",
        font=("Arial", 10)
    )
    style.configure(
        "Treeview.Heading",
        background="#E8EEF5",
        foreground="#14243A",
        font=("Arial", 10, "bold"),
        padding=10
    )
    style.map(
        "Treeview",
        background=[("selected", "#D5E9F0")],
        foreground=[("selected", "#14243A")]
    )

    table.tag_configure("Applied", foreground="#2471A3")
    table.tag_configure("Shortlisted", foreground="#168B83")
    table.tag_configure("Selected", foreground="#218838")
    table.tag_configure("Rejected", foreground="#C0392B")

    scrollbar = ttk.Scrollbar(
        table_frame, orient="vertical", command=table.yview
    )
    table.configure(yscrollcommand=scrollbar.set)

    table.grid(row=0, column=0, sticky="nsew", padx=(12, 0), pady=12)
    scrollbar.grid(row=0, column=1, sticky="ns", padx=(0, 12), pady=12)

    def load_applications():
        for item in table.get_children():
            table.delete(item)

        connection = create_connection()

        if connection is None:
            messagebox.showerror(
                "Database Error",
                "Could not connect to the database."
            )
            return

        try:
            cursor = connection.cursor()

            query = """
                SELECT
                    a.application_id,
                    s.full_name,
                    c.company_name,
                    p.job_role,
                    a.application_date,
                    a.application_status
                FROM applications a
                JOIN students s
                    ON a.student_id = s.student_id
                JOIN placement_drives p
                    ON a.drive_id = p.drive_id
                JOIN companies c
                    ON p.company_id = c.company_id
                ORDER BY a.application_id
            """

            cursor.execute(query)
            records = cursor.fetchall()

            counts = {
                "Applied": 0,
                "Shortlisted": 0,
                "Selected": 0,
                "Rejected": 0
            }

            for record in records:
                status = record[5]
                counts[status] = counts.get(status, 0) + 1

                date_value = (
                    record[4].strftime("%d-%m-%Y")
                    if record[4] else "-"
                )

                table.insert(
                    "",
                    "end",
                    values=(
                        record[0],
                        record[1],
                        record[2],
                        record[3],
                        date_value,
                        status
                    ),
                    tags=(status,)
                )

            total_label.configure(
                text=f"TOTAL APPLICATIONS\n{len(records)}"
            )

            status_label.configure(
                text=(
                    f"APPLIED: {counts.get('Applied', 0)}   |   "
                    f"SHORTLISTED: {counts.get('Shortlisted', 0)}\n"
                    f"SELECTED: {counts.get('Selected', 0)}   |   "
                    f"REJECTED: {counts.get('Rejected', 0)}"
                )
            )

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"Unable to load applications:\n{error}"
            )

        finally:
            cursor.close()
            connection.close()

    refresh_button = ctk.CTkButton(
        toolbar,
        text="↻  Refresh Data",
        width=145,
        height=36,
        fg_color="#168B83",
        hover_color="#116E68",
        command=load_applications
    )
    refresh_button.grid(row=0, column=1, sticky="e")

    load_applications()

    return window