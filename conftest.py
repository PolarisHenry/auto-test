import os
import platform
import shutil

import allure
import pytest
from loguru import logger
from settings import ROOT_PATH


# ================= 日志配置 =================
logger.add(
    ROOT_PATH / "logs/test_{time:YYYY-MM-DD}.log",
    rotation="1 day",
    level="INFO",
    encoding="utf-8",
    enqueue=True,
)

# ================= 必要目录 =================
os.makedirs(ROOT_PATH / "reports/screenshots", exist_ok=True)
os.makedirs(ROOT_PATH / "reports/videos", exist_ok=True)
os.makedirs(ROOT_PATH / "reports/allure-results", exist_ok=True)
os.makedirs(ROOT_PATH / "logs", exist_ok=True)


# ================= Playwright 配置 =================
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, tmp_path_factory):
    """配置浏览器上下文参数"""
    # 避免 playwright 默认 test-results，视频临时保存到 pytest 的临时目录
    video_dir = tmp_path_factory.mktemp("videos")
    args = {
        **browser_context_args,
        "viewport": {"width": 1536, "height": 791},
        "record_video_dir": str(video_dir),
    }
    # Windows 环境忽略 HTTPS 错误
    if platform.system() == "Windows":
        args["ignore_https_errors"] = True
    return args


@pytest.fixture(autouse=True)
def log_test_start_and_end(request):
    """记录测试开始和结束"""
    test_name = request.node.name
    logger.info(f"开始执行测试: {test_name}")

    def log_test_end():
        logger.info(f"测试执行完成: {test_name}")

    request.addfinalizer(log_test_end)


# ================= 测试失败时处理（截图+视频） =================
@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """
    在测试阶段结束后，判断是否失败，失败时自动附加截图和视频到 allure 报告。
    截图在 call 阶段执行（页面可用），视频在 teardown 阶段执行（context 关闭后视频才完整写入）。
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)

    if rep.when == "call" and rep.failed:
        page = item.funcargs.get("page")  # 依赖 pytest-playwright 提供的 page fixture
        if page:
            # 截图（call 阶段页面还在，立即截图）
            screenshots_dir = ROOT_PATH / "reports/screenshots"
            screenshot_path = screenshots_dir / f"{item.nodeid.replace('/', '_').replace('::', '__')}.png"
            page.screenshot(path=str(screenshot_path))
            allure.attach.file(
                str(screenshot_path),
                name="失败截图",
                attachment_type=allure.attachment_type.PNG
            )

            # 暂存视频路径，等 teardown 阶段（context 关闭后视频写完了）再处理
            if page.video:
                item._video_path = page.video.path()

    if rep.when == "teardown":
        # 检查 call 阶段是否失败，而非 teardown 本身
        call_report = getattr(item, "rep_call", None)
        if call_report and call_report.failed:
            video_path = getattr(item, "_video_path", None)
            if video_path and os.path.exists(video_path):
                videos_dir = ROOT_PATH / "reports/videos"
                final_video_path = videos_dir / f"{item.nodeid.replace('/', '_').replace('::', '__')}.webm"
                try:
                    # 此时 browser context 已关闭，视频文件已完整写入磁盘
                    shutil.move(video_path, str(final_video_path))
                    allure.attach.file(
                        str(final_video_path),
                        name="失败视频",
                        attachment_type=allure.attachment_type.WEBM
                    )
                except Exception as e:
                    logger.warning(f"视频处理失败: {e}")


# ================= 自定义断言信息 =================
def pytest_assertrepr_compare(config, op, left, right):
    """
    用中文重写断言失败时的比较信息，支持常见操作符。
    """
    logger.error(f"断言失败: {op} 比较失败，实际值: {left!r}，期望值: {right!r}")

    if op == "==":
        return ["断言失败：两者相等 (==) 比较失败", f"实际值: {left!r}", f"期望值: {right!r}"]
    elif op == "!=":
        return ["断言失败：两者不等 (!=) 比较失败", f"实际值: {left!r}", f"期望值: {right!r}"]
    elif op == "in":
        return ["断言失败：实际值元素未包含于期望值 (in) 比较失败", f"实际值: {left!r}", f"期望值: {right!r}"]
    elif op == "not in":
        return ["断言失败：实际值元素包含于期望值 (not in) 比较失败", f"实际值: {left!r}", f"期望值: {right!r}"]
    elif op == ">":
        return ["断言失败：实际值不大于期望值 (>) 比较失败", f"实际值: {left!r}", f"期望值: {right!r}"]
    elif op == ">=":
        return ["断言失败：实际值不大于等于期望值 (>=) 比较失败", f"实际值: {left!r}", f"期望值: {right!r}"]
    elif op == "<":
        return ["断言失败：实际值不小于期望值 (<) 比较失败", f"实际值: {left!r}", f"期望值: {right!r}"]
    elif op == "<=":
        return ["断言失败：实际值不小于等于期望值 (<=) 比较失败", f"实际值: {left!r}", f"期望值: {right!r}"]
    elif op == "is":
        return ["断言失败：两者不是同一对象 (is) 比较失败", f"实际值: {left!r}", f"期望值: {right!r}"]
    elif op == "is not":
        return ["断言失败：两者是同一对象 (is not) 比较失败", f"实际值: {left!r}", f"期望值: {right!r}"]
    elif op == "not":
        return ["断言失败：not 比较失败", f"对象: {left!r}"]
    return None