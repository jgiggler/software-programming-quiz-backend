CREATE TABLE Employer (
    ID int NOT NULL AUTO_INCREMENT,
    Email varchar(255) NOT NULL,
    Password varchar(255) NOT NULL,
    PRIMARY KEY (ID),
    UNIQUE (Email)
);

CREATE TABLE Quiz (
    ID int NOT NULL AUTO_INCREMENT,
    EmployerID int NOT NULL,
    Title varchar(255) NOT NULL,
    QuizDescription varchar(255) NOT NULL,
    PRIMARY KEY (ID),
    UNIQUE (ID),
    FOREIGN KEY (EmployerID) REFERENCES Employer(ID) ON DELETE CASCADE
);

CREATE TABLE Questions (
    ID int NOT NULL AUTO_INCREMENT,
    QuizID int NOT NULL,
    Question varchar(255) NOT NULL,
    QuestionType ENUM('Multiple Choice', 'Free text', 'Checkbox') NOT NULL,
    PRIMARY KEY (ID),
    FOREIGN KEY (QuizID) REFERENCES Quiz(ID) ON DELETE CASCADE
);

CREATE TABLE Stats (
    Candidate_Email varchar(255) NOT NULL,
    Link_ID varchar(255) NOT NULL,
    Quiz_ID int NOT NULL,
    Grade float(4,2) NOT NULL,
    PRIMARY KEY (Candidate_Email, Quiz_ID),
    UNIQUE (Link_ID),
    FOREIGN KEY (Quiz_ID) REFERENCES Quiz(ID) ON DELETE CASCADE
);

CREATE TABLE Answers (
    ID int NOT NULL AUTO_INCREMENT,
    QuestionID int NOT NULL,
    Answer varchar(255) NOT NULL,
    is_correct BOOL NOT NULL,
    PRIMARY KEY (ID),
    FOREIGN KEY (QuestionID) REFERENCES Questions(ID) ON DELETE CASCADE
);