import keyboard
import time
import pandas as pd


def load_saved_dataframe():
    try:
        dwell_times = pd.read_csv('saved_files/dwell_times.csv')
        flight_times = pd.read_csv('saved_files/flight_times.csv')
        return dwell_times, flight_times
    except pd.errors.EmptyDataError: 
        return pd.DataFrame(), pd.DataFrame()


def record_keystrokes(dwell_df, flight_df):
    start_time = time.time()
    last_key_time = start_time
    while True:
        try:
            event = keyboard.read_event()
            timestamp = time.time() - start_time
            if event.event_type == keyboard.KEY_DOWN:
                dwell_time = timestamp - last_key_time
                last_key_time = timestamp
                dwell_df.append(dwell_time)
            elif event.event_type == keyboard.KEY_UP:
                flight_time = timestamp - last_key_time
                last_key_time = timestamp
                flight_df.append(flight_time)
        except KeyboardInterrupt as e:
            break


def main():
    dwell_times, flight_times = load_saved_dataframe()
    record_keystrokes(dwell_times, flight_times)


if __name__ == "__main__":
    main()
