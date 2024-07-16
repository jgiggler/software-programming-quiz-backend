CREATE TABLE Employer (
    ID int NOT NULL AUTO_INCREMENT,
    Email varchar(255) NOT NULL,
    Password varchar(255) NOT NULL,
    PRIMARY KEY (ID)
);

CREATE TABLE Quiz (
    ID int NOT NULL AUTO_INCREMENT,
    EmployerID int NOT NULL,
    Title varchar(255) NOT NULL,
    QuizDescription varchar(255) NOT NULL,
    PRIMARY KEY (ID)
);

CREATE TABLE Questions (
    ID int NOT NULL AUTO_INCREMENT,
    QuizID int NOT NULL,
    Question varchar(255) NOT NULL,
    QuestionType ENUM("Multiple Choice", "Free text", "Checkbox") NOT NULL,
    PRIMARY KEY (ID)
);

CREATE TABLE Stats (
    Candidate_Email varchar(255) NOT NULL AUTO_INCREMENT,
    Link_ID varchar(255) NOT NULL,
    Quiz_ID int NOT NULL,
    Grade float(4,2) NOT NULL,
    PRIMARY KEY (Candidate_Email),
    UNIQUE (Link_ID)
);

CREATE TABLE Answers (
    ID int NOT NULL AUTO_INCREMENT,
    QuestionID int NOT NULL,
    Answer varchar(255) NOT NULL,
    is_correct BOOL NOT NULL,
    PRIMARY KEY (ID)
);
