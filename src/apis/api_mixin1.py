# This file is auto-generated from API database
from src.core.http_response import CustomResponse

class ApiMixin1:
    """
    API mixin 1
    """

    def request(self):
        pass


    def api_v1_base_access_token_p(self,username=None,password=None,**kw) -> CustomResponse:
        """
        接口名：获取token
        url: /api/v1/base/access_token

        Args:
            username (string): 必填: 是, 用户名称
            password (string): 必填: 是, 密码
            kw: 额外参数，如 raw_method, raw_params: 路径参数一般是get请求, raw_data: 表单参数, raw_json: json格式的参数

        Returns:
            {}
            response 支持jmespath和re正则提取数据，res.search(expression), res.find_all(pattern), res.find_one(pattern)
        """

        # 处理路径参数
        url = "/api/v1/base/access_token"
        
        
        method = "POST"
        if kw.get('raw_method'):
            method = kw.get('raw_method').upper()

        params = {
        }
        if kw.get('raw_params'):
            params = kw.get('raw_params')

        data = {
        }
        if kw.get('raw_data'):
            data = kw.get('raw_data')

        json_data = {
            "username": username,
            "password": password
        }
        if kw.get('raw_json'):
            json_data = kw.get('raw_json')

        files = {
        }
        if kw.get('raw_files'):
            files = kw.get('raw_files')

        response = self.request(url=url, method=method, params=params, data=data, json=json_data, files=files)
        return response


    def api_v1_base_userinfo_g(self,**kw) -> CustomResponse:
        """
        接口名：查看用户信息
        url: /api/v1/base/userinfo

        Args:
        
            kw: 额外参数，如 raw_method, raw_params: 路径参数一般是get请求, raw_data: 表单参数, raw_json: json格式的参数

        Returns:
            {}
            response 支持jmespath和re正则提取数据，res.search(expression), res.find_all(pattern), res.find_one(pattern)
        """

        # 处理路径参数
        url = "/api/v1/base/userinfo"
        
        
        method = "GET"
        if kw.get('raw_method'):
            method = kw.get('raw_method').upper()

        params = {
        }
        if kw.get('raw_params'):
            params = kw.get('raw_params')

        data = {
        }
        if kw.get('raw_data'):
            data = kw.get('raw_data')

        json_data = {
        }
        if kw.get('raw_json'):
            json_data = kw.get('raw_json')

        files = {
        }
        if kw.get('raw_files'):
            files = kw.get('raw_files')

        response = self.request(url=url, method=method, params=params, data=data, json=json_data, files=files)
        return response


    def api_v1_base_usermenu_g(self,**kw) -> CustomResponse:
        """
        接口名：查看用户菜单
        url: /api/v1/base/usermenu

        Args:
        
            kw: 额外参数，如 raw_method, raw_params: 路径参数一般是get请求, raw_data: 表单参数, raw_json: json格式的参数

        Returns:
            {}
            response 支持jmespath和re正则提取数据，res.search(expression), res.find_all(pattern), res.find_one(pattern)
        """

        # 处理路径参数
        url = "/api/v1/base/usermenu"
        
        
        method = "GET"
        if kw.get('raw_method'):
            method = kw.get('raw_method').upper()

        params = {
        }
        if kw.get('raw_params'):
            params = kw.get('raw_params')

        data = {
        }
        if kw.get('raw_data'):
            data = kw.get('raw_data')

        json_data = {
        }
        if kw.get('raw_json'):
            json_data = kw.get('raw_json')

        files = {
        }
        if kw.get('raw_files'):
            files = kw.get('raw_files')

        response = self.request(url=url, method=method, params=params, data=data, json=json_data, files=files)
        return response


    def api_v1_base_userapi_g(self,**kw) -> CustomResponse:
        """
        接口名：查看用户API
        url: /api/v1/base/userapi

        Args:
        
            kw: 额外参数，如 raw_method, raw_params: 路径参数一般是get请求, raw_data: 表单参数, raw_json: json格式的参数

        Returns:
            {}
            response 支持jmespath和re正则提取数据，res.search(expression), res.find_all(pattern), res.find_one(pattern)
        """

        # 处理路径参数
        url = "/api/v1/base/userapi"
        
        
        method = "GET"
        if kw.get('raw_method'):
            method = kw.get('raw_method').upper()

        params = {
        }
        if kw.get('raw_params'):
            params = kw.get('raw_params')

        data = {
        }
        if kw.get('raw_data'):
            data = kw.get('raw_data')

        json_data = {
        }
        if kw.get('raw_json'):
            json_data = kw.get('raw_json')

        files = {
        }
        if kw.get('raw_files'):
            files = kw.get('raw_files')

        response = self.request(url=url, method=method, params=params, data=data, json=json_data, files=files)
        return response


    def api_v1_base_update_password_p(self,old_password=None,new_password=None,**kw) -> CustomResponse:
        """
        接口名：修改密码
        url: /api/v1/base/update_password

        Args:
            old_password (string): 必填: 是, 旧密码
            new_password (string): 必填: 是, 新密码
            kw: 额外参数，如 raw_method, raw_params: 路径参数一般是get请求, raw_data: 表单参数, raw_json: json格式的参数

        Returns:
            {}
            response 支持jmespath和re正则提取数据，res.search(expression), res.find_all(pattern), res.find_one(pattern)
        """

        # 处理路径参数
        url = "/api/v1/base/update_password"
        
        
        method = "POST"
        if kw.get('raw_method'):
            method = kw.get('raw_method').upper()

        params = {
        }
        if kw.get('raw_params'):
            params = kw.get('raw_params')

        data = {
        }
        if kw.get('raw_data'):
            data = kw.get('raw_data')

        json_data = {
            "old_password": old_password,
            "new_password": new_password
        }
        if kw.get('raw_json'):
            json_data = kw.get('raw_json')

        files = {
        }
        if kw.get('raw_files'):
            files = kw.get('raw_files')

        response = self.request(url=url, method=method, params=params, data=data, json=json_data, files=files)
        return response


    def api_v1_user_list_g(self,page=1,page_size=10,username='',email='',dept_id=None,**kw) -> CustomResponse:
        """
        接口名：查看用户列表
        url: /api/v1/user/list

        Args:
            page (integer): 必填: 否, 页码
            page_size (integer): 必填: 否, 每页数量
            username (string): 必填: 否, 用户名称，用于搜索
            email (string): 必填: 否, 邮箱地址
            dept_id (integer): 必填: 否, 部门ID
            kw: 额外参数，如 raw_method, raw_params: 路径参数一般是get请求, raw_data: 表单参数, raw_json: json格式的参数

        Returns:
            {}
            response 支持jmespath和re正则提取数据，res.search(expression), res.find_all(pattern), res.find_one(pattern)
        """

        # 处理路径参数
        url = "/api/v1/user/list"
        
        
        method = "GET"
        if kw.get('raw_method'):
            method = kw.get('raw_method').upper()

        params = {
            "page": page,
            "page_size": page_size,
            "username": username,
            "email": email,
            "dept_id": dept_id
        }
        if kw.get('raw_params'):
            params = kw.get('raw_params')

        data = {
        }
        if kw.get('raw_data'):
            data = kw.get('raw_data')

        json_data = {
        }
        if kw.get('raw_json'):
            json_data = kw.get('raw_json')

        files = {
        }
        if kw.get('raw_files'):
            files = kw.get('raw_files')

        response = self.request(url=url, method=method, params=params, data=data, json=json_data, files=files)
        return response


    def api_v1_user_get_g(self,user_id=None,**kw) -> CustomResponse:
        """
        接口名：查看用户
        url: /api/v1/user/get

        Args:
            user_id (integer): 必填: 是, 用户ID
            kw: 额外参数，如 raw_method, raw_params: 路径参数一般是get请求, raw_data: 表单参数, raw_json: json格式的参数

        Returns:
            {}
            response 支持jmespath和re正则提取数据，res.search(expression), res.find_all(pattern), res.find_one(pattern)
        """

        # 处理路径参数
        url = "/api/v1/user/get"
        
        
        method = "GET"
        if kw.get('raw_method'):
            method = kw.get('raw_method').upper()

        params = {
            "user_id": user_id
        }
        if kw.get('raw_params'):
            params = kw.get('raw_params')

        data = {
        }
        if kw.get('raw_data'):
            data = kw.get('raw_data')

        json_data = {
        }
        if kw.get('raw_json'):
            json_data = kw.get('raw_json')

        files = {
        }
        if kw.get('raw_files'):
            files = kw.get('raw_files')

        response = self.request(url=url, method=method, params=params, data=data, json=json_data, files=files)
        return response


    def api_v1_user_create_p(self,email=None,username=None,password=None,is_active=True,is_superuser=False,role_ids=[],dept_id=0,**kw) -> CustomResponse:
        """
        接口名：创建用户
        url: /api/v1/user/create

        Args:
            email (string): 必填: 是, 
            username (string): 必填: 是, 
            password (string): 必填: 是, 
            is_active (string): 必填: 否, 
            is_superuser (string): 必填: 否, 
            role_ids (string): 必填: 否, 
            dept_id (string): 必填: 否, 部门ID
            kw: 额外参数，如 raw_method, raw_params: 路径参数一般是get请求, raw_data: 表单参数, raw_json: json格式的参数

        Returns:
            {}
            response 支持jmespath和re正则提取数据，res.search(expression), res.find_all(pattern), res.find_one(pattern)
        """

        # 处理路径参数
        url = "/api/v1/user/create"
        
        
        method = "POST"
        if kw.get('raw_method'):
            method = kw.get('raw_method').upper()

        params = {
        }
        if kw.get('raw_params'):
            params = kw.get('raw_params')

        data = {
        }
        if kw.get('raw_data'):
            data = kw.get('raw_data')

        json_data = {
            "email": email,
            "username": username,
            "password": password,
            "is_active": is_active,
            "is_superuser": is_superuser,
            "role_ids": role_ids,
            "dept_id": dept_id
        }
        if kw.get('raw_json'):
            json_data = kw.get('raw_json')

        files = {
        }
        if kw.get('raw_files'):
            files = kw.get('raw_files')

        response = self.request(url=url, method=method, params=params, data=data, json=json_data, files=files)
        return response


    def api_v1_user_update_p(self,id=None,email=None,username=None,is_active=True,is_superuser=False,role_ids=[],dept_id=0,**kw) -> CustomResponse:
        """
        接口名：更新用户
        url: /api/v1/user/update

        Args:
            id (integer): 必填: 是, 
            email (string): 必填: 是, 
            username (string): 必填: 是, 
            is_active (string): 必填: 否, 
            is_superuser (string): 必填: 否, 
            role_ids (string): 必填: 否, 
            dept_id (string): 必填: 否, 
            kw: 额外参数，如 raw_method, raw_params: 路径参数一般是get请求, raw_data: 表单参数, raw_json: json格式的参数

        Returns:
            {}
            response 支持jmespath和re正则提取数据，res.search(expression), res.find_all(pattern), res.find_one(pattern)
        """

        # 处理路径参数
        url = "/api/v1/user/update"
        
        
        method = "POST"
        if kw.get('raw_method'):
            method = kw.get('raw_method').upper()

        params = {
        }
        if kw.get('raw_params'):
            params = kw.get('raw_params')

        data = {
        }
        if kw.get('raw_data'):
            data = kw.get('raw_data')

        json_data = {
            "id": id,
            "email": email,
            "username": username,
            "is_active": is_active,
            "is_superuser": is_superuser,
            "role_ids": role_ids,
            "dept_id": dept_id
        }
        if kw.get('raw_json'):
            json_data = kw.get('raw_json')

        files = {
        }
        if kw.get('raw_files'):
            files = kw.get('raw_files')

        response = self.request(url=url, method=method, params=params, data=data, json=json_data, files=files)
        return response


    def api_v1_user_delete_del(self,user_id=None,**kw) -> CustomResponse:
        """
        接口名：删除用户
        url: /api/v1/user/delete

        Args:
            user_id (integer): 必填: 是, 用户ID
            kw: 额外参数，如 raw_method, raw_params: 路径参数一般是get请求, raw_data: 表单参数, raw_json: json格式的参数

        Returns:
            {}
            response 支持jmespath和re正则提取数据，res.search(expression), res.find_all(pattern), res.find_one(pattern)
        """

        # 处理路径参数
        url = "/api/v1/user/delete"
        
        
        method = "DELETE"
        if kw.get('raw_method'):
            method = kw.get('raw_method').upper()

        params = {
            "user_id": user_id
        }
        if kw.get('raw_params'):
            params = kw.get('raw_params')

        data = {
        }
        if kw.get('raw_data'):
            data = kw.get('raw_data')

        json_data = {
        }
        if kw.get('raw_json'):
            json_data = kw.get('raw_json')

        files = {
        }
        if kw.get('raw_files'):
            files = kw.get('raw_files')

        response = self.request(url=url, method=method, params=params, data=data, json=json_data, files=files)
        return response


    def api_v1_user_reset_password_p(self,user_id=None,**kw) -> CustomResponse:
        """
        接口名：重置密码
        url: /api/v1/user/reset_password

        Args:
            user_id (integer): 必填: 是, 用户ID
            kw: 额外参数，如 raw_method, raw_params: 路径参数一般是get请求, raw_data: 表单参数, raw_json: json格式的参数

        Returns:
            {}
            response 支持jmespath和re正则提取数据，res.search(expression), res.find_all(pattern), res.find_one(pattern)
        """

        # 处理路径参数
        url = "/api/v1/user/reset_password"
        
        
        method = "POST"
        if kw.get('raw_method'):
            method = kw.get('raw_method').upper()

        params = {
        }
        if kw.get('raw_params'):
            params = kw.get('raw_params')

        data = {
        }
        if kw.get('raw_data'):
            data = kw.get('raw_data')

        json_data = {
            "user_id": user_id
        }
        if kw.get('raw_json'):
            json_data = kw.get('raw_json')

        files = {
        }
        if kw.get('raw_files'):
            files = kw.get('raw_files')

        response = self.request(url=url, method=method, params=params, data=data, json=json_data, files=files)
        return response


    def api_v1_role_list_g(self,page=1,page_size=10,role_name='',**kw) -> CustomResponse:
        """
        接口名：查看角色列表
        url: /api/v1/role/list

        Args:
            page (integer): 必填: 否, 页码
            page_size (integer): 必填: 否, 每页数量
            role_name (string): 必填: 否, 角色名称，用于查询
            kw: 额外参数，如 raw_method, raw_params: 路径参数一般是get请求, raw_data: 表单参数, raw_json: json格式的参数

        Returns:
            {}
            response 支持jmespath和re正则提取数据，res.search(expression), res.find_all(pattern), res.find_one(pattern)
        """

        # 处理路径参数
        url = "/api/v1/role/list"
        
        
        method = "GET"
        if kw.get('raw_method'):
            method = kw.get('raw_method').upper()

        params = {
            "page": page,
            "page_size": page_size,
            "role_name": role_name
        }
        if kw.get('raw_params'):
            params = kw.get('raw_params')

        data = {
        }
        if kw.get('raw_data'):
            data = kw.get('raw_data')

        json_data = {
        }
        if kw.get('raw_json'):
            json_data = kw.get('raw_json')

        files = {
        }
        if kw.get('raw_files'):
            files = kw.get('raw_files')

        response = self.request(url=url, method=method, params=params, data=data, json=json_data, files=files)
        return response


    def api_v1_role_get_g(self,role_id=None,**kw) -> CustomResponse:
        """
        接口名：查看角色
        url: /api/v1/role/get

        Args:
            role_id (integer): 必填: 是, 角色ID
            kw: 额外参数，如 raw_method, raw_params: 路径参数一般是get请求, raw_data: 表单参数, raw_json: json格式的参数

        Returns:
            {}
            response 支持jmespath和re正则提取数据，res.search(expression), res.find_all(pattern), res.find_one(pattern)
        """

        # 处理路径参数
        url = "/api/v1/role/get"
        
        
        method = "GET"
        if kw.get('raw_method'):
            method = kw.get('raw_method').upper()

        params = {
            "role_id": role_id
        }
        if kw.get('raw_params'):
            params = kw.get('raw_params')

        data = {
        }
        if kw.get('raw_data'):
            data = kw.get('raw_data')

        json_data = {
        }
        if kw.get('raw_json'):
            json_data = kw.get('raw_json')

        files = {
        }
        if kw.get('raw_files'):
            files = kw.get('raw_files')

        response = self.request(url=url, method=method, params=params, data=data, json=json_data, files=files)
        return response


    def api_v1_role_create_p(self,name=None,desc='',**kw) -> CustomResponse:
        """
        接口名：创建角色
        url: /api/v1/role/create

        Args:
            name (string): 必填: 是, 
            desc (string): 必填: 否, 
            kw: 额外参数，如 raw_method, raw_params: 路径参数一般是get请求, raw_data: 表单参数, raw_json: json格式的参数

        Returns:
            {}
            response 支持jmespath和re正则提取数据，res.search(expression), res.find_all(pattern), res.find_one(pattern)
        """

        # 处理路径参数
        url = "/api/v1/role/create"
        
        
        method = "POST"
        if kw.get('raw_method'):
            method = kw.get('raw_method').upper()

        params = {
        }
        if kw.get('raw_params'):
            params = kw.get('raw_params')

        data = {
        }
        if kw.get('raw_data'):
            data = kw.get('raw_data')

        json_data = {
            "name": name,
            "desc": desc
        }
        if kw.get('raw_json'):
            json_data = kw.get('raw_json')

        files = {
        }
        if kw.get('raw_files'):
            files = kw.get('raw_files')

        response = self.request(url=url, method=method, params=params, data=data, json=json_data, files=files)
        return response


    def api_v1_role_update_p(self,id=None,name=None,desc='',**kw) -> CustomResponse:
        """
        接口名：更新角色
        url: /api/v1/role/update

        Args:
            id (integer): 必填: 是, 
            name (string): 必填: 是, 
            desc (string): 必填: 否, 
            kw: 额外参数，如 raw_method, raw_params: 路径参数一般是get请求, raw_data: 表单参数, raw_json: json格式的参数

        Returns:
            {}
            response 支持jmespath和re正则提取数据，res.search(expression), res.find_all(pattern), res.find_one(pattern)
        """

        # 处理路径参数
        url = "/api/v1/role/update"
        
        
        method = "POST"
        if kw.get('raw_method'):
            method = kw.get('raw_method').upper()

        params = {
        }
        if kw.get('raw_params'):
            params = kw.get('raw_params')

        data = {
        }
        if kw.get('raw_data'):
            data = kw.get('raw_data')

        json_data = {
            "id": id,
            "name": name,
            "desc": desc
        }
        if kw.get('raw_json'):
            json_data = kw.get('raw_json')

        files = {
        }
        if kw.get('raw_files'):
            files = kw.get('raw_files')

        response = self.request(url=url, method=method, params=params, data=data, json=json_data, files=files)
        return response


    def api_v1_role_delete_del(self,role_id=None,**kw) -> CustomResponse:
        """
        接口名：删除角色
        url: /api/v1/role/delete

        Args:
            role_id (integer): 必填: 是, 角色ID
            kw: 额外参数，如 raw_method, raw_params: 路径参数一般是get请求, raw_data: 表单参数, raw_json: json格式的参数

        Returns:
            {}
            response 支持jmespath和re正则提取数据，res.search(expression), res.find_all(pattern), res.find_one(pattern)
        """

        # 处理路径参数
        url = "/api/v1/role/delete"
        
        
        method = "DELETE"
        if kw.get('raw_method'):
            method = kw.get('raw_method').upper()

        params = {
            "role_id": role_id
        }
        if kw.get('raw_params'):
            params = kw.get('raw_params')

        data = {
        }
        if kw.get('raw_data'):
            data = kw.get('raw_data')

        json_data = {
        }
        if kw.get('raw_json'):
            json_data = kw.get('raw_json')

        files = {
        }
        if kw.get('raw_files'):
            files = kw.get('raw_files')

        response = self.request(url=url, method=method, params=params, data=data, json=json_data, files=files)
        return response


    def api_v1_role_authorized_g(self,id=None,**kw) -> CustomResponse:
        """
        接口名：查看角色权限
        url: /api/v1/role/authorized

        Args:
            id (integer): 必填: 是, 角色ID
            kw: 额外参数，如 raw_method, raw_params: 路径参数一般是get请求, raw_data: 表单参数, raw_json: json格式的参数

        Returns:
            {}
            response 支持jmespath和re正则提取数据，res.search(expression), res.find_all(pattern), res.find_one(pattern)
        """

        # 处理路径参数
        url = "/api/v1/role/authorized"
        
        
        method = "GET"
        if kw.get('raw_method'):
            method = kw.get('raw_method').upper()

        params = {
            "id": id
        }
        if kw.get('raw_params'):
            params = kw.get('raw_params')

        data = {
        }
        if kw.get('raw_data'):
            data = kw.get('raw_data')

        json_data = {
        }
        if kw.get('raw_json'):
            json_data = kw.get('raw_json')

        files = {
        }
        if kw.get('raw_files'):
            files = kw.get('raw_files')

        response = self.request(url=url, method=method, params=params, data=data, json=json_data, files=files)
        return response


    def api_v1_role_authorized_p(self,id=None,menu_ids=[],api_infos=[],**kw) -> CustomResponse:
        """
        接口名：更新角色权限
        url: /api/v1/role/authorized

        Args:
            id (integer): 必填: 是, 
            menu_ids (array): 必填: 否, 
            api_infos (array): 必填: 否, 
            kw: 额外参数，如 raw_method, raw_params: 路径参数一般是get请求, raw_data: 表单参数, raw_json: json格式的参数

        Returns:
            {}
            response 支持jmespath和re正则提取数据，res.search(expression), res.find_all(pattern), res.find_one(pattern)
        """

        # 处理路径参数
        url = "/api/v1/role/authorized"
        
        
        method = "POST"
        if kw.get('raw_method'):
            method = kw.get('raw_method').upper()

        params = {
        }
        if kw.get('raw_params'):
            params = kw.get('raw_params')

        data = {
        }
        if kw.get('raw_data'):
            data = kw.get('raw_data')

        json_data = {
            "id": id,
            "menu_ids": menu_ids,
            "api_infos": api_infos
        }
        if kw.get('raw_json'):
            json_data = kw.get('raw_json')

        files = {
        }
        if kw.get('raw_files'):
            files = kw.get('raw_files')

        response = self.request(url=url, method=method, params=params, data=data, json=json_data, files=files)
        return response


    def api_v1_menu_list_g(self,page=1,page_size=10,**kw) -> CustomResponse:
        """
        接口名：查看菜单列表
        url: /api/v1/menu/list

        Args:
            page (integer): 必填: 否, 页码
            page_size (integer): 必填: 否, 每页数量
            kw: 额外参数，如 raw_method, raw_params: 路径参数一般是get请求, raw_data: 表单参数, raw_json: json格式的参数

        Returns:
            {}
            response 支持jmespath和re正则提取数据，res.search(expression), res.find_all(pattern), res.find_one(pattern)
        """

        # 处理路径参数
        url = "/api/v1/menu/list"
        
        
        method = "GET"
        if kw.get('raw_method'):
            method = kw.get('raw_method').upper()

        params = {
            "page": page,
            "page_size": page_size
        }
        if kw.get('raw_params'):
            params = kw.get('raw_params')

        data = {
        }
        if kw.get('raw_data'):
            data = kw.get('raw_data')

        json_data = {
        }
        if kw.get('raw_json'):
            json_data = kw.get('raw_json')

        files = {
        }
        if kw.get('raw_files'):
            files = kw.get('raw_files')

        response = self.request(url=url, method=method, params=params, data=data, json=json_data, files=files)
        return response


    def api_v1_menu_get_g(self,menu_id=None,**kw) -> CustomResponse:
        """
        接口名：查看菜单
        url: /api/v1/menu/get

        Args:
            menu_id (integer): 必填: 是, 菜单id
            kw: 额外参数，如 raw_method, raw_params: 路径参数一般是get请求, raw_data: 表单参数, raw_json: json格式的参数

        Returns:
            {}
            response 支持jmespath和re正则提取数据，res.search(expression), res.find_all(pattern), res.find_one(pattern)
        """

        # 处理路径参数
        url = "/api/v1/menu/get"
        
        
        method = "GET"
        if kw.get('raw_method'):
            method = kw.get('raw_method').upper()

        params = {
            "menu_id": menu_id
        }
        if kw.get('raw_params'):
            params = kw.get('raw_params')

        data = {
        }
        if kw.get('raw_data'):
            data = kw.get('raw_data')

        json_data = {
        }
        if kw.get('raw_json'):
            json_data = kw.get('raw_json')

        files = {
        }
        if kw.get('raw_files'):
            files = kw.get('raw_files')

        response = self.request(url=url, method=method, params=params, data=data, json=json_data, files=files)
        return response


    def api_v1_menu_create_p(self,menu_type='catalog',name=None,icon='ph:user-list-bold',path=None,order=None,parent_id=0,is_hidden=False,component='Layout',keepalive=True,redirect='',**kw) -> CustomResponse:
        """
        接口名：创建菜单
        url: /api/v1/menu/create

        Args:
            menu_type (string): 必填: 否, 
            name (string): 必填: 是, 
            icon (string): 必填: 否, 
            path (string): 必填: 是, 
            order (string): 必填: 是, 
            parent_id (string): 必填: 否, 
            is_hidden (string): 必填: 否, 
            component (string): 必填: 否, 
            keepalive (string): 必填: 否, 
            redirect (string): 必填: 否, 
            kw: 额外参数，如 raw_method, raw_params: 路径参数一般是get请求, raw_data: 表单参数, raw_json: json格式的参数

        Returns:
            {}
            response 支持jmespath和re正则提取数据，res.search(expression), res.find_all(pattern), res.find_one(pattern)
        """

        # 处理路径参数
        url = "/api/v1/menu/create"
        
        
        method = "POST"
        if kw.get('raw_method'):
            method = kw.get('raw_method').upper()

        params = {
        }
        if kw.get('raw_params'):
            params = kw.get('raw_params')

        data = {
        }
        if kw.get('raw_data'):
            data = kw.get('raw_data')

        json_data = {
            "menu_type": menu_type,
            "name": name,
            "icon": icon,
            "path": path,
            "order": order,
            "parent_id": parent_id,
            "is_hidden": is_hidden,
            "component": component,
            "keepalive": keepalive,
            "redirect": redirect
        }
        if kw.get('raw_json'):
            json_data = kw.get('raw_json')

        files = {
        }
        if kw.get('raw_files'):
            files = kw.get('raw_files')

        response = self.request(url=url, method=method, params=params, data=data, json=json_data, files=files)
        return response


    def api_v1_menu_update_p(self,id=None,menu_type=None,name=None,icon='ph:user-list-bold',path=None,order=None,parent_id=None,is_hidden=False,component=None,keepalive=False,redirect='',**kw) -> CustomResponse:
        """
        接口名：更新菜单
        url: /api/v1/menu/update

        Args:
            id (integer): 必填: 是, 
            menu_type (string): 必填: 是, 
            name (string): 必填: 是, 
            icon (string): 必填: 否, 
            path (string): 必填: 是, 
            order (string): 必填: 是, 
            parent_id (string): 必填: 是, 
            is_hidden (string): 必填: 否, 
            component (string): 必填: 是, 
            keepalive (string): 必填: 否, 
            redirect (string): 必填: 否, 
            kw: 额外参数，如 raw_method, raw_params: 路径参数一般是get请求, raw_data: 表单参数, raw_json: json格式的参数

        Returns:
            {}
            response 支持jmespath和re正则提取数据，res.search(expression), res.find_all(pattern), res.find_one(pattern)
        """

        # 处理路径参数
        url = "/api/v1/menu/update"
        
        
        method = "POST"
        if kw.get('raw_method'):
            method = kw.get('raw_method').upper()

        params = {
        }
        if kw.get('raw_params'):
            params = kw.get('raw_params')

        data = {
        }
        if kw.get('raw_data'):
            data = kw.get('raw_data')

        json_data = {
            "id": id,
            "menu_type": menu_type,
            "name": name,
            "icon": icon,
            "path": path,
            "order": order,
            "parent_id": parent_id,
            "is_hidden": is_hidden,
            "component": component,
            "keepalive": keepalive,
            "redirect": redirect
        }
        if kw.get('raw_json'):
            json_data = kw.get('raw_json')

        files = {
        }
        if kw.get('raw_files'):
            files = kw.get('raw_files')

        response = self.request(url=url, method=method, params=params, data=data, json=json_data, files=files)
        return response


    def api_v1_menu_delete_del(self,id=None,**kw) -> CustomResponse:
        """
        接口名：删除菜单
        url: /api/v1/menu/delete

        Args:
            id (integer): 必填: 是, 菜单id
            kw: 额外参数，如 raw_method, raw_params: 路径参数一般是get请求, raw_data: 表单参数, raw_json: json格式的参数

        Returns:
            {}
            response 支持jmespath和re正则提取数据，res.search(expression), res.find_all(pattern), res.find_one(pattern)
        """

        # 处理路径参数
        url = "/api/v1/menu/delete"
        
        
        method = "DELETE"
        if kw.get('raw_method'):
            method = kw.get('raw_method').upper()

        params = {
            "id": id
        }
        if kw.get('raw_params'):
            params = kw.get('raw_params')

        data = {
        }
        if kw.get('raw_data'):
            data = kw.get('raw_data')

        json_data = {
        }
        if kw.get('raw_json'):
            json_data = kw.get('raw_json')

        files = {
        }
        if kw.get('raw_files'):
            files = kw.get('raw_files')

        response = self.request(url=url, method=method, params=params, data=data, json=json_data, files=files)
        return response


    def api_v1_api_list_g(self,page=1,page_size=10,path=None,summary=None,tags=None,**kw) -> CustomResponse:
        """
        接口名：查看API列表
        url: /api/v1/api/list

        Args:
            page (integer): 必填: 否, 页码
            page_size (integer): 必填: 否, 每页数量
            path (string): 必填: 否, API路径
            summary (string): 必填: 否, API简介
            tags (string): 必填: 否, API模块
            kw: 额外参数，如 raw_method, raw_params: 路径参数一般是get请求, raw_data: 表单参数, raw_json: json格式的参数

        Returns:
            {}
            response 支持jmespath和re正则提取数据，res.search(expression), res.find_all(pattern), res.find_one(pattern)
        """

        # 处理路径参数
        url = "/api/v1/api/list"
        
        
        method = "GET"
        if kw.get('raw_method'):
            method = kw.get('raw_method').upper()

        params = {
            "page": page,
            "page_size": page_size,
            "path": path,
            "summary": summary,
            "tags": tags
        }
        if kw.get('raw_params'):
            params = kw.get('raw_params')

        data = {
        }
        if kw.get('raw_data'):
            data = kw.get('raw_data')

        json_data = {
        }
        if kw.get('raw_json'):
            json_data = kw.get('raw_json')

        files = {
        }
        if kw.get('raw_files'):
            files = kw.get('raw_files')

        response = self.request(url=url, method=method, params=params, data=data, json=json_data, files=files)
        return response


    def api_v1_api_get_g(self,id=None,**kw) -> CustomResponse:
        """
        接口名：查看Api
        url: /api/v1/api/get

        Args:
            id (integer): 必填: 是, Api
            kw: 额外参数，如 raw_method, raw_params: 路径参数一般是get请求, raw_data: 表单参数, raw_json: json格式的参数

        Returns:
            {}
            response 支持jmespath和re正则提取数据，res.search(expression), res.find_all(pattern), res.find_one(pattern)
        """

        # 处理路径参数
        url = "/api/v1/api/get"
        
        
        method = "GET"
        if kw.get('raw_method'):
            method = kw.get('raw_method').upper()

        params = {
            "id": id
        }
        if kw.get('raw_params'):
            params = kw.get('raw_params')

        data = {
        }
        if kw.get('raw_data'):
            data = kw.get('raw_data')

        json_data = {
        }
        if kw.get('raw_json'):
            json_data = kw.get('raw_json')

        files = {
        }
        if kw.get('raw_files'):
            files = kw.get('raw_files')

        response = self.request(url=url, method=method, params=params, data=data, json=json_data, files=files)
        return response


    def api_v1_api_create_p(self,path=None,summary='',method=None,tags=None,**kw) -> CustomResponse:
        """
        接口名：创建Api
        url: /api/v1/api/create

        Args:
            path (string): 必填: 是, API路径
            summary (string): 必填: 否, API简介
            method (string): 必填: 是, API方法
            tags (string): 必填: 是, API标签
            kw: 额外参数，如 raw_method, raw_params: 路径参数一般是get请求, raw_data: 表单参数, raw_json: json格式的参数

        Returns:
            {}
            response 支持jmespath和re正则提取数据，res.search(expression), res.find_all(pattern), res.find_one(pattern)
        """

        # 处理路径参数
        url = "/api/v1/api/create"
        
        
        method = "POST"
        if kw.get('raw_method'):
            method = kw.get('raw_method').upper()

        params = {
        }
        if kw.get('raw_params'):
            params = kw.get('raw_params')

        data = {
        }
        if kw.get('raw_data'):
            data = kw.get('raw_data')

        json_data = {
            "path": path,
            "summary": summary,
            "method": method,
            "tags": tags
        }
        if kw.get('raw_json'):
            json_data = kw.get('raw_json')

        files = {
        }
        if kw.get('raw_files'):
            files = kw.get('raw_files')

        response = self.request(url=url, method=method, params=params, data=data, json=json_data, files=files)
        return response


    def api_v1_api_update_p(self,path=None,summary='',method=None,tags=None,id=None,**kw) -> CustomResponse:
        """
        接口名：更新Api
        url: /api/v1/api/update

        Args:
            path (string): 必填: 是, API路径
            summary (string): 必填: 否, API简介
            method (string): 必填: 是, API方法
            tags (string): 必填: 是, API标签
            id (integer): 必填: 是, 
            kw: 额外参数，如 raw_method, raw_params: 路径参数一般是get请求, raw_data: 表单参数, raw_json: json格式的参数

        Returns:
            {}
            response 支持jmespath和re正则提取数据，res.search(expression), res.find_all(pattern), res.find_one(pattern)
        """

        # 处理路径参数
        url = "/api/v1/api/update"
        
        
        method = "POST"
        if kw.get('raw_method'):
            method = kw.get('raw_method').upper()

        params = {
        }
        if kw.get('raw_params'):
            params = kw.get('raw_params')

        data = {
        }
        if kw.get('raw_data'):
            data = kw.get('raw_data')

        json_data = {
            "path": path,
            "summary": summary,
            "method": method,
            "tags": tags,
            "id": id
        }
        if kw.get('raw_json'):
            json_data = kw.get('raw_json')

        files = {
        }
        if kw.get('raw_files'):
            files = kw.get('raw_files')

        response = self.request(url=url, method=method, params=params, data=data, json=json_data, files=files)
        return response


    def api_v1_api_delete_del(self,api_id=None,**kw) -> CustomResponse:
        """
        接口名：删除Api
        url: /api/v1/api/delete

        Args:
            api_id (integer): 必填: 是, ApiID
            kw: 额外参数，如 raw_method, raw_params: 路径参数一般是get请求, raw_data: 表单参数, raw_json: json格式的参数

        Returns:
            {}
            response 支持jmespath和re正则提取数据，res.search(expression), res.find_all(pattern), res.find_one(pattern)
        """

        # 处理路径参数
        url = "/api/v1/api/delete"
        
        
        method = "DELETE"
        if kw.get('raw_method'):
            method = kw.get('raw_method').upper()

        params = {
            "api_id": api_id
        }
        if kw.get('raw_params'):
            params = kw.get('raw_params')

        data = {
        }
        if kw.get('raw_data'):
            data = kw.get('raw_data')

        json_data = {
        }
        if kw.get('raw_json'):
            json_data = kw.get('raw_json')

        files = {
        }
        if kw.get('raw_files'):
            files = kw.get('raw_files')

        response = self.request(url=url, method=method, params=params, data=data, json=json_data, files=files)
        return response


    def api_v1_api_refresh_p(self,**kw) -> CustomResponse:
        """
        接口名：刷新API列表
        url: /api/v1/api/refresh

        Args:
        
            kw: 额外参数，如 raw_method, raw_params: 路径参数一般是get请求, raw_data: 表单参数, raw_json: json格式的参数

        Returns:
            {}
            response 支持jmespath和re正则提取数据，res.search(expression), res.find_all(pattern), res.find_one(pattern)
        """

        # 处理路径参数
        url = "/api/v1/api/refresh"
        
        
        method = "POST"
        if kw.get('raw_method'):
            method = kw.get('raw_method').upper()

        params = {
        }
        if kw.get('raw_params'):
            params = kw.get('raw_params')

        data = {
        }
        if kw.get('raw_data'):
            data = kw.get('raw_data')

        json_data = {
        }
        if kw.get('raw_json'):
            json_data = kw.get('raw_json')

        files = {
        }
        if kw.get('raw_files'):
            files = kw.get('raw_files')

        response = self.request(url=url, method=method, params=params, data=data, json=json_data, files=files)
        return response


    def api_v1_dept_list_g(self,name=None,**kw) -> CustomResponse:
        """
        接口名：查看部门列表
        url: /api/v1/dept/list

        Args:
            name (string): 必填: 否, 部门名称
            kw: 额外参数，如 raw_method, raw_params: 路径参数一般是get请求, raw_data: 表单参数, raw_json: json格式的参数

        Returns:
            {}
            response 支持jmespath和re正则提取数据，res.search(expression), res.find_all(pattern), res.find_one(pattern)
        """

        # 处理路径参数
        url = "/api/v1/dept/list"
        
        
        method = "GET"
        if kw.get('raw_method'):
            method = kw.get('raw_method').upper()

        params = {
            "name": name
        }
        if kw.get('raw_params'):
            params = kw.get('raw_params')

        data = {
        }
        if kw.get('raw_data'):
            data = kw.get('raw_data')

        json_data = {
        }
        if kw.get('raw_json'):
            json_data = kw.get('raw_json')

        files = {
        }
        if kw.get('raw_files'):
            files = kw.get('raw_files')

        response = self.request(url=url, method=method, params=params, data=data, json=json_data, files=files)
        return response


    def api_v1_dept_get_g(self,id=None,**kw) -> CustomResponse:
        """
        接口名：查看部门
        url: /api/v1/dept/get

        Args:
            id (integer): 必填: 是, 部门ID
            kw: 额外参数，如 raw_method, raw_params: 路径参数一般是get请求, raw_data: 表单参数, raw_json: json格式的参数

        Returns:
            {}
            response 支持jmespath和re正则提取数据，res.search(expression), res.find_all(pattern), res.find_one(pattern)
        """

        # 处理路径参数
        url = "/api/v1/dept/get"
        
        
        method = "GET"
        if kw.get('raw_method'):
            method = kw.get('raw_method').upper()

        params = {
            "id": id
        }
        if kw.get('raw_params'):
            params = kw.get('raw_params')

        data = {
        }
        if kw.get('raw_data'):
            data = kw.get('raw_data')

        json_data = {
        }
        if kw.get('raw_json'):
            json_data = kw.get('raw_json')

        files = {
        }
        if kw.get('raw_files'):
            files = kw.get('raw_files')

        response = self.request(url=url, method=method, params=params, data=data, json=json_data, files=files)
        return response


    def api_v1_dept_create_p(self,name=None,desc='',order=0,parent_id=0,**kw) -> CustomResponse:
        """
        接口名：创建部门
        url: /api/v1/dept/create

        Args:
            name (string): 必填: 是, 部门名称
            desc (string): 必填: 否, 备注
            order (integer): 必填: 否, 排序
            parent_id (integer): 必填: 否, 父部门ID
            kw: 额外参数，如 raw_method, raw_params: 路径参数一般是get请求, raw_data: 表单参数, raw_json: json格式的参数

        Returns:
            {}
            response 支持jmespath和re正则提取数据，res.search(expression), res.find_all(pattern), res.find_one(pattern)
        """

        # 处理路径参数
        url = "/api/v1/dept/create"
        
        
        method = "POST"
        if kw.get('raw_method'):
            method = kw.get('raw_method').upper()

        params = {
        }
        if kw.get('raw_params'):
            params = kw.get('raw_params')

        data = {
        }
        if kw.get('raw_data'):
            data = kw.get('raw_data')

        json_data = {
            "name": name,
            "desc": desc,
            "order": order,
            "parent_id": parent_id
        }
        if kw.get('raw_json'):
            json_data = kw.get('raw_json')

        files = {
        }
        if kw.get('raw_files'):
            files = kw.get('raw_files')

        response = self.request(url=url, method=method, params=params, data=data, json=json_data, files=files)
        return response


    def api_v1_dept_update_p(self,name=None,desc='',order=0,parent_id=0,id=None,**kw) -> CustomResponse:
        """
        接口名：更新部门
        url: /api/v1/dept/update

        Args:
            name (string): 必填: 是, 部门名称
            desc (string): 必填: 否, 备注
            order (integer): 必填: 否, 排序
            parent_id (integer): 必填: 否, 父部门ID
            id (integer): 必填: 是, 
            kw: 额外参数，如 raw_method, raw_params: 路径参数一般是get请求, raw_data: 表单参数, raw_json: json格式的参数

        Returns:
            {}
            response 支持jmespath和re正则提取数据，res.search(expression), res.find_all(pattern), res.find_one(pattern)
        """

        # 处理路径参数
        url = "/api/v1/dept/update"
        
        
        method = "POST"
        if kw.get('raw_method'):
            method = kw.get('raw_method').upper()

        params = {
        }
        if kw.get('raw_params'):
            params = kw.get('raw_params')

        data = {
        }
        if kw.get('raw_data'):
            data = kw.get('raw_data')

        json_data = {
            "name": name,
            "desc": desc,
            "order": order,
            "parent_id": parent_id,
            "id": id
        }
        if kw.get('raw_json'):
            json_data = kw.get('raw_json')

        files = {
        }
        if kw.get('raw_files'):
            files = kw.get('raw_files')

        response = self.request(url=url, method=method, params=params, data=data, json=json_data, files=files)
        return response


    def api_v1_dept_delete_del(self,dept_id=None,**kw) -> CustomResponse:
        """
        接口名：删除部门
        url: /api/v1/dept/delete

        Args:
            dept_id (integer): 必填: 是, 部门ID
            kw: 额外参数，如 raw_method, raw_params: 路径参数一般是get请求, raw_data: 表单参数, raw_json: json格式的参数

        Returns:
            {}
            response 支持jmespath和re正则提取数据，res.search(expression), res.find_all(pattern), res.find_one(pattern)
        """

        # 处理路径参数
        url = "/api/v1/dept/delete"
        
        
        method = "DELETE"
        if kw.get('raw_method'):
            method = kw.get('raw_method').upper()

        params = {
            "dept_id": dept_id
        }
        if kw.get('raw_params'):
            params = kw.get('raw_params')

        data = {
        }
        if kw.get('raw_data'):
            data = kw.get('raw_data')

        json_data = {
        }
        if kw.get('raw_json'):
            json_data = kw.get('raw_json')

        files = {
        }
        if kw.get('raw_files'):
            files = kw.get('raw_files')

        response = self.request(url=url, method=method, params=params, data=data, json=json_data, files=files)
        return response


    def api_v1_auditlog_list_g(self,page=1,page_size=10,username='',module='',method='',summary='',path='',status=None,start_time='',end_time='',**kw) -> CustomResponse:
        """
        接口名：查看操作日志
        url: /api/v1/auditlog/list

        Args:
            page (integer): 必填: 否, 页码
            page_size (integer): 必填: 否, 每页数量
            username (string): 必填: 否, 操作人名称
            module (string): 必填: 否, 功能模块
            method (string): 必填: 否, 请求方法
            summary (string): 必填: 否, 接口描述
            path (string): 必填: 否, 请求路径
            status (integer): 必填: 否, 状态码
            start_time (string): 必填: 否, 开始时间
            end_time (string): 必填: 否, 结束时间
            kw: 额外参数，如 raw_method, raw_params: 路径参数一般是get请求, raw_data: 表单参数, raw_json: json格式的参数

        Returns:
            {}
            response 支持jmespath和re正则提取数据，res.search(expression), res.find_all(pattern), res.find_one(pattern)
        """

        # 处理路径参数
        url = "/api/v1/auditlog/list"
        
        
        method = "GET"
        if kw.get('raw_method'):
            method = kw.get('raw_method').upper()

        params = {
            "page": page,
            "page_size": page_size,
            "username": username,
            "module": module,
            "method": method,
            "summary": summary,
            "path": path,
            "status": status,
            "start_time": start_time,
            "end_time": end_time
        }
        if kw.get('raw_params'):
            params = kw.get('raw_params')

        data = {
        }
        if kw.get('raw_data'):
            data = kw.get('raw_data')

        json_data = {
        }
        if kw.get('raw_json'):
            json_data = kw.get('raw_json')

        files = {
        }
        if kw.get('raw_files'):
            files = kw.get('raw_files')

        response = self.request(url=url, method=method, params=params, data=data, json=json_data, files=files)
        return response


    def search_g(self,q=None,page=1,sort=None,**kw) -> CustomResponse:
        """
        接口名：Search resources
        url: /search

        Args:
            q (string): 必填: 是, Search keyword.
            page (integer): 必填: 否, Page number.
            sort (string): 必填: 否, Sorting order.
            kw: 额外参数，如 raw_method, raw_params: 路径参数一般是get请求, raw_data: 表单参数, raw_json: json格式的参数

        Returns:
            {"type": "array", "items": {"type": "object", "properties": {"id": {"type": "integer"}, "name": {"type": "string"}}}}
            response 支持jmespath和re正则提取数据，res.search(expression), res.find_all(pattern), res.find_one(pattern)
        """

        # 处理路径参数
        url = "/search"
        
        
        method = "GET"
        if kw.get('raw_method'):
            method = kw.get('raw_method').upper()

        params = {
            "q": q,
            "page": page,
            "sort": sort
        }
        if kw.get('raw_params'):
            params = kw.get('raw_params')

        data = {
        }
        if kw.get('raw_data'):
            data = kw.get('raw_data')

        json_data = {
        }
        if kw.get('raw_json'):
            json_data = kw.get('raw_json')

        files = {
        }
        if kw.get('raw_files'):
            files = kw.get('raw_files')

        response = self.request(url=url, method=method, params=params, data=data, json=json_data, files=files)
        return response


    def users__userId_g(self,userId=None,**kw) -> CustomResponse:
        """
        接口名：Get user by ID
        url: /users/{userId}

        Args:
            userId (integer): 必填: 是, Unique user ID.
            kw: 额外参数，如 raw_method, raw_params: 路径参数一般是get请求, raw_data: 表单参数, raw_json: json格式的参数

        Returns:
            {"type": "object", "properties": {"id": {"type": "integer"}, "username": {"type": "string"}, "email": {"type": "string"}}}
            response 支持jmespath和re正则提取数据，res.search(expression), res.find_all(pattern), res.find_one(pattern)
        """

        # 处理路径参数
        url = "/users/{userId}"
        
        # 替换路径参数
        
        url = url.replace('{' + 'userId' + '}', str(userId))
        
        
        
        method = "GET"
        if kw.get('raw_method'):
            method = kw.get('raw_method').upper()

        params = {
        }
        if kw.get('raw_params'):
            params = kw.get('raw_params')

        data = {
        }
        if kw.get('raw_data'):
            data = kw.get('raw_data')

        json_data = {
        }
        if kw.get('raw_json'):
            json_data = kw.get('raw_json')

        files = {
        }
        if kw.get('raw_files'):
            files = kw.get('raw_files')

        response = self.request(url=url, method=method, params=params, data=data, json=json_data, files=files)
        return response


    def users__userId_put(self,userId=None,username=None,email=None,**kw) -> CustomResponse:
        """
        接口名：Update user by ID
        url: /users/{userId}

        Args:
            userId (integer): 必填: 是, 
            username (string): 必填: 否, 
            email (string): 必填: 否, 
            kw: 额外参数，如 raw_method, raw_params: 路径参数一般是get请求, raw_data: 表单参数, raw_json: json格式的参数

        Returns:
            {}
            response 支持jmespath和re正则提取数据，res.search(expression), res.find_all(pattern), res.find_one(pattern)
        """

        # 处理路径参数
        url = "/users/{userId}"
        
        # 替换路径参数
        
        url = url.replace('{' + 'userId' + '}', str(userId))
        
        
        
        method = "PUT"
        if kw.get('raw_method'):
            method = kw.get('raw_method').upper()

        params = {
        }
        if kw.get('raw_params'):
            params = kw.get('raw_params')

        data = {
        }
        if kw.get('raw_data'):
            data = kw.get('raw_data')

        json_data = {
            "username": username,
            "email": email
        }
        if kw.get('raw_json'):
            json_data = kw.get('raw_json')

        files = {
        }
        if kw.get('raw_files'):
            files = kw.get('raw_files')

        response = self.request(url=url, method=method, params=params, data=data, json=json_data, files=files)
        return response


    def users__userId_del(self,userId=None,**kw) -> CustomResponse:
        """
        接口名：Delete user by ID
        url: /users/{userId}

        Args:
            userId (integer): 必填: 是, 
            kw: 额外参数，如 raw_method, raw_params: 路径参数一般是get请求, raw_data: 表单参数, raw_json: json格式的参数

        Returns:
            {}
            response 支持jmespath和re正则提取数据，res.search(expression), res.find_all(pattern), res.find_one(pattern)
        """

        # 处理路径参数
        url = "/users/{userId}"
        
        # 替换路径参数
        
        url = url.replace('{' + 'userId' + '}', str(userId))
        
        
        
        method = "DELETE"
        if kw.get('raw_method'):
            method = kw.get('raw_method').upper()

        params = {
        }
        if kw.get('raw_params'):
            params = kw.get('raw_params')

        data = {
        }
        if kw.get('raw_data'):
            data = kw.get('raw_data')

        json_data = {
        }
        if kw.get('raw_json'):
            json_data = kw.get('raw_json')

        files = {
        }
        if kw.get('raw_files'):
            files = kw.get('raw_files')

        response = self.request(url=url, method=method, params=params, data=data, json=json_data, files=files)
        return response


    def users_p(self,username=None,password=None,**kw) -> CustomResponse:
        """
        接口名：Create new user (JSON request body)
        url: /users

        Args:
            username (string): 必填: 是, 
            password (string): 必填: 是, 
            kw: 额外参数，如 raw_method, raw_params: 路径参数一般是get请求, raw_data: 表单参数, raw_json: json格式的参数

        Returns:
            {}
            response 支持jmespath和re正则提取数据，res.search(expression), res.find_all(pattern), res.find_one(pattern)
        """

        # 处理路径参数
        url = "/users"
        
        
        method = "POST"
        if kw.get('raw_method'):
            method = kw.get('raw_method').upper()

        params = {
        }
        if kw.get('raw_params'):
            params = kw.get('raw_params')

        data = {
        }
        if kw.get('raw_data'):
            data = kw.get('raw_data')

        json_data = {
            "username": username,
            "password": password
        }
        if kw.get('raw_json'):
            json_data = kw.get('raw_json')

        files = {
        }
        if kw.get('raw_files'):
            files = kw.get('raw_files')

        response = self.request(url=url, method=method, params=params, data=data, json=json_data, files=files)
        return response


    def login_p(self,username=None,password=None,**kw) -> CustomResponse:
        """
        接口名：Login with form data
        url: /login

        Args:
            username (string): 必填: 是, 
            password (string): 必填: 否, 
            kw: 额外参数，如 raw_method, raw_params: 路径参数一般是get请求, raw_data: 表单参数, raw_json: json格式的参数

        Returns:
            {}
            response 支持jmespath和re正则提取数据，res.search(expression), res.find_all(pattern), res.find_one(pattern)
        """

        # 处理路径参数
        url = "/login"
        
        
        method = "POST"
        if kw.get('raw_method'):
            method = kw.get('raw_method').upper()

        params = {
        }
        if kw.get('raw_params'):
            params = kw.get('raw_params')

        data = {
            "username": username,
            "password": password
        }
        if kw.get('raw_data'):
            data = kw.get('raw_data')

        json_data = {
        }
        if kw.get('raw_json'):
            json_data = kw.get('raw_json')

        files = {
        }
        if kw.get('raw_files'):
            files = kw.get('raw_files')

        response = self.request(url=url, method=method, params=params, data=data, json=json_data, files=files)
        return response


    def upload_p(self,file=None,**kw) -> CustomResponse:
        """
        接口名：Upload a file (multipart form)
        url: /upload

        Args:
            file (file): 必填: 否, 文件上传参数
            kw: 额外参数，如 raw_method, raw_params: 路径参数一般是get请求, raw_data: 表单参数, raw_json: json格式的参数

        Returns:
            {}
            response 支持jmespath和re正则提取数据，res.search(expression), res.find_all(pattern), res.find_one(pattern)
        """

        # 处理路径参数
        url = "/upload"
        
        
        method = "POST"
        if kw.get('raw_method'):
            method = kw.get('raw_method').upper()

        params = {
        }
        if kw.get('raw_params'):
            params = kw.get('raw_params')

        data = {
        }
        if kw.get('raw_data'):
            data = kw.get('raw_data')

        json_data = {
        }
        if kw.get('raw_json'):
            json_data = kw.get('raw_json')

        files = {
            "file": file
        }
        if kw.get('raw_files'):
            files = kw.get('raw_files')

        response = self.request(url=url, method=method, params=params, data=data, json=json_data, files=files)
        return response

