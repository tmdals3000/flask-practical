from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    # TODO: 본인 이름과 학번으로 바꾸세요
    name = "이승민"
    student_id = "24013735"
    return render_template("home.html", name=name, student_id=student_id)


@app.route("/profile")
def profile():
    hobbies = ["연극보기", "게임하기", "유튜브 보기"]
    return render_template("profile.html", hobbies=hobbies)


@app.route("/greet/<name>")
def greet(name):
    return render_template("greet.html", name=name)
