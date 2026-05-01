import subprocess
import sys
from pathlib import Path
import xml.etree.ElementTree as ET
import os
import json
import shutil
import urllib.request
import platform

from loguru import logger


def run_command(command, description, show_output: bool = True):
    """执行命令并显示结果（可控输出）"""
    if show_output:
        print(f"\n{'='*50}")
        print(f"执行: {description}")
        print(f"命令: {' '.join(command)}")
        print(f"{'='*50}")

    try:
        result = subprocess.run(command, capture_output=True, text=True, cwd=Path.cwd())

        if show_output and result.stdout:
            print("输出:")
            print(result.stdout)

        if show_output and result.stderr:
            print("错误:")
            print(result.stderr)

        return result.returncode == 0

    except Exception:
        return False


def run_system(command_str: str, description: str, show_output: bool = True) -> bool:
    """使用操作系统的 shell 执行命令（适配 Windows/macOS/Linux）"""
    if show_output:
        print(f"\n{'='*50}")
        print(f"执行: {description}")
        print(f"命令: {command_str}")
        print(f"{'='*50}")
    try:
        # Windows下需要使用shell=True来执行复合命令
        shell = platform.system() == 'Windows'
        code = os.system(command_str)
        return code == 0
    except Exception:
        return False


def ensure_dirs():
    reports_dir = Path('reports')
    allure_results = reports_dir / 'allure-results'
    html_dir = reports_dir / 'html'
    pytest_tmp = reports_dir / '.pytest_tmp'
    reports_dir.mkdir(parents=True, exist_ok=True)
    allure_results.mkdir(parents=True, exist_ok=True)
    html_dir.mkdir(parents=True, exist_ok=True)
    pytest_tmp.mkdir(parents=True, exist_ok=True)


def copy_allure_history():
    """复制历史数据以启用 Allure 趋势图"""
    src = Path('reports') / 'html' / 'history'
    dst_root = Path('reports') / 'allure-results'
    dst = dst_root / 'history'
    if src.exists() and src.is_dir():
        try:
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
        except Exception:
            pass


def _format_rate(rate: float) -> str:
    return f"{rate*100:.2f}%"


def _calc_rate(bucket):
    executed = bucket['passed'] + bucket['failed']
    if executed == 0:
        return 0.0, executed
    return bucket['passed'] / executed, executed


def _colorize(text: str, is_warning: bool, is_success: bool = False) -> str:
    # 企业微信 markdown 支持 <font color="warning">...</font> 和 <font color="info">...</font>
    if is_success:
        return f"<font color=\"info\">{text}</font>"
    return f"<font color=\"warning\">{text}</font>" if is_warning else text


