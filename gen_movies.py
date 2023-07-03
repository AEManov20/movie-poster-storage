import json
import numpy

movies = json.load(open('./movies.json'))

query = "INSERT INTO public.movies (name, description, genre, release_date, length, poster_image_url) VALUES ('{name}', '{description}', '{genre}', '{release_date}', {length}, '{poster_image_url}');\n"

output = open('out.sql', 'w')

for movie in movies:
    output.write(
        query.format(
            name=movie['title'].replace('\'', '\'\''),
            description=movie['plot'].replace('\'', '\'\''),
            genre='|'.join(movie['genres']).replace('\'', '\'\''),
            release_date=f'01-01-{movie["year"]}',
            length=movie['runtime'],
            poster_image_url=movie['posterUrl']
        )
    )

output.close()