use actix_web::{web, HttpResponse};
use crate::models::{User, ExerciseRoutine, ExerciseLog};
use crate::db;
use deadpool_postgres::{Pool, Client};

pub fn config(cfg: &mut web::ServiceConfig) {
    cfg.service(
        web::resource("/users/{user_id}/exercise_logs/{date}")
            .route(web::get().to(get_exercise_logs)),
    )
        .service(
            web::resource("/users")
                .route(web::post().to(create_user)),
        )
        .service(
            web::resource("/users/{user_id}")
                .route(web::delete().to(delete_user)),
        )
        .service(
            web::resource("/users/{user_id}/goal_weight")
                .route(web::get().to(get_goal_weight)),
        );
}

async fn get_exercise_logs(pool: web::Data<Pool>, info: web::Path<(i32, String)>) -> HttpResponse {
    let (user_id, date) = info.into_inner();
    match db::get_exercise_logs_for_user_on_date(&pool, user_id, &date).await {
        Ok(logs) => HttpResponse::Ok().json(logs),
        Err(_) => HttpResponse::InternalServerError().finish(),
    }
}

async fn create_user(pool: web::Data<Pool>, user: web::Json<User>) -> HttpResponse {
    match db::create_user(&pool, user.into_inner()).await {
        Ok(user) => HttpResponse::Created().json(user),
        Err(_) => HttpResponse::InternalServerError().finish(),
    }
}

async fn delete_user(pool: web::Data<Pool>, user_id: web::Path<i32>) -> HttpResponse {
    match db::delete_user(&pool, user_id.into_inner()).await {
        Ok(_) => HttpResponse::Ok().finish(),
        Err(_) => HttpResponse::InternalServerError().finish(),
    }
}

async fn get_goal_weight(pool: web::Data<Pool>, user_id: web::Path<i32>) -> HttpResponse {
    match db::get_goal_weight_for_user(&pool, user_id.into_inner()).await {
        Ok(goal_weight) => HttpResponse::Ok().json(goal_weight),
        Err(_) => HttpResponse::InternalServerError().finish(),
    }
}