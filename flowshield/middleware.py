"""
FlowShield Middleware
Flask integration for rate limiting (global or per-IP)
"""
import json
from flask import request, make_response
from .core import get_limiter, reset_limiter


def protect_app(app, limit: int = 100, per_ip: bool = False, ip_ttl: int = 3600):
    """
    Protect Flask app with rate limiting middleware.
    
    Args:
        app: Flask application instance
        limit: Max requests per second (default: 100)
        per_ip: Enable per-IP rate limiting (default: False for global)
        ip_ttl: Seconds before removing inactive IP (default: 3600 = 1 hour)
    
    Example:
        # Global rate limit (all users share limit)
        protect_app(app, limit=100)
        
        # Per-IP rate limit (each IP has own limit)
        protect_app(app, limit=100, per_ip=True)
        
        # Per-IP with 30-minute cleanup
        protect_app(app, limit=100, per_ip=True, ip_ttl=1800)
    """
    # Reset limiter to use new settings
    reset_limiter()
    
    limiter = get_limiter(limit, per_ip=per_ip, ip_ttl=ip_ttl)
    
    @app.before_request
    def rate_limit_check():
        """Check rate limit before processing request."""
        # Get client IP (handles proxies)
        client_ip = request.headers.get('X-Forwarded-For', '').split(',')[0].strip()
        if not client_ip:
            client_ip = request.remote_addr or 'unknown'
        
        # Check if request is allowed
        if not limiter.allow_request(ip=client_ip):
            response_data = {
                "status": "busy",
                "message": "Rate limit exceeded",
                "retry_after": limiter.get_retry_after(),
                "limit": limiter.limit,
                "mode": "per-ip" if per_ip else "global"
            }
            
            response = make_response(json.dumps(response_data), 429)
            response.headers["Content-Type"] = "application/json"
            response.headers["Retry-After"] = str(limiter.get_retry_after())
            
            return response
