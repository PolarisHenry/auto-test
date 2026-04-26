# -*- coding: utf-8 -*-
"""
数据库客户端模块
提供 MySQL 和 SQLite 数据库操作功能，支持连接池、事务管理等特性
"""

import sqlite3
import re
import pymysql
from dbutils.pooled_db import PooledDB
from contextlib import contextmanager
from loguru import logger


class GlobalData:
    """全局数据类，用于存储共享数据"""
    pass


class MysqlClient:
    """
    MySQL 数据库客户端类
    
    支持多数据库连接池、自动归还连接、事务管理等功能。
    采用懒加载模式，只有在需要时才创建连接池。
    
    主要功能：
    - 数据库连接池管理
    - 查询、插入、更新、删除操作
    - 批量操作和事务支持
    - SQL 文件执行
    """

    _pools = {}  # 存储多个数据库的连接池
    _pool_configs = {}  # 存储数据库配置，用于懒加载

    def __init__(self, db_conf):
        """
        初始化数据库客户端（懒加载模式）
        
        Args:
            db_conf (dict): 数据库配置字典，包含 host、port、database 等连接参数
        """
        # 根据 db_conf 自动生成唯一的 db_name
        self.db_name = self._generate_db_name(db_conf)

        # 只保存配置，不立即创建连接池
        if self.db_name not in MysqlClient._pool_configs:
            MysqlClient._pool_configs[self.db_name] = db_conf.copy()

    def _ensure_pool_exists(self):
        """
        确保连接池存在，如果不存在则创建（懒加载）
        
        Raises:
            Exception: 连接池创建失败时抛出异常
        """
        if self.db_name not in MysqlClient._pools:
            try:
                db_conf = MysqlClient._pool_configs[self.db_name]
                MysqlClient._pools[self.db_name] = PooledDB(
                    creator=pymysql,  # 使用 pymysql 作为数据库驱动
                    maxconnections=10,  # 最大连接数
                    mincached=0,  # 懒加载，不预创建连接
                    maxcached=5,  # 最大空闲连接数
                    blocking=True,  # 超过最大连接数时是否阻塞等待
                    ping=1,  # 自动检查连接是否可用
                    **db_conf  # 数据库连接参数
                )
                logger.info(f"数据库【{self.db_name}】连接池初始化成功")
            except Exception as e:
                logger.error(f"初始化数据库【{self.db_name}】连接池失败，错误原因：{e}")
                raise

    @staticmethod
    def _generate_db_name(db_conf):
        """
        根据 db_conf 自动生成唯一的 db_name
        
        Args:
            db_conf (dict): 数据库配置字典
            
        Returns:
            str: 唯一的数据库标识符
        """
        # 组合 host、port 和 database 字段生成唯一标识符
        key = f"{db_conf['host']}:{db_conf['port']}:{db_conf['database']}"
        return key

    @contextmanager
    def get_connection(self):
        """
        获取数据库连接并自动归还连接池
        
        Yields:
            pymysql.connections.Connection: 数据库连接对象
            
        Raises:
            Exception: 获取连接失败时抛出异常
        """
        # 确保连接池存在（懒加载）
        self._ensure_pool_exists()

        conn = None
        try:
            # 从连接池中获取连接
            conn = MysqlClient._pools[self.db_name].connection()
            yield conn
        except Exception as e:
            logger.error(f"获取数据库连接失败，错误原因：{e}")
            raise
        finally:
            if conn:
                # 归还连接到连接池
                conn.close()

    def query(self, sql):
        """
        查询数据
        
        Args:
            sql (str): SQL 查询语句
            
        Returns:
            list: 查询结果列表，每个元素为字典形式
            
        Raises:
            Exception: 查询失败时抛出异常
        """
        with self.get_connection() as conn:
            cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
            try:
                cur.execute(sql)
                data = cur.fetchall()

                # 日志记录
                msg = f"\n================== query details ==================\n"
                msg += sql
                msg += "\n----------------- 日志仅记录前5条数据 -----------------\n"
                result = data[:5]
                for i in result:
                    msg += str(i) + "\n"
                logger.debug(msg)

                return data
            except Exception as e:
                logger.error(f"查询数据失败，错误原因：{e}")
                raise

    def execute(self, sql: str, args=None):
        """
        执行更新/新增/删除操作
        
        Args:
            sql (str): SQL 语句
            args (tuple, optional): SQL 参数
            
        Returns:
            int: 插入操作返回插入 ID，更新操作返回影响行数，其他操作返回 None
        """
        with self.get_connection() as conn:
            cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
            try:
                sql_string = sql % args if args else sql
                logger.debug(f"\nSQL：{sql_string}")

                cur.execute(sql, args=args)
                conn.commit()
                if sql.lower().strip().startswith('insert'):
                    inserted_id = cur.lastrowid
                    logger.debug("插入操作完成，插入 ID：{}".format(inserted_id))
                    return inserted_id
                elif sql.lower().strip().startswith('update'):
                    rowcount = cur.rowcount
                    logger.debug("更新操作完成，影响行数：{}".format(rowcount))
                    return rowcount
                else:
                    return None

            except Exception as e:
                logger.error(f"执行 SQL 失败，错误原因：{e}")
                raise

    def execute_many(self, sql: str):
        """
        执行多条 SQL 语句
        
        Args:
            sql (str): 包含多条 SQL 的字符串，以分号分隔
        """
        with self.get_connection() as conn:
            try:
                conn.begin()
                with conn.cursor() as cur:
                    statements = re.split(r';\s*[\r\n]*', sql)
                    for statement in statements:
                        if statement.strip():
                            logger.debug(f'执行：{statement}')
                            cur.execute(statement)
                conn.commit()
            except Exception as e:
                logger.error(f"执行多条 SQL 失败，所有操作将回滚，错误原因：{e}")
                conn.rollback()

    def execute_file(self, path, **kwargs):
        """
        执行 SQL 文件
        
        Args:
            path (str): SQL 文件路径
            **kwargs: 动态参数，用于 SQL 文件中的变量替换
        """
        with self.get_connection() as conn:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    sql_str = f.read().replace('\n', '')
                sqls = sql_str.split(';')

                conn.begin()
                locals().update(kwargs)
                for ori_sql in sqls:
                    if ori_sql == '':
                        continue
                    # 兼容 SQL 文件带有变量
                    sql = eval("f'''%s;'''" % ori_sql)
                    logger.debug(f"\nSQL：{sql}")
                    with conn.cursor() as cur:
                        cur.execute(sql)
                conn.commit()
            except Exception as e:
                logger.error(f"执行 SQL 文件失败，所有操作将回滚，错误原因：{e}")
                conn.rollback()

    def insert_executes_many(self, insert_sql, args):
        """
        批量插入数据
        
        Args:
            insert_sql (str): 插入 SQL 语句
            args (list): 批量插入的数据列表
        """
        with self.get_connection() as conn:
            try:
                with conn.cursor() as cur:
                    cur.executemany(insert_sql, args)
                    conn.commit()
                    logger.debug("批量插入数据成功")
            except Exception as e:
                conn.rollback()
                logger.error(f"{insert_sql}批量插入数据失败，错误原因：{e}")

    def insert(self, table: str, fields: str, data: tuple):
        """
        写入单条数据到数据库
        
        Args:
            table (str): 表名
            fields (str): 字段名称，多个字段用逗号分隔
            data (tuple): 要插入的数据值
            
        Raises:
            ValueError: 参数不完整时抛出异常
        """
        if not table or not fields or not data:
            logger.error("请检查您的参数：表名或字段名或数据不正确")
            raise ValueError("表名、字段名和数据不能为空")

        # 根据字段数量生成占位符
        field_count = len(fields.split(","))
        placeholders = ",".join(["%s"] * field_count)
        
        data_sql = f"INSERT INTO {table} ({fields}) VALUES({placeholders})"
        logger.info(f"数据库：{self.db_name}，当前执行sql为：{data_sql}\nsql值为：{data}")
        
        # 使用 execute 方法执行插入
        self.execute(data_sql, data)

    def delete(self, table: str, condition: str):
        """
        删除数据库数据
        
        Args:
            table (str): 表名
            condition (str): 删除条件
            
        Raises:
            ValueError: 参数不完整时抛出异常
        """
        if not table or not condition:
            logger.error("请检查您的参数：表名或删除条件不能为空")
            raise ValueError("表名和删除条件不能为空")

        delete_sql = f"DELETE FROM {table} WHERE {condition}"
        logger.info(f"数据库：{self.db_name}，当前执行sql为：{delete_sql}")
        # 执行删除sql
        self.execute(delete_sql)

    def update(self, table: str, condition: str, update_result: str):
        """
        修改数据库数据
        
        Args:
            table (str): 表名
            condition (str): 更新条件
            update_result (str): 需要更新的字段和值
            
        Raises:
            ValueError: 参数不完整时抛出异常
        """
        if not table or not condition or not update_result:
            logger.error("请检查您的参数：表名、更新条件或更新结果不能为空")
            raise ValueError("表名、更新条件和更新结果不能为空")

        update_sql = f"UPDATE {table} SET {update_result} WHERE {condition}"
        logger.info(f"数据库：{self.db_name}，当前执行sql为：{update_sql}")
        # 执行更新sql
        self.execute(update_sql)

    def select(self, table: str, condition: str, result: str = "*", join_str: str = ""):
        """
        查询数据库数据
        
        Args:
            table (str): 表名
            condition (str): 查询条件
            result (str, optional): 查询字段，默认为 "*"
            join_str (str, optional): JOIN 语句，默认为空
            
        Returns:
            list: 查询结果列表
            
        Raises:
            ValueError: 参数不完整时抛出异常
        """
        if not table or not condition:
            logger.error("请检查您的参数：表名或查询条件不能为空")
            raise ValueError("表名和查询条件不能为空")

        query_sql = f"SELECT {result} FROM {table} {join_str} WHERE {condition}"
        # 执行查询sql并获取返回结果
        result_query = self.query(query_sql)
        logger.info(f"数据库：{self.db_name}，当前执行sql为：{query_sql}\n执行查询sql返回值为：{result_query[:5]}")
        return result_query


