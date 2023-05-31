from flask import jsonify

from main import app


@app.post("/ping")
def ping():
    return jsonify({})


@app.get("/ready")
def is_ready():
    return jsonify({})
