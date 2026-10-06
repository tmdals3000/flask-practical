from flask import Flask, render_template, request, url_for

app = Flask(__name__)


@app.route("/")
def index():
    return f"<a href='{url_for('about')}'>소개로</a>"


@app.route("/about")
def about():
    return "소개 페이지"


@app.route("/user/<username>")
def user_profile(username):
    return render_template("profile.html",
                           username=username,
                           posts=["첫 글", "두 번째 글"])


@app.route("/newuser/<username>")
def new_user(username):
    return render_template("profile.html",
                           username=username,
                           posts=[])


@app.route("/post/<int:pid>")
def post(pid):
    return f"{pid}번 글 (자료형: {type(pid).__name__})"


@app.route("/notes/")
def notes():
    return "메모 목록"


@app.route("/hello")
@app.route("/hello/<name>")
def hello(name=None):
    if name:
        return f"안녕하세요, {name} 님"
    return "안녕하세요"


@app.route("/search")
def search():
    query = request.args.get("q", "")
    page = request.args.get("page", "1")
    if not query:
        return "검색어를 입력하세요"
    return f'"{query}" 검색 결과 ({page} 페이지)'


@app.route("/write", methods=["GET", "POST"])
def write():
    if request.method == "POST":
        banana = request.form["banana"]
        melon = request.form["melon"]
        return (f"banana = {banana} ({type(banana).__name__}) / "
                f"melon = {melon} ({type(melon).__name__})")
    return """
    <form method="post">
      <input type="text" name="banana">
      <input type="number" name="melon">
      <button type="submit">보내기</button>
    </form>"""


@app.route("/attach", methods=["GET", "POST"])
def attach():
    if request.method == "POST":
        f = request.files.get("cherry")
        if f is None:
            return "cherry 가 files 에 없습니다"
        return f"{f.filename} / {len(f.read())} 바이트"
    return """
    <form method="post"
          enctype="multipart/form-data">
      <input type="text" name="banana">
      <input type="file" name="cherry">
      <button type="submit">보내기</button>
    </form>"""


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return do_the_login()
    else:
        return show_the_login_form()


def do_the_login():
    return f'Logged in as {request.form["username"]}'


def show_the_login_form():
    return """
    <form method="post">
        Username: <input type="text" name="username"><br>
        Password: <input type="password" name="password"><br>
        <input type="submit" value="Log In">
    </form>
    """


@app.route("/path/<path:subpath>")
def show_subpath(subpath):
    return f"Subpath {subpath}"


@app.route("/blog/<int:year>/<int:month>/<int:day>")
def show_blog_post(year, month, day):
    return f"Blog post from {year}-{month:02d}-{day:02d}"


@app.route("/test/<text>")
def route_sample(text):
    return f"<h1>{text}</h1>"


@app.route("/age/<num>")
def age_any(num):
    return f"<h1>{num} 살 — 타입은 {type(num).__name__}</h1>"


@app.route("/age2/<int:num>")
def age_int(num):
    return f"<h1>{num} 살 — 타입은 {type(num).__name__}</h1>"


@app.route("/hi/<name>")
def hi_template_render(name):
    return render_template("hi.html", name=name)


if __name__ == "__main__":
    app.run(debug=True)
