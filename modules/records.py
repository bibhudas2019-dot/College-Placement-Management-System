import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox

from database.db_config import create_connection


TABLES = {
    "students": "Student Management",
    "companies": "Company Management",
    "placement_drives": "Placement Drive Management"
}


def open_records(parent, table_name):

    if table_name not in TABLES:
        messagebox.showerror("Error", "Invalid table.")
        return

    window = ctk.CTkToplevel(parent)
    window.title(TABLES[table_name])
    window.geometry("1150x720")
    window.minsize(850, 550)
    window.configure(fg_color="#F3F6FA")

    navy = "#14243A"
    blue = "#2563EB"

    columns_info = []
    primary_key = None
    display_columns = []

    # ---------------- HEADER ----------------

    header = ctk.CTkFrame(
        window, fg_color=navy, corner_radius=0, height=100
    )
    header.pack(fill="x")

    ctk.CTkLabel(
        header,
        text=TABLES[table_name].upper(),
        font=("Arial", 24, "bold"),
        text_color="white"
    ).pack(anchor="w", padx=30, pady=(20, 5))

    ctk.CTkLabel(
        header,
        text="Manage records directly from your MySQL database",
        font=("Arial", 13),
        text_color="#B8C7D9"
    ).pack(anchor="w", padx=30)

    # ---------------- TOOLBAR ----------------

    toolbar = ctk.CTkFrame(
        window, fg_color="transparent"
    )
    toolbar.pack(fill="x", padx=25, pady=18)

    # ---------------- TABLE ----------------

    table_frame = ctk.CTkFrame(
        window, fg_color="white", corner_radius=12
    )
    table_frame.pack(
        fill="both", expand=True, padx=25, pady=(0, 20)
    )

    tree = ttk.Treeview(
        table_frame,
        show="headings",
        selectmode="browse"
    )

    tree_scroll_y = ttk.Scrollbar(
        table_frame,
        orient="vertical",
        command=tree.yview
    )

    tree_scroll_x = ttk.Scrollbar(
        table_frame,
        orient="horizontal",
        command=tree.xview
    )

    tree.configure(
        yscrollcommand=tree_scroll_y.set,
        xscrollcommand=tree_scroll_x.set
    )

    tree.pack(
        side="top", fill="both", expand=True,
        padx=10, pady=(10, 0)
    )

    tree_scroll_y.pack(side="right", fill="y")
    tree_scroll_x.pack(side="bottom", fill="x")

    style = ttk.Style()
    style.theme_use("clam")
    style.configure(
        "Treeview",
        rowheight=35,
        font=("Arial", 10),
        background="white",
        fieldbackground="white"
    )
    style.configure(
        "Treeview.Heading",
        font=("Arial", 10, "bold"),
        background="#E8EEF5",
        padding=8
    )

    # ---------------- DATABASE STRUCTURE ----------------

    def get_structure():

        nonlocal columns_info, primary_key, display_columns

        connection = create_connection()

        if connection is None:
            raise Exception("Database connection failed.")

        try:
            cursor = connection.cursor()

            cursor.execute(
                f"SHOW COLUMNS FROM `{table_name}`"
            )

            columns_info = cursor.fetchall()

            cursor.execute(
                f"SHOW KEYS FROM `{table_name}` "
                "WHERE Key_name = 'PRIMARY'"
            )

            keys = cursor.fetchall()

            primary_key = keys[0][4] if keys else None

            display_columns = [column[0] for column in columns_info]

            tree["columns"] = display_columns

            for column in display_columns:
                tree.heading(column, text=column)
                tree.column(
                    column,
                    width=150,
                    minwidth=100,
                    anchor="center"
                )

        finally:
            cursor.close()
            connection.close()

    # ---------------- LOAD RECORDS ----------------

    def load_records():

        for item in tree.get_children():
            tree.delete(item)

        connection = create_connection()

        if connection is None:
            messagebox.showerror(
                "Database Error",
                "Could not connect to MySQL."
            )
            return

        try:
            cursor = connection.cursor()

            cursor.execute(
                f"SELECT * FROM `{table_name}`"
            )

            records = cursor.fetchall()

            for record in records:
                tree.insert("", "end", values=record)

        except Exception as error:
            messagebox.showerror(
                "Load Error", str(error)
            )

        finally:
            cursor.close()
            connection.close()

    # ---------------- ADD / EDIT FORM ----------------

    def open_form(edit=False):

        selected = tree.selection()

        if edit and not selected:
            messagebox.showwarning(
                "Select Record",
                "Please select a record to edit."
            )
            return

        old_values = (
            tree.item(selected[0], "values")
            if edit else None
        )

        form = ctk.CTkToplevel(window)
        form.title(
            "Edit Record" if edit else "Add New Record"
        )
        form.geometry("650x700")
        form.minsize(450, 450)
        form.configure(fg_color="#F3F6FA")

        ctk.CTkLabel(
            form,
            text="EDIT RECORD" if edit else "ADD NEW RECORD",
            font=("Arial", 22, "bold"),
            text_color=navy
        ).pack(anchor="w", padx=25, pady=20)

        scroll = ctk.CTkScrollableFrame(
            form, fg_color="white", corner_radius=12
        )
        scroll.pack(
            fill="both", expand=True,
            padx=20, pady=(0, 15)
        )

        entries = {}

        for index, column in enumerate(columns_info):

            name = column[0]
            data_type = str(column[1]).lower()
            nullable = column[2] == "YES"
            default_value = column[4]
            extra = str(column[5]).lower()

            # Skip automatically generated IDs
            if "auto_increment" in extra:
                continue

            # Primary key must not be changed during editing
            if edit and name == primary_key:
                continue

            ctk.CTkLabel(
                scroll,
                text=name.replace("_", " ").title(),
                font=("Arial", 12, "bold"),
                text_color=navy
            ).pack(anchor="w", padx=15, pady=(12, 3))

            entry = ctk.CTkEntry(
                scroll,
                height=38,
                placeholder_text=f"Enter {name}"
            )
            entry.pack(fill="x", padx=15)

            if edit:
                position = display_columns.index(name)
                value = old_values[position]

                if value is not None:
                    entry.insert(0, str(value))

            elif default_value is not None:
                entry.insert(0, str(default_value))

            entries[name] = {
                "entry": entry,
                "nullable": nullable,
                "default": default_value,
                "type": data_type
            }

        def save_record():

            values = {}
            for name, info in entries.items():

                value = info["entry"].get().strip()

                if value == "":
                    if not info["nullable"] and info["default"] is None:
                        messagebox.showwarning(
                            "Required Field",
                            f"{name} cannot be empty."
                        )
                        return

                    values[name] = (
                        None if info["nullable"] else ""
                    )
                else:
                    values[name] = value

            connection = create_connection()

            if connection is None:
                messagebox.showerror(
                    "Database Error",
                    "Could not connect to MySQL."
                )
                return

            cursor = None

            try:
                cursor = connection.cursor()

                if edit:

                    if not primary_key:
                        raise Exception(
                            "This table has no primary key."
                        )

                    set_clause = ", ".join(
                        f"`{name}` = %s"
                        for name in values
                    )

                    query = (
                        f"UPDATE `{table_name}` SET {set_clause} "
                        f"WHERE `{primary_key}` = %s"
                    )

                    position = display_columns.index(primary_key)
                    primary_value = old_values[position]

                    cursor.execute(
                        query,
                        tuple(values.values()) + (primary_value,)
                    )

                else:

                    if not values:
                        raise Exception(
                            "No fields available to insert."
                        )

                    field_names = ", ".join(
                        f"`{name}`" for name in values
                    )

                    placeholders = ", ".join(
                        ["%s"] * len(values)
                    )

                    query = (
                        f"INSERT INTO `{table_name}` "
                        f"({field_names}) VALUES ({placeholders})"
                    )

                    cursor.execute(
                        query, tuple(values.values())
                    )

                connection.commit()

                messagebox.showinfo(
                    "Success",
                    "Record updated successfully!"
                    if edit else "Record added successfully!"
                )

                form.destroy()
                load_records()

            except Exception as error:
                connection.rollback()
                messagebox.showerror(
                    "Database Error", str(error)
                )

            finally:
                if cursor:
                    cursor.close()
                connection.close()

        ctk.CTkButton(
            form,
            text="UPDATE RECORD" if edit else "SAVE RECORD",
            height=42,
            fg_color=blue,
            hover_color="#1D4ED8",
            command=save_record
        ).pack(fill="x", padx=20, pady=(0, 20))

    # ---------------- DELETE RECORD ----------------

    def delete_record():

        selected = tree.selection()

        if not selected:
            messagebox.showwarning(
                "Select Record",
                "Please select a record to delete."
            )
            return

        if not primary_key:
            messagebox.showerror(
                "Error",
                "This table has no primary key."
            )
            return

        values = tree.item(selected[0], "values")
        position = display_columns.index(primary_key)
        record_id = values[position]

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this record?"
        )

        if not confirm:
            return

        connection = create_connection()

        if connection is None:
            messagebox.showerror(
                "Database Error",
                "Could not connect to MySQL."
            )
            return

        cursor = None

        try:
            cursor = connection.cursor()

            cursor.execute(
                f"DELETE FROM `{table_name}` "
                f"WHERE `{primary_key}` = %s",
                (record_id,)
            )

            connection.commit()

            messagebox.showinfo(
                "Deleted",
                "Record deleted successfully."
            )

            load_records()

        except Exception as error:
            connection.rollback()
            messagebox.showerror(
                "Delete Error",
                f"{error}\n\n"
                "This record may be linked to other records."
            )

        finally:
            if cursor:
                cursor.close()
            connection.close()

    # ---------------- BUTTONS ----------------

    ctk.CTkButton(
        toolbar,
        text="+ Add New",
        width=120,
        fg_color="#168B83",
        command=lambda: open_form(False)
    ).pack(side="left", padx=5)

    ctk.CTkButton(
        toolbar,
        text="Edit Selected",
        width=130,
        fg_color=blue,
        command=lambda: open_form(True)
    ).pack(side="left", padx=5)

    ctk.CTkButton(
        toolbar,
        text="Delete Selected",
        width=140,
        fg_color="#DC2626",
        hover_color="#B91C1C",
        command=delete_record
    ).pack(side="left", padx=5)

    ctk.CTkButton(
        toolbar,
        text="↻ Refresh",
        width=110,
        fg_color="#475569",
        command=load_records
    ).pack(side="right", padx=5)

    # Initialize
    try:
        get_structure()
        load_records()
    except Exception as error:
        messagebox.showerror(
            "Database Error", str(error)
        )

    return window


