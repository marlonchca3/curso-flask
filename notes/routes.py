from flask import redirect, render_template, request, url_for, Blueprint, flash, session
from models import Note, db

notes_bp = Blueprint("notes", __name__)


@notes_bp.route("/")
def home():
    if "user" not in session:
        flash("Para poder ver las notas debes iniciar sesión", "error")
        return redirect(url_for("auth.login"))

    notes = Note.query.all()
    return render_template("home.html", notes=notes)


@notes_bp.route("/editar-nota/<int:id>", methods=["GET", "POST"])
def edit_note(id):
    note = Note.query.get_or_404(id)
    if request.method == "POST":
        title = request.form.get("title", "")
        content = request.form.get("content", "")
        note.title = title
        note.content = content
        db.session.commit()
        return redirect(url_for("notes.home"))

    return render_template("edit_note.html", note=note)


@notes_bp.route("/eliminar-nota/<int:id>", methods=["POST"])
def delete_note(id):
    note = Note.query.get_or_404(id)
    db.session.delete(note)
    db.session.commit()
    return redirect(url_for("notes.home"))
