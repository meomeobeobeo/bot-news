import openai

API_KEY = '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'

openai.api_key = API_KEY
model_id = 'gpt-3.5-turbo'
def ChatGPT_conversation():
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "do you know about sailjs javaScript"},
        ]
    )
    print(res)
    return res

ChatGPT_conversation()