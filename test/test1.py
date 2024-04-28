import pyodbc

# 配置数据源名称（DSN），这需要与ODBC数据源管理器中配置的名称匹配
dsn = 'MySQL'
user = 'root'
password = '123456'
server = '127.0.0.1'  # 或者MySQL服务器的IP地址
database = 'yami_dev'

# 连接到MySQL数据库
conn_str = f'DSN={dsn};SERVER={server};DATABASE={database};UID={user};PWD={password}'
conn = pyodbc.connect(conn_str)

# 创建一个游标对象
cursor = conn.cursor()

# 执行一个SQL查询
d = cursor.execute("show tables")
data= d.fetchall()
print(data)