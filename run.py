import tkinter as tk
from tkinter import messagebox, filedialog
import random
import json
import os

# Function to load quiz data from a JSON file
def load_quiz_data(file_name):
    try:
        script_dir = os.path.dirname(__file__)  # Directory of the script
        file_path = os.path.join(script_dir, file_name)
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load quiz data: {e}")
        return []

# Function to load menu configuration
def load_menu_config():
    try:
        script_dir = os.path.dirname(__file__)  # Directory of the script
        file_path = os.path.join(script_dir, "config.json")
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load menu configuration: {e}")
        return []

# Function to save menu configuration
def save_menu_config(config):
    try:
        script_dir = os.path.dirname(__file__)  # Directory of the script
        file_path = os.path.join(script_dir, "config.json")
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(config, file, indent=4)
        messagebox.showinfo("Success", "Configuration updated successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save menu configuration: {e}")

# Initialize global variables
quiz_data = []
selected_answers = set()  # To track the user's selected answers

# Function to check the answer
def check_answer(selected_option, correct_answers, option_button):
    global selected_answers
    if selected_option in correct_answers:
        selected_answers.add(selected_option)  # Add correct answer to the set
        option_button.config(bg="green", fg="white")
    else:
        option_button.config(bg="red", fg="white")
        messagebox.showerror("Incorrect!", "Sorry, that's incorrect!")
        return  # Exit early if an incorrect answer is clicked

    # Check if all correct answers have been selected
    if selected_answers == set(correct_answers):
        # Highlight all correct answers
        for btn in option_buttons:
            if btn.cget("text") in correct_answers:
                btn.config(bg="green", fg="white")
        messagebox.showinfo("Correct!", "You have selected all correct answers!")
        selected_answers.clear()  # Reset for the next question
        display_question()

# Function to highlight correct answers (Hint button functionality)
def show_hint():
    for btn in option_buttons:
        if btn.cget("text") in correct_answers.get():
            btn.config(bg="orange", fg="black")

# Function to display a random question
def display_question():
    global quiz_data
    if not quiz_data:
        messagebox.showerror("Error", "No quiz data available.")
        return

    # Reset button colors (cross-platform compatible)
    for btn in option_buttons:
        btn.config(bg="lightgray", fg="black")

    question = random.choice(quiz_data)
    question_text.set(question["question"])
    correct_answers.set(question["answers"])
    correct_count.set(f"Correct answers: {len(question['answers'])}")
    for i, option in enumerate(question["options"]):
        option_buttons[i].config(
            text=option,
            command=lambda opt=option, btn=option_buttons[i]: check_answer(opt, correct_answers.get(), btn)
        )

# Function to start the quiz with the selected question set
def start_quiz(file_name):
    global quiz_data
    quiz_data = load_quiz_data(file_name)
    if quiz_data:
        menu_frame.pack_forget()  # Hide the menu
        quiz_frame.pack()  # Show the quiz interface
        display_question()

# Function to return to the menu
def return_to_menu():
    quiz_frame.pack_forget()  # Hide the quiz interface
    menu_frame.pack()  # Show the menu

# Function to open form for adding a new question set
def open_add_form():
    def save_new_set():
        name = name_entry.get()
        file_path = file_entry.get()
        if not name or not file_path:
            messagebox.showerror("Error", "Both fields are required!")
            return
        new_item = {"name": name, "questions": file_path}
        config = load_menu_config()
        config.append(new_item)
        save_menu_config(config)
        add_form.destroy()
        refresh_menu()

    def browse_file():
        file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        file_entry.delete(0, tk.END)
        file_entry.insert(0, file_path)

    add_form = tk.Toplevel(root)
    add_form.title("Add New Question Set")

    tk.Label(add_form, text="Name:").pack(pady=5)
    name_entry = tk.Entry(add_form, width=30)
    name_entry.pack(pady=5)

    tk.Label(add_form, text="File Path:").pack(pady=5)
    file_entry = tk.Entry(add_form, width=30)
    file_entry.pack(pady=5)

    browse_button = tk.Button(add_form, text="Browse", command=browse_file)
    browse_button.pack(pady=5)

    save_button = tk.Button(add_form, text="Save", command=save_new_set)
    save_button.pack(pady=10)

# Function to delete a question set
def delete_set(name):
    config = load_menu_config()
    config = [item for item in config if item["name"] != name]
    save_menu_config(config)
    refresh_menu()

# Function to refresh menu buttons
def refresh_menu():
    for widget in menu_frame.winfo_children():
        widget.destroy()

    menu_label = tk.Label(menu_frame, text="Select a question set:", font=("Arial", 14))
    menu_label.pack(pady=20)

    menu_config = load_menu_config()
    for item in menu_config:
        button_frame = tk.Frame(menu_frame)
        button_frame.pack(pady=5, fill="x")

        button = tk.Button(button_frame, text=item["name"], command=lambda file=item["questions"]: start_quiz(file), font=("Arial", 12, "bold"), width=20, anchor="w")
        button.pack(side="left", padx=5)

        delete_button = tk.Button(button_frame, text="Delete", command=lambda name=item["name"]: delete_set(name), font=("Arial", 12, "bold"), width=10)
        delete_button.pack(side="left", padx=5)

    add_set_button = tk.Button(menu_frame, text="Add New Set", command=open_add_form, font=("Arial", 12, "bold"), width=30)
    add_set_button.pack(pady=10)

# Create the GUI
root = tk.Tk()
root.title("Quiz App")

# Menu frame for selecting the question set
menu_frame = tk.Frame(root)
menu_frame.pack()

refresh_menu()

# Quiz frame for displaying questions
quiz_frame = tk.Frame(root)

question_text = tk.StringVar()
correct_answers = tk.StringVar()
correct_count = tk.StringVar()

# Display correct answer count
correct_count_label = tk.Label(quiz_frame, textvariable=correct_count, font=("Arial", 10), anchor="w", justify="left")
correct_count_label.pack(anchor="nw", padx=10, pady=5)

# Question label
question_label = tk.Label(quiz_frame, textvariable=question_text, wraplength=600, font=("Arial", 12), justify="center")
question_label.pack(pady=20)

# Option buttons
option_buttons = []
for i in range(4):
    btn = tk.Button(quiz_frame, text="", width=100, wraplength=500, font=("Arial", 10), anchor="w", justify="left")
    btn.pack(pady=5)
    option_buttons.append(btn)

# Buttons for Next Question, Hint, and Return to Menu
button_frame = tk.Frame(quiz_frame)
button_frame.pack(pady=20)

next_button = tk.Button(button_frame, text="Next question", command=display_question, font=("Arial", 12, "bold"))
next_button.pack(side="left", padx=10)

hint_button = tk.Button(button_frame, text="Hint", command=show_hint, font=("Arial", 12, "bold"))
hint_button.pack(side="left", padx=10)

menu_button = tk.Button(button_frame, text="Return to Menu", command=return_to_menu, font=("Arial", 12, "bold"))
menu_button.pack(side="left", padx=10)

# Run the app
root.mainloop()
