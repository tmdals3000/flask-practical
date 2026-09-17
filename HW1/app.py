from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    # TODO: 본인 이름과 학번으로 바꾸세요
    name = "홍길동"
    student_id = "20xx000000"
    return render_template("home.html", name=name, student_id=student_id)


@app.route("/profile")
def profile():
    # TODO: 본인 취미 3가지로 바꾸세요
    hobbies = ["취미 1", "취미 2", "취미 3"]
    return render_template("profile.html", hobbies=hobbies)


@app.route("/greet/<name>")
def greet(name):
    return render_template("greet.html", name=name)
