import json
from pathlib import Path
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import OperationalError as SQLAlchemyOperationalError
from settings import API_DB_PATH, OPENPAI_PATH, OPENPAI_URLS
from src.core.data.models import Base, Apis

DATABASE_URL_SYNC = f"sqlite:///{API_DB_PATH}"

class ApiSqliteDbMannager:
    def __init__(self):
        """初始化ApiSqliteDbMannager对象"""
        self.engine = create_engine(DATABASE_URL_SYNC, echo=False)
        self.SessionLocal = sessionmaker(bind=self.engine)
        self._db_initialized = False

    @classmethod
    def create(cls):
        """工厂方法：创建并初始化数据库管理器"""
        db = cls()
        db.init_db()
        return db

    def __del__(self):
        """对象销毁时自动关闭数据库连接"""
        if self.engine:
            self.engine.dispose()
            print("数据库连接已关闭")

    def init_db(self):
        """初始化数据库连接池并创建表结构"""
        try:
            Base.metadata.create_all(bind=self.engine)
            self._db_initialized = True
            print("数据库连接池初始化成功，表结构已创建/检查")
        except Exception as e:
            print(f"数据库初始化失败: {e}")
            raise

    def get_db(self) -> Session:
        """获取数据库会话"""
        db = self.SessionLocal()
        try:
            return db
        finally:
            db.close()

    def check_db_connection(self):
        """检查数据库连接状态"""
        try:
            db = self.get_db()
            db.query(Apis).first()
            return True
        except SQLAlchemyOperationalError:
            return False
        except Exception:
            return False

    def close_db(self):
        """关闭数据库连接"""
        if self.engine:
            self.engine.dispose()
            print("数据库连接已关闭")

    def reconnect_db(self, max_retries=3, retry_delay=2):
        """数据库重连机制"""
        for attempt in range(max_retries):
            try:
                self.close_db()
                # time.sleep(retry_delay) # For synchronous, use time.sleep
                self.engine = create_engine(DATABASE_URL_SYNC, echo=False)
                self.SessionLocal = sessionmaker(bind=self.engine)
                self.init_db()
                if self.check_db_connection():
                    print(f"数据库重连成功 (尝试 {attempt + 1})")
                    return True
            except Exception as e:
                print(f"重连尝试 {attempt + 1} 失败: {e}")
        return False


    def create_api_db_data(self):
        """创建API数据库数据，自动处理OPENPAI_PATH下所有的.json文件"""
        # 获取OPENPAI_PATH下所有的.json文件
        json_files = []
        try:
            for file_path in OPENPAI_PATH.glob("*.json"):
                if file_path.is_file():
                    json_files.append(file_path.stem)  # 获取不含扩展名的文件名
        except Exception as e:
            print(f"获取JSON文件列表失败: {e}")
            raise

        if not json_files:
            print(f"在 {OPENPAI_PATH} 目录下未找到任何.json文件")
            return

        print(f"将处理以下文件: {json_files}")

        if not self._db_initialized or not self.check_db_connection():
            if not self.reconnect_db():
                raise Exception("数据库连接不可用，无法创建数据")

        db = self.get_db()
        total_processed = 0

        for file_name in json_files:
            openapi_file_path = OPENPAI_PATH / f'{file_name}.json'
            print(f"正在处理文件: {openapi_file_path}")

            try:
                if not openapi_file_path.exists():
                    print(f"文件不存在: {openapi_file_path}")
                    continue

                openapi_data = openapi_file_path.read_text(encoding='utf-8')
                data = json.loads(openapi_data)
                paths = data.get('paths', {})

                file_processed = 0

                for path, methods in paths.items():
                    for method, details in methods.items():
                        title = details.get('summary', '')
                        tags = ','.join(details.get('tags', []))
                        operation_id = details.get('operationId', '')

                        # Extract parameters
                        params_data = {}
                        query_params = []

                        path_params = []

                        for param in details.get('parameters', []):
                            if param['in'] == 'query':
                                query_params.append(param)
                            elif param['in'] == 'path':
                                path_params.append(param)

                        if query_params:
                            params_data['query'] = query_params
                        if path_params:
                            params_data['path'] = path_params

                        # Extract request body
                        req_body_content = details.get('requestBody', {}).get('content', {})
                        json_data = {}
                        data_data = {}
                        files_data = {}
                        
                        if 'application/json' in req_body_content:
                            schema_ref = req_body_content['application/json'].get('schema', {}).get('$ref')
                            if schema_ref:
                                # Resolve schema reference
                                schema_name = schema_ref.split('/')[-1]
                                json_data = data.get('components', {}).get('schemas', {}).get(schema_name, {})
                            else:
                                json_data = req_body_content['application/json'].get('schema', {})
                        elif 'application/x-www-form-urlencoded' in req_body_content:
                            schema_ref = req_body_content['application/x-www-form-urlencoded'].get('schema', {}).get('$ref')
                            if schema_ref:
                                schema_name = schema_ref.split('/')[-1]
                                component_schema = data.get('components', {}).get('schemas', {}).get(schema_name, {})
                                data_data = component_schema
                            else:
                                data_data = req_body_content['application/x-www-form-urlencoded'].get('schema', {})
                        elif 'multipart/form-data' in req_body_content:
                            schema_ref = req_body_content['multipart/form-data'].get('schema', {}).get('$ref')
                            if schema_ref:
                                schema_name = schema_ref.split('/')[-1]
                                files_data = data.get('components', {}).get('schemas', {}).get(schema_name, {})
                            else:
                                files_data = req_body_content['multipart/form-data'].get('schema', {})

                        # Extract response body
                        res_body = {}
                        responses = details.get('responses', {})
                        for status_code, response_details in responses.items():
                            if '200' in status_code or 'default' in status_code:
                                content = response_details.get('content', {})
                                if 'application/json' in content:
                                    res_body = content['application/json'].get('schema', {})
                                break

                        existing_api = db.query(Apis).filter(Apis.method == method.upper(), Apis.url == path).first()

                        if existing_api:
                            existing_api.title = title
                            existing_api.params = json.dumps(params_data, ensure_ascii=False)
                            existing_api.data = json.dumps(data_data, ensure_ascii=False)
                            existing_api.json = json.dumps(json_data, ensure_ascii=False)
                            existing_api.files = json.dumps(files_data, ensure_ascii=False)
                            existing_api.res_body = json.dumps(res_body, ensure_ascii=False)
                        else:
                            new_api = Apis(
                                title=title,
                                method=method.upper(),
                                url=path,
                                params=json.dumps(params_data, ensure_ascii=False),
                                data=json.dumps(data_data, ensure_ascii=False),
                                json=json.dumps(json_data, ensure_ascii=False),
                                files=json.dumps(files_data, ensure_ascii=False),
                                res_body=json.dumps(res_body, ensure_ascii=False),
                            )
                            db.add(new_api)

                        file_processed += 1
                        total_processed += 1

                db.commit()
                print(f"文件 {file_name} 处理完成，共处理 {file_processed} 个API")

            except Exception as e:
                print(f"处理文件 {file_name} 时出错: {e}")
                # 继续处理下一个文件，不中断整个流程

        print(f"所有文件处理完成，总共处理了 {total_processed} 个API")

    def get_all_apis(self):
        """获取所有API记录"""
        try:
            if not self._db_initialized or not self.check_db_connection():
                if not self.reconnect_db():
                    raise Exception("数据库连接不可用")

            db = self.get_db()
            apis = db.query(Apis).all()
            return apis
        except Exception as e:
            print(f"获取API记录失败: {e}")
            return []

    def main_sync(self):
        """同步主函数示例（内部实例方法）"""
        try:
            self.create_api_db_data()

            # 示例：获取所有API记录
            apis = self.get_all_apis()
            print(f"共获取到 {len(apis)} 条API记录")

        except Exception as e:
            print(f"主程序执行失败: {e}")


def get_project_data():
    """获取openapi数据（同步方法，不涉及数据库）, 可替换为真实的 openapi 地址"""
    session = requests.session()
    for k, v in OPENPAI_URLS.items():
        res = session.get(v).text
        Path(OPENPAI_PATH / f"{k}.json").write_text(
            res, encoding='utf-8'
        )


# 为了兼容原有代码，提供一个函数来运行同步主程序
def main(get_apis: bool = True):
    """主函数（用于兼容原有调用）"""
    if get_apis:
        get_project_data()
    db = ApiSqliteDbMannager.create()
    try:
        
        db.create_api_db_data()

        # 示例：获取所有API记录
        apis = db.get_all_apis()
        print(f"共获取到 {len(apis)} 条API记录")

    except Exception as e:
        print(f"主程序执行失败: {e}")
        raise e


if __name__ == "__main__":
    main(False)
