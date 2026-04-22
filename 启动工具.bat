@echo off
setlocal
title PDF 图片提取工具启动器

:: 检查 Python 是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未找到 Python，请确保已安装 Python 并将其添加到系统环境变量。
    pause
    exit /b
)

:: 检查 gui.py 是否存在
if not exist "gui.py" (
    echo [错误] 找不到 gui.py 文件，请确保在正确的文件夹中运行。
    pause
    exit /b
)

:: 尝试使用 pythonw (无黑框模式) 启动
echo 正在启动界面...
start "" pythonw gui.py

:: 检查 start 命令本身是否成功
if %errorlevel% neq 0 (
    echo [警告] 无窗口模式启动失败，尝试普通模式...
    python gui.py
    if %errorlevel% neq 0 (
        echo [错误] 程序运行崩溃，请检查依赖是否安装。
        pause
    )
) else (
    :: 启动成功后，稍等片刻自动退出黑框
    timeout /t 2 >nul
    exit
)
