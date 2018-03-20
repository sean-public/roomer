''' Load CSV data from file into the DB by using the REST API.
    The CSV must have a header row and include fields named
    exaclty "timestamp","direction", and "dpu_id".

    Syntax: python load_csv.py <filename.csv>
                 ^--or "python3" as needed
'''

import csv
import requests
from sys import argv


# This is the default for local dev `manage.py runserver`
POST_URL = 'http://localhost:8000/dpu/{}/'

if len(argv) != 2:
    print('Please specify a CSV file to load!')
else:
    lines = 0
    with open(argv[1], 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            post_data = {
                'timestamp': row.get('timestamp'),
                'direction': row.get('direction'),
            }
            r = requests.post(POST_URL.format(row.get('dpu_id')), data=post_data)

            # Halt on any unexpected errors and display the status code & traceback
            if r.status_code not in [200, 409]:
                r.raise_for_status()
            lines += 1

    print(f'Finished importing {lines} lines of data')
