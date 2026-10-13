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
    note = db.Column(db.String(200))
    done = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Todo {self.id} {self.text}>'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        todo = Todo(text=request.form['todo'],
                    note=request.form['note'])
        db.session.add(todo)
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


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    todo = db.get_or_404(Todo, id)
    if request.method == 'POST':
        todo.text = request.form['todo']
        todo.note = request.form['note']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', todo=todo)


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
