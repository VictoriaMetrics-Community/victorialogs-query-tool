
import requests
import toml


def getConfig():
    # 读取toml文件
    with open("vlog2_business.toml", "r") as f:
        config = toml.load(f)
    return config


if __name__ == "__main__":
    config = getConfig()

    # 拼接 msg _msg:UpdateFixedRecommendSort _msg:bbb
    msg = ""
    for value in config.get("_msg", []):
        # _msg 为list
        # 打印 key 和 value 的类型
        msg += f"_msg:{value} "

    # 拼接 caller  caller:business/fixed_recommend_sort.go
    caller = f"caller:{config.get('caller', '')}"

    # start_datetime 和 end_datetime
    start_datetime = config.get("start_datetime", "")
    end_datetime = config.get("end_datetime", "")

    # limit
    limit = config.get("limit", 0)

    # 请求vlog 日志

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",  # 注意这里的内容类型
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }

    query = f"{msg}{caller}"
    print(query)
    form_data = {
        "query": query,
        "start": start_datetime,
        "end": end_datetime,
        "limit": limit
    }
    url = "https://vlogs.hellotalk8.com/select/logsql/query"
    response = requests.post(url, headers=headers, data=form_data)
    print(response.text)
