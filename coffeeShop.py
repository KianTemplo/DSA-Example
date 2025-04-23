import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

# Global data
applicants = []
image_refs = []

# Register window
def open_register():
    def upload_file():
        path = filedialog.askopenfilename(filetypes=[
            ("Image Files", "*.png;*.jpg;*.jpeg"),
            ("PDF Files", "*.pdf"),
            ("All Files", "*.*")
        ])
        if path:
            file_var.set(path)

    def submit():
        try:
            name = name_entry.get()
            sid = id_entry.get()
            course = course_entry.get()
            gpa = float(gpa_entry.get())
            email = email_entry.get()
            doc = file_var.get()

            if all([name, sid, course, email, doc]):
                applicants.append({
                    "Name": name,
                    "ID": sid,
                    "Course": course,
                    "GPA": gpa,
                    "Email": email,
                    "Document": doc
                })
                messagebox.showinfo("Success", "Registration complete!")
                reg_win.destroy()
            else:
                messagebox.showwarning("Missing", "Please fill all fields.")
        except ValueError:
            messagebox.showerror("Error", "GPA must be a number.")

    reg_win = tk.Toplevel(root)
    reg_win.title("Register")
    reg_win.geometry("400x350")

    tk.Label(reg_win, text="Name").grid(row=0, column=0)
    name_entry = tk.Entry(reg_win)
    name_entry.grid(row=0, column=1)

    tk.Label(reg_win, text="Student ID").grid(row=1, column=0)
    id_entry = tk.Entry(reg_win)
    id_entry.grid(row=1, column=1)

    tk.Label(reg_win, text="Course").grid(row=2, column=0)
    course_entry = tk.Entry(reg_win)
    course_entry.grid(row=2, column=1)

    tk.Label(reg_win, text="GPA").grid(row=3, column=0)
    gpa_entry = tk.Entry(reg_win)
    gpa_entry.grid(row=3, column=1)

    tk.Label(reg_win, text="Email").grid(row=4, column=0)
    email_entry = tk.Entry(reg_win)
    email_entry.grid(row=4, column=1)

    file_var = tk.StringVar()
    tk.Button(reg_win, text="Upload Document", command=upload_file).grid(row=5, column=0)
    tk.Label(reg_win, textvariable=file_var, wraplength=200).grid(row=5, column=1)

    tk.Button(reg_win, text="Submit", command=submit).grid(row=6, column=0)
    tk.Button(reg_win, text="Back", command=reg_win.destroy).grid(row=6, column=1)

# View window
def view_applicants():
    view_win = tk.Toplevel(root)
    view_win.title("Applicants List")
    view_win.geometry("850x500")

    headers = ["Name", "ID", "Course", "GPA", "Document", "Preview"]
    for i, h in enumerate(headers):
        tk.Label(view_win, text=h, font=("Arial", 10, "bold")).grid(row=0, column=i)

    content_frame = tk.Frame(view_win)
    content_frame.grid(row=1, column=0, columnspan=6)

    def show_data(app_list):
        for widget in content_frame.winfo_children():
            widget.destroy()

        image_refs.clear()

        for row, app in enumerate(app_list):
            tk.Label(content_frame, text=app["Name"]).grid(row=row, column=0)
            tk.Label(content_frame, text=app["ID"]).grid(row=row, column=1)
            tk.Label(content_frame, text=app["Course"]).grid(row=row, column=2)
            tk.Label(content_frame, text=app["GPA"]).grid(row=row, column=3)
            tk.Label(content_frame, text=os.path.basename(app["Document"])).grid(row=row, column=4)

            doc = app["Document"]
            if doc.lower().endswith((".png", ".jpg", ".jpeg")) and os.path.exists(doc):
                try:
                    img = Image.open(doc)
                    img.thumbnail((80, 80))
                    img_tk = ImageTk.PhotoImage(img)
                    image_refs.append(img_tk)
                    tk.Label(content_frame, image=img_tk).grid(row=row, column=5)
                except:
                    tk.Label(content_frame, text="Image error").grid(row=row, column=5)
            else:
                tk.Label(content_frame, text="No image").grid(row=row, column=5)

    # Sorting button
    sort_state = {"sorted": False}
    def toggle_sort():
        if not sort_state["sorted"]:
            sorted_list = sorted(applicants, key=lambda x: x["GPA"], reverse=True)
            sort_btn.config(text="Unsort")
        else:
            sorted_list = applicants
            sort_btn.config(text="Sort by GPA")
        sort_state["sorted"] = not sort_state["sorted"]
        show_data(sorted_list)

    sort_btn = tk.Button(view_win, text="Sort by GPA", command=toggle_sort)
    sort_btn.grid(row=2, column=0, pady=10)

    tk.Button(view_win, text="Back", command=view_win.destroy).grid(row=2, column=1)

    show_data(applicants)

# Main window
root = tk.Tk()
root.title("Scholarship Registration System")
root.geometry("300x250")

tk.Label(root, text="Scholarship Registration", font=("Arial", 14)).pack(pady=20)
tk.Button(root, text="Register", width=25, command=open_register).pack(pady=5)
tk.Button(root, text="View Applicants", width=25, command=view_applicants).pack(pady=5)
tk.Button(root, text="Exit", width=25, command=root.quit).pack(pady=20)

root.mainloop()
