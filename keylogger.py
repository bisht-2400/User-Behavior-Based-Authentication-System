import time
import pandas
import keyboard


def is_key_event(string) -> bool:
    keywords = ['alt', 'alt gr', 'ctrl', 'left alt', 'left ctrl', 'left shift', 'left windows', 'right alt',
                'right ctrl', 'right shift', 'right windows', 'shift', 'windows', 'enter', 'space', 'tab',
                'insert', 'caps lock', 'esc', 'left', 'right', 'up', 'down', 'backspace', 'print screen']
    if string in keywords:
        return False
    else:
        return True


def update_df(df):
    df.drop(index=df.index[:2500], inplace=True)


class Keylogger:
    def __init__(self, logger):
        self.dwell_time = []
        self.flight_time = []
        self.dwell_start_time = 0
        self.flight_start_time = None
        self.running = True
        self.last_key = "~"
        self.flight_dataframe = pandas.DataFrame()
        self.dwell_dataframe = pandas.DataFrame()
        self.logger = logger

    def get_length(self) -> int:
        if self.flight_dataframe.shape[0] >= self.dwell_dataframe.shape[0]:
            return self.dwell_dataframe.shape[0]
        else:
            return self.flight_dataframe.shape[0]

    def get_cache_len(self) -> int:
        if self.dwell_time >= self.flight_time:
            return len(self.flight_time)
        else:
            return len(self.dwell_time)

    def record_keys(self, event) -> None:
        if event.event_type == keyboard.KEY_DOWN and is_key_event(event.name):
            self.dwell_start_time = event.time
            if self.flight_start_time is not None:
                f_time = event.time - self.flight_start_time
                if 0 < f_time < 1:
                    self.flight_time.append([f_time, ord(event.name), ord(self.last_key)])

        elif event.event_type == keyboard.KEY_UP and is_key_event(event.name):
            self.flight_start_time = event.time
            d_time = event.time - self.dwell_start_time

            if d_time > 0:
                self.dwell_time.append([d_time, ord(event.name), ord(self.last_key)])
            self.last_key = event.name

    def flush_cache(self) -> None:
        self.dwell_time.clear()
        self.flight_time.clear()

    def start_keylogger(self) -> None:
        self.load_dataframe()
        self.running = True
        keyboard.hook(self.record_keys)
        while self.running:
            time.sleep(0.1)

    def stop_keylogger(self) -> None:
        self.running = False
        keyboard.unhook_all()

    def convert_to_df(self) -> None:
        df_dwell = pandas.DataFrame({
            'dwell_times': [entry[0] for entry in self.dwell_time],
            'current_key': [entry[1] for entry in self.dwell_time],
            'last_key': [entry[2] for entry in self.dwell_time]

        })

        df_flight = pandas.DataFrame({
            'flight_times': [entry[0] for entry in self.flight_time],
            'current_key': [entry[1] for entry in self.flight_time],
            'last_key': [entry[2]for entry in self.flight_time]
        })

        if self.flight_dataframe.empty:
            self.flight_dataframe = df_flight
        else:
            self.flight_dataframe = pandas.concat([self.flight_dataframe, df_flight], ignore_index=True)

        if self.dwell_dataframe.empty:
            self.dwell_dataframe = df_dwell
        else:
            self.dwell_dataframe = pandas.concat([self.dwell_dataframe, df_dwell], ignore_index=True)

    def save_dataframe(self) -> None:
        self.convert_to_df()
        if self.get_length() >= 12500:
            update_df(self.dwell_dataframe)
            update_df(self.flight_dataframe)
        self.flight_dataframe.to_excel('./saved_files/flight_data.xlsx', index=False)
        self.dwell_dataframe.to_excel('./saved_files/dwell_data.xlsx', index=False)
        self.flush_cache()
        # self.flight_dataframe.to_pickle('./saved_files/unauthorized_flight_data_2.pkl')
        # self.dwell_dataframe.to_pickle('./saved_files/unauthorized_dwell_data_2.pkl')

    def load_dataframe(self) -> None:
        try:
            self.flight_dataframe = pandas.read_excel('./saved_files/flight_data.xlsx')
            self.dwell_dataframe = pandas.read_excel('./saved_files/dwell_data.xlsx')

            # self.flight_dataframe.to_pickle('./saved_files/unauthorized_flight_data_2.pkl')
            # self.dwell_dataframe.to_pickle('./saved_files/unauthorized_dwell_data_2.pkl')

        except FileNotFoundError:
            pass

    def print_times(self) -> None:
        print("Dwell times: ", self.dwell_time, "Count: ", len(self.dwell_time))
        print("Flight times: ", self.flight_time, "Count: ", len(self.flight_time))

    def __repr__(self) -> str:
        if not self.dwell_dataframe.empty and not self.flight_dataframe.empty:
            return (f"Flight Dataframe: {self.flight_dataframe.tail(50), self.flight_dataframe.shape[0]}\n"
                    f"Dwell Dataframe: {self.dwell_dataframe.tail(50), self.dwell_dataframe.shape[0]}")
        else:
            return f"Dataframe: {self.flight_dataframe, self.dwell_dataframe}"


# def main():
#     logger = Logger()
#     keylogger = Keylogger(logger)
#
#     keylog_thread = threading.Thread(target=keylogger.start_keylogger)
#     keylog_thread.start()
#     try:
#         while True:
#             cmd = int(input("1. Start Keylogging.\n"
#                             "2. Stop Keylogging.\n"
#                             "3. Print Times.\n"
#                             "4. Print keyboard object. \n"
#                             "Enter Command: "))
#             if cmd == 1:
#                 keylog_thread.start()
#             elif cmd == 2:
#                 keylogger.stop_keylogger()
#             elif cmd == 3:
#                 keylogger.print_times()
#             elif cmd == 4:
#                 print(keylogger)
#     except KeyboardInterrupt or ValueError:
#         keylogger.stop_keylogger()
#         keylog_thread.join()
#
#
# if __name__ == '__main__':
#     main()
