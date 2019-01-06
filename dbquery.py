import config
import pymssql

def Get_SaleForecast(t1,t2):
    conn = pymssql.connect(server = config.server_ip, user = config.user_name, password = config.password, database = config.db_name)
    cursor = conn.cursor()
    t1 = "'" + t1 + "'"
    t2 = "'" + t2 + "'"
    query = config.queryoccupy.format(t1,t2)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result



