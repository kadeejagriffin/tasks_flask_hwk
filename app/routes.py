from flask import request
from app import app, db 
from fake_data.tasks import tasks_list
from datetime import datetime
from app.models import User, Task

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
    check_users = db.session.execute(db.select(User).where((User.username==username)|(User.email==email))).scalars().all() 
    # If the list is not empty then someone alrady has that username or email
    if check_users:
        return {'error': ' A user with that username and/or email already exists'}, 400
    # Create a new user dict instance which will add it to the database
    new_user = User(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
    return new_user.to_dict(), 201


# TASKS ENDPOINT

# Create a route that will get rid of all the tasks
@app.route('/tasks')
def get_tasks():
    # Get tasks from storage (fake data)
    tasks = db.session.execute(db.select(Task)).scalars().all
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
        
        # Create a new instance of Task which will add to our database
        new_task = Task(title=title, description=description)
        return new_task.to_dict(), 201

