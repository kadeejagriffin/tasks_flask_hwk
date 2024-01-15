from app import app 
from fake_data.tasks import tasks_list

@app.route('/')
def index():
    first_name = 'Kadeeja'
    last_name = 'Griffin'
    age = 27
    return f'Hello World! - From {first_name} {last_name}'

# TASKS ENDPOINT

# Get all tasks
@app.route('/tasks')
def get_tasks():
    # Get tasks from storage (fake data)
    tasks = tasks_list
    return tasks 

# Get single task by ID
@app.route('/tasks/<int:task_id>')
def get_task(task_id):
    # print(f"The task ID is {task_id} and the type is {type(task_id)}")
    # return str(task_id)
    tasks = tasks_list
    # For each dictionary in the list of taks dictionaries
    for task in tasks:
        # if the key of 'id' on the task dictionary matched the task_id from the URL
        if task['id'] == task_id:
            #return that task dictionary
            return task
    # If we loop through all of the tasks without returning, the task with that ID does not exist
    return {'error': f'Task with an ID of {task_id} does not exist'}, 404
    
