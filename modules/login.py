<<<<<<< HEAD
import customtkinter as ctk
from tkinter import messagebox


def open_login():

    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title("College Placement Management System")
    app.geometry("1000x600")
    app.resizable(False, False)

    navy = "#14243A"
    teal = "#16A6A1"
    light = "#F4F7FB"

    app.configure(fg_color=light)

    # LEFT PANEL
    left = ctk.CTkFrame(
        app,
        width=480,
        corner_radius=0,
        fg_color=navy
    )
    left.pack(side="left", fill="both")
    left.pack_propagate(False)

    ctk.CTkLabel(
        left,
        text="CAMPUS CONNECT",
        font=("Arial", 15, "bold"),
        text_color="#6DE0D3"
    ).pack(anchor="w", padx=55, pady=(85, 30))

    ctk.CTkLabel(
        left,
        text="Build Your\nCareer With Us.",
        font=("Arial", 37, "bold"),
        text_color="white",
        justify="left"
    ).pack(anchor="w", padx=55, pady=10)

    ctk.CTkLabel(
        left,
        text="A smarter way to manage campus\nplacements and recruitment activities.",
        font=("Arial", 16),
        text_color="#C1CDDC",
        justify="left"
    ).pack(anchor="w", padx=55, pady=15)

    ctk.CTkLabel(
        left,
        text="STUDENT  •  COMPANY  •  OPPORTUNITY",
        font=("Arial", 11, "bold"),
        text_color="#6DE0D3"
    ).pack(anchor="w", padx=55, pady=(100, 10))

    # RIGHT PANEL
    right = ctk.CTkFrame(
        app,
        fg_color=light,
        corner_radius=0
    )
    right.pack(side="right", fill="both", expand=True)

    card = ctk.CTkFrame(
        right,
        width=370,
        height=440,
        fg_color="white",
        corner_radius=18
    )
    card.place(relx=0.5, rely=0.5, anchor="center")
    card.pack_propagate(False)

    ctk.CTkLabel(
        card,
        text="Welcome Back",
        font=("Arial", 28, "bold"),
        text_color=navy
    ).pack(anchor="w", padx=35, pady=(45, 5))

    ctk.CTkLabel(
        card,
        text="Sign in to your administrator account",
        font=("Arial", 13),
        text_color="#778397"
    ).pack(anchor="w", padx=35, pady=(0, 30))

    ctk.CTkLabel(
        card,
        text="Username",
        font=("Arial", 13, "bold"),
        text_color=navy
    ).pack(anchor="w", padx=35)

    username = ctk.CTkEntry(
        card,
        width=300,
        height=45,
        placeholder_text="Enter your username",
        corner_radius=9,
        border_color="#DCE3EC"
    )
    username.pack(padx=35, pady=(7, 18))

    ctk.CTkLabel(
        card,
        text="Password",
        font=("Arial", 13, "bold"),
        text_color=navy
    ).pack(anchor="w", padx=35)

    password = ctk.CTkEntry(
        card,
        width=300,
        height=45,
        placeholder_text="Enter your password",
        show="*",
        corner_radius=9,
        border_color="#DCE3EC"
    )
    password.pack(padx=35, pady=(7, 25))

    def login():
        if username.get() == "admin" and password.get() == "admin123":
            from modules.dashboard import open_dashboard
            app.destroy()
            open_dashboard()
        else:
            messagebox.showerror(
                "Login Failed",
                "Invalid username or password."
            )

    ctk.CTkButton(
        card,
        text="SIGN IN",
        width=300,
        height=46,
        fg_color=teal,
        hover_color="#11847F",
        corner_radius=9,
        font=("Arial", 14, "bold"),
        command=login
    ).pack(padx=35)

    ctk.CTkLabel(
        card,
        text="College Placement Management System",
        font=("Arial", 10),
        text_color="#98A2B3"
    ).pack(pady=22)

    app.mainloop()


if __name__ == "__main__":
=======
import customtkinter as ctk
from tkinter import messagebox


