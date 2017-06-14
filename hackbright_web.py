"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')

    first, last, github = hackbright.get_student_by_github(github)

    project_grades = hackbright.get_grades_by_github(github)

    html = render_template("student_info.html", first=first, last=last, github=github, project_grades=project_grades)

    return html


@app.route("/project")
def get_project_info():
    """ Show information about a project. """

    title = request.args.get('title')

    project = hackbright.get_project_by_title(title)
    title, description, max_grade = project

    students_completed = hackbright.get_grades_by_title(title)

    student_name = hackbright.get_student_by_github(students_completed[0])

    html = render_template("project_info.html", title=title, description=description, max_grade=max_grade, students_completed=students_completed, student_name=student_name)

    return html


@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")


@app.route("/student-add")
def student_add():
    """Add a student. """

    return render_template('new_student.html')


@app.route("/student-add", methods=['POST'])
def student_added():

    first = request.form.get('first')
    last = request.form.get('last')
    github = request.form.get('github')

    hackbright.make_new_student(first, last, github)

    return render_template("successful_add.html", first=first, last=last, github=github)


if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
