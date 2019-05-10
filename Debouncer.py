
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
        if self.current_signal < self.half_signal:
            self.current_state = False
        else:
            self.current_state = True

    def get_state(self):
        return self.current_state

    def set_signal(self, signal):
        self.add_to_history()
        self.current_signal = signal
        if self.detect_state_change():
            self.change_state()

    def detect_state_change(self):
        if self.signal_history[2] >= self.signal_history[1] >= self.signal_history[0]:
            if abs(self.signal_history[0] - self.signal_history[2]) > self.stability_threshold:
                return 1
        elif self.signal_history[0] >= self.signal_history[1] >= self.signal_history[2]:
            if abs(self.signal_history[0] - self.signal_history[2]) > self.stability_threshold:
                return 1
        return 0

    def add_to_history(self):
        print ("Current signal: %i" % self.current_signal)
        self.signal_history.append(self.current_signal)
        if len(self.signal_history) > 3:
            self.signal_history.pop(0)

    def update(self):
        self.add_to_history()
        # Get the current signal here
        if self.detect_state_change():
            self.change_state()