def open_login():

    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title("College Placement Management System")
    app.geometry("1000x600")
    app.resizable(False, False)

    navy = "#14243A"
    teal = "#16A6A1"
    light = "#F4F7FB"

    app.configure(fg_color=light)

    # LEFT PANEL
    left = ctk.CTkFrame(
        app,
        width=480,
        corner_radius=0,
        fg_color=navy
    )
    left.pack(side="left", fill="both")
    left.pack_propagate(False)

    ctk.CTkLabel(
        left,
        text="CAMPUS CONNECT",
        font=("Arial", 15, "bold"),
        text_color="#6DE0D3"
    ).pack(anchor="w", padx=55, pady=(85, 30))

    ctk.CTkLabel(
        left,
        text="Build Your\nCareer With Us.",
        font=("Arial", 37, "bold"),
        text_color="white",
        justify="left"
    ).pack(anchor="w", padx=55, pady=10)

    ctk.CTkLabel(
        left,
        text="A smarter way to manage campus\nplacements and recruitment activities.",
        font=("Arial", 16),
        text_color="#C1CDDC",
        justify="left"
    ).pack(anchor="w", padx=55, pady=15)

    ctk.CTkLabel(
        left,
        text="STUDENT  •  COMPANY  •  OPPORTUNITY",
        font=("Arial", 11, "bold"),
        text_color="#6DE0D3"
    ).pack(anchor="w", padx=55, pady=(100, 10))

    # RIGHT PANEL
    right = ctk.CTkFrame(
        app,
        fg_color=light,
        corner_radius=0
    )
    right.pack(side="right", fill="both", expand=True)

    card = ctk.CTkFrame(
        right,
        width=370,
        height=440,
        fg_color="white",
        corner_radius=18
    )
    card.place(relx=0.5, rely=0.5, anchor="center")
    card.pack_propagate(False)

    ctk.CTkLabel(
        card,
        text="Welcome Back",
        font=("Arial", 28, "bold"),
        text_color=navy
    ).pack(anchor="w", padx=35, pady=(45, 5))

    ctk.CTkLabel(
        card,
        text="Sign in to your administrator account",
        font=("Arial", 13),
        text_color="#778397"
    ).pack(anchor="w", padx=35, pady=(0, 30))

    ctk.CTkLabel(
        card,
        text="Username",
        font=("Arial", 13, "bold"),
        text_color=navy
    ).pack(anchor="w", padx=35)

    username = ctk.CTkEntry(
        card,
        width=300,
        height=45,
        placeholder_text="Enter your username",
        corner_radius=9,
        border_color="#DCE3EC"
    )
    username.pack(padx=35, pady=(7, 18))

    ctk.CTkLabel(
        card,
        text="Password",
        font=("Arial", 13, "bold"),
        text_color=navy
    ).pack(anchor="w", padx=35)

    password = ctk.CTkEntry(
        card,
        width=300,
        height=45,
        placeholder_text="Enter your password",
        show="*",
        corner_radius=9,
        border_color="#DCE3EC"
    )
    password.pack(padx=35, pady=(7, 25))

    def login():
        if username.get() == "admin" and password.get() == "admin123":
            from modules.dashboard import open_dashboard
            app.destroy()
            open_dashboard()
        else:
            messagebox.showerror(
                "Login Failed",
                "Invalid username or password."
            )

    ctk.CTkButton(
        card,
        text="SIGN IN",
        width=300,
        height=46,
        fg_color=teal,
        hover_color="#11847F",
        corner_radius=9,
        font=("Arial", 14, "bold"),
        command=login
    ).pack(padx=35)

    ctk.CTkLabel(
        card,
        text="College Placement Management System",
        font=("Arial", 10),
        text_color="#98A2B3"
    ).pack(pady=22)

    app.mainloop()


if __name__ == "__main__":
>>>>>>> 24669ef91ad9a39de534320428a60ef7db8acb63
    open_login()