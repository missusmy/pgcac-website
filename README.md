The PGCAC website is based on the pgeu-website template engine.

A static website can be generated from these templates with the following steps:

1. git clone https://git.postgresql.org/git/pgcac-website.git
2. git clone https://git.postgresql.org/git/pgeu-website.git
3. Setup a python virtualenv:

    ```shell script
    python3 -m venv pythonenv
    . pythonenv/bin/activate
    pip install Markdown==2.6.5 python-dateutil jinja2
    ```

4. Run the deploystatic.py script:

    ```shell script
    python pgeu-website/tools/deploystatic/deploystatic.py `pwd`/pgcac-website `pwd`/postgres.ca
    ```

5. Test the resulting build:

    ```shell script
    cd postgres.ca
    python -m http.server
    ```
