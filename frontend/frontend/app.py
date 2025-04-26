from pathlib import Path
import flask
import jinja2


TEMPLATES_DIR = Path(__file__).parent.parent / "templates"
app = flask.Flask(__name__, template_folder=TEMPLATES_DIR)


@app.route("/")
def index():
    return flask.render_template("index.html.j2")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
