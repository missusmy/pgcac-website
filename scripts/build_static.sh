#!/bin/bash

# Navigate to the pgcac-website directory
cd ../pgcac-website

# Run the deploystatic.py script to generate the static site
python tools/deploystatic.py `pwd` `pwd`/postgres.ca

# Navigate to the postgres.ca directory
cd postgres.ca

# Start the HTTP server
python -m http.server