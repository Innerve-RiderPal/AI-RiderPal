from flask import Flask, request, jsonify
import subprocess
import os
from dotenv import load_dotenv

app = Flask(__name__)

@app.route('/', methods=['GET'])
def make_call():
    phone_number = os.getenv('CALL_TO')

    if not phone_number:
        return jsonify({"error": "Phone number is required."}), 400

    try:
        # Run the main.py script with the phone number
        result = subprocess.run(
            ["python", "main.py", f"--call={phone_number}"],
            capture_output=True, text=True
        )
        
        return jsonify({
            "status": "success",
            "stdout": result.stdout,
            "stderr": result.stderr
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3005)
