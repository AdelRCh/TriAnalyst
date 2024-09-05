import time

# Preventing the "Too Many Requests" error code, avoiding rate limitations.
def pause_between_reqs(needed:bool=False):
    if needed:
        time.sleep(10)
