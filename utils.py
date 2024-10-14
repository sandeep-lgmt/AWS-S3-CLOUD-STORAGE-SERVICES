import os
import sys
import psutil

def check_single_instance():
    pid_file = "agent.pid"
    if os.path.exists(pid_file):
        sys.exit("Another instance is already running.")
    with open(pid_file, "w") as f:
        f.write(str(os.getpid()))

def detect_battery_level():
    battery = psutil.sensors_battery()
    if battery:
        return battery.percent
    return 100  # Assume full battery if no sensor detected