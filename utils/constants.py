from typing import List

HIVE_SUPPORTED_DATA_TYPES: List[str] = ['TINYINT', 'SMALLINT', 'INT', 'BIGINT', 'FLOAT', 'DOUBLE', 'DECIMAL', 'TIMESTAMP', 'DATE', 'STRING', 'VARCHAR', 'CHAR', 'BOOLEAN', 'BINARY', ]
REQUIRED_KEYS: List[str] = ['schema_name', 'table_name', 'columns', 'input_format']
DATA_TYPE_COMPATIBILITY_MAP = {}