# _*_ coding:utf-8 _*_

import pyodbc

class SQLServerConnector:
    def __init__(self, server, database, username, password):
        # 构建连接字符串
        self.connection_string = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={server};"
            f"DATABASE={database};"
            f"UID={username};"
            f"PWD={password}"
        )
        self.connection = None

    def connect(self):
        # 建立数据库连接
        try:
            self.connection = pyodbc.connect(self.connection_string)
            print("数据库连接成功")
        except pyodbc.Error as e:
            print("数据库连接失败:", e)

    def disconnect(self):
        # 关闭数据库连接
        if self.connection:
            self.connection.close()
            print("数据库连接已关闭")

    def execute_stored_procedure(self, procedure_name, parameters):
        # 执行存储过程
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(f"EXEC {procedure_name} ?", parameters)
                # 如果存储过程返回结果，可以使用 cursor.fetchall() 获取
                results = cursor.fetchall()
                return results
            except pyodbc.Error as e:
                print("执行存储过程失败:", e)
                return None

# 使用示例
if __name__ == "__main__":
    # 数据库连接参数
    server = '你的服务器地址'
    database = '你的数据库名'
    username = '你的用户名'
    password = '你的密码'

    # 创建SQLServerConnector对象
    connector = SQLServerConnector(server, database, username, password)

    # 连接数据库
    connector.connect()

    # 执行存储过程，假设存储过程名为 'usp_MyStoredProcedure'
    # 参数是一个元组，存储过程需要的参数
    procedure_name = 'usp_MyStoredProcedure'
    parameters = ('参数1', 123)  # 示例参数，根据实际情况调整
    results = connector.execute_stored_procedure(procedure_name, parameters)

    # 打印结果
    if results:
        for row in results:
            print(row)

    # 断开连接
    connector.disconnect()