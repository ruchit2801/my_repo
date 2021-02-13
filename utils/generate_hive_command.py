from typing import Any, Dict, List, Optional, Set, Tuple
from pyhive import hive
from pyhive.exc import OperationalError

def generate_hive_command_from_json(operation, json_data):
    if(operation == "removed"):
        # Generate drop table command
        pass
    elif(operation == "modified"):
        # Generte ALT table command
        pass
    else:
        columns_list = [f"{k} {v}" for k,v in json_data["columns"].items()]
        columns = ', '.join(columns_list)
        ROW_FORMAT_SERDE = "org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe"
        
        LOCATION = f"s3://zanalytics-jumbo/{json_data['schema_name'] + '.db'}/{json_data['table_name']}"
        TBLPROPERTIES = "'skip.header.line.count'='1'"
        WITH_SERDEPROPERTIES = "'field.delim'=',', 'serialization.format'=','"
        use_command = f"use {json_data['schema_name']}"
        #####
        # IMPORTANT : SPECIFY LOCATION OF DATA. IGNORED DURING TESTING. 
        ####
        create_command = f"create external table {json_data['table_name']}({columns}) \
                    ROW FORMAT SERDE '{ROW_FORMAT_SERDE}' \
                    WITH SERDEPROPERTIES ({WITH_SERDEPROPERTIES}) \
                    STORED AS INPUTFORMAT '{STORED_AS_INPUTFORMAT}'\
                    TBLPROPERTIES ({TBLPROPERTIES})"
        return [use_command, create_command]




from typing import Any, Dict, List, Optional, Set, Tuple
from pyhive import hive
from pyhive.exc import OperationalError
def generate_pyhive_command_from_json(json_data: Dict[str, Dict[str, any]]):
    
json_data = {
    "schema_name": "test",
    "table_name": "test2",
    "description": "this is a sample description",
    "columns": {
        "column1": "string",
        "column2": "bigint"
    },
    "partitioned":{
        "column3":"string"
    }
}
query_list = generate_pyhive_command_from_json(json_data)
cursor = hive.connect('localhost').cursor()
for query in query_list:
    cursor.execute(query)
# cursor.execute("use test1")
# cursor.execute("show tables")
# print(cursor.fetchall())
# for result in cursor.fetchall():
#   print(result)



