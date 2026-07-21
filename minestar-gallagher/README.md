# MineStar ↔ Gallagher Integration

Syncs Caterpillar MineStar operator/vehicle qualifications to Gallagher Command Centre for AOZ gate access.

**Key Design**
- MineStar is the source of truth for operator login and competency.
- Gallagher handles final gate decision using the `AOZ_MINESTAR_AUTHORISED` competency.
- Competency lasts for the full shift (enabled on login, disabled on logout).
- Runs as a Windows Service with localhost-only communication.
- SQLite for local state, audit, and mappings.

## Folder Structure
See the recommended layout in the project root.

## Quick Start (Development)

1. **Activate venv**
   ```cmd
   .venv\Scripts\activate