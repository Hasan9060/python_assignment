import random

def generate_secret_number():
    return str(random.randint(100, 999))  # Generates a 3-digit number

def get_feedback(secret, guess):
    feedback = []
    for i in range(3):
        if guess[i] == secret[i]:  # Correct digit in the correct place
            feedback.append("👌")  
        elif guess[i] in secret:  # Correct digit in the wrong place
            feedback.append("👍")  
        else:  # No correct digits
            feedback.append("❌")  
    return "".join(feedback)

def play_game():
    secret_number = generate_secret_number()
    attempts = 10

    print("Welcome to the Guessing Game! 🤔")
    print("Try to guess the secret 3-digit number!")

    for attempt in range(1, attempts + 1):
        guess = input(f"Attempt {attempt}/{attempts} - Enter a 3-digit number: ")

        if not guess.isdigit() or len(guess) != 3:
            print("Invalid input! Please enter a valid 3-digit number.")
            continue

        feedback = get_feedback(secret_number, guess)
        print(feedback)

        if guess == secret_number:
            print("🎉 You Got IT! The secret number was:", secret_number)
            break
    else:
        print("❌ Game Over! The secret number was:", secret_number)

play_game()
