from flask import Flask, render_template, redirect, request
from mysqlconnection import MySQLConnector
app=Flask(__name__)

app.secret_key = ' b095b9a1a8875bdb2b99c729af325f5689b80cb1'

mysql = MySQLConnector(app, 'friendsdb')

@app.route('/')
def index():
    friends = mysql.query_db("SELECT * FROM friends")
    # print friends
    return render_template('index.html', friends=friends)

@app.route('/friends', methods=['POST'])
def create():
    first_name=request.form['first_name']
    last_name=request.form['last_name']
    age = request.form['age']
    met_on=request.form['met_on']
    email=request.form['email']

    query = "INSERT INTO friends (first_name, last_name, age, met_on, email, created_at, updated_at) VALUES (:first_name, :last_name, :age,:met_on, :email, NOW(), NOW())"

    data = {
         'first_name': request.form['first_name'],
         'last_name':  request.form['last_name'],
         'age': request.form['age'],
         'met_on': request.form['met_on'],
         'email': request.form['email']
       }
    mysql.query_db(query, data)
    return redirect('/')

@app.route('/update/<route_id>')
def update(route_id):
    query = "SELECT * FROM friends WHERE id=:data_id"
    data = {'data_id': route_id}
    friend = mysql.query_db(query, data)
    return render_template('edit.html',friend_to_edit=friend[0], data=data)

@app.route('/friends_edit', methods=['POST'])
def update_friend():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    age = request.form['age']
    met_on = request.form['met_on']
    email = request.form['email']    
    data_id = request.form['data_id']
    query = "UPDATE friends SET first_name = :first_name, last_name = :last_name, age = :age, met_on = :met_on, email = :email  Where id = :data_id"

    data = {
         'first_name': request.form['first_name'],
         'last_name':  request.form['last_name'],
         'age': request.form['age'],
         'met_on': request.form['met_on'],
         'email': request.form['email'],
         'data_id': request.form['data_id']
       }
    mysql.query_db(query, data)
    return redirect('/')

@app.route('/remove_friend/<route_id>', methods=['POST'])
def remove_friend(route_id):
    query = "DELETE FROM friends WHERE id =:data_id"
    data = {'data_id': route_id}
    mysql.query_db(query, data)
    return redirect('/')

# @app.route("/delete")
# def clear():
#     mysql.query_db("DELETE FROM friends")
#     return redirect('/')

app.run(debug=True)
