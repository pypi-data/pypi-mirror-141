import sqlite3

from liteorm.util import cov_table2dict
from superorm.engine import ExecuteEngine, ConnHandle, QueryResult, CountResult, ExecResult, ConnBuilder
from superorm.logger import Logger


class SQLiteConnBuilder(ConnBuilder):

    db_path = None

    def __init__(self, db_path: str):
        """
        Init SQLite Conn Builder
        :param db_path: db_path
        """
        self.db_path = db_path

    def connect(self) -> sqlite3.Connection:
        """
        Gets the database connection method
        """
        return sqlite3.connect(self.db_path)


class SQLiteConnHandle(ConnHandle):

    def ping(self, conn: sqlite3.Connection):
        """
        Test whether the connection is available, and reconnect
        :param conn: database conn
        """
        pass

    def commit(self, conn: sqlite3.Connection):
        """
        Commit the connection
        :param conn: database conn
        """
        conn.commit()

    def rollback(self, conn: sqlite3.Connection):
        """
        Rollback the connection
        :param conn: database conn
        """
        conn.rollback()


class SQLiteExecuteEngine(ExecuteEngine):
    """
    SQLite Execution Engine
    """
    def query(self, conn: sqlite3.Connection, logger: Logger, sql: str, parameter: list) -> QueryResult:
        """
        Query list information
        :param conn database conn
        :param logger logger
        :param sql: SQL statement to be executed
        :param parameter: parameter
        :return: Query results
        """
        cursor = conn.cursor()

        exception = None
        try:
            logger.print_info(sql, parameter)
            sql = sql.replace("%s", "?")
            cursor.execute(sql, parameter)
        except Exception as e:
            logger.print_error(e)
            cursor.close()
            raise exception

        # get result
        result = cursor.fetchall()
        # get column
        col_list = []
        for col_info in cursor.description:
            col_list.append(col_info[0])
        # Close cursor
        cursor.close()
        return cov_table2dict(col_list, result)

    def count(self, conn: sqlite3.Connection, logger: Logger, sql: str, parameter: list) -> CountResult:
        """
        Query quantity information
        :param conn database conn
        :param logger logger
        :param sql: SQL statement to be executed
        :param parameter: parameter
        :return: Query results
        """
        result = self.query(conn, logger, sql, parameter)
        if len(result) == 0:
            return 0
        for value in result[0].values():
            return value

    # noinspection SpellCheckingInspection
    def exec(self, conn: sqlite3.Connection, logger: Logger, sql: str, parameter: list) -> ExecResult:
        """
        Execute SQL statement
        :param conn database conn
        :param logger logger
        :param sql: SQL statement to be executed
        :param parameter: parameter
        :return: Last inserted ID, affecting number of rows
        """
        cursor = conn.cursor()

        exception = None
        try:
            logger.print_info(sql, parameter)
            sql = sql.replace("%s", "?")
            cursor.execute(sql, parameter)
        except Exception as e:
            logger.print_error(e)
            cursor.close()
            raise exception

        # Number of rows affected
        rowcount = cursor.rowcount
        # Last insert ID
        lastrowid = cursor.lastrowid
        # Close cursor
        cursor.close()
        return lastrowid, rowcount
