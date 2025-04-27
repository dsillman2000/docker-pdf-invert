from pathlib import Path
import flask
import flask_wtf
import wtforms
import os
import jinja2


TEMPLATES_DIR = Path(__file__).parent.parent / "templates"
app = flask.Flask(__name__, template_folder=TEMPLATES_DIR)

SECRET_KEY = os.urandom(32)
app.config["SECRET_KEY"] = SECRET_KEY


class PdfFileField(wtforms.FileField):
    def __call__(self, *args, **kwargs):
        # Set the accept attribute to only allow PDF files
        kwargs.setdefault("accept", "*.pdf")
        return super().__call__(*args, **kwargs)


class InvertPdfForm(flask_wtf.FlaskForm):
    file = PdfFileField(
        "PDF File",
        validators=[
            wtforms.validators.DataRequired(),
            wtforms.validators.regexp(r".*\.pdf$", message="File must be a PDF"),
        ],
    )
    submit = wtforms.SubmitField("Invert PDF")


@app.route("/")
def index():
    form = InvertPdfForm()
    return flask.render_template("index.html.j2", form=form)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
