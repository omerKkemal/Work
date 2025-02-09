from flask import Flask

from note.inner_html import html

app = Flask(__name__)


@app.route('/')
def index():
    return html


if __name__ == "__main__":
    app.run()
