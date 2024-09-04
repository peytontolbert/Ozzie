from flask import Flask, render_template, jsonify, request
from utils.logger import Logger
from utils.error_handler import ErrorHandler
app = Flask(__name__)
logger = Logger("OzzieProgressDashboard")
error_handler = ErrorHandler()

class ProgressTracker:
    def __init__(self):
        self.tasks_completed = 0
        self.learning_progress = 0
        self.current_task = None

    def update(self, tasks_completed, learning_progress, current_task):
        self.tasks_completed = tasks_completed
        self.learning_progress = learning_progress
        self.current_task = current_task

progress_tracker = ProgressTracker()

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/progress')
def get_progress():
    try:
        return jsonify({
            "tasks_completed": progress_tracker.tasks_completed,
            "learning_progress": progress_tracker.learning_progress,
            "current_task": progress_tracker.current_task
        })
    except Exception as e:
        error_handler.handle_error(e, "Error getting progress data")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/update_progress', methods=['POST'])
def update_progress():
    try:
        data = request.json
        progress_tracker.update(
            data.get('tasks_completed', progress_tracker.tasks_completed),
            data.get('learning_progress', progress_tracker.learning_progress),
            data.get('current_task', progress_tracker.current_task)
        )
        return jsonify({"message": "Progress updated successfully"})
    except Exception as e:
        error_handler.handle_error(e, "Error updating progress data")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5001)  # Using a different port to avoid conflict with the main web interface