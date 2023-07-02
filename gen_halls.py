import json
import numpy

AMOUNT = 14000

language_ids = json.load(open('./language_ids.json'))
theatre_ids = json.load(open('./theatre_ids.json'))
movies = json.load(open('./movies.json'))
names = json.load(open('./names.json'))

query = "INSERT INTO public.halls (theatre_id, name, seat_data) VALUES ('{theatre_id}', '{name}', '{seat_data}');\n";

random_tids = numpy.random.choice(theatre_ids, AMOUNT)
random_names = numpy.random.choice(names, AMOUNT)
random_numbers = list(map(lambda x: round(x), numpy.random.uniform(int(1), int(5), AMOUNT)))

output = open('out.sql', 'w')

for n in range(AMOUNT):
    output.write(query.format(theatre_id=random_tids[n], name="{} {}".format(random_names[n], random_numbers[n]), seat_data="[[1]]"))

output.close()