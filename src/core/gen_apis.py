import json
from typing import Dict, List, Any, Optional
from jinja2 import Template
from settings import ROOT_PATH
from src.core.data.gen_api_db import ApiSqliteDbMannager


def normalize_default(value: Any) -> Any:
    """标准化默认值，将字符串'true'/'false'转换为布尔值"""
    if isinstance(value, str) and value.lower() == 'true':
        return True
    elif isinstance(value, str) and value.lower() == 'false':
        return False
    return value


def safe_load_json(json_str: Optional[str], default: Optional[Dict] = None) -> Dict:
    """安全加载JSON字符串"""
    if not json_str:
        return default or {}
    try:
        return json.loads(json_str)
    except (json.JSONDecodeError, ValueError):
        return default or {}


def parse_api_parameters(api) -> Dict[str, Any]:
    """解析API参数，返回处理后的参数信息"""
    params_dict = safe_load_json(api.params, {})
    data_dict = safe_load_json(api.data, {})
    json_dict = safe_load_json(api.json, {})
    files_dict = safe_load_json(api.files, {})

    params_names = []
    data_names = []
    json_names = []
    files_names = []
    path_params = []
    all_params = []

    # 处理路径参数
    if params_dict and isinstance(params_dict, dict) and 'path' in params_dict:
        for param in params_dict['path']:
            name = param.get('name', '')
            if name:
                path_params.append(name)
                all_params.append({
                    'name': name,
                    'required': param.get('required', True),
                    'type': param.get('schema', {}).get('type', 'string'),
                    'desc': param.get('description', ''),
                    'default': normalize_default(param.get('schema', {}).get('default', None)),
                })

    # 处理查询参数
    if params_dict and isinstance(params_dict, dict) and 'query' in params_dict:
        for param in params_dict['query']:
            name = param.get('name', '')
            if name:
                params_names.append(name)
                all_params.append({
                    'name': name,
                    'required': param.get('required', False),
                    'type': param.get('schema', {}).get('type', 'string'),
                    'desc': param.get('description', ''),
                    'default': normalize_default(param.get('schema', {}).get('default', None)),
                })

    # 处理表单数据参数
    if data_dict and isinstance(data_dict, dict):
        # 检查是否有properties结构
        if 'properties' in data_dict:
            properties = data_dict['properties']
            required = data_dict.get('required', [])
            for name, info in properties.items():
                if name:
                    data_names.append(name)
                    if isinstance(info, dict):
                        param_type = info.get('type', 'string')
                        # 如果是文件类型，检查format
                        if param_type == 'string' and info.get('format') == 'binary':
                            param_type = 'file'
                        all_params.append({
                            'name': name,
                            'required': name in required,
                            'type': param_type,
                            'desc': info.get('description', ''),
                            'default': normalize_default(info.get('default', None)),
                        })
                    else:
                        # 如果info不是字典，创建默认结构
                        all_params.append({
                            'name': name,
                            'required': name in required,
                            'type': 'string',
                            'desc': str(info) if info else '',
                            'default': None,
                        })
        else:
            # 如果没有properties结构，直接处理每一项
            for name, info in data_dict.items():
                if name and name != 'required':  # 排除required字段本身
                    data_names.append(name)
                    if isinstance(info, dict):
                        param_type = info.get('type', 'string')
                        # 如果是文件类型，检查format
                        if param_type == 'string' and info.get('format') == 'binary':
                            param_type = 'file'
                        all_params.append({
                            'name': name,
                            'required': name in data_dict.get('required', []),
                            'type': param_type,
                            'desc': info.get('description', ''),
                            'default': normalize_default(info.get('default', None)),
                        })
                    else:
                        # 如果info不是字典，创建默认结构
                        all_params.append({
                            'name': name,
                            'required': name in data_dict.get('required', []),
                            'type': 'string',
                            'desc': str(info) if info else '',
                            'default': None,
                        })

    # 处理JSON参数
    if json_dict and isinstance(json_dict, dict):
        # 检查是否有properties结构
        if 'properties' in json_dict:
            properties = json_dict['properties']
            required = json_dict.get('required', [])
            for name, info in properties.items():
                if name:
                    json_names.append(name)
                    if isinstance(info, dict):
                        param_type = info.get('type', 'string')
                        # 如果是文件类型，检查format
                        if param_type == 'string' and info.get('format') == 'binary':
                            param_type = 'file'
                        all_params.append({
                            'name': name,
                            'required': name in required,
                            'type': param_type,
                            'desc': info.get('description', ''),
                            'default': normalize_default(info.get('default', None)),
                        })
                    else:
                        # 如果info不是字典，创建默认结构
                        all_params.append({
                            'name': name,
                            'required': name in required,
                            'type': 'string',
                            'desc': str(info) if info else '',
                            'default': None,
                        })
        else:
            # 如果没有properties结构，直接处理每一项
            for name, info in json_dict.items():
                if name and name != 'required':  # 排除required字段本身
                    json_names.append(name)
                    if isinstance(info, dict):
                        param_type = info.get('type', 'string')
                        # 如果是文件类型，检查format
                        if param_type == 'string' and info.get('format') == 'binary':
                            param_type = 'file'
                        all_params.append({
                            'name': name,
                            'required': name in json_dict.get('required', []),
                            'type': param_type,
                            'desc': info.get('description', ''),
                            'default': normalize_default(info.get('default', None)),
                        })
                    else:
                        # 如果info不是字典，创建默认结构
                        all_params.append({
                            'name': name,
                            'required': name in json_dict.get('required', []),
                            'type': 'string',
                            'desc': str(info) if info else '',
                            'default': None,
                        })

    # 处理文件上传参数
    if files_dict and isinstance(files_dict, dict):
        # 检查是否有properties结构
        if 'properties' in files_dict:
            properties = files_dict['properties']
            required = files_dict.get('required', [])
            for name, info in properties.items():
                if name:
                    files_names.append(name)
                    if isinstance(info, dict):
                        all_params.append({
                            'name': name,
                            'required': name in required,
                            'type': 'file',
                            'desc': info.get('description', '文件上传参数'),
                            'default': None,
                        })
                    else:
                        # 如果info不是字典，创建默认结构
                        all_params.append({
                            'name': name,
                            'required': name in required,
                            'type': 'file',
                            'desc': str(info) if info else '文件上传参数',
                            'default': None,
                        })
        else:
            # 如果没有properties结构，直接处理每一项
            for name, info in files_dict.items():
                if name and name != 'required':  # 排除required字段本身
                    files_names.append(name)
                    if isinstance(info, dict):
                        all_params.append({
                            'name': name,
                            'required': name in files_dict.get('required', []),
                            'type': 'file',
                            'desc': info.get('description', '文件上传参数'),
                            'default': None,
                        })
                    else:
                        # 如果info不是字典，创建默认结构
                        all_params.append({
                            'name': name,
                            'required': name in files_dict.get('required', []),
                            'type': 'file',
                            'desc': str(info) if info else '文件上传参数',
                            'default': None,
                        })

    return {
        'params_names': params_names,
        'data_names': data_names,
        'json_names': json_names,
        'files_names': files_names,
        'path_params': path_params,
        'all_params': all_params
    }


