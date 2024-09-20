import random
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import time

def update_background(event=None):
    global bg_image  # Declare bg_image as global to prevent garbage collection

    width = root.winfo_width()
    height = root.winfo_height()

    try:
        image_path = r"C:\Users\yashd\OneDrive\Desktop\internship projects\Project1-Number game\Project_one\bgimage.png"
        print(f"Attempting to load image from: {image_path}")

        # Load and resize the image
        image = Image.open(image_path)
        image = image.resize((width, height), Image.LANCZOS)
        bg_image = ImageTk.PhotoImage(image)

        # Update the background label
        bg_label.config(image=bg_image)
        bg_label.image = bg_image  # Keep a reference to avoid garbage collection
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # Cover the entire window

    except Exception as e:
        print(f"Error loading background image: {e}")

def start_game():
    global number, remaining_attempts, level, game_active, start_time
    level = level_var.get()

    level_mapping = {
        "Easy": (0, 100, 7),
        "Medium": (0, 100, 5),
        "Hard": (0, 100, 3)
    }

    if level not in level_mapping:
        messagebox.showerror("Invalid Input", "Please select a valid level.")
        return

    min_value, max_value, max_attempts = level_mapping[level]
    number = random.randint(min_value, max_value)
    remaining_attempts = max_attempts

    game_active = True
    start_time = time.time()  # Start the timer

    # Update result_label with multiline message
    result_label.config(text=f"Game started!\nLevel: {level}\nEnter a number between {min_value} and {max_value}.", fg="orange", width=50)
    result_label.pack(pady=(10, 20))  # Adjust placement above guess entry

    attempts_label.config(text=f"Remaining Attempts: {remaining_attempts}")

    # Hide level selection elements
    level_heading.pack_forget()
    level_frame.pack_forget()
    start_button.pack_forget()

    # Start the timer update
    update_timer()

def update_timer():
    global game_active

    if game_active:
        elapsed_time = int(time.time() - start_time)
        remaining_time = max(0, 60 - elapsed_time)  # 60 seconds countdown
        timer_label.config(text=f"Time Left: {remaining_time} seconds", fg="red")

        if remaining_time > 0:
            root.after(1000, update_timer)  # Update the timer every second
        else:
            result_label.config(text="Time's up! Game over.", fg="red")
            submit_button.config(state=tk.DISABLED)
            game_active = False

def check_guess():
    global remaining_attempts, number, game_active

    if not game_active:
        return

    try:
        guess = int(guess_entry.get())
    except ValueError:
        result_label.config(text="Please enter a valid number.", fg="red")
        return

    if remaining_attempts > 0:
        remaining_attempts -= 1
        if guess > number:
            result_label.config(text="Too high! Try again.", fg="orange")
        elif guess < number:
            result_label.config(text="Too low! Try again.", fg="orange")
        else:
            result_label.config(text="Congratulations! You've guessed the number!", fg="green")
            result_label.config(bg="lightgreen")
            submit_button.config(state=tk.DISABLED)
            game_active = False
            return
    else:
        result_label.config(text="Game over. No attempts left.", fg="red")
        submit_button.config(state=tk.DISABLED)
        game_active = False
        return

    attempts_label.config(text=f"Remaining Attempts: {remaining_attempts}")

    if remaining_attempts == 0:
        result_label.config(text=f"Game over. The number was {number}.", fg="red")
        game_active = False

def reset_game():
    global number, remaining_attempts, level, game_active, start_time

    # Reset all game variables to initial state
    number = None
    remaining_attempts = 0
    level = None
    game_active = False
    start_time = None

    # Reset UI elements
    guess_entry.delete(0, tk.END)
    result_label.config(text="", bg="#333333")
    attempts_label.config(text="")
    level_var.set(None)

    # Reset level selection buttons
    easy_rb.config(bg="light yellow")
    medium_rb.config(bg="light yellow")
    hard_rb.config(bg="light yellow")

    # Show level selection elements
    level_heading.pack(pady=10)
    level_frame.pack(pady=10)
    easy_rb.pack(side=tk.LEFT, padx=5)
    medium_rb.pack(side=tk.LEFT, padx=5)
    hard_rb.pack(side=tk.LEFT, padx=5)
    start_button.pack(pady=10, fill=tk.X)

    # Enable submit button
    submit_button.config(state=tk.NORMAL)

    # Reset timer label
    timer_label.config(text="Time Left: 60 seconds", fg="red")

    # Update background image
    update_background()

    # Clear any existing game messages
    result_label.config(text="")

    # Update game state
    game_active = False
    
    
