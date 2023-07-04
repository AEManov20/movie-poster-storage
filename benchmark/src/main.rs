use rayon::prelude::*;
use reqwest::blocking as reqwest;

const MOVIE_IDS_JSON: &str = include_str!("../../movie_ids.json");
const THEATRE_IDS_JSON: &str = include_str!("../../theatre_ids.json");
const LANGUAGE_IDS_JSON: &str = include_str!("../../language_ids.json");

const API_BASE_URL: &str = "http://localhost:8080";
const API_HALLS_URL: &str = "/api/v1/theatre/{}/hall/all";
const API_MOVIES_URL: &str = "/api/v1/movie/{}";

// "INSERT INTO public.theatre_screenings (movie_id, theatre_id, hall_id, subtitles_language_id, audio_language_id, starting_time, is_3d, status) VALUES ({movie_id}, {theatre_id}, {hall_id}, {subtitles_language_id}, {audio_language_id}, {starting_time}, {is_3d}, {status});\n"
fn main() {
    let movie_ids: Vec<uuid::Uuid> = serde_json::from_str(MOVIE_IDS_JSON).unwrap();
    let theatre_ids: Vec<uuid::Uuid> = serde_json::from_str(THEATRE_IDS_JSON).unwrap();
    let language_ids: Vec<uuid::Uuid> = serde_json::from_str(THEATRE_IDS_JSON).unwrap();

    let client = reqwest::Client::builder().build().unwrap();

    theatre_ids
        .par_iter()
        .map(|x| {
            client.get(format!("{}/api/v1/theatre/{}/screening/timeline?start_date=2023-07-04T06%3A19%3A22.777Z", API_BASE_URL, x))
                .send()
                .unwrap()
                .text()
                .unwrap()
        })
        .collect::<Vec<_>>();
}