def generate_function_name(api_url: str, api_method: str) -> str:
    """生成函数名"""
    # 处理路径参数，将{param}替换为_param
    import re
    function_name = re.sub(r'\{([^}]+)\}', r'_\1', api_url)

    # 将其他特殊字符替换为下划线
    function_name = function_name.replace('-', '_').replace('/', '_').lstrip('_')

    method_suffix_map = {
        'post': '_p',
        'get': '_g',
        'put': '_put',
        'delete': '_del',
        'patch': '_patch'
    }

    method_lower = api_method.lower()
    if method_lower in method_suffix_map:
        function_name += method_suffix_map[method_lower]
    else:
        function_name += f'_{method_lower}'

    return function_name


def generate_parameters_string(all_params: List[Dict[str, Any]]) -> str:
    """生成函数参数字符串"""
    param_list = []

    for param in all_params:
        if param['default'] is not None:
            param_list.append(f"{param['name']}={repr(param['default'])}")
        else:
            # 为所有参数添加默认值None，避免Python语法错误
            param_list.append(f"{param['name']}=None")

    params_str = ','.join(param_list)
    if params_str:
        params_str += ','

    return params_str


def generate_parameters_doc(all_params: List[Dict[str, Any]]) -> str:
    """生成参数文档字符串"""
    param_docs = [
        f"    {param['name']} ({param['type']}): 必填: {'是' if param['required'] else '否'}, {param['desc']}"
        for param in all_params
    ]
    return '\n        '.join(param_docs)


