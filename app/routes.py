from app import app 

@app.route('/')
def index():
    first_name = 'Kadeeja'
    last_name = 'Griffin'
    age = 27
    return f'Hello World! - From {first_name} {last_name}'
