from flask import Flask, request, jsonify
import model  

app = Flask(__name__)

@app.route("/")
def home():
    return "Flask is running!"

@app.route('/simulate', methods=['POST'])
def simulate():
    data = request.json
    result = model.run_simulation(data)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
