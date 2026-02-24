from typing import Dict, List
from collections import defaultdict

class ConversationStore:
    def __init__(self):
        self.sessions: Dict[str, List[Dict[str, str]]] = defaultdict(list)

    def add_message(self, session_id: str, role: str, content: str):
        self.sessions[session_id].append({
            "role": role,
            "content": content
        })

    def get_history(self, session_id: str):
        return self.sessions[session_id]

    def clear(self, session_id: str):
        self.sessions[session_id] = []


conversation_store = ConversationStore()