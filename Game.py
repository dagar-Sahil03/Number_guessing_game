import random

# Get user input for the maximum level
max_value = int(input('Enter your level: '))

# Check if the entered level is zero
if max_value == 0:
    print("\n\tLevel zero is not available\n\t\tGame over\n\nError: Invalid level")
    exit()  # Terminate the game

# Initialize remaining attempts and calculate based on the level
remaining_attempts = 75 // max_value

# Initialize player and bot states
player_state = False
bot_state = False

# Determine the level based on the maximum value
if max_value <= 10:
    level = "Easy"
elif 10 < max_value <= 40:
    level = "Hard"
else:
    level = "Impossible"
    remaining_attempts = max(1, remaining_attempts - (15 // max_value))  # Avoid negative attempts

# Display the chosen level and the number of attempts
print('Level applied: ', level, "\nYou got", remaining_attempts, "attempts")

# Generate a random number for the player to guess
number = random.randint(1, max_value)

# Allow the player to make guesses for the remaining attempts
while remaining_attempts > 0:
    try:
        # Get user input for the guess
        guess = int(input('\nEnter your guess: '))
        
        # Bot makes a guess in every attempt
        bot_input = random.randint(1, max_value)

        # Check if the bot's guess matches the number
        if bot_input == number:
            bot_state = True
            print("Bot guessed the number correctly!")
            break

        # Provide feedback based on the user's guess
        if guess > number:
            print('Too high')
        elif guess < number:
            print('Too low')
        else:
            player_state = True
            bonus = float(remaining_attempts + 10)
            remaining_attempts += bonus
            print("\nCongratulations, you got", bonus, "bonus points!")
            break

        remaining_attempts -= 1

    except ValueError:
        print("\nInvalid Input\n")

# Display game over message
print("\nGame over")

# Check if the player or bot won the game
if player_state:
    print("You win!")
elif bot_state:
    print("Bot wins!")
else:
    print("You lose the game\n")
