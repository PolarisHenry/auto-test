"""
文件操作工具类

提供各种文件和目录操作、读写、验证等实用功能
"""
import os
import shutil
import json
import yaml
import csv
import mimetypes
from pathlib import Path
from typing import List, Optional, Dict, Any, Union, Tuple
import datetime
import hashlib


class FileUtils:
    """文件操作工具类"""

    @classmethod
    def get_file_size(cls, file_path: str) -> int:
        """获取文件大小（字节）

        Args:
            file_path: 文件路径

        Returns:
            文件大小（字节）
        """
        return os.path.getsize(file_path)

    @classmethod
    def format_file_size(cls, size_bytes: int) -> str:
        """格式化文件大小显示

        Args:
            size_bytes: 文件大小（字节）

        Returns:
            格式化的文件大小字符串（如：1.2 MB）
        """
        if size_bytes == 0:
            return "0 B"

        size_names = ["B", "KB", "MB", "GB", "TB"]
        size_index = 0
        while size_bytes >= 1024 and size_index < len(size_names) - 1:
            size_bytes /= 1024.0
            size_index += 1

        if size_index == 0:
            return f"{int(size_bytes)} {size_names[size_index]}"
        else:
            return f"{size_bytes:.1f} {size_names[size_index]}"

    @classmethod
    def get_file_extension(cls, file_path: str) -> str:
        """获取文件扩展名

        Args:
            file_path: 文件路径

        Returns:
            文件扩展名（不包含点）
        """
        return Path(file_path).suffix[1:].lower()

    @classmethod
    def get_filename_without_extension(cls, file_path: str) -> str:
        """获取不含扩展名的文件名

        Args:
            file_path: 文件路径

        Returns:
            不含扩展名的文件名
        """
        return Path(file_path).stem

    @classmethod
    def get_file_mime_type(cls, file_path: str) -> str:
        """获取文件MIME类型

        Args:
            file_path: 文件路径

        Returns:
            MIME类型字符串
        """
        mime_type, _ = mimetypes.guess_type(file_path)
        return mime_type or "application/octet-stream"

    @classmethod
    def is_image_file(cls, file_path: str) -> bool:
        """判断是否为图片文件

        Args:
            file_path: 文件路径

        Returns:
            是否为图片文件
        """
        mime_type = cls.get_file_mime_type(file_path)
        return mime_type.startswith('image/')

    @classmethod
    def is_video_file(cls, file_path: str) -> bool:
        """判断是否为视频文件

        Args:
            file_path: 文件路径

        Returns:
            是否为视频文件
        """
        mime_type = cls.get_file_mime_type(file_path)
        return mime_type.startswith('video/')

    @classmethod
    def is_audio_file(cls, file_path: str) -> bool:
        """判断是否为音频文件

        Args:
            file_path: 文件路径

        Returns:
            是否为音频文件
        """
        mime_type = cls.get_file_mime_type(file_path)
        return mime_type.startswith('audio/')

    @classmethod
    def is_text_file(cls, file_path: str) -> bool:
        """判断是否为文本文件

        Args:
            file_path: 文件路径

        Returns:
            是否为文本文件
        """
        mime_type = cls.get_file_mime_type(file_path)
        return mime_type.startswith('text/') or mime_type in [
            'application/json', 'application/javascript', 'application/xml'
        ]

    @classmethod
    def ensure_dir(cls, dir_path: str) -> bool:
        """确保目录存在，如果不存在则创建

        Args:
            dir_path: 目录路径

        Returns:
            是否成功
        """
        try:
            os.makedirs(dir_path, exist_ok=True)
            return True
        except Exception:
            return False

    @classmethod
    def copy_file(cls, src_file: str, dst_file: str) -> bool:
        """复制文件

        Args:
            src_file: 源文件路径
            dst_file: 目标文件路径

        Returns:
            是否成功
        """
        try:
            # 确保目标目录存在
            cls.ensure_dir(os.path.dirname(dst_file))
            shutil.copy2(src_file, dst_file)
            return True
        except Exception:
            return False

    @classmethod
    def move_file(cls, src_file: str, dst_file: str) -> bool:
        """移动文件

        Args:
            src_file: 源文件路径
            dst_file: 目标文件路径

        Returns:
            是否成功
        """
        try:
            # 确保目标目录存在
            cls.ensure_dir(os.path.dirname(dst_file))
            shutil.move(src_file, dst_file)
            return True
        except Exception:
            return False

    @classmethod
    def delete_file(cls, file_path: str) -> bool:
        """删除文件

        Args:
            file_path: 文件路径

        Returns:
            是否成功
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
            return True
        except Exception:
            return False

    @classmethod
    def read_file(cls, file_path: str, encoding: str = 'utf-8') -> Optional[str]:
        """读取文本文件

        Args:
            file_path: 文件路径
            encoding: 文件编码

        Returns:
            文件内容，如果读取失败返回None
        """
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                return f.read()
        except Exception:
            return None

    @classmethod
    def write_file(cls, file_path: str, content: str, encoding: str = 'utf-8') -> bool:
        """写入文本文件

        Args:
            file_path: 文件路径
            content: 要写入的内容
            encoding: 文件编码

        Returns:
            是否成功
        """
        try:
            # 确保目录存在
            cls.ensure_dir(os.path.dirname(file_path))
            with open(file_path, 'w', encoding=encoding) as f:
                f.write(content)
            return True
        except Exception:
            return False

    @classmethod
    def append_file(cls, file_path: str, content: str, encoding: str = 'utf-8') -> bool:
        """追加内容到文件

        Args:
            file_path: 文件路径
            content: 要追加的内容
            encoding: 文件编码

        Returns:
            是否成功
        """
        try:
            # 确保目录存在
            cls.ensure_dir(os.path.dirname(file_path))
            with open(file_path, 'a', encoding=encoding) as f:
                f.write(content)
            return True
        except Exception:
            return False

    @classmethod
    def read_json_file(cls, file_path: str) -> Optional[Dict[str, Any]]:
        """读取JSON文件

        Args:
            file_path: JSON文件路径

        Returns:
            JSON数据，如果读取失败返回None
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return None

    @classmethod
    def write_json_file(cls, file_path: str, data: Dict[str, Any], indent: int = 4) -> bool:
        """写入JSON文件

        Args:
            file_path: JSON文件路径
            data: 要写入的数据
            indent: 缩进空格数

        Returns:
            是否成功
        """
        try:
            cls.ensure_dir(os.path.dirname(file_path))
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=indent, ensure_ascii=False)
            return True
        except Exception:
            return False

    @classmethod
    def read_yaml_file(cls, file_path: str) -> Optional[Dict[str, Any]]:
        """读取YAML文件

        Args:
            file_path: YAML文件路径

        Returns:
            YAML数据，如果读取失败返回None
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception:
            return None

    @classmethod
    def write_yaml_file(cls, file_path: str, data: Dict[str, Any]) -> bool:
        """写入YAML文件

        Args:
            file_path: YAML文件路径
            data: 要写入的数据

        Returns:
            是否成功
        """
        try:
            cls.ensure_dir(os.path.dirname(file_path))
            with open(file_path, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
            return True
        except Exception:
            return False

    @classmethod
    def read_csv_file(cls, file_path: str, encoding: str = 'utf-8') -> Optional[List[Dict[str, Any]]]:
        """读取CSV文件

        Args:
            file_path: CSV文件路径
            encoding: 文件编码

        Returns:
            CSV数据（字典列表），如果读取失败返回None
        """
        try:
            with open(file_path, 'r', encoding=encoding, newline='') as f:
                reader = csv.DictReader(f)
                return [row for row in reader]
        except Exception:
            return None

    @classmethod
    def write_csv_file(cls, file_path: str, data: List[Dict[str, Any]], encoding: str = 'utf-8') -> bool:
        """写入CSV文件

        Args:
            file_path: CSV文件路径
            data: 要写入的数据（字典列表）
            encoding: 文件编码

        Returns:
            是否成功
        """
        try:
            if not data:
                return False

            cls.ensure_dir(os.path.dirname(file_path))
            with open(file_path, 'w', encoding=encoding, newline='') as f:
                writer = csv.DictWriter(f, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
            return True
        except Exception:
            return False

    @classmethod
    def list_files(cls, dir_path: str, pattern: str = "*", recursive: bool = False) -> List[str]:
        """列出目录中的文件

        Args:
            dir_path: 目录路径
            pattern: 文件匹配模式（如：*.txt）
            recursive: 是否递归搜索

        Returns:
            文件路径列表
        """
        if recursive:
            return [str(p) for p in Path(dir_path).rglob(pattern)]
        else:
            return [str(p) for p in Path(dir_path).glob(pattern)]

    @classmethod
    def find_files_by_extension(cls, dir_path: str, extensions: List[str], recursive: bool = False) -> List[str]:
        """按扩展名查找文件

        Args:
            dir_path: 目录路径
            extensions: 扩展名列表（如：['.txt', '.md']）
            recursive: 是否递归搜索

        Returns:
            文件路径列表
        """
        files = []
        for ext in extensions:
            pattern = f"*{ext}"
            files.extend(cls.list_files(dir_path, pattern, recursive))
        return files

    @classmethod
    def find_files_by_content(cls, dir_path: str, content: str, recursive: bool = False) -> List[str]:
        """按内容查找文件

        Args:
            dir_path: 目录路径
            content: 要查找的内容
            recursive: 是否递归搜索

        Returns:
            包含指定内容的文件的路径列表
        """
        matching_files = []
        files = cls.list_files(dir_path, "*", recursive)

        for file_path in files:
            if cls.is_text_file(file_path):
                file_content = cls.read_file(file_path)
                if file_content and content in file_content:
                    matching_files.append(file_path)

        return matching_files

    @classmethod
    def get_file_hash(cls, file_path: str, hash_type: str = 'md5') -> Optional[str]:
        """计算文件哈希值

        Args:
            file_path: 文件路径
            hash_type: 哈希类型（'md5', 'sha1', 'sha256'）

        Returns:
            哈希值，如果计算失败返回None
        """
        try:
            hash_func = getattr(hashlib, hash_type)()
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_func.update(chunk)
            return hash_func.hexdigest()
        except Exception:
            return None

    @classmethod
    def get_file_create_time(cls, file_path: str) -> Optional[datetime.datetime]:
        """获取文件创建时间

        Args:
            file_path: 文件路径

        Returns:
            创建时间，如果获取失败返回None
        """
        try:
            timestamp = os.path.getctime(file_path)
            return datetime.datetime.fromtimestamp(timestamp)
        except Exception:
            return None

    @classmethod
    def get_file_modify_time(cls, file_path: str) -> Optional[datetime.datetime]:
        """获取文件修改时间

        Args:
            file_path: 文件路径

        Returns:
            修改时间，如果获取失败返回None
        """
        try:
            timestamp = os.path.getmtime(file_path)
            return datetime.datetime.fromtimestamp(timestamp)
        except Exception:
            return None

    @classmethod
    def backup_file(cls, file_path: str, backup_suffix: str = ".bak") -> bool:
        """备份文件

        Args:
            file_path: 文件路径
            backup_suffix: 备份文件后缀

        Returns:
            是否成功
        """
        if not os.path.exists(file_path):
            return False

        backup_path = f"{file_path}{backup_suffix}"
        return cls.copy_file(file_path, backup_path)

    @classmethod
    def clear_empty_dirs(cls, dir_path: str) -> int:
        """清理空目录

        Args:
            dir_path: 目录路径

        Returns:
            删除的空目录数量
        """
        deleted_count = 0

        for root, dirs, files in os.walk(dir_path, topdown=False):
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                if not os.listdir(dir_path):  # 检查目录是否为空
                    try:
                        os.rmdir(dir_path)
                        deleted_count += 1
                    except Exception:
                        pass

        return deleted_count

    @classmethod
    def get_disk_usage(cls, path: str = '.') -> Dict[str, int]:
        """获取磁盘使用情况

        Args:
            path: 路径

        Returns:
            包含总大小、已使用大小、可用大小的字典
        """
        try:
            total, used, free = shutil.disk_usage(path)
            return {
                'total': total,
                'used': used,
                'free': free,
                'used_percent': (used / total) * 100 if total > 0 else 0
            }
        except Exception:
            return {'total': 0, 'used': 0, 'free': 0, 'used_percent': 0}

    @classmethod
    def compress_file(cls, src_file: str, dst_file: str, format_type: str = 'zip') -> bool:
        """压缩文件

        Args:
            src_file: 源文件路径
            dst_file: 目标压缩文件路径
            format_type: 压缩格式（'zip', 'gz', 'bz2'）

        Returns:
            是否成功
        """
        try:
            if format_type == 'zip':
                import zipfile
                with zipfile.ZipFile(dst_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    zipf.write(src_file, os.path.basename(src_file))
            elif format_type in ['gz', 'bz2']:
                import gzip
                import bz2

                with open(src_file, 'rb') as f_in:
                    if format_type == 'gz':
                        with gzip.open(dst_file, 'wb') as f_out:
                            shutil.copyfileobj(f_in, f_out)
                    else:  # bz2
                        with bz2.open(dst_file, 'wb') as f_out:
                            shutil.copyfileobj(f_in, f_out)
            return True
        except Exception:
            return False

    @classmethod
    def extract_archive(cls, archive_path: str, extract_to: str) -> bool:
        """解压文件

        Args:
            archive_path: 压缩文件路径
            extract_to: 解压目标目录

        Returns:
            是否成功
        """
        try:
            cls.ensure_dir(extract_to)
            shutil.unpack_archive(archive_path, extract_to)
            return True
        except Exception:
            return False

    @classmethod
    def safe_filename(cls, filename: str) -> str:
        """生成安全的文件名（移除非法字符）

        Args:
            filename: 原文件名

        Returns:
            安全的文件名
        """
        # 非法字符列表
        illegal_chars = '<>:"/\\|?*'
        safe_name = filename

        for char in illegal_chars:
            safe_name = safe_name.replace(char, '_')

        return safe_name

    @classmethod
    def batch_rename(cls, dir_path: str, old_pattern: str, new_pattern: str) -> int:
        """批量重命名文件

        Args:
            dir_path: 目录路径
            old_pattern: 旧名称模式（支持通配符）
            new_pattern: 新名称模式

        Returns:
            重命名的文件数量
        """
        renamed_count = 0
        files = cls.list_files(dir_path)

        for file_path in files:
            filename = os.path.basename(file_path)
            if old_pattern in filename:
                new_filename = filename.replace(old_pattern, new_pattern)
                new_path = os.path.join(dir_path, new_filename)

                try:
                    os.rename(file_path, new_path)
                    renamed_count += 1
                except Exception:
                    pass

        return renamed_count