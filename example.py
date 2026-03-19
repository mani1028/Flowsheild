"""
FlowShield Example Flask Application
Demonstrates ultra-fast rate limiting in action
"""
from flask import Flask, jsonify, request
from flowshield import protect_app

# Create Flask app
app = Flask(__name__)

# OPTION 1: Global rate limiting (all users share the limit)
# protect_app(app, limit=100)

# OPTION 2: Per-IP rate limiting (each IP has its own limit) ⭐ RECOMMENDED
protect_app(app, limit=100, per_ip=True)


@app.route("/test", methods=["GET"])
def test():
    """Simple test endpoint."""
    return jsonify({
        "status": "ok",
        "message": "Request successful",
        "your_ip": request.remote_addr
    })


@app.route("/hello", methods=["GET"])
def hello():
    """Hello endpoint."""
    return jsonify({"status": "ok", "message": "Hello, World!"})


@app.route("/data", methods=["GET"])
def get_data():
    """Data endpoint."""
    return jsonify({
        "status": "ok",
        "data": {
            "timestamp": __import__("time").time(),
            "version": "1.0",
            "mode": "per-ip"
        }
    })


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy"})


if __name__ == "__main__":
    print("🚀 FlowShield v1 Example Server (Production-Ready)")
    print("📍 Starting on http://localhost:8000")
    print("⚡ Rate limit: 100 requests/second (per-IP)")
    print("🔒 Thread-safe with per-IP tracking")
    print("\nAvailable endpoints:")
    print("  GET /test")
    print("  GET /hello")
    print("  GET /data")
    print("  GET /health")
    print("\n💡 Try: curl http://localhost:8000/test")
    print("or with proxy headers: curl -H 'X-Forwarded-For: 192.168.1.1' http://localhost:8000/test")
    
    app.run(debug=False, threaded=True, port=8000)
