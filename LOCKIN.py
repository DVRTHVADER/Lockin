from flask import Flask, jsonify, request, render_template
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# In-memory storage
todos = [
    {"id": 1, "name": "LOCK IN."},
    {"id": 2, "name": "Read the Quran"},
    {"id": 3, "name": "Build an app"}
]
done_tasks = []

# Home page route
@app.route('/')
def home():
    return render_template('Home.html')

# To-Do List page route
@app.route('/todo')
def todo_page():
    return render_template('To-Do.html')

# Fetch all todos
@app.route('/api/todos', methods=['GET'])
def get_todos():
    return jsonify(todos)

# Add a new todo
@app.route('/api/todos', methods=['POST'])
def add_todo():
    new_todo = request.get_json()
    if 'name' not in new_todo:
        return jsonify({"error": "Missing 'name' field"}), 400
    new_todo['id'] = max([todo['id'] for todo in todos], default=0) + 1
    new_todo['done'] = False
    todos.append(new_todo)
    return jsonify(new_todo), 201

# Delete a todo
@app.route('/api/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):
    global todos
    todos = [todo for todo in todos if todo["id"] != id]
    return '', 204

# Mark a todo as done
@app.route('/api/todos/<int:id>/done', methods=['PUT'])
def mark_done(id):
    for todo in todos:
        if todo["id"] == id:
            todo["done"] = True
            todo["done_at"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            done_tasks.append(todo)
            todos.remove(todo)
            return jsonify(todo), 200
    return jsonify({"error": "Task not found"}), 404

# Fetch completed tasks
@app.route('/api/todos/done', methods=['GET'])
def get_done_tasks():
    return jsonify(done_tasks)

# Ghost Mode route
@app.route('/ghost_mode')
def ghost_mode():
    return render_template('Ghost_Mode.html')

# Quran page route
@app.route('/quran')
def quran():
    return render_template('Quran.html')

# No Sugar Challenge route
@app.route('/no_sugar_challenge')
def no_sugar_challenge():
    return render_template('NoSugarChallenge.html')

if __name__ == '__main__':
    app.run(debug=True)
