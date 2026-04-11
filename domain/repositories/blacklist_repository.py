import os
import psycopg2
from typing import Optional, List, Dict
import uuid
from datetime import datetime

class BlacklistRepository:
    def __init__(self):
        self.db_host = os.environ.get("DB_HOST")
        self.db_port = os.environ.get("DB_PORT")
        self.db_name = os.environ.get("DB_NAME")
        self.db_user = os.environ.get("DB_USER")
        self.db_password = os.environ.get("DB_PASSWORD")

    def _get_conn(self):
        return psycopg2.connect(
            host=self.db_host,
            port=self.db_port,
            dbname=self.db_name,
            user=self.db_user,
            password=self.db_password
        )

    def add(self, blacklist: dict) -> None:
        query = '''
            INSERT INTO blacklist (id, email, app_uuid, blocked_reason, ip_address, created_at)
            VALUES (%s, %s, %s, %s, %s, %s)
        '''
        values = (
            str(uuid.uuid4()),
            blacklist["email"],
            blacklist.get("app_uuid", "dummy-app-uuid"),
            blacklist.get("blocked_reason"),
            blacklist.get("ip_address"),
            blacklist.get("created_at", datetime.utcnow())
        )
        with self._get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(query, values)
                conn.commit()

    def get_by_email(self, email: str) -> Optional[dict]:
        query = "SELECT id, email, app_uuid, blocked_reason, ip_address, created_at FROM blacklist WHERE email = %s"
        with self._get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (email,))
                row = cur.fetchone()
                if row:
                    return {
                        "id": row[0],
                        "email": row[1],
                        "app_uuid": row[2],
                        "blocked_reason": row[3],
                        "ip_address": row[4],
                        "created_at": row[5].isoformat() if row[5] else None
                    }
        return None

    def get_all(self) -> List[Dict]:
        query = "SELECT id, email, app_uuid, blocked_reason, ip_address, created_at FROM blacklist"
        with self._get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                rows = cur.fetchall()
                return [
                    {
                        "id": row[0],
                        "email": row[1],
                        "app_uuid": row[2],
                        "blocked_reason": row[3],
                        "ip_address": row[4],
                        "created_at": row[5].isoformat() if row[5] else None
                    }
                    for row in rows
                ]