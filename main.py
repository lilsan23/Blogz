from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:buildablog@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'fyuyjgklui'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        title = request.form['title']
        post = request.form['post']
        new_post = Blog(title, post)
        db.session.add(new_post)
        db.session.commit()

#     tasks = Task.query.filter_by(completed=False).all()
#     completed_tasks = Task.query.filter_by(completed=True).all()
#     return render_template('todos.html',title="Get It Done!", 
#         tasks=tasks, completed_tasks=completed_tasks)


# @app.route('/delete-task', methods=['POST'])
# def delete_task():

#     task_id = int(request.form['task-id'])
#     task = Task.query.get(task_id)
#     task.completed = True
#     db.session.add(task)
#     db.session.commit()

#     return redirect('/')

    if title == "":
        title_error = "Please enter a title"

    if post == "":
        post_error = "Please enter data"

    if not title_error and not post_error:
        return render_template('blog.html', title=title)

    else:
        return render_template('signup.html', title_error=title_error, 
            post_error=post_error,
            title=title,
            body=body)     

# if __name__ == '__main__':
    app.run()