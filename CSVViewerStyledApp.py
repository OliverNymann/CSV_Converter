
import tkinter as tk
from tkinter import filedialog, ttk
import pandas as pd
from fpdf import FPDF
import matplotlib.pyplot as plt

# Apply dark theme to matplotlib plots
plt.style.use("dark_background")

class CSVViewerApp:
    def __init__(self, root):
        self.root = root
        self.apply_theme()
        self.root.title("CSV Data Display")
        self.root.geometry("1000x800")

        self.df = pd.DataFrame()
        self.setup_gui()

    def apply_theme(self):
        self.root.configure(background='#333333')
        style = ttk.Style(self.root)
        style.theme_use("clam")

        style.configure("Treeview", background="#333333", foreground="white", fieldbackground="#333333", borderwidth=0)
        style.configure("Treeview.Heading", background="#666666", foreground="white", relief="flat")
        style.map("Treeview", background=[('selected', '#0052cc')], foreground=[('selected', 'white')])
        
        style.configure("TButton", font=("Arial", 10, "bold"), background="#333333", foreground="white", borderwidth=1)
        style.map("TButton", background=[('active', '#0052cc')], foreground=[('active', 'white')])

        style.configure("TCombobox", fieldbackground="#333333", background="#666666", foreground="white")
        style.configure("TLabel", background="#333333", foreground="white")

        # Note: ttk does not support border-radius or exact padding control like CSS. These styles are approximations.

    def setup_gui(self):
        self.browse_button = ttk.Button(self.root, text="Browse CSV", command=self.browse_files)
        self.browse_button.pack(padx=10, pady=10)

        self.remove_columns_button = ttk.Button(self.root, text="Remove Columns", command=self.remove_columns)
        self.remove_columns_button.pack(padx=10, pady=5)

        self.file_format_var = tk.StringVar()
        self.file_format_dropdown = ttk.Combobox(self.root, textvariable=self.file_format_var, values=["xlsx", "pdf"], state="readonly")

        self.file_format_dropdown.pack(padx=10, pady=10)

        self.save_button = ttk.Button(self.root, text="Save File", command=self.save_file)
        self.save_button.pack(padx=10, pady=10)

        self.table_frame = tk.Frame(self.root, bg="#333333")
        self.table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(self.table_frame, columns=(), show="headings")
        self.tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT, padx=10, pady=10)

        self.scrollbar = ttk.Scrollbar(self.table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(fill=tk.Y, side=tk.RIGHT)

    # Remaining methods (browse_files, display_data, remove_columns, update_columns, save_file, save_pdf, save_image)
    # remain unchanged from the previous version of the code.
    
    def browse_files(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.df = pd.read_csv(file_path)
            self.display_data()

    def display_data(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        self.tree["columns"] = list(self.df.columns)
        for col in self.df.columns:
            self.tree.heading(col, text=col)

        for _, row in self.df.iterrows():
            self.tree.insert("", tk.END, values=list(row))

    def remove_columns(self):
        self.column_removal_window = tk.Toplevel(self.root)
        self.column_removal_window.title("Remove Columns")
        self.column_removal_window.configure(background='#333333')  # Set background color

        style = ttk.Style(self.column_removal_window)
        style.configure("TRemove.TButton", font=("Arial", 10, "bold"), background="#333333", foreground="white", borderwidth=1)
        style.map("TRemove.TButton", background=[('active', '#0052cc')], foreground=[('active', 'white')])

        self.checkbuttons = []
        self.column_vars = {}
        for col in self.df.columns:
            var = tk.BooleanVar()
            chk = tk.Checkbutton(self.column_removal_window, text=col, var=var, bg='#333333', fg='white', selectcolor='#0052cc', activebackground='#333333', activeforeground='white')
            chk.pack(anchor='w', padx=10, pady=5)
            self.checkbuttons.append(chk)
            self.column_vars[col] = var

        remove_button = ttk.Button(self.column_removal_window, text="Remove Selected", style="TRemove.TButton", command=self.update_columns)
        remove_button.pack(pady=10)


        tk.Button(self.column_removal_window, text="Remove Selected", command=self.update_columns).pack()

    def update_columns(self):
        columns_to_remove = [col for col, var in self.column_vars.items() if var.get()]
        self.df.drop(columns=columns_to_remove, inplace=True)
        self.display_data()
        self.column_removal_window.destroy()

    def save_file(self):
        selected_format = self.file_format_var.get()
        save_path = filedialog.asksaveasfilename(defaultextension=f".{selected_format}")

        if save_path:
            if selected_format == "xlsx":
                self.df.to_excel(save_path, index=False)
            elif selected_format == "pdf":
                self.save_pdf(save_path)
            

    def save_pdf(self, path):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        for _, row in self.df.iterrows():
            pdf.cell(0, 10, '  '.join(str(x) for x in row), 0, 1)
        pdf.output(path)


if __name__ == "__main__":
    root = tk.Tk()
    app = CSVViewerApp(root)
    root.mainloop()
