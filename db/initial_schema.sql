-- 회원정보 테이블
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    sns_login_info TEXT,  -- 어떤 식으로 기록되는 지 잘 모르겠습니다.
    nickname VARCHAR(255) NOT NULL,
    height FLOAT NOT NULL,
    weight FLOAT NOT NULL,
    goal_weight FLOAT,
    gender CHAR(1) NOT NULL,  -- M / F
    birthdate DATE NOT NULL,
    weekly_exercise_freq INTEGER NOT NULL,
    usual_exercise_intensity VARCHAR(30),  -- 예: 맨날 뛰어 다닌다, 하루에 3걸음만 움직인다 등
    preferred_exercise_type VARCHAR(10)  -- 예: "런닝, 플랭크"
);

-- 운동 루틴 추가 테이블
CREATE TABLE exercise_routines (
    routine_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    exercise_name VARCHAR(255) NOT NULL,
    start_time TIME NOT NULL,  -- 운동 시작 시간
    end_time TIME NOT NULL,  -- 운동 종료 시간
    base_date DATE NOT NULL,  -- 반복을 위한 기준 날짜
    repetition_type CHAR(1) NOT NULL,  -- D: Daily, W: Weekly, M: Monthly
    repetition_value INTEGER NOT NULL
);

-- 운동 기록 테이블
CREATE TABLE exercise_logs (
    log_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    routine_id INTEGER REFERENCES exercise_routines(routine_id),
    exercise_date DATE NOT NULL,
    completed BOOLEAN NOT NULL
);