def send_wecom_markdown(content: str) -> bool:
    """发送企业微信机器人 Markdown 消息。
    读取环境变量 WECOM_WEBHOOK 或 settings.WECOM_WEBHOOK。
    """
    webhook = os.environ.get('WECOM_WEBHOOK')
    if not webhook:
        try:
            import settings  # type: ignore
            webhook = getattr(settings, 'WECOM_WEBHOOK', None)
        except Exception:
            webhook = None
    if not webhook:
        return False

    headers = {"Content-Type": "application/json"}
    data = {"msgtype": "markdown", "markdown": {"content": content}}
    req = urllib.request.Request(webhook, data=json.dumps(data).encode('utf-8'), headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status == 200
    except Exception:
        logger.error("发送企业微信消息失败", exc_info=True)
        return False


def parse_junit_and_summary(junit_path: Path, notify_wecom: bool = True):
    """解析 JUnit XML，计算通过率并输出精简摘要（仅显示api和ui通过率）；可选发送企业微信。"""
    if not junit_path.exists():
        return

    try:
        tree = ET.parse(junit_path)
        root = tree.getroot()
    except Exception:
        return

    def init_bucket():
        return {"passed": 0, "failed": 0, "skipped": 0}

    overall = init_bucket()
    # 简化分类：只区分api和ui
    api_tests = init_bucket()
    ui_tests = init_bucket()

    for tc in root.iter('testcase'):
        file_path = tc.get('file') or ''
        classname = tc.get('classname') or ''

        # 简化分类：只区分api和ui
        test_type = None

        # 根据文件路径分类
        if file_path:
            path_str = Path(file_path).as_posix().lower()
            if 'api' in path_str:
                test_type = 'api'
            elif 'ui' in path_str:
                test_type = 'ui'

        # 如果路径中没有明确标识，从类名中提取
        if not test_type and classname:
            class_lower = classname.lower()
            if 'api' in class_lower:
                test_type = 'api'
            elif 'ui' in class_lower:
                test_type = 'ui'

        # 如果仍然无法分类，默认为api
        if not test_type:
            test_type = 'api'

        has_failure = tc.find('failure') is not None
        has_error = tc.find('error') is not None
        is_skipped = tc.find('skipped') is not None

        if is_skipped:
            outcome = 'skipped'
        elif has_failure or has_error:
            outcome = 'failed'
        else:
            outcome = 'passed'

        overall[outcome] += 1

        # 只统计api和ui的通过率
        if test_type == 'api':
            api_tests[outcome] += 1
        elif test_type == 'ui':
            ui_tests[outcome] += 1

    # 计算通过率
    overall_rate, overall_exec = _calc_rate(overall)
    api_rate, api_exec = _calc_rate(api_tests)
    ui_rate, ui_exec = _calc_rate(ui_tests)

    title_lines = []
    title_lines.append("自动化测试通过率统计")

    def line(label_cn: str, passed: int, executed: int, rate: float) -> str:
        rate_text = _format_rate(rate)
        warn = rate < 0.90
        is_perfect = rate >= 1.0
        rate_text = _colorize(rate_text, warn, is_perfect)
        return f"{label_cn}: 用例总数：{executed}，用例通过数：{passed}，用例通过率：{rate_text}"

    # 简化输出 - 只显示api和ui通过率
    print("\n" + "="*60)
    print("自动化测试通过率报告")
    print("="*60)

    print(line("总体", overall['passed'], overall_exec, overall_rate))

    if api_exec > 0:
        print(line("API测试", api_tests['passed'], api_exec, api_rate))

    if ui_exec > 0:
        print(line("UI测试", ui_tests['passed'], ui_exec, ui_rate))

    print("="*60)
    print("测试执行完成")

    if not notify_wecom:
        return

    # 企业微信 Markdown 内容（简化版）
    md_lines = []
    md_lines.append("### 自动化测试通过率报告")
    md_lines.append("---")
    md_lines.append(line("总体", overall['passed'], overall_exec, overall_rate))

    if api_exec > 0:
        md_lines.append(line("API测试", api_tests['passed'], api_exec, api_rate))

    if ui_exec > 0:
        md_lines.append(line("UI测试", ui_tests['passed'], ui_exec, ui_rate))

    md_lines.append("---")
    md_lines.append("测试执行完成")

    # 附加 Allure 报告链接（仅 Jenkins 环境）
    try:
        from settings import ALLURE_REPORT_URL
        if ALLURE_REPORT_URL:
            md_lines.append(f"\n[查看 Allure 报告]({ALLURE_REPORT_URL})")
    except Exception:
        pass

    send_wecom_markdown("\n".join(md_lines))


def main():
    ensure_dirs()

    # 运行测试（生成 JUnit XML）
    junit_path = Path('reports') / 'junit.xml'
    basetemp = Path('reports') / '.pytest_tmp'
    pytest_cmd = [
        "pytest",
        "-q",
        f"--basetemp={basetemp.as_posix()}",
        f"--junitxml={junit_path.as_posix()}",
    ]
    # 静默运行测试，仅用于产物
    run_command(pytest_cmd, "运行自动化测试并生成 JUnit 报告", show_output=False)

    # 输出通过率（控制台 + 可选企业微信）
    parse_junit_and_summary(junit_path, notify_wecom=True)

    # Allure 趋势：复制历史后再生成（优化跨平台兼容性）
    copy_allure_history()

    # 生成 Allure 报告（仅在 allure 命令可用时执行）
    allure_results_path = Path('reports') / 'allure-results'
    allure_html_path = Path('reports') / 'html'

    if shutil.which('allure') is not None:
        if platform.system() == 'Windows':
            allure_cmd = f"allure generate \"{allure_results_path}\" -o \"{allure_html_path}\" --clean"
        else:
            allure_cmd = f"allure generate {allure_results_path} -o {allure_html_path} --clean"

        run_system(allure_cmd, "生成Allure报告", show_output=False)
    else:
        logger.info("allure 未安装，跳过本地 Allure 报告生成")

    return 0


if __name__ == "__main__":
    sys.exit(main())