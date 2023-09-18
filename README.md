# Diary app

This is a simple diary application powered by a relational database and python.

Using flask we render journal/diary entries to the user via web pages and allow users to add new entries.

## Development

To develop you need flask

```shell
python -m pip install flask
```

To seed a SQLite development database, run `init_db.py`

The code is primarily in `app.py` and what this file does is leverage HTML template files in `./templates` directory to render your website.

