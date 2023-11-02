use std::env;
use tokio_postgres::NoTls;
use tokio_postgres::error::Error as PgError;
use crate::models::{User, ExerciseLog};
use deadpool_postgres::{Pool, Client};
use tokio_pg_mapper::FromTokioPostgresRow;
use thiserror::Error;

#[derive(Debug, Error)]
pub enum DbError {
    #[error("Database error: {0}")]
    DatabaseError(#[from] PgError),

    #[error("Data not found")]
    DataNotFound,

    #[error("Internal error")]
    InternalError,
}

pub type Result<T> = std::result::Result<T, DbError>;

pub async fn connect() -> Result<Pool> {
    let config = deadpool_postgres::Config::from_env()?;
    let pool = config.create_pool(NoTls)?;
    Ok(pool)
}

async fn get_client(pool: &Pool) -> Result<Client> {
    pool.get().await.map_err(DbError::from)
}

pub async fn get_exercise_logs_for_user_on_date(pool: &Pool, user_id: i32, date: &str) -> Result<Vec<ExerciseLog>> {
    let client = get_client(pool).await?;
    let statement = client.prepare("SELECT * FROM exercise_logs WHERE user_id = $1 AND exercise_date = $2").await?;
    let logs = client.query(&statement, &[&user_id, &date])
        .await?
        .iter()
        .map(|row| ExerciseLog::from_row_ref(row).unwrap())
        .collect();
    Ok(logs)
}

pub async fn create_user(pool: &Pool, user: User) -> Result<User> {
    let client = get_client(pool).await?;
    let statement = client.prepare("INSERT INTO users (sns_login_info, nickname, height, weight, goal_weight, gender, birthdate, weekly_exercise_freq, usual_exercise_intensity, preferred_exercise_type) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10) RETURNING *").await?;
    let user = client.query(&statement, &[
        &user.sns_login_info,
        &user.nickname,
        &user.height,
        &user.weight,
        &user.goal_weight,
        &user.gender,
        &user.birthdate,
        &user.weekly_exercise_freq,
        &user.usual_exercise_intensity,
        &user.preferred_exercise_type
    ])
        .await?
        .iter()
        .map(|row| User::from_row_ref(row).unwrap())
        .next()
        .ok_or(DbError::DataNotFound)?;

    Ok(user)
}

pub async fn delete_user(pool: &Pool, user_id: i32) -> Result<()> {
    let client = get_client(pool).await?;
    let statement = client.prepare("DELETE FROM users WHERE user_id = $1").await?;
    client.execute(&statement, &[&user_id]).await?;
    Ok(())
}

pub async fn get_goal_weight_for_user(pool: &Pool, user_id: i32) -> Result<Option<f32>> {
    let client = get_client(pool).await?;
    let statement = client.prepare("SELECT goal_weight FROM users WHERE user_id = $1").await?;
    let result = client.query_opt(&statement, &[&user_id])
        .await?
        .map(|row| row.get(0))
        .ok_or(DbError::DataNotFound)?;

    Ok(result)
}