# ==================================================
# REPORTS
# ==================================================

def open_reports(parent):

    window = ctk.CTkToplevel(parent)
    window.title("Placement Reports | Campus Connect")
    window.geometry("950x650")
    window.configure(fg_color="#F3F6FA")

    navy = "#14243A"

    ctk.CTkLabel(
        window,
        text="PLACEMENT REPORTS",
        font=("Arial", 26, "bold"),
        text_color=navy
    ).pack(anchor="w", padx=30, pady=(25, 5))

    ctk.CTkLabel(
        window,
        text="Live reports generated from your MySQL database",
        font=("Arial", 13),
        text_color="#64748B"
    ).pack(anchor="w", padx=30)

    summary = ctk.CTkFrame(
        window, fg_color="white", corner_radius=12
    )
    summary.pack(fill="x", padx=30, pady=25)

    report_text = ctk.CTkLabel(
        summary,
        text="Loading reports...",
        font=("Arial", 15),
        text_color=navy,
        justify="left"
    )
    report_text.pack(anchor="w", padx=25, pady=25)

    result_frame = ctk.CTkFrame(
        window, fg_color="white", corner_radius=12
    )
    result_frame.pack(
        fill="both", expand=True, padx=30, pady=(0, 20)
    )

    tree = ttk.Treeview(
        result_frame,
        columns=("Status", "Total"),
        show="headings"
    )

    tree.heading("Status", text="Application Status")
    tree.heading("Total", text="Number of Applications")

    tree.column("Status", width=300, anchor="center")
    tree.column("Total", width=250, anchor="center")

    tree.pack(fill="both", expand=True, padx=15, pady=15)

    def load_reports():

        for item in tree.get_children():
            tree.delete(item)

        connection = create_connection()

        if connection is None:
            messagebox.showerror(
                "Database Error",
                "Could not connect to MySQL."
            )
            return

        cursor = None

        try:
            cursor = connection.cursor()

            cursor.execute("SELECT COUNT(*) FROM students")
            students = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM companies")
            companies = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM placement_drives")
            drives = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM applications")
            applications = cursor.fetchone()[0]

            cursor.execute("""
                SELECT application_status, COUNT(*)
                FROM applications
                GROUP BY application_status
            """)

            statuses = cursor.fetchall()

            report_text.configure(
                text=(
                    f"TOTAL STUDENTS       : {students}\n"
                    f"TOTAL COMPANIES      : {companies}\n"
                    f"TOTAL PLACEMENT DRIVES: {drives}\n"
                    f"TOTAL APPLICATIONS   : {applications}"
                )
            )

            for status, count in statuses:
                tree.insert(
                    "", "end",
                    values=(status or "Not specified", count)
                )

        except Exception as error:
            messagebox.showerror(
                "Report Error", str(error)
            )

        finally:
            if cursor:
                cursor.close()
            connection.close()

    ctk.CTkButton(
        window,
        text="↻ Refresh Reports",
        fg_color="#168B83",
        hover_color="#116E68",
        command=load_reports
    ).pack(pady=(0, 20))

    load_reports()

    return window