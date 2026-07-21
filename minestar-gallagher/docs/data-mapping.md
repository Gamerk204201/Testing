# Data Mapping

## MineStar → Gallagher

| MineStar Field          | Gallagher Field                  | Notes |
|-------------------------|----------------------------------|-------|
| EmployeeID              | Personnel / TAMS ID              | Unique identifier |
| VehicleCallSign         | Vehicle Cardholder ID            | Main link |
| QualificationCode       | AOZ_MINESTAR_AUTHORISED competency | Enable/disable |
| IsAuthorised            | Competency state                 | True = enable |
| Reason                  | Audit log details                | For troubleshooting |

**Rules**
- Enable competency when operator is logged into vehicle and authorised
- Disable on logout, vehicle change, or loss of qualification
- Keep competency active for full shift (no short expiry)