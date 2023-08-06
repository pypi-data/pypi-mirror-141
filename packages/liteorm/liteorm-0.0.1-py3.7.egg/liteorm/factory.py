from liteorm.info import table_xml, column_xml, get_db_info
from liteorm.mapper import get_mapper_xml
from liteorm.service import Service
from superorm.dao import DAO
from superorm.logger import Logger
from superorm.factory import SQLSessionFactory, SQLSessionFactoryBuild

from liteorm.engine import SQLiteConnHandle, SQLiteExecuteEngine, SQLiteConnBuilder
from superorm.manager import Manager
from superorm.mapper import parse4string


class SQLiteSessionFactory(SQLSessionFactory):

    # Database description information
    database_info = None

    # Database table info
    table_info = None

    # Service dictionary
    _services = None

    def __init__(self, conn_builder: SQLiteConnBuilder, conn_handle: SQLiteConnHandle,
                 execute_engine: SQLiteExecuteEngine, logger: Logger):
        """
        Init session pool
        :param conn_builder: SQLiteConnBuilder
        :param conn_handle: SQLiteConnHandle
        :param execute_engine: SQLiteExecuteEngine
        :param logger: Logger
        """
        super().__init__(conn_builder, conn_handle, execute_engine, False, 1, logger)
        self.load_dao("orm_table_info_dao", parse4string(table_xml))
        self.load_dao("orm_column_info_dao", parse4string(column_xml))
        self.database_info = {}
        self.table_info = {}
        self._services = {}
        _db_info = get_db_info(self._dao)
        self._load_service(_db_info)

    def get_service(self, service_name: str) -> Service:
        """
        Get service
        :param service_name: service name
        :return: DAO
        """
        return self._services[service_name]

    def _load_service(self, database_info: dict):
        """
        load service from database info
        :param database_info: database info
        :return: self
        """
        # for item table in database info
        for table in database_info["tables"]:
            # get mapper xml
            xml_string = get_mapper_xml(database_info, table["Name"])
            # parse to config
            config = parse4string(xml_string)
            # get manager
            manager = Manager(self._engine, config, self._logger)
            # get dao
            dao = DAO(self._session_manager, manager)

            # get the database info && set the table info
            self.table_info[table["Name"]] = table
            # get service
            self._services[table["Name"]] = Service(dao)
        # update the database info
        self.database_info["tables"] = list(self.table_info.values())
        return self


class SQLiteSessionFactoryBuild(SQLSessionFactoryBuild):

    def __init__(self, db_path: str):
        """
        Init
        :param db_path: db_path
        """
        conn_builder = SQLiteConnBuilder(db_path)
        super().__init__(conn_builder, SQLiteConnHandle(), SQLiteExecuteEngine())

    def build(self) -> SQLiteSessionFactory:
        return SQLiteSessionFactory(
            self._conn_builder,
            self._conn_handle,
            self._execute_engine,
            self._logger
        )
