import os
from dotenv import load_dotenv

import psycopg2
from psycopg2.extras import NamedTupleCursor

from contextlib import contextmanager


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


@contextmanager
def get_connection():
    connection = ''
    try:
        connection = psycopg2.connect(DATABASE_URL)
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
    finally:
        if connection:
            connection.close()


class UrlRepository:
    def execute_query(
            self,
            query: str,
            params: tuple[str | int] | None,
    ) -> tuple[str | int] | list[tuple[str | int]] | None:
        """
        Executes a query against the database.
        Args:
            query: The query to execute.
            params: The parameters to pass to the query.

        Returns:
            The result of the query.
        """
        with get_connection() as conn:
            with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
                cur.execute(query, params)
                return cur.fetchall()

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
        return self.execute_query(query, params)[0][0]

    def url_info(self, url_id: int) -> tuple[str | int] | None:
        query = "SELECT * FROM urls WHERE id = %s"
        params = (url_id,)
        try:
            return self.execute_query(query, params)[0]
        except IndexError:
            return None

    def get_url_id(self, url: str) -> int:
        query = "SELECT id FROM urls WHERE url = %s"
        params = (url,)
        return self.execute_query(query, params)[0][0]

    def get_url(self, url_id: int) -> str:
        query = "SELECT url FROM urls WHERE id = %s"
        params = (url_id,)
        return self.execute_query(query, params)[0][0]

    def show_urls(self) -> tuple[str | int] | list[tuple[str | int]] | None:
        """
        Returns data about all urls in database that shows:
        url id, url, date of last check and status code of page.
        """
        query = """SELECT 
                urls.id AS id, 
                urls.url AS url, 
                COALESCE(CAST(checks.created_at AS TEXT), '') AS last_check, 
                COALESCE(CAST(checks.status_code AS TEXT), '') AS status_code 
                FROM urls LEFT JOIN checks ON urls.id = checks.url_id
                WHERE checks.id IS NULL OR checks.id = (
                SELECT MAX(id) FROM checks WHERE url_id = urls.id
                )
                ORDER BY id DESC"""
        params = None
        return self.execute_query(query, params)


class CheckRepository:
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
        with get_connection() as conn:
            with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
                cur.execute(query, params)
                return None

    def show_checks(
            self,
            url_id: int
    ) -> tuple[str | int] | list[tuple[str | int]] | None:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
                cur.execute(
                    "SELECT * FROM checks WHERE url_id = %s",
                    (url_id,)
                )
                return cur.fetchall()
