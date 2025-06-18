# query: _msg:UpdateFixedRecommendSort caller:business/fixed_recommend_sort.go
# limit: 50
# start: 2025-03-03T07:51:08.627Z
# end: 2025-03-03T07:56:08.627Z

import requests
import json

url = "https://vlogs.hellotalk8.com/select/logsql/query"


def queryVlogTest():
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",  # 注意这里的内容类型
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }

    # 构建查询字符串
    query = "_msg:UpdateFixedRecommendSort caller:business/fixed_recommend_sort.go"

    # 将时间字符串转换为时间戳
    start_time = "2025-03-03T07:51:08.627Z"
    end_time = "2025-03-03T07:56:08.627Z"

    # 准备表单数据 - 注意这里使用data而不是json
    form_data = {
        'query': query,
        'limit': 50,
        'start': start_time,
        'end': end_time
    }

    print(f"请求URL: {url}")
    print(f"请求数据: {form_data}")

    # 发送POST请求，使用data参数而不是json参数
    response = requests.post(url, headers=headers, data=form_data)

    print(f"状态码: {response.status_code}")

    # 处理响应
    if response.status_code == 200:
        # 尝试解析JSON Lines格式
        json_lines = response.text.splitlines()
        for line in json_lines:
            try:
                parsed_data = json.loads(line)
                print(json.dumps(parsed_data, indent=4))
            except json.JSONDecodeError:
                print(f"无法解析JSON行: {line}")
    else:
        print(f"请求失败: {response.text}")


if __name__ == "__main__":
    queryVlogTest()
