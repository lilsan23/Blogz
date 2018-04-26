
from flask import Flask, request, redirect, render_template, flash
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

# @app.before_request
# def require_login():
#     allowed_routes = ['login', 'register']
#     if request.endpoint not in allowed_routes and 'username' not in session:
#         return redirect('/login')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            # session['username'] = username
            flash("Logged in")
            return redirect('/')
        else:
            flash('User password incorrect, or user does not exist', 'error')

    return render_template('login.html')


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
            # session['username'] = username
            return redirect('/')
        else:
                # TODO - user better response messaging
            return render_template('register.html', username_error=username_error, 
               password_error=password_error, 
               verify_error=verify_error,
               username=username,
               password=password,
               verify=verify)

    return render_template('register.html')

# @app.route('/logout')
# def logout():
#     del session['username']
#     return redirect('/')

@app.route('/')
def index():
    blogs = Blog.query.all()
    return render_template('main.html', title="Blog Posts", blogs=blogs)
  

@app.route('/newpost', methods=['POST', 'GET'])
def new_post():

#    owner = User.query.filter_by(username=session['username']).first()

   if request.method == 'POST':
        name = request.form['title']
        body = request.form['body']
        owner = request.form['owner']
        
        title_error = ""
        post_error = ""

        if name == "":
            title_error = "Enter title"

        if body == "":
            post_error = "Enter data"

        if not title_error and not post_error:
            new_post_name = Blog(name, body, owner)
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