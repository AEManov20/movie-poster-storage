import json
import requests
import random
from multiprocessing import Pool
from datetime import datetime, timedelta

API_BASE_URL = "http://localhost:8080"
API_HALLS_URL = API_BASE_URL + "/api/v1/theatre/{id}/hall/all"
API_MOVIES_URL = API_BASE_URL + "/api/v1/movie/{id}"
QUERY = "INSERT INTO public.theatre_screenings (movie_id, theatre_id, hall_id, subtitles_language_id, audio_language_id, starting_time, is_3d, status) VALUES ({movie_id}, {theatre_id}, {hall_id}, {subtitles_language_id}, {audio_language_id}, {starting_time}, {is_3d}, {status});\n"

movie_ids = json.load(open("./movie_ids.json"))
theatre_ids = json.load(open("./theatre_ids.json"))
language_ids = json.load(open("./language_ids.json"))

def c(x):
    return (x, json.loads(requests.get(API_HALLS_URL.format(id=x)).text))

results = map(c, theatre_ids)

print('received')

queries = []



for result in results:
    print(result[0], "done")
    for hall in result[1]:
        time = datetime(2023, 7, 10, 0, 9, 0)
        for i in range(random.randint(4,6)):
            movie = json.loads(requests.get(API_MOVIES_URL.format(id=random.choice(movie_ids))).text)
            movie_id = random.choice(movie_ids)
            theatre_id = result[0]
            hall_id = hall['id']
            sub_id = random.choice(language_ids)
            aud_id = random.choice(language_ids)
            starting_time = time.strftime('%Y-%m-%dT%H:%M:%SZ')
            is_3d = bool(random.randint(0, 1))

            time += timedelta(hours=movie['length'] + .5)
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