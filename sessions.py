sessions = []

def add_session_string(session_str):
    if session_str not in sessions:
        sessions.append(session_str)
        return True
    return False

def remove_session_string(session_str):
    if session_str in sessions:
        sessions.remove(session_str)
        return True
    return False

def get_all_sessions():
    return sessions
