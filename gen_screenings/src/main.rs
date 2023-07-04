use rayon::prelude::*;
use reqwest::blocking as reqwest;
use serde::{Deserialize, Serialize};

const MOVIE_IDS_JSON: &str = include_str!("../../movie_ids.json");
const THEATRE_IDS_JSON: &str = include_str!("../../theatre_ids.json");
const LANGUAGE_IDS_JSON: &str = include_str!("../../language_ids.json");

const API_BASE_URL: &str = "http://localhost:8080";
const API_HALLS_URL: &str = "/api/v1/theatre/{}/hall/all";
const API_MOVIES_URL: &str = "/api/v1/movie/{}";

#[derive(Serialize, Deserialize)]
struct Movie {
    description: String,
    genre: String,
    id: uuid::Uuid,
    imdb_link: String,
    length: f64,
    name: String,
    poster_image_url: String,
    release_date: chrono::NaiveDate,
}

#[derive(Serialize, Deserialize)]
pub struct Hall {
    pub id: uuid::Uuid,
    pub theatre_id: uuid::Uuid,
    pub name: String,
    pub seat_data: serde_json::Value,
}

#[derive(Serialize, Deserialize)]
pub struct Theatre {
    pub id: uuid::Uuid,
    pub name: String,
    pub location_lat: f64,
    pub location_lon: f64,
    pub logo_image_url: Option<String>,
    pub cover_image_url: Option<String>,
}

// "INSERT INTO public.theatre_screenings (movie_id, theatre_id, hall_id, subtitles_language_id, audio_language_id, starting_time, is_3d, status) VALUES ({movie_id}, {theatre_id}, {hall_id}, {subtitles_language_id}, {audio_language_id}, {starting_time}, {is_3d}, {status});\n"
fn main() {
    let movie_ids: Vec<uuid::Uuid> = serde_json::from_str(MOVIE_IDS_JSON).unwrap();
    let theatre_ids: Vec<uuid::Uuid> = serde_json::from_str(THEATRE_IDS_JSON).unwrap();
    let language_ids: Vec<uuid::Uuid> = serde_json::from_str(THEATRE_IDS_JSON).unwrap();

    let mut res: Vec<(uuid::Uuid, Vec<uuid::Uuid>)> = vec![];

    theatre_ids
        .par_iter()
        .map(|x| {
            (
                *x,
                serde_json::from_str::<Vec<Hall>>(
                    &reqwest::get(format!("{}/api/v1/theatre/{}/hall/all", API_BASE_URL, x))
                        .unwrap()
                        .text()
                        .unwrap(),
                )
                .unwrap()
                .par_iter()
                .map(|x| x.id)
                .collect::<Vec<uuid::Uuid>>(),
            )
        })
        .collect_into_vec(&mut res);

    std::fs::write(
        "./theatre_halls_ids.json",
        serde_json::to_string(&res).unwrap(),
    )
    .unwrap();
}
