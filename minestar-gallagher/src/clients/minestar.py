import pyodbc
import logging
from minestar_gallagher.configuration import settings

logger = logging.getLogger(__name__)

async def get_current_qualifications():
    """Pull current operator/vehicle state from MineStar (source of truth)"""
    try:
        conn = pyodbc.connect(settings.mine_star_sql_connection)
        cursor = conn.cursor()
        
        query = """
            SELECT EmployeeID, VehicleCallSign, IsAuthorised, Reason
            FROM Your_MineStar_Table_Name_Here   # ← CHANGE THIS TO YOUR ACTUAL TABLE
            WHERE IsActive = 1
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()

        states = {}
        for row in rows:
            vehicle = str(row.VehicleCallSign).strip()
            states[vehicle] = {
                "operator_id": str(row.EmployeeID).strip(),
                "is_authorised": bool(row.IsAuthorised),
                "reason": row.Reason or "MineStar login"
            }
        return states
    except Exception as e:
        logger.error("minestar.query_failed", error=str(e))
        raise