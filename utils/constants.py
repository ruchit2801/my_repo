from typing import List

HIVE_SUPPORTED_DATA_TYPES: List[str] = ['tinyint', 'smallint', 'int', 'bigint', 'float', 'double', 'decimal', 'timestamp', 'date', 'string', 'varchar', 'char', 'boolean', 'binary', ]
REQUIRED_KEYS: List[str] = ['schema_name', 'table_name', 'columns', 'input_format']
DATA_TYPE_COMPATIBILITY_MAP = {    
    "boolean": {"boolean"},    
    "tinyint": {"tinyint"},    
    "smallint": {"tinyint", "smallint"},    
    "int": {"tinyint", "smallint", "int"},    
    "bigint": {"tinyint", "smallint", "int", "bigint"},    
    "float": {"float"},    
    "double": {"float", "double"},    
    "decimal": {"decimal"},    
    "varchar": {"varchar"},    
    "timestamp": {"timestamp"},    
    "date": {"date"},
    "binary": {"binary"},
    "string" : {"string"},
    "char": {"char"}
    }