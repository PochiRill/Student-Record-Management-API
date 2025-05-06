from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'mstudent_db'

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        course = request.form['course']
        email = request.form['email']
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        existing_user = cur.fetchone()
        
        if existing_user:
            flash('Email already exists!', 'danger')
        else:
            cur.execute("INSERT INTO users (name, age, course, email) VALUES (%s, %s, %s, %s)", (name, age, course, email))
            mysql.connection.commit()
            flash('User added successfully!', 'success')
        
        cur.close()
        return redirect(url_for('add_user'))
    
    return render_template('add_user.html')

@app.route('/users')
def view_users():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, name, age, course, email FROM users")
    users = cur.fetchall()
    cur.close()
    return render_template('view_user.html', users=users)

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_user(id):
    cur = mysql.connection.cursor()
    
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        course = request.form['course']
        email = request.form['email']
        
        cur.execute("UPDATE users SET name = %s, age = %s, course = %s, email = %s WHERE id = %s", (name, age, course, email, id))
        mysql.connection.commit()
        flash('User updated successfully!', 'success')
        cur.close()
        return redirect(url_for('view_users'))

    cur.execute("SELECT * FROM users WHERE id = %s", (id,))
    user = cur.fetchone()
    cur.close()
    
    return render_template('update_user.html', user=user)

@app.route('/delete/<int:id>')
def delete_user(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    flash('User deleted successfully!', 'success')
    return redirect(url_for('view_users'))

if __name__ == '__main__':
    app.run(debug=True)
