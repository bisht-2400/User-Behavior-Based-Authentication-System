import os
import threading
import time
import pandas
import pandas as pd
import keyboard


def create_path_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Directory created: {path}")
    else:
        print(f"Directory already exists: {path}")


def is_key_event(string):
    keywords = ['alt', 'alt gr', 'ctrl', 'left alt', 'left ctrl', 'left shift', 'left windows', 'right alt',
                'right ctrl', 'right shift', 'right windows', 'shift', 'windows', 'enter', 'space', 'tab',
                'insert', 'caps lock', 'esc', 'left', 'right', 'up', 'down', 'backspace', 'print screen']
    if string in keywords:
        return False
    else:
        return True


class Keylogger:
    def __init__(self):
        self.dwell_time = []
        self.flight_time = []
        self.dwell_start_time = 0
        self.flight_start_time = None
        self.running = True
        self.last_key = "~"
        self.flight_dataframe = pd.DataFrame()
        self.dwell_dataframe = pd.DataFrame()

    def record_keys(self, event):
        if event.event_type == keyboard.KEY_DOWN and is_key_event(event.name):
            self.dwell_start_time = event.time
            if self.flight_start_time is not None:
                f_time = event.time - self.flight_start_time
                if 0 < f_time < 1:
                    self.flight_time.append([f_time, event.name, self.last_key])

        elif event.event_type == keyboard.KEY_UP and is_key_event(event.name):
            self.flight_start_time = event.time
            d_time = event.time - self.dwell_start_time

            if d_time > 0:
                self.dwell_time.append([d_time, event.name, self.last_key])
            self.last_key = event.name

        if len(self.dwell_time) % 50 == 0 and len(self.dwell_time) > 0:
            self.save_dataframe()
            self.dwell_time.clear()
            self.flight_time.clear()

    def start_keylogger(self):
        print('\nPROCESS STARTED\n')
        self.load_dataframe()
        self.running = True
        keyboard.hook(self.record_keys)
        while self.running:
            time.sleep(0.1)

    def stop_keylogger(self):
        self.running = False
        keyboard.unhook_all()

    def convert_to_df(self):
        df_dwell = pd.DataFrame({
            'dwell_times': [entry[0] for entry in self.dwell_time],
            'current_key': [ord(entry[1]) for entry in self.dwell_time],
            'last_key': [ord(entry[2]) for entry in self.dwell_time]

        })

        df_flight = pd.DataFrame({
            'flight_times': [entry[0] for entry in self.flight_time],
            'current_key': [ord(entry[1]) for entry in self.flight_time],
            'last_key': [ord(entry[2]) for entry in self.flight_time]
        })

        if self.flight_dataframe.empty:
            self.flight_dataframe = df_flight
        else:
            self.flight_dataframe = pd.concat([self.flight_dataframe, df_flight], ignore_index=True)

        if self.dwell_dataframe.empty:
            self.dwell_dataframe = df_dwell
        else:
            self.dwell_dataframe = pd.concat([self.dwell_dataframe, df_dwell], ignore_index=True)

    def save_dataframe(self):
        print("\nSAVING DF\n")
        self.convert_to_df()

        self.flight_dataframe.to_excel('./saved_files/flight_data.xlsx', index=False)
        self.dwell_dataframe.to_excel('./saved_files/dwell_data.xlsx', index=False)

        # self.flight_dataframe.to_pickle('./saved_files/unauthorized_flight_data_2.pkl')
        # self.dwell_dataframe.to_pickle('./saved_files/unauthorized_dwell_data_2.pkl')

    def load_dataframe(self):
        try:
            print('\nLOADING FRAMES\n')
            self.flight_dataframe = pandas.read_excel('./saved_files/flight_data.xlsx')
            self.dwell_dataframe = pandas.read_excel('./saved_files/dwell_data.xlsx')

            # self.flight_dataframe.to_pickle('./saved_files/unauthorized_flight_data_2.pkl')
            # self.dwell_dataframe.to_pickle('./saved_files/unauthorized_dwell_data_2.pkl')

        except FileNotFoundError:
            print('\nEMPTY DF DETECTED\n')
        except Exception as e:
            print(f"An Error has occurred: {e}")

    def print_times(self):
        print("Dwell times: ", self.dwell_time, "Count: ", len(self.dwell_time))
        print("Flight times: ", self.flight_time, "Count: ", len(self.flight_time))

    def __repr__(self):
        if not self.dwell_dataframe.empty and not self.flight_dataframe.empty:
            return (f"Flight Dataframe: {self.flight_dataframe.tail(50), self.flight_dataframe.shape[0]}\n"
                    f"Dwell Dataframe: {self.dwell_dataframe.tail(50), self.dwell_dataframe.shape[0]}")
        else:
            return f"Dataframe: {self.flight_dataframe, self.dwell_dataframe}"


def main():
    create_path_if_not_exists('/saved_files')
    keylogger = Keylogger()

    keylog_thread = threading.Thread(target=keylogger.start_keylogger)
    keylog_thread.start()
    try:
        while True:
            cmd = int(input("1. Start Keylogging.\n"
                            "2. Stop Keylogging.\n"
                            "3. Print Times.\n"
                            "4. Print keyboard object. \n"
                            "Enter Command: "))
            if cmd == 1:
                keylog_thread.start()
            elif cmd == 2:
                keylogger.stop_keylogger()
            elif cmd == 3:
                keylogger.print_times()
            elif cmd == 4:
                print(keylogger)
    except KeyboardInterrupt or ValueError:
        keylogger.stop_keylogger()
        keylog_thread.join()


if __name__ == "__main__":
    main()
