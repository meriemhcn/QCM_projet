# Introduction:
This project focuses on developing a Multiple-Choice Questionnaire (MCQ) application designed for Computer Science students. The application offers some functionalities and services to enhance the learning experience by providing a simple, interactive platform for knowledge assessment and progress tracking.

# Project description:
## Features and functionalities:
### User management:
profile creation:
-Users can create a unique profile upon their first use by providing an identifier.
history display:
-Users can view their past performance, including scores, selected categories, and dates of previous quizzes.
Question and answer management:
load questions from file:
-Questions are dynamically loaded from a JSON file, ensuring flexibility and easy updates.
category selection:
-Users can select from predefined categories such as Python, Networks, and Algorithms.
Evaluation and feedback:
score calculation:
-The application automatically calculates the user’s score based on correct and incorrect answers.
-The score is displayed at the end of the quiz, providing immediate performance feedback
feedback on answers:
-After each question, users receive instant feedback on their answers.
-If the answer is incorrect, the correct answer is displayed, helping users learn and improve.
Quiz functionality:
global timer:
-The quiz automatically ends when the timer runs out, and a message is displayed to inform the user.
result export:
-The application automatically saves quiz results, including user scores and performance details, to a CSV file.
Graphical interface:
simple design:
-The application features an easy-to-use interface with clear navigation.


Technical choices:
Programming language:
Python:
Used as the primary language for backend logic, GUI handling, and managing file operations.
GUI framework:
	Tkinter:Utilized for creating the graphical user interface (GUI) of the application. It handles the layout, user inputs, and interaction with various components like buttons, labels, and input fields.
	Tkmacosx: third-party library used specifically for creating custom-styled buttons that are compatible with macOS. This ensures the application has a consistent look across platforms.
	Ttk:for applying additional styling to widgets, like combo boxes, and creating a more modern look for the GUI.
	Pillow:used for displaying and editing images,used for displaying the logo at the beginning.
Data Serialization and Storage:
	JSON:Used for storing and retrieving user data (utilisateurs.json) and quiz questions  (questions.json).
	CSV:Used for exporting quiz results to a .csv file. It stores quiz data like date,time,score..etc.
Data structures:
	user data:
	-Outer Dictionary:stores user data by username.
	-Nested Dictionary:stores user-specific information like "historique".
	-Nested List:stores multiple quiz attempts.
	-Nested Dictionary(stores information for each quiz attempt, such as date, categorie, score, and total_questions.
	questions and answers data:
	–List:stores multiple questions.
	-Nested Dictionary:stores information for each question, including categorie, question, options, and correcte.


Application architecture:
Data flow architecture:
User Profile Management:
When the application starts, it loads users from utilisateurs.json.
If the user is new, a profile is created and stored in the file.
The user’s quiz history is displayed from the file when available.
Question Management:
The user selects a quiz category (e.g., Python, Networks, Algorithms).
The application loads the corresponding questions from questions.json.
Quiz Execution:
The questions are presented to the user with a timer (set to 60 seconds).
The score is updated after each question.
Once the quiz is finished or the time runs out, the final score is displayed.
History and Results Export:
After the quiz, the user's history is updated with the latest quiz data (date, score, category).
The updated history is saved to utilisateurs.json.
The results are also exported to resultats.csv for future reference.
	
Encountered challenges:
Handling the Timer:
solution:Implement a logic to automatically stop the test when the time has expired.

Conclusion:
The MCQ application in Python is a functional tool that helps students assess their knowledge. Through this project, we applied the problem-solving techniques and Python basics learned in the course, focusing on file handling, data storage, and user management. This project allowed us to strengthen our skills and translate theoretical concepts into practical solutions.