class SqliteClient:
    """
    SQLite 数据库客户端类
    
    提供基本的事务管理和数据操作功能，直接操作 SQLite 数据库文件
    不支持连接池，适合轻量级单文件数据库操作
    """

    def __init__(self, db_path: str):
        """
        初始化 SQLite 客户端
        
        Args:
            db_path (str): 数据库文件路径
        """
        self.db_path = db_path
        self.connection = sqlite3.connect(db_path)
        self.connection.row_factory = sqlite3.Row  # 返回字典形式的结果
        self.cursor = self.connection.cursor()

    def query(self, sql: str, params=None):
        """
        查询数据
        
        Args:
            sql (str): 查询 SQL 语句
            params (tuple, optional): 查询参数
            
        Returns:
            list: 查询结果列表，元素为字典
            
        Raises:
            Exception: 查询失败时抛出异常
        """
        try:
            if params:
                self.cursor.execute(sql, params)
            else:
                self.cursor.execute(sql)
            result = self.cursor.fetchall()
            return [dict(row) for row in result]  # 转换为字典列表
        except Exception as e:
            logger.error(f"SQLite 查询失败: {e}")
            return []

    def begin(self):
        """开始事务"""
        self.connection.execute('BEGIN')

    def commit(self):
        """提交事务"""
        self.connection.commit()

    def rollback(self):
        """回滚事务"""
        self.connection.rollback()

    def execute(self, sql: str, params=None):
        """
        执行 SQL 语句
        
        Args:
            sql (str): SQL 语句
            params (tuple, optional): 参数
            
        Raises:
            Exception: 执行失败时抛出异常
        """
        try:
            if params:
                self.cursor.execute(sql, params)
            else:
                self.cursor.execute(sql)
        except Exception as e:
            logger.error(f"SQLite 执行失败: {e}")
            raise

    def insert(self, table: str, fields: str, data: tuple):
        """
        写入单条数据到数据库
        
        Args:
            table (str): 表名
            fields (str): 字段名称，多个字段用逗号分隔
            data (tuple): 要插入的数据值
            
        Raises:
            ValueError: 参数不完整时抛出异常
        """
        if not table or not fields or not data:
            logger.error("请检查您的参数：表名或字段名或数据不正确")
            raise ValueError("表名、字段名和数据不能为空")

        # 为 SQLite 生成占位符
        field_count = len(fields.split(","))
        placeholders = ",".join(["?"] * field_count)
        
        data_sql = f"INSERT INTO {table} ({fields}) VALUES({placeholders})"
        logger.info(f"数据库：{self.db_path}，当前执行sql为：{data_sql}\n sql值为：{data}")
        
        try:
            self.begin()
            self.execute(data_sql, data)
            self.commit()
        except Exception as e:
            self.rollback()
            logger.error(f"插入失败：{e}")
            raise

    def delete(self, table: str, condition: str):
        """
        删除数据库数据
        
        Args:
            table (str): 表名
            condition (str): 删除条件
            
        Raises:
            ValueError: 参数不完整时抛出异常
        """
        if not table or not condition:
            logger.error("请检查您的参数：表名或删除条件不能为空")
            raise ValueError("表名和删除条件不能为空")

        delete_sql = f"DELETE FROM {table} WHERE {condition}"
        logger.info(f"数据库：{self.db_path}，当前执行sql为：{delete_sql}")
        
        try:
            self.begin()
            self.execute(delete_sql)
            self.commit()
        except Exception as e:
            self.rollback()
            logger.error(f"删除失败：{e}")
            raise

    def update(self, table: str, condition: str, update_result: str):
        """
        修改数据库数据
        
        Args:
            table (str): 表名
            condition (str): 更新条件
            update_result (str): 需要更新的字段和值
            
        Raises:
            ValueError: 参数不完整时抛出异常
        """
        if not table or not condition or not update_result:
            logger.error("请检查您的参数：表名、更新条件或更新结果不能为空")
            raise ValueError("表名、更新条件和更新结果不能为空")

        update_sql = f"UPDATE {table} SET {update_result} WHERE {condition}"
        logger.info(f"数据库：{self.db_path}，当前执行sql为：{update_sql}")
        
        try:
            self.begin()
            self.execute(update_sql)
            self.commit()
        except Exception as e:
            self.rollback()
            logger.error(f"更新失败：{e}")
            raise

    def __del__(self):
        """析构函数，自动关闭连接"""
        try:
            self.close()
        except:
            pass  # 忽略关闭时的异常

    def close(self):
        """关闭数据库连接和游标"""
        if hasattr(self, 'cursor') and self.cursor:
            try:
                self.cursor.close()
            except:
                pass
        if hasattr(self, 'connection') and self.connection:
            try:
                self.connection.close()
            except:
                pass


if __name__ == '__main__':
    from settings import *
    res = MysqlClient(DB.fastapi_admin).query("show tables;")
    print(res)