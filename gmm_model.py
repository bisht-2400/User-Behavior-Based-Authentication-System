import random
from sklearn.mixture import GaussianMixture
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
import numpy as np
from main import *


class GMM:
    def __init__(self):
        self.dwell_time = []
        self.flight_time = []
        self.flight_dataframe = pd.DataFrame()
        self.dwell_dataframe = pd.DataFrame()


    def load_dataframe(self):
        try:
            print('\nLOADING FRAMES\n')
            self.flight_dataframe = pandas.read_pickle('./saved_files/flight_data.pkl')
            self.dwell_dataframe = pandas.read_pickle('./saved_files/dwell_data.pkl')
            self.dwell_time = self.dwell_dataframe.values.tolist()
            self.flight_time = self.flight_dataframe.values.tolist()
        except FileNotFoundError:
            print('\nEMPTY DF DETECTED\n')
        except Exception as e:
            print(f"An Error has occurred: {e}")


    def split_dataframe(self):
        if len(self.dwell_time) != 0 & len(self.flight_time) != 0:
            flight_train_set, flight_val_set, flight_test_set = split(self.flight_time)
            dwell_train_set, dwell_val_set, dwell_test_set = split(self.dwell_time)

    def train_gmm(self):
        X = np.array([self.dwell_time, self.flight_time])  # Replace with your actual data

        # Standardize the data (important for GMM)
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Define number of folds
        n_folds = 5
        kf = KFold(n_splits=n_folds, shuffle=True, random_state=42)

        # Store metrics
        log_likelihoods = []

        # Cross-validation
        for train_index, val_index in kf.split(X_scaled):
            X_train, X_val = X_scaled[train_index], X_scaled[val_index]

            # Train the GMM
            gmm = GaussianMixture(n_components=1, covariance_type='full', random_state=42)
            gmm.fit(X_train)

            # Evaluate the model
            val_log_probs = gmm.score_samples(X_val)
            log_likelihoods.extend(val_log_probs)
        print(log_likelihoods)


def split(data):
    split_1 = int(0.7 * len(data))
    split_2 = int(0.85 * len(data))
    return data[:split_1], data[split_1:split_2], data[split_2:]


def main():
    gmm = GMM()
    gmm.load_dataframe()
    gmm.train_gmm()


if __name__ == "__main__":
     main()