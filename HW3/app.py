from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# 데이터베이스 위치. 파일 하나면 끝입니다
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
# MySQL 로 옮길 때는 위 한 줄만 아래로 바꿉니다 (L6 32쪽)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flask_user:password@localhost/flask_todo_db'

db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100), nullable=False)
    # TODO(1): 설명 칸 note 를 더하세요 — db.Column(db.String(200)) (L6 47쪽)
    done = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Todo {self.id} {self.text}>'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # TODO(2): note 도 같이 받아 넣으세요 — Todo(text=..., note=request.form['note'])
        db.session.add(Todo(text=request.form['todo']))
        db.session.commit()
        return redirect(url_for('index'))

    todos = Todo.query.all()
    return render_template('index.html', todos=todos)


@app.route('/toggle/<int:id>')
def toggle(id):
    todo = db.get_or_404(Todo, id)
    todo.done = not todo.done
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/delete/<int:id>')
def delete(id):
    todo = db.get_or_404(Todo, id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))


# TODO(3): /edit/<int:id> 라우트를 GET 과 POST 둘 다 받게 만드세요 (L6 48쪽)
#   - todo = db.get_or_404(Todo, id)
#   - POST 면 text 와 note 를 고치고 commit 한 뒤 목록으로 redirect
#   - 아니면 render_template('edit.html', todo=todo)


@app.route('/search')
def search():
    q = request.args.get('q', '')
    todos = Todo.query.filter(Todo.text.like(f'%{q}%')).all()
    return render_template('index.html', todos=todos)


# 라우트를 모두 적은 다음에 둡니다 (없는 표만 만듭니다)
with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)
