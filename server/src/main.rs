use actix_web::{web, App, HttpServer};
use dotenv::dotenv;
use std::io::Result;
use crate::db::DbPool;

mod routes;
mod models;
mod db;

#[actix_web::main]
async fn main() -> Result<()> {
    //dotenv::from_filename("db_inform.env").ok();
    //dotenv::from_filename("db_inform.env").expect("Failed to load env file");
    dotenv().ok();

    //let db_pool = db::connect().await.unwrap();
    //let db_pool = db::connect().await?;
    let db_pool = db::connect().await.expect("Failed to initialize database pool");

    HttpServer::new(move || {
        App::new()
            .app_data(web::Data::new(db_pool.clone()))
            .configure(routes::config)
    })
        .bind(("127.0.0.1", 8080))?
        .run()
        .await
}