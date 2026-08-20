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

@post_bp.route("/<id>/edit", methods=["GET", "POST"])
def edit_project(id):

    # 1. Procurar o projeto
    project = db.session.scalar(
        sa.select(Project).where(Project.id == id)
    )

    # 2. Verificar se o projeto existe
    if project is None:
        return "Projeto não encontrado", 404

    # 3. Verificar se o projeto pertence ao utilizador
    if project.user_id != current_user.id:
        return "Acesso recusado", 403

    # 4. Se for POST, atualizar o projeto
    if request.method == "POST":
        project.name = request.form["name"]
        project.description = request.form["description"]
        project.markdown = request.form["markdown"]
        project.github_url = request.form["github_url"]
        project.demo_url = request.form["demo_url"]

        # 5. Guardar alterações
        db.session.commit()

        # 6. Voltar para os projetos
        return redirect(
            url_for("projects.user_projects", id=current_user.id)
        )

    # 7. Se for GET, mostrar formulário preenchido
    return render_template(
        "edit_project.html",
        project=project
    )
    
@post_bp.route("/<int:id>/delete", methods=["GET", "POST"])
def delete_project(id):

    project = db.session.scalar(
        sa.select(Project).where(Project.id == id)
    )

    if project is None:
        return "Projeto não encontrado", 404

    if project.user_id != current_user.id:
        return "Acesso recusado", 403

    if request.method == "POST":

        db.session.delete(project)
        db.session.commit()

        return redirect(
            url_for("projects.user_projects", id=current_user.id)
        )

    return render_template(
        "delete_project.html",
        project=project
    )