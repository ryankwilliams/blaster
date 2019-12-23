import signal
import time


def do_stuff():
    print("delay for 10 seconds")
    time.sleep(10)
    print("delay complete")


def handler(signum, frame):
    raise RuntimeError


signal.signal(signal.SIGALRM, handler)


for i in range(1):
    signal.alarm(5)

    try:
        do_stuff()
    except RuntimeError as e:
        print("aborted")
    finally:
        signal.alarm(0)
