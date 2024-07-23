-- Backend Route: /create-account
-- frontend: GET { email: “johndoe@gmail.com”, password: “abcd12” }
-- backend { message: “success”, employer_id: 4103 }
-- SELECT LAST_INSERT_ID() returns employer_id, PK value of the last row inserted

INSERT INTO employer (Email, Password)
VALUES ("example@gmail.com", "1234")
SELECT LAST_INSERT_ID();

INSERT INTO employer (Email, Password)
VALUES ("johndoe@hotmail.com", "123")
SELECT LAST_INSERT_ID();

-- Backend Route: /create-quiz
-- SELECT LAST_INSERT_ID() returns quiz_id, PK value of the last row inserted

INSERT INTO quiz (EmployerID, Title, QuizDescription)
VALUES (1, "MyQuiz", "A description")
SELECT LAST_INSERT_ID();

INSERT INTO quiz (EmployerID, Title, QuizDescription)
VALUES (2, "SuperHardQuiz", "Another description")
SELECT LAST_INSERT_ID();

INSERT INTO quiz (EmployerID, Title, QuizDescription)
VALUES (1, "SecondQuiz", "My second quiz")
SELECT LAST_INSERT_ID();

-- /update-quiz

UPDATE quiz
SET ContactName = 'Alfred Schmidt', City = 'Frankfurt'
WHERE CustomerID = 1;

-- /add-question

INSERT INTO questions (QuizID, Question, QuestionType)
VALUES (1, "What is a string?", "Multiple Choice");

INSERT INTO questions (QuizID, Question, QuestionType)
VALUES (2, "Write out the solution to twosum", "Free text");

INSERT INTO questions (QuizID, Question, QuestionType)
VALUES (1, "Select all languages", "Checkbox");

-- stats

INSERT INTO stats (Candidate_Email, Link_ID, Quiz_ID, Grade)
VALUES ("abc@gmail.com", "a12b", 1, 90);

INSERT INTO stats (Candidate_Email, Link_ID, Quiz_ID, Grade)
VALUES ("janedoe@ab.com", "bc23", 2, 76.5);

INSERT INTO stats (Candidate_Email, Link_ID, Quiz_ID, Grade)
VALUES ("Jack@hit.com", "as34", 1, 40);

-- answers

INSERT INTO answers (ID, QuestionID, Answer, is_correct)
VALUES (1, 1, "Array of Characters", 1);

INSERT INTO answers (ID, QuestionID, Answer, is_correct)
VALUES (2, 1, "An integer", 0);

INSERT INTO answers (ID, QuestionID, Answer, is_correct)
VALUES (3, 1, "Unicorn", 0);

-- Backend Route: /delete-quiz
-- Frontend: POST { employer_id: “4103”, quiz_id: 43}
-- Backend:{ message: “success, quiz was deleted”}

 DELETE FROM quiz WHERE employer_id = 4103 AND quiz_id = 43;

-- Backend Route: /send-quiz
-- Frontend: POST{ employer_id: “4103”, quiz_id: 43, candidate_email: “abc@gmail.com” }
-- Backend:{ message: “success, here is link to quiz”, link: “software-quiz.com/abc23” }



-- Backend Route: /send-result
-- Frontend: POST{ employer_id: “4103”, quiz_id: 43, link: “abc23”, question_id: [1, 4, 5, 10, 25, 34], is_correct: [0, 1, 1, 1, 0, 1] }
-- Backend: { message: “success, quiz completed by candidate” }

