import sys
import time
from datetime import datetime
from fissure_fetcher import fetch_fissures
from display_utils import print_fissures
from config import (
    REFRESH_API,
    REFRESH_UI,
    ANSI_HIDE_CURSOR,
    ANSI_SHOW_CURSOR,
    ANSI_HOME,
    ANSI_CLEAR_SCREEN
)

def setup_tui():
    print(ANSI_HIDE_CURSOR, end="", flush=True)

def teardown_tui():
    print(ANSI_SHOW_CURSOR, end="", flush=True)


def main():
    """DON'T FKING TOUCH THIS AGAIN, FUTURE YOU WILL TRAVEL BACK IN TIME AND SLAP YOU AROUND!"""
    
    fissure_data = []
    last_fetch_time = 0
    pending_update = None
    setup_tui()

    print(ANSI_HOME + ANSI_CLEAR_SCREEN, end="", flush=True)

    try:
        while True:
            current_time = time.monotonic()
            
            # Fetch new data without scaring the UI
            if current_time - last_fetch_time >= REFRESH_API:
                new_data, error = fetch_fissures()
                if not error:
                    pending_update = new_data
                last_fetch_time = current_time
            
            # Apply pending update
            if pending_update is not None:
                fissure_data = pending_update
                pending_update = None
            
            # Update countdown timers
            updated_fissures = []
            for fissure, expiry, is_hard in fissure_data:
                remaining = expiry - datetime.now(expiry.tzinfo)
                updated_fissures.append((fissure, expiry, is_hard, remaining))
            
            # Smooth fucking UI rendering
            print(ANSI_HOME, end="")
            fissure_output = print_fissures([(f, e, h) for f, e, h, _ in updated_fissures])
            print(fissure_output, flush=True)
            
            # Precision sleep
            elapsed = time.monotonic() - current_time
            if elapsed < REFRESH_UI:
                time.sleep(REFRESH_UI - elapsed)
            
    except KeyboardInterrupt:
        print("\n👋 Exiting tracker...")
    finally:
        teardown_tui()

if __name__ == "__main__":
    main()
