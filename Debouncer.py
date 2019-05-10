
# Far more complicated than necessary, designed for use with floating point input
# GPIO only provides 1 and 0, so use moving average cast to an int

class Debouncer:

    # The current state of the switch
    current_state = False

    # The current last signal received
    current_signal = 0
    signal_history = [0.0, 0.0, 0.0]
    delta_signal = 0

    # The maximum and minimum signals the button can produce
    max_signal = 0
    half_signal = 0
    min_signal = 0

    # Permissible variance in the signal
    stability_threshold = 0.4

    def __init__(self, max_signal, min_signal, stability_threshold):
        # Open a bus to the button here
        self.half_signal = (max_signal - min_signal) / 2
        self.max_signal = max_signal
        self.min_signal = min_signal
        self.stability_threshold = stability_threshold

    def change_state(self):
        self.current_state = not self.current_state

    def get_state(self):
        return self.current_state

    def set_signal(self, signal):
        self.add_to_history()
        self.current_signal = signal
        if self.detect_state_change():
            self.change_state()

    def detect_state_change(self):
        average = sum(self.signal_history) // 3
        if self.current_signal != average:
            return True
        return False

    def add_to_history(self):
        self.signal_history.append(self.current_signal)
        if len(self.signal_history) > 3:
            self.signal_history.pop(0)

    def update(self):
        self.add_to_history()
        # Get the current signal here
        if self.detect_state_change():
            self.change_state()