def process_api_data(api) -> Dict[str, Any]:
    """处理单个API数据"""
    parameters = parse_api_parameters(api)
    
    function_name = generate_function_name(api.url, api.method)
    params_str = generate_parameters_string(parameters['all_params'])
    params_doc = generate_parameters_doc(parameters['all_params'])
    
    return {
        'title': api.title,
        'method': api.method,
        'url': api.url,
        'function_name': function_name,
        'path_params': parameters['path_params'],
        'params_names': parameters['params_names'],
        'data_names': parameters['data_names'],
        'json_names': parameters['json_names'],
        'files_names': parameters['files_names'],
        'all_params': parameters['all_params'],
        'params_str': params_str,
        'params_doc': params_doc,
        'res_body': api.res_body,
    }


def generate_api_code():
    """生成API代码主函数"""
    # 创建数据库管理器
    db = ApiSqliteDbMannager.create()

    try:
        # 获取所有API数据
        apis = db.get_all_apis()

        # 处理每个API的数据
        processed_apis = []
        for api in apis:
            api_data = process_api_data(api)
            processed_apis.append(api_data)

        # 将API分块，每200个一个批量
        CHUNK_SIZE = 200
        chunks = [
            processed_apis[i : i + CHUNK_SIZE]
            for i in range(0, len(processed_apis), CHUNK_SIZE)
        ]

        # 读取模板
        template_path = ROOT_PATH / 'src/core/tpl/apis.py.j2'
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()

        # 创建模板
        template = Template(template_content)

        # 生成多个API切片文件
        for i, chunk in enumerate(chunks, 1):
            # 渲染单个切片的模板
            rendered_code = template.render(chunk=chunk, mixin_index=i)

            # 创建文件路径
            output_path = ROOT_PATH / f'src/apis/api_mixin{i}.py'
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(rendered_code)
                
        # 生成__init__.py文件
        init_path = ROOT_PATH / 'src/apis/__init__.py'
        with open(init_path, 'w', encoding='utf-8') as f:
            init_code = ''
            for i in range(1, len(chunks) + 1):
                mixin_file = f'api_mixin{i}'
                mixin_name = f'ApiMixin{i}'
                init_code += f'from .{mixin_file} import {mixin_name}\n'
            init_code += '\n'
            init_code += '\n'
            init_code += 'class AllApiMixin(\n'
            for i in range(1, len(chunks) + 1):
                mixin_name = f'ApiMixin{i}'
                init_code += f'    {mixin_name},\n'
            init_code += '):\n'
            init_code += '    pass\n'
            f.write(init_code)

        print(f"生成了 {len(chunks)} 个API切片文件")
        print("生成了__init__.py文件")

    finally:
        # db.close_db() # SQLAlchemy session is closed by get_db() context manager
        pass



def main():
    """主函数"""
    generate_api_code()


if __name__ == "__main__":
    main()
