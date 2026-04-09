import pymysql
def get_conn():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='123456',
        database='lightmeal',
        charset='utf8mb4'
    )
def init_conn():
    conn = get_conn()
    cursor = conn.cursor()
    return conn, cursor
def query_user_info():
    conn, cursor = init_conn()
    cursor.execute('select * from 用户信息')
    result = cursor.fetchall()  # 获取数据
    cursor.close()
    conn.close()
    return result
def insert_user_info(username,gender,height,weight):
    """
    插入用户信息到数据库
    返回: True-成功, False-失败
    """
    conn = None
    cursor = None
    try:
        conn, cursor = init_conn()
        
        # 执行插入语句
        cursor.execute('insert into 用户信息(用户名,性别,身高,体重)  values(%s,%s,%s,%s)', 
                      (username, gender, height, weight))
        
        # 提交事务
        conn.commit()
        print(f"用户数据插入成功: {username}, {gender}, {height}cm, {weight}kg")
        return True
        
    except Exception as e:
        # 发生错误时回滚事务
        if conn:
            conn.rollback()
        print(f"插入用户数据失败: {str(e)}")
        return False
        
    finally:
        # 关闭游标和连接
        if cursor:
            cursor.close()
        if conn:
            conn.close()