from collections import defaultdict

from config import MAX_HISTORY_MESSAGES

# session_id -> list of {"role": ..., "content": ...}; lost on restart.
_sessions: dict[str, list[dict]] = defaultdict(list)


def get_history(session_id: str) -> list[dict]:
    return list(_sessions[session_id])


def add_turn(session_id: str, user_msg: str, bot_msg: str) -> None:
    history = _sessions[session_id]
    history.append({"role": "user", "content": user_msg})
    history.append({"role": "assistant", "content": bot_msg})
    del history[:-MAX_HISTORY_MESSAGES]
