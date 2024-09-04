from flask import Flask, render_template, request, jsonify
from utils.logger import Logger
from utils.error_handler import ErrorHandler

app = Flask(__name__)
logger = Logger("WebInterface")
error_handler = ErrorHandler()

# This would be the actual Ozzie agent in production
class MockOzzie:
    def get_status(self):
        return "Operational"
    def execute_workflow(self, name):
        return f"Executed workflow: {name}"
    def list_workflows(self):
        return ["workflow1", "workflow2", "workflow3"]

ozzie = MockOzzie()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/status')
def get_status():
    try:
        status = ozzie.get_status()
        return jsonify({"status": status})
    except Exception as e:
        error_handler.handle_error(e, "Error getting Ozzie's status")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/workflows')
def list_workflows():
    try:
        workflows = ozzie.list_workflows()
        return jsonify({"workflows": workflows})
    except Exception as e:
        error_handler.handle_error(e, "Error listing workflows")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/execute_workflow', methods=['POST'])
def execute_workflow():
    try:
        workflow_name = request.json.get('workflow_name')
        if not workflow_name:
            return jsonify({"error": "Workflow name is required"}), 400
        result = ozzie.execute_workflow(workflow_name)
        return jsonify({"result": result})
    except Exception as e:
        error_handler.handle_error(e, f"Error executing workflow: {workflow_name}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(debug=True)