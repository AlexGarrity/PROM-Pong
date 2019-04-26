


class Debouncer:

    # The current state of the switch
    current_state = False
    # The current last signal received
    current_signal = 0
    last_signal = 0
    delta_signal = 0
    # The maximum and minimum signals the button can produce
    max_signal = 0
    half_signal = 0
    min_signal = 0
    # Permissible variance in the signal
    stability_threshold = 0.1

    def __init__(self, minimum_time):
        self.minimum_time = minimum_time
        # Open a bus to the button here
        self.half_signal = self.max_signal / 2

    def change_state(self):
        if self.current_signal < self.half_signal:
            self.current_signal = False
        else:
            self.current_signal = True

    def get_state(self):
        return self.current_state

    def update(self):
        self.last_signal = self.current_signal
        # Get the current signal here
        self.delta_signal = abs(self.last_signal - self.current_signal)
        if self.delta_signal > self.half_signal:
            self.change_state()
