# Diary app

This is a simple diary application powered by a relational database and python.

Using flask we render journal/diary entries to the user via web pages and allow users to add new entries.

## Development

To develop you need flask

```shell
pip install flask
```

To seed a SQLite development database, run `init_db.py`

The code is primarily in `app.py` and what this file does is leverage HTML template files in `./templates` directory to render your website.

## Testing

Unit tests verify the code does what we expect.

```shell
pip install pytest coverage
```

Install the module and Run pytest

```shell
pip install -e .

pytest
```

Run coverage

```shell
coverage run -m pytest

coverage report

coverage html
```

## Build and install

```shell
pip install build

python -m build --wheel
```

When running publically, you use a WSGI server such as `Waitress`

```shell
pip install waitress
```

To run, import and call the app

```shell
waitress-serve --call 'diary:create_app'
```