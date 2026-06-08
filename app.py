from flask import Flask, flash, redirect, render_template, request, url_for

from config import Config
from models import Note, db
from notes.routes import notes_bp
from auth.routes import auth_bp


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    app.register_blueprint(notes_bp)
    app.register_blueprint(auth_bp)

    with app.app_context():
        db.create_all()

    @app.route("/acerca-de")
    def about():
        return "Esto es una app de notas"

    @app.route("/contacto", methods=["GET", "POST"])
    def contact():
        if request.method == "POST":
            return "Formulario enviado correctamente", 201
        return "Pagina de contacto"

    @app.route("/crear-nota", methods=["GET", "POST"])
    def create_note():
        if request.method == "POST":
            title = request.form.get("title", "")
            content = request.form.get("content", "")

            if not len(title.strip()) > 10:
                flash("El título es muy corto, minimo 10", "error")
                return render_template("note_form.html")

            if not len(content.strip()) > 20:
                flash("El contenido es muy corto, minimo 20", "error")
                return render_template("note_form.html")

            note_db = Note(title=title, content=content)
            db.session.add(note_db)
            db.session.commit()
            flash("Nota creada", "success")
            return redirect(url_for("notes.home"))

        return render_template("note_form.html")

    return app
