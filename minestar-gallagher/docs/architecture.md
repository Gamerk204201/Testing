# Architecture

- MineStar = Source of Truth
- Gallagher = Gate enforcement
- Competency: AOZ_MINESTAR_AUTHORISED (full shift duration)
- Localhost only (no IPs)
- SQLite for mappings & audit
- Windows Service with health endpoint on port 8765