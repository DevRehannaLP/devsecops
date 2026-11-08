# Add getpass hides the password as it is entered for security
import getpass


def greet(name):
    return f"Hello {name}, you're cyberdev environment is running smoothly."


def farewell(name):
    return f"Goodbye {name}, see you next session!"


def check_password_strength():
    #    password = input("Enter a password to analyze: ") is not changed to:
    password = getpass.getpass("Enter a password to analyze: ")

    print("\nAnalyzing password...\n")

    score = 0

    suggestions = []

    # Rule 1: length
    if len(password) < 12:
        print("❌ Password too short - must be at least 12 characters.")
        suggestions.append("Use at least 12 characters for your password.")
    else:
        print("✅ Length is good.")
        score += 1

    # Rule 2: uppercase
    if any(c.isupper() for c in password):
        print("✅ Uppercase letter found.")
        score += 1
    else:
        print("❌ No uppercase letter found.")
        suggestions.append("Use an uppercase letter.")

    # Rule 3: lowercase
    if any(c.islower() for c in password):
        print("✅ Lowercase letter found.")
        score += 1
    else:
        print("❌ No lowercase letter found.")
        suggestions.append("Use a lowercase letter.")

    # Rule 4: Check for numbers
    if any(c.isdigit() for c in password):
        print("✅ Number found.")
        score += 1
    else:
        print("❌ No number found.")
        suggestions.append("Use a number in your password.")

    # Rule 5: Check for symbols (special characters)
    if any(not c.isalnum() for c in password):
        print("✅ Symbol found.")
        score += 1
    else:
        print("❌ No symbol found.")
        suggestions.append("Use a symbol in your password.")

    print(f"\nFinal Strength Rating:")
    print(f"Score: {score}/5")

    if score == 5:
        print("💪🏾 Strong")
    elif score >= 3:
        print("👍🏾 Medium")
    else:
        print("⚠️ Weak")

    if suggestions:
        print("\nSuggestions to improve your password:")
        for tip in suggestions:
            print("-", tip)


def main():
    while True:
        print("Choose an option")
        print("1. Greet me")
        print("2. Say goodbye")
        print("3. Check password strength")
        print("4. Exit")

        choice = input("Enter choice (1/2/3/4): ")

        if choice == "1":
            user_name = input("Enter your name: ")
            print(greet(user_name))

        elif choice == "2":
            user_name = input("Adios!: ")
            print(farewell(user_name))

        elif choice == "3":
            check_password_strength()

        elif choice == "4":
            print("Exiting program...Goodbye!")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
# Next session: add hidden password input using getpass
