import os
import time
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

# ENV vars you need:
#   PROJECT_ENDPOINT - як і в першому скрипті
#   AGENT_ID         - id вже створеного агента (надрукований у попередньому коді)
project_endpoint = os.environ["PROJECT_ENDPOINT"]
agent_id = os.environ["AGENT_ID"]

project_client = AIProjectClient(
    endpoint=project_endpoint,
    credential=DefaultAzureCredential()
)

with project_client:
    # 1) Створюємо thread для всієї сесії
    thread = project_client.agents.threads.create()
    print(f"Thread created: {thread.id}")
    print("Type 'quit' to exit.\n")

    while True:
        user_input = input("You: ")
        if user_input.strip().lower() in ("quit", "exit"):
            break

        # 2) Додаємо повідомлення користувача в thread
        project_client.agents.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_input,
        )

        # 3) Створюємо і одразу обробляємо run
        run = project_client.agents.runs.create_and_process(
            thread_id=thread.id,
            agent_id=agent_id,
        )

        if run.status == "failed":
            print(f"[ERROR] Run failed: {run.last_error}")
            continue

        # 4) Забираємо останню відповідь агента з thread
        messages = list(project_client.agents.messages.list(thread_id=thread.id))
        # шукаємо останнє повідомлення з role == 'assistant' або 'agent'
        last_agent_msg = None
        for msg in reversed(messages):
            role = msg.get("role")
            if role in ("assistant", "agent"):
                last_agent_msg = msg
                break

        if last_agent_msg:
            content = last_agent_msg.get("content", [])
            # контент зазвичай список блоків, перший – text
            if content and isinstance(content, list):
                block = content[0]
                if isinstance(block, dict) and block.get("type") == "text":
                    text = block["text"].get("value") or block["text"].get("content") or ""
                    print(f"Agent: {text}\n")
                else:
                    print(f"Agent (raw content): {content}\n")
        else:
            print("[WARN] No agent message found\n")

    print("Session ended.")