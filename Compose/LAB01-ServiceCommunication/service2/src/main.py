import os

from flask import Flask, jsonify

app = Flask(__name__)

# Environment variables
PORT = os.environ.get("PORT", "5001")


@app.route("/liveness", methods=["GET"])
def liveness():
    return jsonify({"message": "liveness OK"}), 200


@app.route("/readiness", methods=["GET"])
def readiness():
    return jsonify({"message": "readiness OK"}), 200


@app.route("/welcome", methods=["GET"])
def get_message():
    return jsonify({"message": "Welcome to docker compose example"}), 200


@app.route("/welcomeFail", methods=["GET"])
def get_message_fail():
    return jsonify({"message": "This is a failure"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
