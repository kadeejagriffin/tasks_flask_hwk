from flask import request
from app import app, db 
from fake_data.tasks import tasks_list
from datetime import datetime
from app.models import User, Task
from app.auth import basic_auth, token_auth

# USER ENDPOINTS
@app.route("/token")
@basic_auth.login_required
def get_token():
    user = basic_auth.current_user()
    token = user.get_token()
    return {"token": token, 
            "tokenExpiration":user.token_expiration}
    
# Create New User
@app.route('/users', methods=['POST'])
def create_user():
    # Check to see that the request body is JSON
    if not request.is_json:
        return {'error': 'Your content-type must be application/json'}, 400
    
    # Get the data from the request body
    data = request.json
    # Validate that the data has all of the required fields
    required_fields = ['firstName', 'lastName', 'username', 'email', 'password']
    missing_fields = []
    for field in required_fields:
        if field not in data:
            missing_fields.append(field)
    if missing_fields:
        return {'error': f"{', '.join(missing_fields)} must be in the request body"}, 400
    # Get the values from the data
    first_name = data.get('firstName')
    last_name = data.get('lastName')
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    # Check to see if any current users already have that username and/or email
    check_users = db.session.execute(db.select(User).where((User.username==username)|(User.email==email))).scalars().all() 
    # If the list is not empty then someone alrady has that username or email
    if check_users:
        return {'error': ' A user with that username and/or email already exists'}, 400
    # Create a new user dict instance which will add it to the database
    new_user = User(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
    return new_user.to_dict(), 201

    #update 
@app.route('/users/<int:user_id>', methods=['POST'])
@token_auth.login_required
def edit_user(user_id):
    #check if they sent the data correctly
    if not request.is_json:
        return {'error': 'Your content type must be application/json!'}, 400
    # get user based off id
    user = db.session.get(User, user_id)
    # make sure it exists
    if user is None:
        return {'error': f"user with {user_id} does not exist"}, 404
    # get their token 
    current_user = token_auth.current_user()
    # make sure they are the person logged in 
    if user is not current_user:
        return {'error': 'You cannot change this user as you are not them!'}, 403
    # then we update! 
    data = request.json
    user.update(**data)
    return user.to_dict()

# delete
@app.route('/users/<int:user_id>', methods=['DELETE'])
@token_auth.login_required
def delete_user(user_id):
    # get the user based on the id
    user = db.session.get(User, user_id)
    # get token
    current_user = token_auth.current_user()
    # make sure its a real user
    if user is None:
        return {'error': f"User with {user_id} not found!"}, 404
    # make sure user to delete is current user
    if user is not current_user:
        return {'error': 'You cant do that, delete yourself only'}, 403
    # delete user
    user.delete()
    return {'success': f"{user.username} has been deleted"}

# retrieve
@app.route("/users/<int:user_id>")
def get_user(user_id):
    #get the user
    user = db.session.get(User, user_id)
    #if no user let them know
    if user:
        return user.to_dict()
    else:
        return {'error': f"user with id:{user_id} not found"}, 404

# TASKS ENDPOINT

# Create a route that will get rid of all the tasks
@app.route('/tasks')
def get_tasks():
    # Get tasks from storage (fake data)
    tasks = db.session.execute(db.select(Task)).scalars().all()
    # return a list of the dictionary version of each task in tasks
    return [t.to_dict() for t in tasks]

# Get single task by ID
@app.route('/tasks/<int:task_id>')
def get_task(task_id):
    # Get the task from the database based on the ID
    task = db.session.get(Task, task_id)
    if task:
        return task.to_dict()
    else:
        return {'error': f'Task with an ID of {task_id} does not exist'}, 404
    
# create a new task
@app.route('/tasks', methods=['POST'])
@token_auth.login_required
def create_task():
    # Check to see that the request body is JSON
    if not request.is_json:
        return {'error': " Your content-type must be application/json"}, 400
    # Get data from the request
    data = request.json
    # Check that the data has the required fields
    required_fields = ['title', 'description']
    missing_fields = []
    for field in required_fields:
        if field not in data:
            missing_fields.append(field)
        if missing_fields:
            return {'error': f"{', '.join(missing_fields)} must be in the request body"}, 400
        
    # Get the values from the request data
    title = data.get('title')
    description = data.get('description')
    
    #get logged in user
    user = token_auth.current_user()
        
    # Create a new instance of Task which will add to our database
    new_task = Task(title=title, description=description)
    return new_task.to_dict(), 201
    
#update
# edit Task
@app.route('/tasks/<int:task_id>', methods=['PUT'])
@token_auth.login_required
def edit_task(task_id):
    # check if they sent a good request
    if not request.is_json:
        return {'error': "Your content-type is not application/json"}, 400
    # lets find the post in our db
    task = db.session.get(Task, task_id)
    # if we cant find it, let em know
    if task is None:
        return {'error': f'task with the id of {task_id} does not exist'}, 404
    # get the token from current user
    current_user = token_auth.current_user()
    # check if they are the og or they cant edit
    if task.author is not current_user:
        return {'error': 'This is not your task! Try again.'}, 403
    # then they can get green light
    data = request.json
    task.update(**data)
    return task.to_dict()

    #delete
@app.route("/tasks/<int:task_id>", methods=['DELETE'])
@token_auth.login_required
def delete_task(task_id):
    #get the task
    task = db.session.get(Task, task_id)
    # check if it exists 
    if task is None:
        return {'error': f'We cannot locate tasks with the id of {task_id}'}, 404
    # get the logged in user token
    current_user = token_auth.current_user()
    # check to make sure the logged in user is task author
    if task is not current_user:
        return {'error': 'You can not do that, this is not your task!'}, 403
    # delete task
    task.delete()
    return{'success':f"{task.title} has been deleted!"}
    
