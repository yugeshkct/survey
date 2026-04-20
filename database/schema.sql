CREATE TABLE IF NOT EXISTS surveys (
    id SERIAL PRIMARY KEY,
    survey_name VARCHAR(255) NOT NULL,
    page_name VARCHAR(255) NOT NULL,
    survey_monkey_id VARCHAR(100),
    survey_link TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS questions (
    id SERIAL PRIMARY KEY,
    survey_id INTEGER NOT NULL REFERENCES surveys(id) ON DELETE CASCADE,
    question_title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS choices (
    id SERIAL PRIMARY KEY,
    question_id INTEGER NOT NULL REFERENCES questions(id) ON DELETE CASCADE,
    choice_text VARCHAR(255) NOT NULL
);