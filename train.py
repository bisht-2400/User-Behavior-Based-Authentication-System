import json
import pickle
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import OneClassSVM
from sklearn.ensemble import IsolationForest
from enum import Enum

np.set_printoptions(legacy='1.25')
NU = 0.005
CONTAMINATION = 0.001


class ModelType(Enum):
    DWELL = 1
    FLIGHT = 2


class BaseModel:
    def __init__(self):
        self.model = None
        self.train_score = None

    def train(self, X_train):
        raise NotImplementedError("Subclasses must implement this method.")

    def evaluate(self, X_train, X_val, X_test) -> dict:
        train_scores = self._score_samples(X_train)
        val_scores = self._score_samples(X_val)
        test_scores = self._score_samples(X_test)

        train_mean_score = np.mean(train_scores)
        val_mean_score = np.mean(val_scores)
        test_mean_score = np.mean(test_scores)
        mean = (train_mean_score + val_mean_score + test_mean_score) / 3

        self.train_score = mean

        return {
            'Train Mean score': train_mean_score,
            'Val Mean score': val_mean_score,
            'Test Mean score': test_mean_score,
            'mean': mean
        }

    def save_model(self, file_path) -> None:
        with open(file_path, 'wb') as file:
            pickle.dump(self.model, file)

    def _update_config_file(self, model_type_name):
        with open('saved_files/config.json', 'r') as f:
            diction = json.load(f)

        diction[f'{model_type_name.title()}{self.model.__class__.__name__}'] = self.train_score

        with open('saved_files/config.json', 'w') as file:
            json.dump(diction, file, indent=4)

    def _score_samples(self, X):
        raise NotImplementedError("Subclasses must implement this method.")


class SVMmodel(BaseModel):
    def __init__(self, model_type: ModelType, nu=NU):
        super().__init__()
        self.nu = nu
        self.model_type = model_type

    def train(self, X_train) -> None:
        self.model = OneClassSVM(kernel='rbf', gamma='scale', nu=self.nu)
        self.model.fit(X_train)

    def save_model(self, file_path) -> None:
        super().save_model(file_path)
        self._update_config_file(self.model_type.name)

    def _score_samples(self, X):
        return self.model.decision_function(X)


class ISOmodel(BaseModel):
    def __init__(self, model_type: ModelType, contamination=CONTAMINATION):
        super().__init__()
        self.contamination = contamination
        self.model_type=model_type

    def train(self, X_train) -> None:
        self.model = IsolationForest(contamination=self.contamination, random_state=42)
        self.model.fit(X_train)

    def _score_samples(self, X) -> list:
        return self.model.score_samples(X)

    def save_model(self, file_path) -> None:
        super().save_model(file_path)
        self._update_config_file(self.model_type.name)


def train_model(logger) -> None:
    dwell_path = "saved_files/dwell_data.xlsx"
    flight_path = "saved_files/flight_data.xlsx"

    dwell_df = pd.read_excel(dwell_path).reset_index(drop=True).dropna()
    flight_df = pd.read_excel(flight_path).reset_index(drop=True).dropna()

    dwell_X = dwell_df[['dwell_times', 'current_key', 'last_key']]
    dwell_train, dwell_temp = train_test_split(dwell_X, test_size=0.4, random_state=42)
    dwell_val, dwell_test = train_test_split(dwell_temp, test_size=0.5, random_state=42)

    flight_X = flight_df[['flight_times', 'current_key', 'last_key']]
    flight_train, flight_temp = train_test_split(flight_X, test_size=0.4, random_state=42)
    flight_val, flight_test = train_test_split(flight_temp, test_size=0.5, random_state=42)

    dwell_svm = SVMmodel(model_type=ModelType.DWELL)
    dwell_svm.train(dwell_train)
    logger.write_log('Database Size: ' + str([len(dwell_df) if len(dwell_df) < len(flight_df) else len(flight_df)][0]))
    dwell_svm_results = dwell_svm.evaluate(dwell_train, dwell_val, dwell_test)
    logger.write_log(f"Dwell SVM Model Mean Scores:\n {dwell_svm_results}")
    dwell_svm.save_model('models/dwell_svm_model.pkl')

    dwell_iso = ISOmodel(model_type=ModelType.DWELL)
    dwell_iso.train(dwell_train)
    dwell_iso_results = dwell_iso.evaluate(dwell_train, dwell_val, dwell_test)
    logger.write_log(f"Dwell Isolation Forest Model Mean Scores:\n {dwell_iso_results}")
    dwell_iso.save_model('models/dwell_isolation_forest_model.pkl')

    flight_svm = SVMmodel(model_type=ModelType.FLIGHT)
    flight_svm.train(flight_train)
    flight_svm_results = flight_svm.evaluate(flight_train, flight_val, flight_test)
    logger.write_log(f"Flight SVM Model Mean Scores:\n {flight_svm_results}")
    flight_svm.save_model('models/flight_svm_model.pkl')

    flight_iso = ISOmodel(model_type=ModelType.FLIGHT)
    flight_iso.train(flight_train)
    flight_iso_results = flight_iso.evaluate(flight_train, flight_val, flight_test)
    logger.write_log(f"Flight Isolation Forest Model Mean Scores:\n {flight_iso_results}")
    flight_iso.save_model('models/flight_isolation_forest_model.pkl')

