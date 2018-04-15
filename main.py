
from flask import Flask, request, redirect, render_template

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('newpost.html')  
    
    title_error = ""
    post_error = ""

    if title == "":
        title_error = "Enter title"

    if post == "":
        post_error = "Enter data"

    if not title_error and not post_error:
        return render_template('blog.html', title=title, post=post)
    else:
        return render_template('newpost.html', title_error=title_error, 
            post_error=post_error,
            title=title,
            post=post)


# @app.route('/newpost', methods=['POST'])
# def add_entry():

#     blog_id = int(request.form['blog-id'])
#     entry = Blog.query.get(blog_id)

#     return redirect('/')


# if __name__ == '__main__':
app.run()