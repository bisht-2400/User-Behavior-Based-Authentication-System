import os
import threading
import time
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from logger import Logger
import train
from keylogger import Keylogger
from predict import predict
from math import exp, log
import smtplib
import json
import pandas as pd


def create_path_if_not_exists(path) -> None:
    if not os.path.exists(path):
        os.makedirs(path)


def read_json() -> dict:
    with open('saved_files/config.json', 'r') as file:
        diction = json.load(file)
    if diction['email'] is not None:
        return diction


def compare_score(train_scores: tuple, predict_scores: tuple) -> tuple:
    train_add = abs(train_scores[0]) + abs(train_scores[1]) + abs(train_scores[2]) + abs(train_scores[3])
    predict_add = abs(predict_scores[0]) + abs(predict_scores[1]) + abs(predict_scores[2]) + abs(predict_scores[3])
    train_score = exp(log(train_add) / 4)
    predict_score = exp(log(predict_add) / 4)
    return train_score, predict_score


def send_email(email) -> str:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    sender_email = "ubasproject2024@gmail.com"
    sender_password = "suxc vvzo npkv faly"
    receiver_email = email
    subject = "UBBAS SYSTEM::Intruder Detected"
    body = f"Unauthorized User Detected at approximate: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        return f"Email sent to {email}"


def main():
    create_path_if_not_exists('saved_files')
    create_path_if_not_exists('models')
    create_path_if_not_exists('logs')

    logger = Logger()
    logger.write_log('Program Started')
    config = read_json()

    # dwell_path = "./saved_files/unauth_dwell_data_2.xlsx"
    # flight_path = "./saved_files/unauth_flight_data_2.xlsx"
    # dwell_df = pd.read_excel(dwell_path).tail(50)
    # flight_df = pd.read_excel(flight_path).tail(50)
    # mean_scores = predict(dwell_df, flight_df)
    # compare_score(mean_scores, (config["DwellOneClassSVM"],
    #                             config["DwellIsolationForest"],
    #                             config["FlightOneClassSVM"],
    #                             config["FlightIsolationForest"]))

    email = config['email']

    keylog = Keylogger(logger)
    keylog_thread = threading.Thread(target=keylog.start_keylogger)
    keylog_thread.start()
    while True:
        cache_len = keylog.get_cache_len()
        if keylog.get_length() >= 5000 and keylog.get_length() % 500 <= 10:
            logger.write_log("Training Models")
            train.train_model(logger)
        elif cache_len % 50 <= 10 and cache_len >= 50:
            if keylog.get_length() < 5000:
                keylog.save_dataframe()
                logger.write_log(f"Cache Added to Database.(Cache Len: {cache_len})")
            elif keylog.get_length() >= 5000:
                mean_scores = predict(pd.DataFrame(keylog.dwell_time, columns=['dwell_times',
                                                                               'current_key', 'last_key']),
                                      pd.DataFrame(keylog.flight_time, columns=['flight_times',
                                                                                'current_key', 'last_key']))
                scores = compare_score(mean_scores, (config["DwellOneClassSVM"],
                                                     config["DwellIsolationForest"],
                                                     config["FlightOneClassSVM"],
                                                     config["FlightIsolationForest"]))
                if scores[0] - scores[1] > 20:  # If pattern matches
                    logger.write_log(f'No Anomaly Detected: {scores[0] - scores[1]} difference in scores')
                    keylog.save_dataframe()  # add to df
                    logger.write_log(f"Cache Added to Database.(Cache Len: {cache_len})")
                else:
                    logger.write_log(f"ANOMALY DETECTED: {scores[0] - scores[1]} difference in scores")
                    keylog.flush_cache()  # flush the list
                    logger.write_log(send_email(email))  # send the email
        else:
            time.sleep(2)


if __name__ == "__main__":
    main()
