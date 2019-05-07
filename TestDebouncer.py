
import random
import Debouncer
import time

noise = []

def lerp(t, old, new):
    return old + t * (new - old)


if __name__ == "__main__":
    target_signal = 0.0
    debouncer = Debouncer.Debouncer(1.0, 0.0, 0.4)
    debouncer.set_signal(0.0)
    for k in range(3):
        if target_signal > 0.5:
            target_signal = 0.13575424
        else:
            target_signal = 0.96346422
        print("\nTarget Signal %f\n" % target_signal)

        for j in range(10):
            print("Current signal\t%f" % debouncer.current_signal)
            print("Last signals\t%s" % debouncer.signal_history)
            print("Current state\t%s\n" % str(debouncer.get_state()))
            new_value = lerp(0.6, debouncer.current_signal, target_signal) + ((random.random() - 0.5) / 10)
            debouncer.set_signal(new_value)
            time.sleep(0.125)
