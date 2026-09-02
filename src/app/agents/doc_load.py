import requests
import json
import time

# 第一步：获取签名上传 URL
BASE_URL="https://mineru.net/api/v1/agent"
api_url = "https://mineru.net/api/v1/agent/parse/file"
# data = {
#     "file_name": "车间生产SOP_含图片.pdf",
#     "language": "ch",
#     "page_range": "1-10",
#     "enable_table": True,
#     "is_ocr": False,
#     "enable_formula": True
# }
#
# res = requests.post(api_url, json=data)
#
# result = res.json()
# task_id = result["data"]["task_id"]
# file_url = result["data"]["file_url"]
#
# print(f"任务已创建, task_id: {task_id}")
#
#
# # 第二步：PUT 上传文件到 OSS
# with open(r"..\..\doc\车间生产SOP_含图片.pdf", "rb") as f:
#     put_res = requests.put(file_url, data=f)
#     print(type(put_res))
#     print(f"{put_res[data].markdown_url}")
#
#     # print(json.dumps(put_res.json()))
#     # print(f"文件上传状态: {put_res.status_code}")
#     #
#     #
#     # url = f"{BASE_URL}parse/{task_id}"
#     #
#     # res = requests.get(url)
#     #
#     # print(json.dumps(res.json(),indent=2))
#
#



def parse_by_file(file_path, language="ch", page_range=None, enable_table=True, is_ocr=False, enable_formula=True):
    """通过文件上传提交文档解析任务并等待结果。"""
    file_name = file_path.split("/")[-1].split("\\")[-1]

    # 1. 获取签名上传 URL
    data = {"file_name": file_name, "language": language, "enable_table": enable_table, "is_ocr": is_ocr, "enable_formula": enable_formula}
    if page_range:
        data["page_range"] = page_range

    resp = requests.post(f"{BASE_URL}/parse/file", json=data)
    result = resp.json()
    if result["code"] != 0:
        print(f"获取上传链接失败: {result['msg']}")
        return None

    task_id = result["data"]["task_id"]
    file_url = result["data"]["file_url"]
    print(f"任务已创建, task_id: {task_id}")

    # 2. PUT 上传文件到 OSS
    with open(file_path, "rb") as f:
        put_resp = requests.put(file_url, data=f)
        if put_resp.status_code not in (200, 201):
            print(f"文件上传失败, HTTP {put_resp.status_code}")
            return None
    print("文件上传成功，等待解析...")

    # 3. 轮询等待结果
    return poll_result(task_id)


def poll_result(task_id, timeout=300, interval=3):
    """轮询查询解析结果。"""
    state_labels = {
        "pending": "排队中",
        "running": "解析中",
        "waiting-file": "等待文件上传",
    }
    start = time.time()
    while time.time() - start < timeout:
        resp = requests.get(f"{BASE_URL}/parse/{task_id}")
        result = resp.json()
        state = result["data"]["state"]
        elapsed = int(time.time() - start)

        if state == "done":
            markdown_url = result["data"]["markdown_url"]
            print(f"[{elapsed}s] 解析完成, Markdown 下载链接: {markdown_url}")
            md_resp = requests.get(markdown_url)
            return md_resp.text

        if state == "failed":
            print(f"[{elapsed}s] 解析失败: {result['data'].get('err_msg', '未知错误')}")
            return None

        print(f"[{elapsed}s] {state_labels.get(state, state)}...")
        time.sleep(interval)

    print(f"轮询超时 ({timeout}s)，请稍后手动查询 task_id: {task_id}")
    return None


# 使用示例
if __name__ == "__main__":
    content = parse_by_file("../../doc/车间生产SOP_含图片.pdf")