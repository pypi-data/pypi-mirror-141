from typing import Dict

DAOMap = Dict
DataBaseInfo = Dict

# noinspection SpellCheckingInspection
table_xml = """
<xml>
    <mapper column="name" parameter="Name"/>
    <mapper column="tbl_name" parameter="TblName"/>
    <mapper column="rootpage" parameter="RootPage"/>
    <mapper column="sql" parameter="SQL"/>
    <sql>
        <key>GetList</key>
        <value>
            SELECT name, tbl_name, rootpage, sql FROM sqlite_master WHERE type = 'table'
        </value>
    </sql>
</xml>
"""

# noinspection SpellCheckingInspection
column_xml = """
<xml>
    <mapper column="cid" parameter="Cid"/>
    <mapper column="name" parameter="Name"/>
    <mapper column="type" parameter="Type"/>
    <mapper column="notnull" parameter="NullAble"/>
    <mapper column="dflt_value" parameter="Defaule"/>
    <mapper column="pk" parameter="PK"/>
    <sql>
        <key>GetList</key>
        <value>
            PRAGMA table_info({{ table_name }})
        </value>
    </sql>
</xml>
"""


# noinspection SpellCheckingInspection
def get_db_info(dao_map: DAOMap) -> DataBaseInfo:
    """
    Get database information
    :param dao_map: the database info dao
    :return: database information
    """
    return _get_info(dao_map, "GetList", {})


def _get_info(dao_map: DAOMap, query_name: str, query_param: dict) -> DataBaseInfo:
    """
    Get database information
    :param dao_map: the database info dao
    :param query_name: table manager query name
    :param query_param: table manager query name && query param
    :return: database information
    """
    # builder manager
    table_manager = dao_map["orm_table_info_dao"]
    column_manager = dao_map["orm_column_info_dao"]

    # Query table structure information
    tables = table_manager.query(query_name, query_param)
    for table in tables:
        table["AutoIncrement"] = table["SQL"].find("AUTOINCREMENT")
        table["columns"] = column_manager.query(
            "GetList", {"table_name": table["Name"]}
        )
    return {"tables": tables}
