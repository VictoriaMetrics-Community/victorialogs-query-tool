import requests
from datetime import datetime, timedelta
import json
import argparse
import pyperclip
from rich.console import Console
from rich.highlighter import Highlighter
from rich.theme import Theme
from rich.syntax import Syntax

class JSONHighlighter(Highlighter):
    def __init__(self, fields_to_highlight):
        super().__init__()
        self.fields_to_highlight = fields_to_highlight

    def highlight(self, text):
        """Highlight specific fields in JSON."""
        for field in self.fields_to_highlight:
            text.highlight_regex(f'"{field}"', "field_name")
            text.highlight_regex(f'(?<="{field}": )("[^"]*"|\d+)', "field_value")
        # Highlight the level field
        text.highlight_regex(r'"level":\s*"error"', "level_error")
        text.highlight_regex(r'"level":\s*"warning"', "level_warning")
        text.highlight_regex(r'"level":\s*"info"', "level_info")

def get_timestamp(datetime_str):
    dt = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S%z")
    return int(dt.timestamp())

def parse_duration(duration_str):
    """Parse duration string like '5m' into a timedelta object."""
    unit = duration_str[-1]
    amount = int(duration_str[:-1])
    
    if unit == 'm':
        return timedelta(minutes=amount)
    elif unit == 'h':
        return timedelta(hours=amount)
    elif unit == 'd':
        return timedelta(days=amount)
    else:
        raise ValueError(f"Unknown duration unit: {unit}")

def build_query(config):
    query_parts = []
    
    if "RequestPath" in config and config["RequestPath"]:
        for path in config["RequestPath"]:
            query_parts.append(f'RequestPath:{path}')
    
    if "topic" in config and config["topic"]:
        query_parts.append(f'topic:{config["topic"]}')
    
    if "request_X-Ht-Uid" in config and config["request_X-Ht-Uid"]:
        for uid in config["request_X-Ht-Uid"]:
            query_parts.append(f'request_X-Ht-Uid:{uid}')
    
    if "OriginStatus" in config and config["OriginStatus"]:
        for status in config["OriginStatus"]:
            query_parts.append(f'OriginStatus:{status}')
    
    query_parts.append('_time:20d')
    
    if "_stream" in config and config["_stream"]:
        stream_parts = []
        for key, value in config["_stream"].items():
            stream_parts.append(f'{key}="{value}"')
        query_parts.append(f'_stream:{{{" , ".join(stream_parts)}}}')
    
    query_parts.append('level:*')
    
    if "_msg" in config and config["_msg"]:
        for msg in config["_msg"]:
            query_parts.append(f'_msg:{msg}')
    
    if "caller" in config and config["caller"]:
        query_parts.append(f'caller:{config["caller"]}')
    
    if "customize" in config and config["customize"]:
        for key, value in config["customize"].items():
            query_parts.append(f'{key}:{value}')
    
    if "fields" in config and config["fields"]:
        fields_str = ', '.join(config["fields"])
        query_parts.append(f'| fields {fields_str}')
    
    query_parts.append('| sort by (_time) desc')
    
    return ' '.join(query_parts)

def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--conf', type=str, required=True,
                        help='the configuration file to use')
    args = parser.parse_args()

    # 检查是否传递了配置文件参数
    if not args.conf:
        print("Error: Configuration file (--conf) is required.")
        return

    # 读取配置文件
    with open(args.conf, 'r') as f:
        config = json.load(f)

    # 检查是否提供了 API URL
    api_url = config.get("api_url")
    if not api_url:
        print("Error: API URL (api_url) is required in the configuration file.")
        return

    # 构建查询字符串
    query = build_query(config)
    print(f"Query: {query}")
    # 获取查询限制
    limit = config.get("limit", 1000)  # 默认值为1000

    # 构建 POST 请求的数据
    data = {
        'query': query,
        'limit': limit
    }

    # 处理 last_duration 或者 start_datetime 和 end_datetime
    if "last_duration" in config and config["last_duration"]:
        duration = parse_duration(config["last_duration"])
        now = datetime.now().astimezone()
        start_datetime = int((now - duration).timestamp())
        data['start'] = start_datetime
    else:
        start_datetime = get_timestamp(config["start_datetime"])
        end_datetime = get_timestamp(config["end_datetime"])
        data['start'] = start_datetime
        data['end'] = end_datetime

    # 执行 HTTP POST 请求
    response = requests.post(
        api_url,
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
        data=data
    )

    # 处理并美化输出 JSON Lines 数据
    custom_theme = Theme({
        "field_name": "bright_yellow",
        "field_value": "white",
        "level_error": "bold red",
        "level_warning": "bold yellow",
        "level_info": "bold green"
    })
    console = Console(theme=custom_theme, style="light_slate_grey")  # 设置默认颜色为淡白色
    
    # 获取需要高亮的字段
    fields_to_highlight = config.get("highlight_fields", [])
    highlighter = JSONHighlighter(fields_to_highlight)
    
    data = response.text
    json_lines = data.splitlines()
    for line in json_lines:
        try:
            parsed_data = json.loads(line)
            if limit == 1:
                # 打印漂亮的格式化 JSON
                json_str = json.dumps(parsed_data, indent=4)
                # 复制到系统剪贴板
                pyperclip.copy(json_str)
                syntax = Syntax(json_str, "json", theme="monokai", line_numbers=True)
                console.print(syntax)
            else:
                # 单行显示 JSON
                json_str = json.dumps(parsed_data)
                console.print(highlighter(json_str))
        except json.JSONDecodeError:
            console.print(f"[red]Error decoding JSON:[/red] {line}")

if __name__ == "__main__":
    main()

