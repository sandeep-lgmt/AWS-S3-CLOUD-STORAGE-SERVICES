import time

class TimezoneHandler:
    def __init__(self):
        self.current_timezone = time.tzname

    def handle_timezone_change(self):
        if time.tzname != self.current_timezone:
            self.current_timezone = time.tzname
            print(f"Timezone changed to {self.current_timezone}")