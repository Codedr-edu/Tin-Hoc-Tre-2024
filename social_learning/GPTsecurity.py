import requests
# import json

# Replace with your actual values
personal_access_token = "pat_XSNlrVHnA3TtGOZIOZhsHJk0YkPEMAvRITqsobgau2QPFep3OJXHajsBHe9U2EBJ"
bot_id = "7363628797154836498"
# yourquery = "Make a polite and short greeting and then introduce about yourself and tell about what you can do"

url = "https://api.coze.com/open_api/v2/chat"

headers = {
    "Authorization": f"Bearer {personal_access_token}",
    "Content-Type": "application/json",
    "Accept": "*/*",
    "Host": "api.coze.com",
    "Connection": "keep-alive"
}


def check_image(image, bot_id=bot_id, url=url, headers=headers):
    prompt = "Hãy đọc và kiểm tra nội dung nhạy cảm nếu chúng xuất hiện trong bức ảnh trong đường link: https://bdt.pythonanywhere.com/" + \
        str(image)
    data = {
        "conversation_id": "123",
        "bot_id": bot_id,
        "user": "123333333",
        "query": prompt,
        "stream": False
    }

    response = requests.post(url, headers=headers, json=data)

    # Check for successful response
    if response.status_code == 200:
        data = response.json()
        # data = json.loads(data)
        # print(data[1]["content"])
        # print(response.json())
        # answer_content = response.json()["content"]
        # print(f"Answer content: {answer_content}")
        for message in data["messages"]:
            if message["type"] == "answer":
                return message["content"]
    else:
        return f"Error: API request failed with status code {response.status_code}"
        # print(response.text)


def check_document(image, bot_id=bot_id, url=url, headers=headers):
    prompt = "Hãy đọc và kiểm tra nội dung nhạy cảm nếu chúng xuất hiện trong file trong đường link sau: https://bdt.pythonanywhere.com" + \
        str(image)
    data = {
        "conversation_id": "123",
        "bot_id": bot_id,
        "user": "123333333",
        "query": prompt,
        "stream": False
    }

    response = requests.post(url, headers=headers, json=data)

    # Check for successful response
    if response.status_code == 200:
        data = response.json()
        # data = json.loads(data)
        # print(data[1]["content"])
        # print(response.json())
        # answer_content = response.json()["content"]
        # print(f"Answer content: {answer_content}")
        for message in data["messages"]:
            if message["type"] == "answer":
                return message["content"]
    else:
        return f"Error: API request failed with status code {response.status_code}"
        # print(response.text)


def check_content(image, bot_id=bot_id, url=url, headers=headers):
    prompt = "Hãy đọc và kiểm tra nội dung nhạy cảm nếu chúng xuất hiện trong đoạn văn bản sau: " + \
        str(image)
    data = {
        "conversation_id": "123",
        "bot_id": bot_id,
        "user": "123333333",
        "query": prompt,
        "stream": False
    }

    response = requests.post(url, headers=headers, json=data)

    # Check for successful response
    if response.status_code == 200:
        data = response.json()
        # data = json.loads(data)
        # print(data[1]["content"])
        # print(response.json())
        # answer_content = response.json()["content"]
        # print(f"Answer content: {answer_content}")
        for message in data["messages"]:
            if message["type"] == "answer":
                return message["content"]
    else:
        return f"Error: API request failed with status code {response.status_code}"
        # print(response.text)
