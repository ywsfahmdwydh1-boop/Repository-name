import tkinter as tk
import random

correct_guess = random.randint(1, 10)
attempts = 0

def check_guess():
    global attempts

    try:
        guess = int(entry.get())
    except ValueError:
        result.config(text="اكتب رقمًا صحيحًا فقط")
        return

    attempts += 1
    attempts_label.config(text=f"المحاولات: {attempts}")

    if guess == correct_guess:
        result.config(text=f"صح! الرقم هو {correct_guess}")
        guess_button.config(state="disabled")
    elif guess < correct_guess:
        result.config(text="أعلى من كده")
    else:
        result.config(text="أقل من كده")

def new_game():
    global correct_guess, attempts

    correct_guess = random.randint(1, 10)
    attempts = 0

    entry.delete(0, tk.END)
    result.config(text="خمن رقم من 1 إلى 10")
    attempts_label.config(text="المحاولات: 0")
    guess_button.config(state="normal")
    entry.focus_set()

window = tk.Tk()
window.title("لعبة خمن الرقم")
window.geometry("400x450")
window.resizable(False, False)

title = tk.Label(
    window,
    text="لعبة خمن الرقم",
    font=("Arial", 24, "bold")
)
title.pack(pady=30)

instruction = tk.Label(
    window,
    text="خمن رقم من 1 إلى 10",
    font=("Arial", 16)
)
instruction.pack(pady=10)

entry = tk.Entry(
    window,
    font=("Arial", 20),
    justify="center"
)
entry.pack(pady=20)
entry.focus_set()

guess_button = tk.Button(
    window,
    text="خمن",
    font=("Arial", 16),
    command=check_guess
)
guess_button.pack(pady=10)

result = tk.Label(
    window,
    text="خمن رقم من 1 إلى 10",
    font=("Arial", 15)
)
result.pack(pady=20)

attempts_label = tk.Label(
    window,
    text="المحاولات: 0",
    font=("Arial", 14)
)
attempts_label.pack(pady=10)

new_game_button = tk.Button(
    window,
    text="لعبة جديدة",
    font=("Arial", 14),
    command=new_game
)
new_game_button.pack(pady=20)

window.bind("<Return>", lambda event: check_guess())
window.mainloop()