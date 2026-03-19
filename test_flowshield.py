"""
FlowShield Unit Tests
Tests for rate limiter including thread safety and per-IP tracking
"""
import time
import pytest
from threading import Thread
from flowshield import RateLimiter, allow_request, get_limiter, reset_limiter


class TestRateLimiter:
    """Test cases for RateLimiter class."""
    
    def test_allow_request_under_limit(self):
        """Should allow requests under limit."""
        limiter = RateLimiter(limit=5)
        
        for i in range(5):
            assert limiter.allow_request() is True
    
    def test_reject_request_over_limit(self):
        """Should reject requests over limit."""
        limiter = RateLimiter(limit=2)
        
        assert limiter.allow_request() is True
        assert limiter.allow_request() is True
        assert limiter.allow_request() is False
    
    def test_counter_resets_on_second_boundary(self):
        """Should reset counter when second changes."""
        limiter = RateLimiter(limit=2)
        
        # Use up limit in first second
        assert limiter.allow_request() is True
        assert limiter.allow_request() is True
        assert limiter.allow_request() is False
        
        # Move to next second
        limiter.current_second += 1
        
        # Should allow more requests
        assert limiter.allow_request() is True
        assert limiter.allow_request() is True
    
    def test_get_retry_after(self):
        """Should return 1 second retry time."""
        limiter = RateLimiter()
        assert limiter.get_retry_after() == 1
    
    def test_zero_limit(self):
        """Should reject all requests with limit=0."""
        limiter = RateLimiter(limit=0)
        assert limiter.allow_request() is False
    
    def test_high_limit(self):
        """Should allow many requests with high limit."""
        limiter = RateLimiter(limit=1000)
        
        for i in range(1000):
            assert limiter.allow_request() is True
        
        assert limiter.allow_request() is False


class TestPerIPTracking:
    """Test per-IP rate limiting."""
    
    def test_per_ip_independent_limits(self):
        """Each IP should have independent limit."""
        limiter = RateLimiter(limit=2, per_ip=True)
        
        # IP 1: use up limit
        assert limiter.allow_request(ip="192.168.1.1") is True
        assert limiter.allow_request(ip="192.168.1.1") is True
        assert limiter.allow_request(ip="192.168.1.1") is False
        
        # IP 2: should have fresh limit
        assert limiter.allow_request(ip="192.168.1.2") is True
        assert limiter.allow_request(ip="192.168.1.2") is True
        assert limiter.allow_request(ip="192.168.1.2") is False
    
    def test_per_ip_resets_per_ip(self):
        """Each IP should reset independently."""
        limiter = RateLimiter(limit=1, per_ip=True)
        
        # IP 1 uses limit
        assert limiter.allow_request(ip="192.168.1.1") is True
        assert limiter.allow_request(ip="192.168.1.1") is False
        
        # Move to next second
        limiter.ip_counters["192.168.1.1"] = (limiter.ip_counters["192.168.1.1"][0] + 1, 0)
        
        # IP 1 should have fresh limit
        assert limiter.allow_request(ip="192.168.1.1") is True
    
    def test_per_ip_no_ip_fallback(self):
        """If no IP provided, should fallback to global."""
        limiter = RateLimiter(limit=2, per_ip=True)
        
        # Without IP
        assert limiter.allow_request(ip=None) is True
        assert limiter.allow_request(ip=None) is True
        assert limiter.allow_request(ip=None) is False


class TestThreadSafety:
    """Test thread-safe operation."""
    
    def test_concurrent_requests_global(self):
        """Should handle concurrent requests safely (global)."""
        limiter = RateLimiter(limit=50)
        results = []
        
        def make_requests():
            for _ in range(20):
                results.append(limiter.allow_request())
        
        threads = [Thread(target=make_requests) for _ in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        # Should have exactly 50 allowed (due to limit)
        allowed = sum(results)
        assert allowed == 50, f"Expected 50 allowed, got {allowed}"
    
    def test_concurrent_requests_per_ip(self):
        """Should handle concurrent requests safely (per-IP)."""
        limiter = RateLimiter(limit=20, per_ip=True)
        results = []
        
        def make_requests(ip):
            for _ in range(30):
                results.append(limiter.allow_request(ip=ip))
        
        threads = [Thread(target=make_requests, args=(f"192.168.1.{i}",)) for i in range(3)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        # Each IP should respect its limit
        allowed = sum(results)
        assert allowed == 60, f"Expected 60 allowed, got {allowed}"


class TestStatistics:
    """Test statistics reporting."""
    
    def test_global_stats(self):
        """Should report global stats correctly."""
        limiter = RateLimiter(limit=100)
        limiter.allow_request()
        
        stats = limiter.get_stats()
        assert stats["mode"] == "global"
        assert stats["limit"] == 100
        assert stats["current_count"] == 1
    
    def test_per_ip_stats(self):
        """Should report per-IP stats correctly."""
        limiter = RateLimiter(limit=100, per_ip=True)
        limiter.allow_request(ip="192.168.1.1")
        limiter.allow_request(ip="192.168.1.2")
        
        stats = limiter.get_stats()
        assert stats["mode"] == "per-ip"
        assert stats["limit"] == 100
        assert stats["tracked_ips"] == 2


class TestGlobalFunctions:
    """Test module-level functions."""
    
    def test_allow_request_function(self):
        """Test global allow_request function."""
        reset_limiter()
        result = allow_request(limit=5)
        assert isinstance(result, bool)
    
    def test_get_limiter_function(self):
        """Test get_limiter returns RateLimiter."""
        reset_limiter()
        limiter = get_limiter(limit=100)
        assert isinstance(limiter, RateLimiter)
        assert limiter.limit == 100
    
    def test_reset_limiter(self):
        """Test reset_limiter clears global instance."""
        get_limiter(limit=100)
        reset_limiter()
        
        # Should create new instance with default limit
        limiter = get_limiter(limit=200)
        assert limiter.limit == 200


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
