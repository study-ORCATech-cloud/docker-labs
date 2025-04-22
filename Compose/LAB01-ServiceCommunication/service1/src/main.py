import os

import requests
from flask import Flask, jsonify

app = Flask(__name__)

# Environment variables
PORT = os.environ.get("PORT", "5000")
SERVICE2_NAME = os.environ.get("SERVICE2_NAME", "service2")


@app.route("/liveness", methods=["GET"])
def liveness():
    return jsonify({"message": "liveness OK"}), 200


@app.route("/readiness", methods=["GET"])
def readiness():
    return jsonify({"message": "readiness OK"}), 200


@app.route("/getMessage", methods=["GET"])
def get_message():
    try:
        response = requests.get(f"http://{SERVICE2_NAME}:5001/welcome", timeout=5)
        response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
        return jsonify({"message": response.json()}), 200
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
