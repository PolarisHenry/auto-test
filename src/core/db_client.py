# -*- coding: utf-8 -*-
"""
数据库客户端模块

提供 MySQL 和 SQLite 两种数据库的操作封装，支持连接池、事务管理、批量操作等功能。
- MysqlClient: 基于 PyMySQL + DBUtils 连接池，适用于多并发场景
- SqliteClient: 轻量级本地数据库客户端，适用于单文件场景
"""

import re
import sqlite3

import pymysql
from contextlib import contextmanager
from dbutils.pooled_db import PooledDB
from loguru import logger


class MysqlClient:
    """
    MySQL 数据库客户端

    基于 DBUtils 连接池实现，支持：
    - 懒加载连接池（首次使用时才创建连接）
    - 多数据库实例隔离（按 host:port:database 区分）
    - 事务自动提交/回滚
    - 批量操作与 SQL 文件执行
    """

    _pools = {}
    _pool_configs = {}

    def __init__(self, db_conf: dict):
        """
        初始化客户端（懒加载，不立即创建连接池）

        Args:
            db_conf: 数据库连接参数，需包含 host, port, database 等 pymysql 支持的字段
        """
        self.db_name = self._generate_db_name(db_conf)

        if self.db_name not in MysqlClient._pool_configs:
            MysqlClient._pool_configs[self.db_name] = db_conf.copy()

    def _ensure_pool_exists(self):
        """确保连接池已创建，未创建则按配置初始化"""
        if self.db_name in MysqlClient._pools:
            return

        db_conf = MysqlClient._pool_configs[self.db_name]
        try:
            MysqlClient._pools[self.db_name] = PooledDB(
                creator=pymysql,
                maxconnections=10,
                mincached=0,
                maxcached=5,
                blocking=True,
                ping=1,
                **db_conf,
            )
            logger.info(f"数据库 [{self.db_name}] 连接池初始化成功")
        except Exception as e:
            logger.error(f"初始化数据库 [{self.db_name}] 连接池失败: {e}")
            raise

    @staticmethod
    def _generate_db_name(db_conf: dict) -> str:
        """以 host:port:database 组合作为数据库实例的唯一标识"""
        return f"{db_conf['host']}:{db_conf['port']}:{db_conf['database']}"

    @contextmanager
    def get_connection(self):
        """
        获取数据库连接的上下文管理器，退出时自动归还连接池

        Yields:
            pymysql.connections.Connection
        """
        self._ensure_pool_exists()

        conn = None
        try:
            conn = MysqlClient._pools[self.db_name].connection()
            yield conn
        except Exception as e:
            logger.error(f"获取数据库连接失败: {e}")
            raise
        finally:
            if conn:
                conn.close()

    def query(self, sql: str) -> list:
        """
        执行 SELECT 查询

        Args:
            sql: 查询 SQL 语句

        Returns:
            list[dict]: 查询结果，每行为一个字典
        """
        with self.get_connection() as conn:
            cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
            try:
                cur.execute(sql)
                data = cur.fetchall()

                preview = data[:5]
                logger.debug(
                    f"\n{'='*20} query details {'='*20}\n"
                    f"{sql}\n"
                    f"{'-'*20} 前 5 条预览 {'-'*20}\n"
                    + "\n".join(str(row) for row in preview)
                )

                return data
            except Exception as e:
                logger.error(f"查询数据失败: {e}")
                raise

    def execute(self, sql: str, args: tuple = None) -> int | None:
        """
        执行 INSERT / UPDATE / DELETE

        Args:
            sql: SQL 语句，支持 %s 占位符
            args: 参数元组

        Returns:
            INSERT 返回 lastrowid，UPDATE/DELETE 返回影响行数，其他返回 None
        """
        with self.get_connection() as conn:
            cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
            try:
                logger.debug(f"SQL: {sql % args if args else sql}")

                cur.execute(sql, args=args)
                conn.commit()

                sql_lower = sql.strip().lower()
                if sql_lower.startswith("insert"):
                    inserted_id = cur.lastrowid
                    logger.debug(f"插入完成, lastrowid={inserted_id}")
                    return inserted_id
                elif sql_lower.startswith("update") or sql_lower.startswith("delete"):
                    rowcount = cur.rowcount
                    logger.debug(f"操作完成, 影响行数={rowcount}")
                    return rowcount
                return None

            except Exception as e:
                logger.error(f"执行 SQL 失败: {e}")
                raise

    def execute_many(self, sql: str):
        """
        执行以分号分隔的多条 SQL 语句（在同一事务中）

        Args:
            sql: 包含多条 SQL 的字符串，以 ; 分隔
        """
        with self.get_connection() as conn:
            try:
                conn.begin()
                with conn.cursor() as cur:
                    statements = re.split(r';\s*[\r\n]*', sql)
                    for statement in statements:
                        statement = statement.strip()
                        if statement:
                            logger.debug(f"执行: {statement}")
                            cur.execute(statement)
                conn.commit()
            except Exception as e:
                logger.error(f"执行多条 SQL 失败，已回滚: {e}")
                conn.rollback()

    def execute_file(self, path: str, **kwargs):
        """
        执行 SQL 文件

        支持 SQL 中包含 {key} 格式的占位符，通过 kwargs 传入替换值。

        Args:
            path: SQL 文件路径
            **kwargs: 用于替换 SQL 中 {key} 占位符的键值对
        """
        with self.get_connection() as conn:
            try:
                with open(path, "r", encoding="utf-8") as f:
                    sql_str = f.read()

                sqls = [s.strip() for s in sql_str.split(";") if s.strip()]

                conn.begin()
                for ori_sql in sqls:
                    sql = ori_sql.format(**kwargs) if kwargs else ori_sql
                    logger.debug(f"SQL: {sql}")
                    with conn.cursor() as cur:
                        cur.execute(sql)
                conn.commit()
            except Exception as e:
                logger.error(f"执行 SQL 文件失败，已回滚: {e}")
                conn.rollback()

    def insert_executes_many(self, insert_sql: str, args: list):
        """
        批量插入（使用 executemany）

        Args:
            insert_sql: INSERT 语句
            args: 批量数据列表，每个元素为一条记录的值元组
        """
        with self.get_connection() as conn:
            try:
                with conn.cursor() as cur:
                    cur.executemany(insert_sql, args)
                    conn.commit()
                    logger.debug(f"批量插入完成, 共 {len(args)} 条")
            except Exception as e:
                conn.rollback()
                logger.error(f"批量插入失败: {e}")

    def insert(self, table: str, fields: str, data: tuple):
        """
        插入单条数据

        Args:
            table: 表名
            fields: 字段名，逗号分隔，如 "name,age"
            data: 数据值元组，顺序与 fields 一一对应

        Raises:
            ValueError: 参数为空时抛出
        """
        if not table or not fields or not data:
            raise ValueError("表名、字段名和数据不能为空")

        field_count = len(fields.split(","))
        placeholders = ",".join(["%s"] * field_count)
        sql = f"INSERT INTO {table} ({fields}) VALUES({placeholders})"

        logger.info(f"数据库: {self.db_name}, SQL: {sql}, 参数: {data}")
        self.execute(sql, data)

    def delete(self, table: str, condition: str):
        """
        按条件删除数据

        Args:
            table: 表名
            condition: WHERE 条件（不含 WHERE 关键字）

        Raises:
            ValueError: 参数为空时抛出
        """
        if not table or not condition:
            raise ValueError("表名和删除条件不能为空")

        sql = f"DELETE FROM {table} WHERE {condition}"
        logger.info(f"数据库: {self.db_name}, SQL: {sql}")
        self.execute(sql)

    def update(self, table: str, condition: str, update_result: str):
        """
        按条件更新数据

        Args:
            table: 表名
            condition: WHERE 条件（不含 WHERE 关键字）
            update_result: SET 子句内容，如 "name='tom', age=20"

        Raises:
            ValueError: 参数为空时抛出
        """
        if not table or not condition or not update_result:
            raise ValueError("表名、更新条件和更新结果不能为空")

        sql = f"UPDATE {table} SET {update_result} WHERE {condition}"
        logger.info(f"数据库: {self.db_name}, SQL: {sql}")
        self.execute(sql)

    def select(self, table: str, condition: str, result: str = "*", join_str: str = "") -> list:
        """
        按条件查询数据

        Args:
            table: 表名
            condition: WHERE 条件（不含 WHERE 关键字）
            result: 查询字段，默认 *
            join_str: JOIN 子句，如 "LEFT JOIN t2 ON t1.id=t2.id"

        Returns:
            list[dict]: 查询结果

        Raises:
            ValueError: 参数为空时抛出
        """
        if not table or not condition:
            raise ValueError("表名和查询条件不能为空")

        sql = f"SELECT {result} FROM {table} {join_str} WHERE {condition}"
        result_data = self.query(sql)
        logger.info(f"数据库: {self.db_name}, SQL: {sql}, 返回行数: {len(result_data)}")
        return result_data


