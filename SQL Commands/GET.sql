-- Backend Route: /login
-- Frontend: GET { email: “johndoe@gmail.com”, password: “abcd12” }
-- Backend: { message: “success”, employer_id: 4103 }

SELECT employer_id FROM employer WHERE email = "johndoe@gmail.com" AND password = "abcd12";

-- Backend Route: /user-quiz
-- Frontend: GET { employer_id: “4103” }
-- Backend:{ message: “success, return all user quizzes”, quiz_id: [1, 24, 54], title: [“my quiz”, “quiz1”, “EpicQuiz”], description: [“first quiz”, “my description”, “this will be epic”]}

SELECT * FROM Quiz WHERE EmployerID = “4103”;

-- Backend Route: /quiz-results
-- Frontend: GET{ employer_id: “4103”, quiz_id: 43 }
-- { message: “success”, candidate_email: [“abc@gmail.com”, “xyz@hotmail.com”], grades: [0.95, 0.85] }

SELECT * FROM Quiz WHERE employer_id = “4103” AND quiz_id = 43;
