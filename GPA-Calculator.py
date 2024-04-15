import tkinter as tk
from tkinter import messagebox

class GPACalculatorApp:
    def __init__(self, master):
        self.master = master
        master.title("GPA Calculator")
        master.geometry("800x600")  # Set window size
        master.configure(bg="#f0f0f0")  # Set background color
        self.center_window(master)  # Center the window on the screen

        # Font style
        self.font_style = ("Comic Sans MS", 12)

        # Freshman or Not Freshman Selection
        self.label_freshman = tk.Label(master, text="Are you a freshman?", font=self.font_style, bg="#f0f0f0", fg="black")
        self.label_freshman.grid(row=0, column=0, pady=20, columnspan=3)
        self.freshman_var = tk.BooleanVar(value=False)  # Set default value to False
        self.freshman_yes = tk.Radiobutton(master, text="Yes", variable=self.freshman_var, value=True, font=self.font_style, bg="#f0f0f0", fg="black")
        self.freshman_no = tk.Radiobutton(master, text="No", variable=self.freshman_var, value=False, font=self.font_style, bg="#f0f0f0", fg="black")
        self.freshman_yes.grid(row=1, column=0)
        self.freshman_no.grid(row=1, column=1)
        self.submit_freshman_button = tk.Button(master, text="Submit", command=self.process_freshman_selection, bg="#4CAF50", fg="black", padx=10, pady=5, borderwidth=0, font=self.font_style)
        self.submit_freshman_button.grid(row=1, column=2, pady=20)

        # Help Button on the Freshman or Not Freshman screen
        self.help_button_freshman = tk.Button(master, text="Help", command=self.display_help_page, bg="#2196F3", fg="black", padx=10, pady=5, borderwidth=0, font=self.font_style)
        self.help_button_freshman.grid(row=2, column=0, columnspan=3, pady=10, sticky='sw')

        self.is_freshman = None
        self.num_classes = 0
        self.class_data = []

        # Set row and column weights for resizing
        for i in range(3):
            master.grid_rowconfigure(i, weight=1)
            master.grid_columnconfigure(i, weight=1)

    def process_freshman_selection(self):
        # Get user's selection of freshman or not
        self.is_freshman = self.freshman_var.get()
        # Display GPA calculator
        self.display_gpa_calculator()

    def display_gpa_calculator(self):
        # Freshman or Not Freshman Selection Widgets
        self.label_freshman.grid_remove()
        self.freshman_yes.grid_remove()
        self.freshman_no.grid_remove()
        self.submit_freshman_button.grid_remove()
        self.help_button_freshman.grid_remove()

        # Add Class Button
        self.add_class_button = tk.Button(self.master, text="Add Class", command=self.add_class, bg="#FFC107", fg="black", padx=10, pady=5, borderwidth=0, font=self.font_style)
        self.add_class_button.grid(row=1, column=0, pady=10, sticky='w')

        # Delete Class Button
        self.delete_class_button = tk.Button(self.master, text="Delete Class", command=self.delete_class, bg="#FFC107", fg="black", padx=10, pady=5, borderwidth=0, font=self.font_style)
        self.delete_class_button.grid(row=1, column=1, pady=10, sticky='w')

        # Class List
        self.class_list_label = tk.Label(self.master, text="Class List:", font=self.font_style, bg="#f0f0f0", fg="black")
        self.class_list_label.grid(row=1, column=2, pady=10, sticky='n')
        self.class_listbox = tk.Listbox(self.master, width=50, height=20, font=self.font_style)
        self.class_listbox.grid(row=2, column=2, padx=10, pady=10, rowspan=5, sticky='nsew')
        # Make the list scrollable
        scrollbar = tk.Scrollbar(self.master, orient="vertical", command=self.class_listbox.yview)
        scrollbar.grid(row=2, column=3, rowspan=5, sticky='ns')
        self.class_listbox.config(yscrollcommand=scrollbar.set)

        # Calculate GPA
        self.submit_button = tk.Button(self.master, text="Calculate GPA", command=self.calculate_gpa, bg="#FF5722", fg="black", padx=10, pady=5, borderwidth=0, font=self.font_style)
        self.submit_button.grid(row=3, column=0, columnspan=2, pady=10, sticky='w')

        # Help Button on the GPA calculator page
        self.help_button_gpa_calculator = tk.Button(self.master, text="Help", command=self.display_help_page, bg="#2196F3", fg="black", padx=10, pady=5, borderwidth=0, font=self.font_style)
        self.help_button_gpa_calculator.grid(row=4, column=0, columnspan=2, pady=10, sticky='w')

    def add_class(self):
        class_window = tk.Toplevel(self.master)
        class_window.title("Add Class")
        class_window.geometry("250x150")  # Set window size
        class_window.configure(bg="#f0f0f0")  # Set background color
        self.center_window(class_window)  # Center the window on the screen

        # Class Name
        label_name = tk.Label(class_window, text="Enter class name:", font=self.font_style, bg="#f0f0f0", fg="black")
        label_name.grid(row=0, column=0, pady=5)
        entry_name = tk.Entry(class_window, font=self.font_style)
        entry_name.grid(row=0, column=1, pady=5)

        # Class Grade
        label_grade = tk.Label(class_window, text="Enter grade:", font=self.font_style, bg="#f0f0f0", fg="black")
        label_grade.grid(row=1, column=0, pady=5)
        entry_grade = tk.Entry(class_window, font=self.font_style)
        entry_grade.grid(row=1, column=1, pady=5)

        # Weighted Checkbox
        weighted_var = tk.BooleanVar()
        check_button = tk.Checkbutton(class_window, text="Weighted", variable=weighted_var, font=self.font_style, bg="#f0f0f0", fg="black")
        check_button.grid(row=2, column=0, columnspan=2, pady=5)

        # Submit Class Button
        submit_button = tk.Button(class_window, text="Submit", command=lambda: self.save_class(entry_name.get(), entry_grade.get().upper(), weighted_var.get(), class_window), bg="#4CAF50", fg="black", padx=10, pady=5, borderwidth=0, font=self.font_style)
        submit_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Set row and column weights for resizing
        for i in range(4):
            class_window.grid_rowconfigure(i, weight=1)
            class_window.grid_columnconfigure(i, weight=1)

    def save_class(self, name, grade, weighted, class_window):
        # Check if the entered grade is valid
        if self.is_freshman:
            if grade not in ["A", "B", "C", "D", "F"]:
                messagebox.showerror("Error", "Please enter a valid letter grade (A, B, C, D, F) for freshmen.")
                return
        else:
            if grade not in ["A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-", "F"]:
                messagebox.showerror("Error", "Please enter a valid letter grade.")
                return

        # Save class data
        self.class_data.append((name, grade, weighted))
        self.num_classes += 1
        self.class_listbox.insert(tk.END, name)
        class_window.destroy()

    def delete_class(self):
        # Get selected class index
        selected_index = self.class_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "Please select a class to delete.")
            return

        # Remove selected class from listbox and class data
        index = selected_index[0]
        del self.class_data[index]
        self.class_listbox.delete(index)
        self.num_classes -= 1

    def calculate_gpa(self):
        if not self.class_data:
            messagebox.showerror("Error", "Please add classes before calculating GPA.")
            return

        # GPA Mapping based on freshman or not
        if self.is_freshman:
            grade_mapping = {"A": 4.00, "B": 3.00, "C": 2.00, "D": 1.00, "F": 0}
        else:
            grade_mapping = {
                "A": 4.00, "A-": 3.66, "B+": 3.33, "B": 3.00,
                "B-": 2.66, "C+": 2.33, "C": 2.00, "C-": 1.66,
                "D+": 1.33, "D": 1.00, "D-": 0.66, "F": 0
            }

        weighted_gpa_sum = 0
        unweighted_gpa_sum = 0
        for _, grade, weighted in self.class_data:
            gpa = grade_mapping.get(grade, 0)

            if weighted and grade != "F":  # Exclude the +1 bonus for weighted F
                gpa += 1.0

            weighted_gpa_sum += gpa

            # Update unweighted GPA sum without the weight bonus
            unweighted_gpa_sum += grade_mapping.get(grade, 0)

        total_weighted_gpa = weighted_gpa_sum / self.num_classes

        # Ensure unweighted GPA does not exceed 4.0
        total_unweighted_gpa = min(unweighted_gpa_sum / self.num_classes, 4.0)

        # Display GPA
        messagebox.showinfo("GPA Results", f"Your weighted GPA is: {total_weighted_gpa:.2f}\nYour unweighted GPA is: {total_unweighted_gpa:.2f}")

    def display_help_page(self):
        help_window = tk.Toplevel(self.master)
        help_window.title("Help Page")
        help_window.geometry("800x450")  # Set window size
        help_window.configure(bg="#f0f0f0")  # Set background color
        self.center_window(help_window)  # Center the window on the screen

        help_text = """
        Welcome to the GPA Calculator Help Page!

        This program allows you to calculate your GPA based on the classes you've taken.

        If you are a freshman, the grading scale is as follows:
        A: 4.00, B: 3.00, C: 2.00, D: 1.00, F: 0.00

        If you are not a freshman, the grading scale includes '+' and '-' symbols:
        A: 4.00, A-: 3.66, B+: 3.33, B: 3.00, B-: 2.66, C+: 2.33, C: 2.00,
        C-: 1.66, D+: 1.33, D: 1.00, D-: 0.66, F: 0.00
        (For those who took high school classes as a class of 2027 student or below before the new grading system, refer to this)

        To use the GPA Calculator:
        1. Select whether you are a freshman or not.
        2. Enter the details of each class, including the class name, grade, and whether it is weighted.
        3. Click the 'Calculate GPA' button to view your GPA.

        Click the button below to return to the program.
        """

        help_label = tk.Label(help_window, text=help_text, justify=tk.LEFT, bg="#f0f0f0", fg="black", font=self.font_style)
        help_label.pack(padx=20, pady=20)

        return_button = tk.Button(help_window, text="Return to Program", command=help_window.destroy, bg="#4CAF50", fg="black", padx=10, pady=5, borderwidth=0, font=self.font_style)
        return_button.pack(pady=10)

    def center_window(self, window):
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

def main():
    root = tk.Tk()
    app = GPACalculatorApp(root) 
    root.mainloop()

if __name__ == "__main__":
    main()
