import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Any


class UrlRepository:
    def __init__(self, db_url: str):
        self.db_url = db_url

    def execute_query(
            self,
            query: str,
            params: tuple,
            cursor_factory=None
    ) -> tuple[Any] | dict | None:
        """
        Executes a query against the database.
        Args:
            query: The query to execute.
            params: The parameters to pass to the query.
            cursor_factory: Optional cursor factory.

        Returns:
            The result of the query.
        """
        with psycopg2.connect(self.db_url) as conn:
            with conn.cursor(cursor_factory=cursor_factory) as cur:
                cur.execute(query, params)
                result = cur.fetchone()
            conn.commit()
        return result

    def add_url(self, url: str) -> int:
        """
        Adds a new url to the database.
        Args:
            url: Url to add.

        Returns:
            Id of the newly added url.
        """
        query = "INSERT INTO urls (url) VALUES (%s) RETURNING id"
        params = (url,)
        return self.execute_query(query, params)[0]

    def url_info(self, url_id: int) -> dict | None:
        query = "SELECT * FROM urls WHERE id = %s"
        params = (url_id,)
        return self.execute_query(
            query,
            params,
            cursor_factory=RealDictCursor
        )

    def get_url_id(self, url: str) -> int:
        query = "SELECT id FROM urls WHERE url = %s"
        params = (url,)
        return self.execute_query(query, params)[0]

    def get_url(self, url_id: int) -> str:
        query = "SELECT url FROM urls WHERE id = %s"
        params = (url_id,)
        return self.execute_query(query, params)[0]


class CheckRepository:
    def __init__(self, db_url: str):
        self.db_url = db_url

    def execute_query(
            self,
            query: str,
            params: tuple | None,
            fetchone: bool = False,
            need_return: bool = True,
            cursor_factory=None
    ) -> tuple[Any] | dict | None:
        """
        Executes a query against the database.
        Args:
            query: The query to execute.
            params: The parameters to pass to the query.
            fetchone: Determines whether to fetch the first row
            from the database or fetch all rows.
            need_return: Determines whether to return a result or not.
            cursor_factory: Optional cursor factory.

        Returns:
            The result of the query.
        """
        with psycopg2.connect(self.db_url) as conn:
            with conn.cursor(cursor_factory=cursor_factory) as cur:
                cur.execute(query, params)
                if need_return:
                    result = cur.fetchone() if fetchone else cur.fetchall()
                else:
                    result = None
            conn.commit()
        return result

    def add_check(self, url_check: dict, url_id: int) -> None:
        query = """INSERT INTO checks
        (status_code, url_id, h1, title, description)
        VALUES (%s, %s, %s, %s, %s)"""
        params = (
            url_check.get('status_code'),
            url_id,
            url_check.get('h1'),
            url_check.get('title'),
            url_check.get('description')
        )
        return self.execute_query(query, params, need_return=False)

    def show_checks(self, url_id: int) -> dict:
        query = "SELECT * FROM checks WHERE url_id = %s"
        params = (url_id,)
        return self.execute_query(query, params, cursor_factory=RealDictCursor)

    def show_urls(self) -> dict:
        """
        Returns data about all urls in database that shows:
        url id, url, date of last check and status code of page.
        """
        query = """SELECT 
                urls.id AS id, 
                urls.url AS url, 
                checks.created_at AS last_check, 
                checks.status_code AS status_code 
                FROM urls LEFT JOIN checks ON urls.id = checks.url_id
                WHERE checks.id IS NULL OR checks.id = (
                SELECT MAX(id) FROM checks WHERE url_id = urls.id
                )
                ORDER BY id DESC"""
        params = None
        return self.execute_query(query, params, cursor_factory=RealDictCursor)
