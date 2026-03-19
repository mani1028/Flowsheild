"""
FlowShield Core Engine
Ultra-fast, in-memory request rate limiter with optional per-IP tracking
"""
import time
from threading import Lock
from typing import Optional, Dict


class RateLimiter:
    """
    Thread-safe rate limiter with sliding window algorithm.
    Supports both global and per-IP rate limiting.
    Includes automatic cleanup of inactive IPs (TTL-based).
    """
    
    def __init__(self, limit: int = 100, per_ip: bool = False, ip_ttl: int = 3600):
        """
        Initialize rate limiter.
        
        Args:
            limit: Max requests per second
            per_ip: If True, track limits per IP address (else global)
            ip_ttl: Seconds before removing inactive IP from tracking (default: 1 hour)
        """
        self.limit = limit
        self.per_ip = per_ip
        self.ip_ttl = ip_ttl
        self.lock = Lock()
        
        # Always initialize global counters (for fallback)
        self.current_second = int(time.time())
        self.request_count = 0
        
        if per_ip:
            # Dict of {ip: (current_second, request_count)}
            self.ip_counters: Dict[str, tuple] = {}
            # Track last activity per IP for cleanup
            self.ip_last_seen: Dict[str, int] = {}
    
    def allow_request(self, ip: Optional[str] = None) -> bool:
        """
        Check if request is allowed based on rate limit.
        
        Args:
            ip: Client IP address (required if per_ip=True)
        
        Returns:
            bool: True if request allowed, False if rate limit exceeded
        """
        with self.lock:
            now = int(time.time())
            
            if self.per_ip:
                return self._check_per_ip(ip, now)
            else:
                return self._check_global(now)
    
    def _check_global(self, now: int) -> bool:
        """Check global rate limit (thread-safe)."""
        # Reset counter if we've moved to a new second
        if now != self.current_second:
            self.current_second = now
            self.request_count = 0
        
        # Check if under limit
        if self.request_count < self.limit:
            self.request_count += 1
            return True
        
        return False
    
    def _check_per_ip(self, ip: Optional[str], now: int) -> bool:
        """Check per-IP rate limit (thread-safe)."""
        if not ip:
            # Fallback to global if no IP provided
            return self._check_global(now)
        
        # Clean up inactive IPs periodically (every 100 requests)
        if len(self.ip_counters) % 100 == 0:
            self._cleanup_inactive_ips(now)
        
        # Get or initialize IP counter
        if ip not in self.ip_counters:
            self.ip_counters[ip] = (now, 0)
            self.ip_last_seen[ip] = now
        
        second, count = self.ip_counters[ip]
        
        # Reset counter if second boundary crossed
        if now != second:
            second = now
            count = 0
        
        # Check limit
        if count < self.limit:
            count += 1
            self.ip_counters[ip] = (second, count)
            self.ip_last_seen[ip] = now
            return True
        
        self.ip_counters[ip] = (second, count)
        self.ip_last_seen[ip] = now
        return False
    
    def _cleanup_inactive_ips(self, now: int) -> None:
        """Remove IPs inactive for longer than ip_ttl seconds."""
        inactive_ips = [
            ip for ip, last_seen in self.ip_last_seen.items()
            if now - last_seen > self.ip_ttl
        ]
        
        for ip in inactive_ips:
            self.ip_counters.pop(ip, None)
            self.ip_last_seen.pop(ip, None)
    
    def get_retry_after(self) -> int:
        """Return seconds until next second window."""
        return 1
    
    def get_stats(self) -> Dict:
        """Get current limiter statistics."""
        with self.lock:
            if self.per_ip:
                return {
                    "mode": "per-ip",
                    "limit": self.limit,
                    "tracked_ips": len(self.ip_counters),
                    "ip_ttl": self.ip_ttl
                }
            else:
                return {
                    "mode": "global",
                    "limit": self.limit,
                    "current_count": self.request_count
                }


# Global instance
_limiter: Optional[RateLimiter] = None
_limiter_lock = Lock()


def get_limiter(limit: int = 100, per_ip: bool = False, ip_ttl: int = 3600) -> RateLimiter:
    """
    Get or create global limiter instance.
    
    Args:
        limit: Rate limit (requests per second)
        per_ip: Enable per-IP tracking
        ip_ttl: Seconds before removing inactive IP (default: 3600)
    """
    global _limiter
    
    with _limiter_lock:
        if _limiter is None:
            _limiter = RateLimiter(limit, per_ip=per_ip, ip_ttl=ip_ttl)
    
    return _limiter


def allow_request(limit: int = 100, ip: Optional[str] = None) -> bool:
    """
    Global function to check if request is allowed.
    
    Args:
        limit: Rate limit (requests per second)
        ip: Client IP (optional, for per-IP tracking)
    
    Returns:
        bool: True if allowed, False if rate limited
    """
    limiter = get_limiter(limit)
    return limiter.allow_request(ip=ip)


def reset_limiter() -> None:
    """Reset global limiter (for testing)."""
    global _limiter
    with _limiter_lock:
        _limiter = None
