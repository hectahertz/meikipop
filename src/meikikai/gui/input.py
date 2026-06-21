# meikikai/gui/input.py
import logging
import threading
import time

import Quartz
from AppKit import NSEvent
from pynput import mouse

from meikikai.config.config import config

logger = logging.getLogger(__name__)

NX_KEYTYPE_PLAY = 16
NX_SUBTYPE_AUX_CONTROL_BUTTONS = 8
NS_SYSTEM_DEFINED = 14
KEY_DOWN_STATE = 0xA
KEY_UP_STATE = 0xB


def toggle_macos_play_pause_key() -> bool:
    """Toggle macOS media playback using the system Play/Pause key event."""
    try:
        for state in (KEY_DOWN_STATE, KEY_UP_STATE):
            event = NSEvent.otherEventWithType_location_modifierFlags_timestamp_windowNumber_context_subtype_data1_data2_(
                NS_SYSTEM_DEFINED,
                (0, 0),
                state << 8,
                0,
                0,
                None,
                NX_SUBTYPE_AUX_CONTROL_BUTTONS,
                (NX_KEYTYPE_PLAY << 16) | (state << 8),
                -1,
            )
            Quartz.CGEventPost(Quartz.kCGHIDEventTap, event.CGEvent())
        return True
    except Exception as e:
        logger.warning(f"Failed to toggle macOS Play/Pause key: {e}")
        return False


class InputLoop(threading.Thread):
    def __init__(self, shared_state):
        super().__init__(daemon=True, name="InputLoop")
        self.shared_state = shared_state
        self.mouse_controller = mouse.Controller()

    def run(self):
        logger.debug("Input thread started.")
        last_mouse_pos = (0, 0)
        self.shared_state.screenshot_trigger_event.set()

        while self.shared_state.running:
            if not config.is_enabled:
                time.sleep(0.1)
                continue
            try:
                current_mouse_pos = self.mouse_controller.position

                # trigger hit_scans + lookups
                if current_mouse_pos != last_mouse_pos:
                    self.shared_state.hit_scan_queue.trigger()

                last_mouse_pos = current_mouse_pos
            except:
                logger.exception("An unexpected error occurred in the input loop. Continuing...")
            finally:
                time.sleep(0.01)
        logger.debug("Input thread stopped.")

    @staticmethod
    def get_mouse_pos():
        pos = mouse.Controller().position
        return (int(pos[0]), int(pos[1]))
