from openai import OpenAI

client = OpenAI(
    api_key="sk-J3vEsFqZXfrV6UtUPCVTYYgfTzUdAr7lrqmhAxO3xDkGOLyL",
    base_url="https://api.chatanywhere.tech/v1"
)


def search_api(promt):
    messages = [
        {"role": "system", "content": "You are a intelligent assistant."}]
    messages.append({"role": "user", "content": promt})
    chat = client.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=messages)
    return chat.choices[0].message.content
