import time

class CircuitBreaker:

    def __init__(self):

        self.failure_count = 0
        self.failure_threshold = 3

        self.state = "CLOSED"

        self.last_failure_time = 0

        self.recovery_timeout = 10

    def can_call(self):

        if self.state == "CLOSED":
            return True

        if self.state == "OPEN":

            current_time = time.time()

            if current_time - self.last_failure_time > self.recovery_timeout:

                self.state = "HALF_OPEN"

                return True

            return False

        return True

    def record_failure(self):

        self.failure_count += 1

        self.last_failure_time = time.time()

        if self.failure_count >= self.failure_threshold:

            self.state = "OPEN"

    def reset(self):

        self.failure_count = 0

        self.state = "CLOSED"