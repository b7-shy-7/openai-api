import os
import openai
from openai import OpenAI


client = OpenAI()
history = ""
while(1):
    message = input()
    if message.lower() == 'stop':
        break
    # message = "1+1=?"
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        # response_format={ 'type': "json_object"},
        messages=[
            # {"role": "system", "content": "you are a hospitable and knowledgable helper"},
            # {"role": "user", "content": message},
            {"role": "assistant", "content": history},
            {"role": "user", "content": message}
        ],
        # seed = 1000000
        stream = True,
    )
    ans = ""
    for chunk in completion:
        print(chunk.choices[0].delta.content, end ='')
        try:
            ans += chunk.choices[0].delta.content
        except:
            pass
    # history += message
    history += (message + ans + ' ')
    print()
    # print(completion.choices[0].message.content)