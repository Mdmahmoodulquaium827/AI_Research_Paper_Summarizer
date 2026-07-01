import customtkinter as ctk
from tkinter import filedialog, messagebox
from reportlab.pdfgen import canvas
import threading
from PIL import Image
from pdf_processor import extract_text
from ai_processor import generate_summary

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# ==================================
# SETTINGS
# ==================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

paper_text = ""

# ==================================
# FUNCTIONS
# ==================================

def upload_pdf():
    
    global paper_text

    file_path = filedialog.askopenfilename(
        filetypes=[("PDF Files", "*.pdf")]
    )

    if not file_path:
        return

    # Clear old data
    paper_text = ""

    output_text.delete(
        "0.0",
        "end"
    )

    status_label.configure(
        text="📄 Loading PDF..."
    )

    # Load new PDF
    paper_text = extract_text(file_path)

    status_label.configure(
        text=f"✅ Loaded: {file_path.split('/')[-1]}"
    )

    progress.set(0)


def run_summary():

    try:

        result = generate_summary(
            paper_text
        )

        output_text.delete(
            "0.0",
            "end"
        )

        output_text.insert(
            "end",
            result
        )

    except Exception as e:

        messagebox.showerror(
            "Error",
            str(e)
        )

    progress.stop()

    summary_button.configure(
        state="normal"
    )


def generate_ai_summary():
    
    if not paper_text:

        messagebox.showwarning(
            "Warning",
            "Please upload a PDF first."
        )

        return

    output_text.delete(
        "0.0",
        "end"
    )

    summary_button.configure(
        state="disabled"
    )

    progress.start()

    threading.Thread(
        target=run_summary,
        daemon=True
    ).start()


def export_pdf():
    
    content = output_text.get(
        "0.0",
        "end"
    )

    if not content.strip():

        messagebox.showwarning(
            "Warning",
            "No summary available."
        )

        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF Files", "*.pdf")]
    )

    if not file_path:
        return

    doc = SimpleDocTemplate(file_path)

    styles = getSampleStyleSheet()

    story = []

    for paragraph in content.split("\n\n"):

        story.append(
            Paragraph(paragraph, styles["BodyText"])
        )

        story.append(
            Spacer(1, 12)
        )

    doc.build(story)

    messagebox.showinfo(
        "Success",
        "PDF exported successfully!"
    )


def change_theme(mode):

    ctk.set_appearance_mode(
        mode
    )


# ==================================
# WINDOW
# ==================================

root = ctk.CTk()

root.title(
    "AI Research Paper Summarizer"
)

root.geometry("1600x900")
root.minsize(1200, 700)
root.iconbitmap(resource_path("icon.ico"))

logo = ctk.CTkImage(
    light_image=Image.open(resource_path("icon.png")),
    dark_image=Image.open(resource_path("icon.png")),
    size=(80, 80)
)

# ==================================
# HEADER
# ==================================

title = ctk.CTkLabel(
    root,
    image=logo,
    text=" AI Research Paper Summarizer",
    compound="left",
    font=("Segoe UI", 40, "bold"),
    text_color="#38BDF8"
)

title.pack(pady=(20, 5))

subtitle = ctk.CTkLabel(
    root,
    text="Summarize, Analyze and Export Research Papers with AI",
    font=("Segoe UI", 16),
    text_color="#9CA3AF"
)

subtitle.pack(pady=(0, 20))

# ==================================
# TOP BAR
# ==================================

top_frame = ctk.CTkFrame(
    root,
    corner_radius=25,
    fg_color="#262626",
    border_width=1,
    border_color="#404040"
)

top_frame.pack(
    fill="x",
    padx=30,
    pady=20
)

# Upload Button

upload_button = ctk.CTkButton(
    top_frame,
    text="📂 Upload PDF",
    width=220,
    height=55,
    corner_radius=25,
    fg_color="#2563EB",
    hover_color="#1D4ED8",
    font=("Segoe UI", 16, "bold"),
    command=upload_pdf
)
upload_button.pack(
    side="left",
    padx=15,
    pady=15
)

# Summary Button

summary_button = ctk.CTkButton(
    top_frame,
    text="✨ Generate Summary",
    width=250,
    height=55,
    corner_radius=25,
    fg_color="#06B6D4",
    hover_color="#0891B2",
    font=("Segoe UI", 16, "bold"),
    command=generate_ai_summary
)

summary_button.pack(
    side="left",
    padx=15
)

# Export Button

export_button = ctk.CTkButton(
    top_frame,
    text="📄 Export PDF",
    width=180,
    height=55,
    corner_radius=25,
    fg_color="#8B5CF6",
    hover_color="#7C3AED",
    font=("Segoe UI", 16, "bold"),
    command=export_pdf
)

export_button.pack(
    side="left",
    padx=15
)

# Theme Selector

theme_menu = ctk.CTkOptionMenu(
    top_frame,
    values=["Dark", "Light"],
    command=change_theme
)

theme_menu.pack(
    side="right",
    padx=20
)

# ==================================
# STATUS
# ==================================

status_label = ctk.CTkLabel(
    root,
    text="📄 No PDF Uploaded",
    font=("Segoe UI", 14),
    text_color="#A1A1AA"
)

status_label.pack(pady=10)



# ==================================
# PROGRESS BAR
# ==================================

progress = ctk.CTkProgressBar(
    root,
    width=500,
    height=18,
    corner_radius=20,
    progress_color="#06B6D4"
)

progress.pack(pady=15)

progress.set(0)
progress.pack(
    pady=10
)



# ==================================
# OUTPUT AREA
# ==================================

output_frame = ctk.CTkFrame(
    root,
    corner_radius=25,
    fg_color="#18181B",
    border_width=1,
    border_color="#404040"
)

output_frame.pack(
    fill="both",
    expand=True,
    padx=25,
    pady=20
)

output_text = ctk.CTkTextbox(
    output_frame,
    font=("Segoe UI", 15),
    corner_radius=20,
    border_width=0
)

output_text.pack(
    fill="both",
    expand=True,
    padx=15,
    pady=15
)

# ==================================
# FOOTER
# ==================================

footer = ctk.CTkLabel(
    root,
    text="Powered by Gemini AI • Version 1.0",
    font=("Segoe UI", 12),
    text_color="#71717A"
)

footer.pack(pady=10)

# ==================================
# RUN
# ==================================

root.mainloop()