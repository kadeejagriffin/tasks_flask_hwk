from flask import request
from app import app, db 
from fake_data.tasks import tasks_list
from datetime import datetime
from app.models import User


users = []

@app.route('/')
def index():
    first_name = 'Kadeeja'
    last_name = 'Griffin'
    age = 27
    return 'Hello World'

# USER ENDPOINTS

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
    for user in users:
        if user['username'] == username or user['email' == email]:
            return {'error': 'A user with that username and/or email already exists'}, 400
    # Create a new user dict and append to the users list
    new_user = {
        "id": len(users) + 1,
        "firstName": first_name,
        "lastName": last_name,
        "usernmae": username,
        "email": email,
        "password": password
    }
    users.append(new_user)
    return new_user, 201
# TASKS ENDPOINT

# Create a route that will get rid of all the tasks
@app.route('/tasks')
def get_tasks():
    # Get tasks from storage (fake data)
    tasks = tasks_list
    return tasks 

# Get single task by ID
@app.route('/tasks/<int:task_id>')
def get_task(task_id):
    # Get all tasks from storage
    tasks = tasks_list
    # For each dictionary in the list of taks dictionaries
    for task in tasks:
        # if the key of 'id' on the task dictionary matched the task_id from the URL
        if task['id'] == task_id:
            #return that task dictionary
            return task
    # If we loop through all of the tasks without returning, the task with that ID does not exist
    return {'error': f'Task with an ID of {task_id} does not exist'}, 404
    
# create a new task
@app.route('/tasks', methods=['POST'])
def create_task():
    # Check to see that the request body is JSON
    if not request.is_json:
        return {'error': " Your content-type must be application/json"}, 400
    # Get data fro the request
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
        
        # Create the new task with the above values
        new_task = {
            "id": len(tasks_list) + 1,
            "title": title,
            "description": description,
            "completed": False,
            "createdAt": datetime.utcnow()
            
        }
        # Add the new task to the tasks
        tasks_list.append(new_task)    
        return new_task, 201

