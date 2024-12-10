# Documentation

## Description
A simple application written in Python using the Tkinter library that allows users to answer quiz questions stored in JSON files. The application supports hints, displaying the number of correct answers, and allows users to manage question sets through an interactive menu.

---

## Features
1. **Dynamic Question Set Selection**:
   - Users can select a question set from a dynamically generated menu. The sets are loaded from `config.json`.

2. **Add New Question Set**:
   - A form allows users to add a new question set by providing a name and selecting a JSON file. The configuration is automatically updated.

3. **Delete Question Set**:
   - Users can delete an existing question set directly from the menu.

4. **Answer Questions**:
   - Users can select answers by clicking buttons. Correct answers are highlighted in green, and incorrect ones in red.

5. **Hints**:
   - Clicking the `Hint` button highlights correct answers in orange.

6. **Display Number of Correct Answers**:
   - The top-left corner of the application shows the number of correct answers for the current question.

7. **Next Question**:
   - The `Next question` button loads a new random question from the selected set.

---

## JSON File Structure
Each question set JSON file should follow this format:

```json
[
    {
        "question": "Question 1?",
        "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
        "answers": ["Correct Answer"]
    },
    {
        "question": "Question 2?",
        "options": ["Option A", "Option B", "Option C", "Option D"],
        "answers": ["Correct Answer"]
    }
]
```

---

## Configuration File Structure
The `config.json` file manages available question sets and should follow this format:

```json
[
    {
        "name": "ITU",
        "questions": "questions_ITU.json"
    },
    {
        "name": "ITA",
        "questions": "questions_ITA.json"
    }
]
```

---

## Running the Application
1. **Prepare the Environment**:
   - Ensure Python version 3.x is installed.

2. **Download Files**:
   - Save the main script as `quiz_app.py`.
   - Create the necessary JSON files for questions and a `config.json` file.

3. **Start the Application**:
   - Open a terminal or command prompt.
   - Navigate to the folder containing `quiz_app.py`.
   - Run the command:
     ```bash
     python quiz_app.py
     ```

4. **Using the Application**:
   - Select a question set from the menu.
   - Answer questions by clicking on the options.
   - Use the `Hint` button for help.
   - Add or delete question sets directly from the menu.

---

## Notes
- The application is designed for educational purposes and simplifies quiz management.
- Contributions, including new question sets or features, are welcome.
- The current question sets are based on study materials for ITU.

---