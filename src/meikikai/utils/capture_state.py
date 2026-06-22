# meikikai/utils/capture_state.py
import threading

_capture_depth = 0
_capture_lock = threading.Lock()


def begin_capture_interaction():
    global _capture_depth
    with _capture_lock:
        _capture_depth += 1


def end_capture_interaction():
    global _capture_depth
    with _capture_lock:
        _capture_depth = max(0, _capture_depth - 1)


def is_capture_interaction_active() -> bool:
    with _capture_lock:
        return _capture_depth > 0