class SqliteClient:
    """
    SQLite 数据库客户端

    轻量级单文件数据库操作，支持手动事务控制。
    与 MysqlClient 保持一致的 insert/delete/update 接口。
    """

    def __init__(self, db_path: str):
        """
        Args:
            db_path: SQLite 数据库文件路径
        """
        self.db_path = db_path
        self.connection = sqlite3.connect(db_path)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

    def query(self, sql: str, params: tuple = None) -> list:
        """
        执行 SELECT 查询

        Args:
            sql: 查询 SQL，支持 ? 占位符
            params: 参数元组

        Returns:
            list[dict]: 查询结果
        """
        try:
            if params:
                self.cursor.execute(sql, params)
            else:
                self.cursor.execute(sql)
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            logger.error(f"SQLite 查询失败: {e}")
            return []

    def begin(self):
        """开始事务"""
        self.connection.execute("BEGIN")

    def commit(self):
        """提交事务"""
        self.connection.commit()

    def rollback(self):
        """回滚事务"""
        self.connection.rollback()

    def execute(self, sql: str, params: tuple = None):
        """
        执行 SQL（INSERT/UPDATE/DELETE），不自动提交

        Args:
            sql: SQL 语句
            params: 参数元组
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
        插入单条数据（带事务控制）

        Args:
            table: 表名
            fields: 字段名，逗号分隔
            data: 数据值元组

        Raises:
            ValueError: 参数为空时抛出
        """
        if not table or not fields or not data:
            raise ValueError("表名、字段名和数据不能为空")

        field_count = len(fields.split(","))
        placeholders = ",".join(["?"] * field_count)
        sql = f"INSERT INTO {table} ({fields}) VALUES({placeholders})"

        logger.info(f"数据库: {self.db_path}, SQL: {sql}, 参数: {data}")

        try:
            self.begin()
            self.execute(sql, data)
            self.commit()
        except Exception as e:
            self.rollback()
            logger.error(f"插入失败: {e}")
            raise

    def delete(self, table: str, condition: str):
        """
        按条件删除数据（带事务控制）

        Args:
            table: 表名
            condition: WHERE 条件

        Raises:
            ValueError: 参数为空时抛出
        """
        if not table or not condition:
            raise ValueError("表名和删除条件不能为空")

        sql = f"DELETE FROM {table} WHERE {condition}"
        logger.info(f"数据库: {self.db_path}, SQL: {sql}")

        try:
            self.begin()
            self.execute(sql)
            self.commit()
        except Exception as e:
            self.rollback()
            logger.error(f"删除失败: {e}")
            raise

    def update(self, table: str, condition: str, update_result: str):
        """
        按条件更新数据（带事务控制）

        Args:
            table: 表名
            condition: WHERE 条件
            update_result: SET 子句内容

        Raises:
            ValueError: 参数为空时抛出
        """
        if not table or not condition or not update_result:
            raise ValueError("表名、更新条件和更新结果不能为空")

        sql = f"UPDATE {table} SET {update_result} WHERE {condition}"
        logger.info(f"数据库: {self.db_path}, SQL: {sql}")

        try:
            self.begin()
            self.execute(sql)
            self.commit()
        except Exception as e:
            self.rollback()
            logger.error(f"更新失败: {e}")
            raise

    def close(self):
        """关闭游标和连接"""
        if hasattr(self, "cursor") and self.cursor:
            try:
                self.cursor.close()
            except Exception:
                pass
        if hasattr(self, "connection") and self.connection:
            try:
                self.connection.close()
            except Exception:
                pass

    def __del__(self):
        """析构时自动关闭连接"""
        try:
            self.close()
        except Exception:
            pass


if __name__ == "__main__":
    from settings import *

    res = MysqlClient(DB.fastapi_admin).query("show tables;")
    print(res)