# Setting up the main window
root = tk.Tk()
root.title("Number Guessing Game")

# Maximize the window
root.state('zoomed')

# Set the initial window size to fit the screen
screen_width = 1000
screen_height = 600
root.geometry(f"{screen_width}x{screen_height}")

# Allow resizing
root.resizable(True, True)

# Initialize the background label
bg_label = tk.Label(root)
bg_label.place(relwidth=1, relheight=1)

# Update background image when window size changes
root.bind("<Configure>", update_background)

# Game title
title_label = tk.Label(root, text="Number Guessing Game", font=("Helvetica", 32, "bold"), fg="Red", bg="#333333")
title_label.pack(pady=20)

# Frame for buttons and input fields
frame = tk.Frame(root, bg="light yellow", bd=5, relief="flat")
frame.pack(side=tk.LEFT, padx=(80, 0), pady=80, anchor='w')

# Level heading
level_heading = tk.Label(frame, text="Select Level:", font=("Helvetica", 18, "bold"), fg="red", bg="light yellow")
level_heading.pack(pady=10)

# Creating the level selection radio buttons in one line
level_var = tk.StringVar(value=None)

level_frame = tk.Frame(frame, bg="light yellow")
level_frame.pack(pady=10)

easy_rb = tk.Radiobutton(level_frame, text="Easy", variable=level_var, value="Easy", font=("Helvetica", 14), bg="light yellow", selectcolor="#009688", indicatoron=0)
easy_rb.pack(side=tk.LEFT, padx=5)

medium_rb = tk.Radiobutton(level_frame, text="Medium", variable=level_var, value="Medium", font=("Helvetica", 14), bg="light yellow", selectcolor="#009688", indicatoron=0)
medium_rb.pack(side=tk.LEFT, padx=5)

hard_rb = tk.Radiobutton(level_frame, text="Hard", variable=level_var, value="Hard", font=("Helvetica", 14), bg="light yellow", selectcolor="#009688", indicatoron=0)
hard_rb.pack(side=tk.LEFT, padx=5)

start_button = tk.Button(frame, text="Start Game", font=("Helvetica", 14), bg="#009688", fg="white", command=start_game)
start_button.pack(pady=10, fill=tk.X)

# Result label adjusted position
result_label = tk.Label(frame, text="", font=("Helvetica", 14), bg="light yellow", fg="yellow", width=50)
result_label.pack(pady=10)  # Adjust placement below level selection

guess_label = tk.Label(frame, text="Enter your guess:", font=("Helvetica", 14), fg="red", bg="light yellow")
guess_label.pack(pady=5)

guess_entry = tk.Entry(frame, font=("Helvetica", 14), bd=2, relief="solid")
guess_entry.pack(pady=5)

submit_button = tk.Button(frame, text="Submit Guess", font=("Helvetica", 14), bg="#009688", fg="white", command=check_guess)
submit_button.pack(pady=10, fill=tk.X)

attempts_label = tk.Label(frame, text="", font=("Helvetica", 12), fg="green", bg="light yellow")
attempts_label.pack(pady=5)

# Timer label
timer_label = tk.Label(frame, text="Time Left: 60 seconds", font=("Helvetica", 12), fg="red", bg="light yellow")
timer_label.pack(pady=5)

reset_button = tk.Button(frame, text="Reset Game", font=("Helvetica", 14), bg="#ff5722", fg="white", command=reset_game)
reset_button.pack(pady=10, fill=tk.X)

# Initialize game state
game_active = False
start_time = None

# Start the Tkinter main loop
root.mainloop()
