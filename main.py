
from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:buildablog@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'hjdshfawefaoidhf'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/')
def index():
    blogs = Blog.query.all()
    return render_template('main.html', title="Blog Posts", blogs=blogs)
  

@app.route('/newpost', methods=['POST', 'GET'])
def new_post():

   if request.method == 'POST':
        name = request.form['title']
        body = request.form['body']
        
        title_error = ""
        post_error = ""

        if name == "":
            title_error = "Enter title"

        if body == "":
            post_error = "Enter data"

        if not title_error and not post_error:
            new_post_name = Blog(name, body)
            db.session.add(new_post_name)
            db.session.commit()
            return redirect("/blog?id=" +str(new_post_name.id))
        else:
            return render_template('newpost.html',title="Add a Post", title_error=title_error, 
                post_error=post_error,
                name=name,
                body=body)

        return render_template('newpost.html',title="Add a Post")
   return render_template('newpost.html')

@app.route('/blog')
def blog():
    blog_id = request.args.get('id')
    blog = Blog.query.filter_by(id=blog_id).first()
    return render_template('blog.html', blog=blog)


if __name__ == '__main__':
    app.run()