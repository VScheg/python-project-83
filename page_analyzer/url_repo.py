import psycopg2
from psycopg2.extras import RealDictCursor


class UrlRepository:
    def __init__(self, db_url):
        self.conn = psycopg2.connect(db_url)

    def add_url(self, url):
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO urls (url) VALUES (%s) RETURNING id",
                (url,)
            )
            id = cur.fetchone()[0]

        self.conn.commit()
        return id

    def url_info(self, url_id):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM urls WHERE id = %s", (url_id,))
            return cur.fetchone()

    def get_url_id(self, url):
        with self.conn.cursor() as cur:
            cur.execute("SELECT id FROM urls WHERE url = %s", (url,))
            return cur.fetchone()[0]

    def get_url(self, url_id):
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT url FROM urls WHERE id = %s",
                (url_id,)
            )
            return cur.fetchone()[0]

    def add_check(self, url_check, url_id):
        with self.conn.cursor() as cur:
            cur.execute(
                """INSERT INTO checks
                (status_code, url_id, h1, title, description)
                VALUES (%s, %s, %s, %s, %s)""",
                (
                    url_check.get('status_code'),
                    url_id,
                    url_check.get('h1'),
                    url_check.get('title'),
                    url_check.get('description')
                )
            )

        self.conn.commit()
        return None

    def show_checks(self, url_id):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM checks WHERE url_id = %s", (url_id,))
            return cur.fetchall()

    def show_urls(self):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """SELECT 
                urls.id AS id, 
                urls.url AS url, 
                checks.created_at AS last_check, 
                checks.status_code AS status_code 
                FROM urls LEFT JOIN checks ON urls.id = checks.url_id
                WHERE checks.id IS NULL OR checks.id = (
                SELECT MAX(id) FROM checks WHERE url_id = urls.id
                )
                ORDER BY id DESC"""
            )
            return cur.fetchall()
