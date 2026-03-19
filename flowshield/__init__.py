"""
FlowShield v1
Ultra-lightweight, high-performance traffic control middleware
Supports both global and per-IP rate limiting with thread safety
"""

from .middleware import protect_app
from .core import allow_request, get_limiter, RateLimiter, reset_limiter

__version__ = "1.0.0"
__author__ = "FlowShield"
__all__ = ["protect_app", "allow_request", "get_limiter", "RateLimiter", "reset_limiter"]
