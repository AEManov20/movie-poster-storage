import json
import requests
import random
from multiprocessing import Pool
from datetime import datetime, timedelta

API_BASE_URL = "http://localhost:8080"
API_HALLS_URL = API_BASE_URL + "/api/v1/theatre/{id}/hall/all"
API_MOVIES_URL = API_BASE_URL + "/api/v1/movie/{id}"
QUERY = "INSERT INTO public.theatre_screenings (movie_id, theatre_id, hall_id, subtitles_language_id, audio_language_id, starting_time, is_3d, status) VALUES ('{movie_id}', '{theatre_id}', '{hall_id}', '{subtitles_language_id}', '{audio_language_id}', '{starting_time}', {is_3d}, {status});\n"

movie_ids = json.load(open("./movie_ids.json"))
theatre_halls_ids = json.load(open("./theatre_halls_ids.json"))
language_ids = json.load(open("./language_ids.json"))

queries = []
movies = {}

for theatre in theatre_halls_ids:
    print(theatre[0], "done")
    for hall_id in theatre[1]:
        time = datetime(2023, 7, 10, 0, 9, 0)
        for i in range(random.randint(10, 16)):
            movie_id = random.choice(movie_ids)

            if not (movie_id in movies):
                print('cache miss')
                movies[movie_id] = json.loads(requests.get(
                    API_MOVIES_URL.format(id=random.choice(movie_ids))).text)

            movie = movies[movie_id]
            theatre_id = theatre[0]
            hall_id = hall_id
            sub_id = random.choice(language_ids)
            aud_id = random.choice(language_ids)
            starting_time = time.strftime('%Y-%m-%dT%H:%M:%SZ')
            is_3d = bool(random.randint(0, 1))

            time += timedelta(minutes=movie['length'] + 240)
            query = QUERY.format(
                movie_id=movie_id,
                theatre_id=theatre_id,
                hall_id=hall_id,
                subtitles_language_id=sub_id,
                audio_language_id=aud_id,
                starting_time=starting_time,
                is_3d=is_3d,
                status=0
            )

            queries.append(query)

f = open('out.sql', 'w')
f.write("".join(queries))
f.close()
