from flask import Flask, request, jsonify, render_template, redirect, url_for
from db import mysql, init_mysql_app

app = Flask(__name__)
init_mysql_app(app)

@app.get('/')
def api_gui():
    return render_template('index.html')


#---------------------------------------------------------------------
#---------------------API to list all users---------------------------
#---------------------------------------------------------------------
# @app.route('/users', methods=['GET'])
@app.get('/users')
def list_users():
    try:
        connection = mysql.connect()
        cursor = connection.cursor()
        
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        return jsonify(users)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

# Form action to redirect (specific user's posts)
@app.get('/users/posts')
def redirect_user_posts():
    user_id = request.args.get('user_id')
    return redirect(url_for('list_user_posts', user_id=user_id))

#---------------------------------------------------------------------
#-----------API to list all posts of a specific user------------------
#---------------------------------------------------------------------
@app.get('/users/<int:user_id>/posts')
def list_user_posts(user_id):
    try:
        connection = mysql.connect()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM posts WHERE user_id = %s", (user_id,))
        posts = cursor.fetchall()
        return jsonify(posts)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

# Form action to redirect (specific post's comments)
@app.get('/posts/comments')
def redirect_post_comments():
    post_id = request.args.get('post_id')
    return redirect(url_for('list_post_comments', post_id=post_id))

#---------------------------------------------------------------------
#--------API to list all comments of a specific post------------------
#---------------------------------------------------------------------
@app.get('/posts/<int:post_id>/comments')
def list_post_comments(post_id):
    try:
        connection = mysql.connect()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM comments WHERE post_id = %s", (post_id,))
        comments = cursor.fetchall()
        return jsonify(comments)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()


#---------------------------------------------------------------------
#----------API to add a new post for a specific user------------------
#---------------------------------------------------------------------
@app.post('/users/posts')
def add_post():
    user_id = request.form['user_id']
    try:
        title = request.form['title']
        description = request.form['description']
        connection = mysql.connect()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO posts (user_id, title, description) VALUES (%s, %s, %s)", (user_id, title, description))
        connection.commit()
        return jsonify({'message': 'Post added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()


#---------------------------------------------------------------------
#------------API to add a comment to a specific post------------------
#---------------------------------------------------------------------
@app.post('/posts/comments')
def add_comment():
    post_id = request.form['post_id']
    try:
        comment = request.form['comment']
        commenter_id = request.form['commenter_id']
        
        connection = mysql.connect()
        cursor = connection.cursor()
        
        # Get poster_id associated with post_id
        cursor.execute("SELECT user_id FROM posts WHERE post_id = %s", (post_id,))
        poster_id = cursor.fetchone()

        if not poster_id:
            return jsonify({'error': 'Post ID not found'}), 404

        poster_id = poster_id[0]

        cursor.execute("INSERT INTO comments (post_id, comment, commenter_id, poster_id) VALUES (%s, %s, %s, %s)", (post_id, comment, commenter_id, poster_id))
        connection.commit()
        return jsonify({'message': 'Comment added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()


#---------------------------------------------------------------------
#-----------------API to delete a specific post-----------------------
#---------------------------------------------------------------------
@app.post('/posts/delete')
def delete_post():
    post_id = request.form['post_id']
    try:
        connection = mysql.connect()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM posts WHERE post_id = %s", (post_id,))
        connection.commit()
        return jsonify({'message': 'Post deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()


#---------------------------------------------------------------------
#---------API to update a specific user's information-----------------
#---------------------------------------------------------------------
@app.post('/users/update')
def update_user():
    user_id = request.form.get('user_id')
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400

    try:
        data = request.form
        name = data.get('name')
        email = data.get('email')
        profession = data.get('profession')

        connection = mysql.connect()
        cursor = connection.cursor()

        if name:
            cursor.execute("UPDATE users SET name = %s WHERE user_id = %s", (name, user_id))
        if email:
            cursor.execute("UPDATE users SET email = %s WHERE user_id = %s", (email, user_id))
        if profession:
            cursor.execute("UPDATE users SET profession = %s WHERE user_id = %s", (profession, user_id))

        connection.commit()
        return jsonify({'message': 'User updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()



if __name__ == '__main__':
    app.run(debug=True)
