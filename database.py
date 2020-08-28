#libraries to import
from libraries import *

#connecting to  the database requires internet conncetion
def get_connection():
    con = pymysql.connect(host='13.234.49.227', user='root', password='I+OZreY/gBNjy79QsyQ=', db='camelot_dev', cursorclass=pymysql.cursors.
    DictCursor)
    cur = con.cursor()
    return con,cur
# Close connection.
#connection.close()

#function for getting all entities
def get_entities():
    try:
        con,cur=get_connection()
        cur.execute("SELECT value FROM  tb_agent_value WHERE agent_id = 1154")
        data = cur.fetchall ()
        entities=[]
        for i in range(len(data)):
            entities.append(data[i]['value'])
        con.close()
        return entities
    except:
        print("Oops! Error occured.")

#function for getting id of respective tag
def get_id_tags():
    try:
        con,cur=get_connection()
        cur.execute("SELECT config_id,name FROM tb_agent_config WHERE data_mode=0")
        id = cur.fetchall ()
        id_dict={}
        for i in id:
            id_dict[i['config_id']]=i['name']
        con.close()
        return id_dict
    except:
        print("Oops! Error occured.")

#getting all entites and id of respective tag
id_dict=get_id_tags()
entities=get_entities()

#storing entities 
tag_intent={}
con,cur=get_connection()
for i in id_dict.keys():
    if id_dict[i] not in ["table_name","column_name","column_value"]:
        spec_enty=[]
        query="SELECT value FROM tb_agent_value WHERE config_id=%s and agent_id = 1154"
        cur.execute(query,(i))
        entys = cur.fetchall ()
        for x in range(len(entys)):
            spec_enty.append(entys[x]['value'])
        tag_intent[id_dict[i]]=list(set(spec_enty))
    else:
        pass
con.close()

#getting table_names, column names and values
# 0--> table  1--> column  2--> value

# storing table_names in the dictionary
con,cur=get_connection()
query="SELECT DISTINCT tb.tag_name from tb_tag_info ta INNER JOIN tb_table_tags tb on tb.root_entity = ta.root_entity where tb.entity_type = 0 AND ta.agent_id=1154"
spec_enty=[]
cur.execute(query)
entys = cur.fetchall ()
for x in range(len(entys)):
    spec_enty.append(entys[x]['tag_name'])
tag_intent['table_name']=spec_enty

# storing column_names in the dictionary
query="SELECT DISTINCT tb.tag_name from tb_tag_info ta INNER JOIN tb_table_tags tb on tb.root_entity = ta.root_entity where tb.entity_type = 1 AND ta.agent_id=1154"
spec_enty=[]
cur.execute(query)
entys = cur.fetchall ()
for x in range(len(entys)):
    spec_enty.append(entys[x]['tag_name'])
tag_intent['column_name']=spec_enty

# storing column_values in the dictionary
query="SELECT DISTINCT tb.tag_name from tb_tag_info ta INNER JOIN tb_table_tags tb on tb.root_entity = ta.root_entity where tb.entity_type = 2 AND ta.agent_id=1154"
spec_enty=[]
cur.execute(query)
entys = cur.fetchall ()
for x in range(len(entys)):
    spec_enty.append(entys[x]['tag_name'])
tag_intent['column_value']=spec_enty
con.close()

change_tags={}
for i in tag_intent.keys():
    change_tags[i]=i
change_tags['AggregationColumn']=change_tags['ComparisonColumnOne']=change_tags['ComparisonColumnTwo']=change_tags['ComparisonColumnThree']=change_tags['ColumnNumberOne']=change_tags['ColumnNumberTwo']=change_tags['ColumnNumberThree']='column_name'
change_tags['GroupByColumn']=change_tags['OrderByColumn']='column_name'       

change_tags['ColumnValueOne']=change_tags['ColumnValueTwo']=change_tags['ColumnValueThree']='column_value'       
 
change_tags['ComparatorOne']=change_tags['ComparatorTwo']=change_tags['ComparatorThree']='comparators'
    
change_tags['binary_logic_operator2']='binary_logic_operator'

tag_intent['AggregationColumn']=tag_intent['ComparisonColumnOne']=tag_intent['ComparisonColumnTwo']=tag_intent['ComparisonColumnThree']=tag_intent['ColumnNumberOne']=tag_intent['ColumnNumberTwo']=tag_intent['ColumnNumberThree']=tag_intent['GroupByColumn']=tag_intent['OrderByColumn']=tag_intent['column_name']       

tag_intent['ColumnValueOne']=tag_intent['ColumnValueTwo']=tag_intent['ColumnValueThree']=tag_intent['column_value']       
 
tag_intent['ComparatorOne']=tag_intent['ComparatorTwo']=tag_intent['ComparatorThree']=tag_intent['comparators']       
    
tag_intent['binary_logic_operator2']=tag_intent['binary_logic_operator']
