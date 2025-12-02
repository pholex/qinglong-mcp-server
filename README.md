# 青龙面板 MCP Server

[![PyPI version](https://badge.fury.io/py/qinglong-mcp-server.svg)](https://badge.fury.io/py/qinglong-mcp-server)

这是一个 Model Context Protocol (MCP) server，用于查询和执行青龙面板中的定时任务。

## 功能

- `list_qinglong_tasks`: 查询青龙面板中的所有定时任务列表
- `run_task`: 执行任务并等待完成，自动返回执行日志（最多等待30秒）
- `run_task_async`: 异步启动任务，不等待执行完成
- `get_task_logs`: 获取青龙面板中指定任务的执行日志
- `get_task_status`: 获取青龙面板中指定任务的执行状态

## 安装

使用 pip 安装：

```bash
pip install qinglong-mcp-server
```

或使用 uvx（推荐，无需安装）：

```bash
uvx qinglong-mcp-server
```

## 配置

创建配置文件 `~/.qinglong-mcp/.env`：

**macOS/Linux:**
```bash
mkdir -p ~/.qinglong-mcp
nano ~/.qinglong-mcp/.env
```

**Windows:**
```cmd
mkdir %USERPROFILE%\.qinglong-mcp
notepad %USERPROFILE%\.qinglong-mcp\.env
```

填入以下内容：

```
QINGLONG_URL=https://your-qinglong-url.com
CLIENT_ID=your_client_id
CLIENT_SECRET=your_client_secret
```

## 使用

### 在 Kiro CLI 中使用

编辑 Kiro CLI 的 MCP 配置文件（`~/.kiro/settings/mcp.json`）：

```json
{
  "mcpServers": {
    "qinglong": {
      "command": "uvx",
      "args": ["qinglong-mcp-server"]
    }
  }
}
```

### 在 Claude Desktop 中使用

编辑配置文件：

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`

**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "qinglong": {
      "command": "uvx",
      "args": ["qinglong-mcp-server"]
    }
  }
}
```

### 开发测试

运行测试脚本：

```bash
./test_run_task.py <任务ID>
```

## 工具说明

### list_qinglong_tasks

查询所有任务，无需参数。

### run_task

执行任务并等待完成，自动返回执行日志（最多等待30秒），需要提供：
- `task_id`: 任务 ID（整数）

### run_task_async

异步启动任务，不等待执行完成，需要提供：
- `task_id`: 任务 ID（整数）

### get_task_logs

获取任务执行日志，需要提供：
- `task_id`: 任务 ID（整数）

### get_task_status

获取任务执行状态，需要提供：
- `task_id`: 任务 ID（整数）

## 升级

```bash
pip install -U qinglong-mcp-server
```

## 项目地址

- PyPI: https://pypi.org/project/qinglong-mcp-server/
- GitHub: https://github.com/pholex/qinglong-mcp-server

## 联系方式

- Email: pholex@gmail.com