# def main():
#     dwell_path = "saved_files/dwell_data.xlsx"
#     flight_path = "saved_files/flight_data.xlsx"
#
#     dwell_df = pd.read_excel(dwell_path).reset_index(drop=True).dropna()
#     flight_df = pd.read_excel(flight_path).reset_index(drop=True).dropna()
#
#     # dwell_df.drop(dwell_df.columns[0], inplace=True, axis=1)
#     # flight_df.drop(flight_df.columns[0], inplace=True, axis=1)
#     dwell_X = dwell_df[['dwell_times', 'current_key', 'last_key']]
#     dwell_train, dwell_temp = train_test_split(dwell_X, test_size=0.4, random_state=42)
#     dwell_val, dwell_test = train_test_split(dwell_temp, test_size=0.5, random_state=42)
#
#     flight_X = flight_df[['flight_times', 'current_key', 'last_key']]
#     flight_train, flight_temp = train_test_split(flight_X, test_size=0.4, random_state=42)
#     flight_val, flight_test = train_test_split(flight_temp, test_size=0.5, random_state=42)
#
#     dwell_df['dwell_times'] = dwell_df['dwell_times'] * 100
#     flight_df['flight_times'] = flight_df['flight_times'] * 100
#
#     X = dwell_df[['dwell_times', 'current_key', 'last_key']]
#
#     dwell_svm_model = OneClassSVM(kernel='rbf', gamma='scale', nu=NU)
#     dwell_svm_model.fit(dwell_train)
#     dwell_svm_results = evaluate_model(dwell_svm_model, dwell_train, dwell_val, dwell_test, model_type="svm")
#     print("Dwell SVM Model Mean Scores:", dwell_svm_results)
#
#     with open('models/dwell_svm_model.pkl', 'wb') as file:
#         pickle.dump(dwell_svm_model, file)
#
#     dwell_iso_forest = IsolationForest(contamination=CONTAMINATION, random_state=42)
#     dwell_iso_forest.fit(dwell_train)
#
#     dwell_iso_results = evaluate_model(dwell_iso_forest, dwell_train, dwell_val, dwell_test,
#                                        model_type="isolation_forest")
#     print("Dwell Isolation Forest Model Mean Scores:", dwell_iso_results)
#
#     with open('models/dwell_isolation_forest_model.pkl', 'wb') as file:
#         pickle.dump(dwell_iso_forest, file)
#
#     flight_svm_model = OneClassSVM(kernel='rbf', gamma='scale', nu=NU)
#     flight_svm_model.fit(flight_train)
#
#     flight_svm_results = evaluate_model(flight_svm_model, flight_train, flight_val, flight_test, model_type="svm")
#     print("Flight SVM Model Mean Scores:", flight_svm_results)
#
#     with open('models/flight_svm_model.pkl', 'wb') as file:
#         pickle.dump(flight_svm_model, file)
#
#     flight_iso_forest = IsolationForest(contamination=CONTAMINATION, random_state=42)
#     flight_iso_forest.fit(flight_train)
#
#     flight_iso_results = evaluate_model(flight_iso_forest, flight_train, flight_val, flight_test,
#                                         model_type="isolation_forest")
#     print("Flight Isolation Forest Model Mean Scores:", flight_iso_results)
#
#     with open('models/flight_isolation_forest_model.pkl', 'wb') as file:
#         pickle.dump(flight_iso_forest, file)
#
# if __name__ == "__main__":
#     main()
