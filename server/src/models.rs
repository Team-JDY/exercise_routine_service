use serde::{Serialize, Deserialize};
use tokio_pg_mapper_derive::PostgresMapper;

#[derive(PostgresMapper)]
pub struct User {
    pub user_id: i32,
    pub sns_login_info: Option<String>,
    pub nickname: String,
    pub height: f32,
    pub weight: f32,
    pub goal_weight: Option<f32>,
    pub gender: String,
    pub birthdate: String,
    pub weekly_exercise_freq: i32,
    pub usual_exercise_intensity: Option<i32>,
    pub preferred_exercise_type: Option<String>,
}

#[derive(PostgresMapper)]
pub struct ExerciseRoutine {
    pub routine_id: i32,
    pub user_id: i32,
    pub exercise_name: String,
    pub start_time: String,
    pub end_time: String,
    pub base_date: String,
    pub repetition_type: i32,
    pub repetition_value: i32,
}

#[derive(PostgresMapper)]
pub struct ExerciseLog {
    pub log_id: i32,
    pub user_id: i32,
    pub routine_id: i32,
    pub exercise_date: String,
    pub completed: bool,
}