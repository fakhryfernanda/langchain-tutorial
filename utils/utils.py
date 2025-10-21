from typing import List, Optional
from langchain.messages import HumanMessage, AIMessage, AnyMessage

def get_last_ai_message(messages: List[AnyMessage]) -> Optional[AIMessage]:
    """
    Returns the last AIMessage in a list of BaseMessage objects.
    If no AIMessage exists, returns None.
    """
    for msg in reversed(messages):
        if isinstance(msg, AIMessage):
            return msg
    return None

def get_text_content(msg: AnyMessage) -> str:
    """
    Safely extract all text from a LangChain BaseMessage.
    Works with both legacy string content and structured content (list[dict]).
    """
    content = msg.content

    if isinstance(content, str):
        return content

    if isinstance(content, list):
        texts = []
        for part in content:
            if isinstance(part, dict):
                if part.get("type") == "text" and "text" in part:
                    texts.append(part["text"])
            elif isinstance(part, str):
                texts.append(part)
        return "".join(texts)

    return str(content)

