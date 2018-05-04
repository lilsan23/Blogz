
from flask import Flask, request, redirect, render_template, flash, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:3306/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'fyuyjgklui'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')
    
    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.before_request
def require_login():
    allowed_routes = ['index', 'login', 'register', 'blog', 'home']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash("Logged in")
            return redirect('/newpost')
        else:
            flash('User password incorrect, or user does not exist', 'error')

    return render_template('login.html', title="Blogz Login")


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']


        username_error = ""
        password_error = ""
        verify_error = ""

        if len(username)<3 or username =="" or (" " in username):
            username_error = "Username does not meet requirements. Try again."

        if len(password) <3 or password =="":
            password_error = "Password does not meet requirements. Try again."
            password=""
        
        if verify != password or verify =="": 
            verify_error = "Password does not match."
            verify=""

        if username == User.query.filter_by(username=username).first():
            username_error = "Duplicate user id."

        if not username_error and not password_error and not verify_error:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            flash("Logged in")
            return redirect('/newpost')
        else:
            
            return render_template('register.html', username_error=username_error, 
               password_error=password_error, 
               verify_error=verify_error,
               username=username,
               password=password,
               verify=verify)

    return render_template('register.html', title="Blogz Registration")

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/blog')

@app.route('/newpost', methods=['POST', 'GET'])
def new_post():

    if request.method == 'POST':
        name = request.form['name']
        body = request.form['body']
        
        name_error = ""
        post_error = ""

        if name == "":
            name_error = "Enter title"

        if body == "":
            post_error = "Enter data"

        if not name_error and not post_error:
            owner = User.query.filter_by(username=session['username']).first()
            new_post_name = Blog(name, body, owner)
            db.session.add(new_post_name)
            db.session.commit()
            return redirect("/blog?id=" +str(new_post_name.id))
        else:
            return render_template('newpost.html',title="New Post", name_error=name_error, 
                post_error=post_error,
                name=name,
                body=body)

    return render_template('newpost.html')

@app.route('/blog')
def blog():
    
    if request.args.get('id'):
        blog_id = request.args.get('id')
        blog = Blog.query.get(blog_id)
        return render_template('blog.html', title= "Blog", blog=blog)

    elif request.args.get('user'):
        user_id = request.args.get('user')
        users = Blog.query.filter_by(owner_id=user_id).all()
        return render_template('myblogs.html', title="Blogs", users=users)

    blogs = Blog.query.all()
    return render_template('main.html', title="Blog Posts", blogs=blogs)    

    
@app.route('/')
def index():

    users = User.query.all()
    return render_template('index.html', title="Blog Posters", users=users)

if __name__ == '__main__':
    app.run()