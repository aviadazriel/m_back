from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
thread = client.beta.threads.create()
import time

assistant_id = os.getenv("ASSISTANT_ID")

def get_answer(run, thread):
    while True:
        run_status = client.beta.threads.runs.retrieve(thread_id=thread.id,
                                                       run_id=run.id)
        if run_status.status == "completed":
            break
        elif run_status.status == "failed":
            print("Run failed:", run_status.last_error)
            break
        time.sleep(0.5)

    messages = client.beta.threads.messages.list(thread.id)
    # number_of_messages = len(messages.data) #todo: if number of msg open new thread
    answer = messages.data[0].content[0].text.value
    # for message in reversed(messages.data):
    #     role = message.role
    #     for content in message.content:
    #         if content.type == 'text':
    #             response = content.text.value
    #             print(f'\n{role}: {response}')

    try:
        answer = messages.data[0].content[0].text.value
    except Exception as e:
        print(e)
        answer = ''


    return answer


def send_chat_msg(msg):
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=msg
    )
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
        temperature=1.0
        # instructions="Please provide the exact steps to solve the equation"
    )


    response = get_answer(run, thread)

    return response
