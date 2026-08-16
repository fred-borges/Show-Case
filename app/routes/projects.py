from flask import Blueprint, redirect, render_template, request, url_for
from ..extensions import db
from ..models.projects import Project
from flask_login import current_user, login_required
import sqlalchemy as sa



post_bp = Blueprint("projects", __name__, url_prefix="/projects")

@login_required
@post_bp.route("/", methods=["GET", "POST"]) 
def project():
    if request.method == "POST":
        name = request.form['name']
        description = request.form['description']
        markdown = request.form['markdown']
        github_url = request.form['github_url']
        demo_url = request.form['demo_url']
        user_id = current_user.id

        new_project = Project(name = name, description = description, markdown = markdown, github_url = github_url, demo_url = demo_url, user_id=user_id)
        db.session.add(new_project)
        db.session.commit()

        return redirect(url_for("inicio"))
    return render_template("project.html")

@login_required
@post_bp.route("/<id>")
def user_projects(id: int):
    
    projects = db.session.scalars(
        sa.select(Project).where(Project.user_id == id)
    ).all()

    return render_template("user_projects.html", projects=projects)