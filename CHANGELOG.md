# Changelog

All notable changes to FlowShield will be documented in this file.

## [1.0.0] - 2026-03-19

### Added
- **Thread-Safe Core**: Integrated `threading.Lock` to ensure safe concurrent access in multi-worker environments without race conditions.
- **Per-IP Rate Limiting**: Added independent tracking quotas per IP address to ensure fairness and prevent single-actor abuse.
- **Memory Growth Control**: Implemented automatic TTL-based cleanup (`ip_ttl`) to periodically purge inactive IPs and prevent memory leaks.
- **Statistics API**: Added `.get_stats()` for real-time monitoring of limit usage and tracked IPs.
- **Comprehensive Testing**: 16 unit tests validating thread safety, boundary resets, and concurrency.
- **Production Benchmarks**: Test suite proving <1ms latency and >1.7M req/s throughput.
