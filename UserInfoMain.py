# 数据库连接测试模块
from Mysql.Mysql_conn import get_conn

def test_database_connection():
    """测试数据库连接功能"""
    try:
        # 调用函数，尝试连接
        conn = get_conn()
        print("✅ 数据库连接成功！")

        # 进一步测试：执行一条简单SQL
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        print("✅ 测试查询成功")
        return True

    except Exception as e:
        print("❌ 连接失败：", e)
        return False

    finally:
        # 不管成功失败，最后关掉连接
        if 'conn' in locals():
            conn.close()
            print("🔌 连接已关闭")

if __name__ == "__main__":
    # 运行数据库连接测试
    test_database_connection()
    print("数据库连接测试完成！")
    print("请使用 app.py 启动Flask应用")