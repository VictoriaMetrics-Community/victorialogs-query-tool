import requests
import base64

# 获取订阅内容的URL
url = "https://service-472jprl5-1322266764.sh.apigw.tencentcs.com/api/v1/client/subscribe?token=b822a71cf24cef2a56cf6ddb60153524"

# 请求头
headers = {
    "accept": "application/json",
    "accept-language": "zh-Hans-CN;q=1.0",
    "http_user_agent": "massive",
    "user-agent": "Leens/1.1.6 (com.biGuoSha.com; build:7; iOS 17.6.1) Alamofire/5.6.3",
    "authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MzUwMTY3LCJzZXNzaW9uIjoiMTM3MWM1Y2Q0M2E5NTkzYjhlMGZkMDkwZjgwOWQxOTgifQ.s3Qp3O1xMW6vNfnzadKNW0C5i2AXFQ-E1LOyXz-O05k",
    "accept-encoding": "br;q=1.0, gzip;q=0.9, deflate;q=0.8",
    "content-length": "0"
}

# 发送请求
response = requests.get(url, headers=headers)
if response.status_code == 200:
    decoded_data = base64.b64decode(response.content).decode('utf-8')
else:
    print(f"Failed to fetch data: {response.status_code}")
    exit()

# 解析节点配置
nodes = decoded_data.split('\r\n')
for node in nodes:
    if node:
        parts = node.split(',')
        if len(parts) >= 7:
            name = parts[0].split('=')[0]
            protocol = parts[0].split('=')[1]
            server = parts[1]
            port = parts[2]
            method = parts[3]
            password = parts[4]
            fast_open = parts[5].split('=')[1]
            udp = parts[6].split('=')[1]

            print(f"Name: {name}")
            print(f"Protocol: {protocol}")
            print(f"Server: {server}")
            print(f"Port: {port}")
            print(f"Method: {method}")
            print(f"Password: {password}")
            print(f"Fast Open: {fast_open}")
            print(f"UDP: {udp}")
            print("----------")
        else:
            print("Invalid node format:", node)

