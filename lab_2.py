import random
import string

def main():
    length = ask_length("Длина пароля: ")
    chosen_sets = build_charset()

    if not chosen_sets:
        print("Не выбрано ни одного типа!")
        return

    password = generate_password(length, chosen_sets)
    print(f"пароль: {password}")

def generate_password(length, chosen_sets):
    password_chars = []

    if length < len(chosen_sets):
        while len(password_chars) < length:
            password_chars.append(random.choice("".join(chosen_sets)))

    else:
        for s in chosen_sets:
            password_chars.append(random.choice(s))

        all_chars = "".join(chosen_sets)
        while len(password_chars) < length:
            password_chars.append(random.choice(all_chars))

        random.shuffle(password_chars)

    return "".join(password_chars)

def build_charset():
    chosen_sets = []

    if ask_yes_no("Буквы в нижнем регистре? (y/n): "):
        chosen_sets.append(string.ascii_lowercase)

    if ask_yes_no("Буквы в верхнем регистре? (y/n): "):
        chosen_sets.append(string.ascii_uppercase)

    if ask_yes_no("Цифры? (y/n): "):
        chosen_sets.append(string.digits)

    if ask_yes_no("Спецсимволы? (y/n): "):
        chosen_sets.append(string.punctuation)

    return chosen_sets

def ask_length(question):
    while True:
        try:
            answer = int(input(question))
            if answer > 0:
                return answer
        except ValueError:
            print("Введите число")
            continue


def ask_yes_no(question):
    while True:
        answer = input(question)
        if answer.lower() == "y":
            return True
        elif answer.lower() == "n":
            return False
        print("Введите y или n!")


if __name__ == "__main__":
    main()