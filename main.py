import random
import os
import json
from word import Word

# Initialize the main words dictionary
words = {}

# Read the word definitions from JSON file
with open("words.json", "r") as json_file:
    word_data = json.load(json_file)

for word, data in word_data.items():
    words[word] = Word(word, data["definitions"])

msg = "Please state your name to read your profile!\nIf you do not have a profile yet, just specify your name for a new profile: "
username = input(msg).lower()

if not username.isalnum():
    print("Profile name must be only alphanumeric (i.e., contains only letters and digits). Please provide a new username!")
    exit(1)

# Check if the file exists
profile_path = f"profiles/{username}.prof"
if os.path.exists(profile_path):
    print(f"Profile '{username}' found! Now loading your profile.\n\n")

    # Initialize the scores
    with open(profile_path) as inp:
        for line in inp:
            word, score = line.strip().split("\t", 1)
            words[word].set_score(score)
else:
    print(f"Profile '{username}' not found! Creating a new profile with that name.\n\n")

# Separate the words into completely learned words and to-learn words
to_learn = {}
complete = {}
for word, word_obj in words.items():
    if word_obj.is_learned():
        complete[word] = word_obj
    else:
        to_learn[word] = word_obj

if not to_learn:
    print("All words have been mastered! You can create a new profile and start from scratch.")
    exit(1)

correct_count = 0
wrong_count = 0

stop = False
while not stop:

    # Randomly choose the quiz type
    quiz_type = random.choice(["word_to_def", "def_to_word"])

    # Randomly obtain a new word to quiz
    main_word = random.choice(list(to_learn.keys()))
    main_definition = words[main_word].get_random_definition()

    # Randomly select 4 alternative words that are not the main word
    alt_words = random.sample([w for w in words.keys() if w != main_word], 4)

    if quiz_type == "word_to_def":
        # Word to Definition quiz
        definitions = [main_definition]
        definitions.extend([words[alt_word].get_random_definition() for alt_word in alt_words])
        random.shuffle(definitions)

        # Obtain the correct answer index
        main_definition_idx = definitions.index(main_definition)

        # Quiz the word
        print(f"The word is: {main_word.upper()}. Please choose the correct definition.")
        for i, definition in enumerate(definitions):
            print(f"    {i+1} -  {definition}")

    else:
        # Definition to Word quiz
        word_choices = [main_word] + alt_words
        random.shuffle(word_choices)

        # Obtain the correct answer index
        main_word_idx = word_choices.index(main_word)

        # Quiz the definition
        print(f"Definition: {main_definition}\nPlease choose the correct word:")
        for i, word in enumerate(word_choices):
            print(f"    {i+1} -  {word.upper()}")

    # Obtain a valid response
    valid = False
    while not valid:
        # Obtain the response
        response = input("\nYour answer is: ").lower()

        # Check if the response is to quit
        if response == "q":
            valid = True
            stop = True

        # Check if the response is a digit
        elif response.isdigit():
            val = int(response)

            # Check if the digit is in the correct range
            if val in range(1, 6):
                # This is a valid answer
                valid = True

                # Check if the answer is correct
                is_correct = (quiz_type == "word_to_def" and val == main_definition_idx + 1) or \
                             (quiz_type == "def_to_word" and val == main_word_idx + 1)

                if is_correct:
                    print("CORRECT!\n")
                    correct_count += 1
                    words[main_word].update_correct()
                else:
                    print("WRONG!\n")
                    wrong_count += 1
                    words[main_word].update_wrong()

                if quiz_type == "word_to_def":
                    print(f"{main_word.upper()} - {main_definition}\n\n")
                else:
                    print(f"{main_word.upper()} - {main_definition}\n\n")

                # Check if the word is learned. If learned, remove from to_learn and add to complete
                if words[main_word].is_learned():
                    del to_learn[main_word]
                    complete[main_word] = words[main_word]

        if not valid:
            print("Please provide a number between 1 and 5. To quit the program, type 'q'.")

print(f"""
FINAL RESULTS:
  Correct answers: {correct_count}
  Wrong answers: {wrong_count}
  Total words mastered: {len(complete)} / {len(words)} ({len(complete)*100.0/len(words):.2f}%)
""")

with open(profile_path, "w") as out:
    for word, word_obj in words.items():
        out.write(word_obj.get_score_str())