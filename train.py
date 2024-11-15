import pickle
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import OneClassSVM
from sklearn.ensemble import IsolationForest

np.set_printoptions(legacy='1.25')
NU = 0.005
CONTAMINATION = 0.001


def evaluate_model(model, X_train, X_val, X_test, model_type="svm"):
    if model_type == "svm":
        # Get anomaly scores: positive values mean inliers, negative means outliers
        train_scores = model.decision_function(X_train)
        val_scores = model.decision_function(X_val)
        test_scores = model.decision_function(X_test)
    elif model_type == "isolation_forest":
        # Isolation Forest provides scores directly; higher means more likely an inlier
        train_scores = model.score_samples(X_train)
        val_scores = model.score_samples(X_val)
        test_scores = model.score_samples(X_test)

    # Calculate mean scores
    train_mean_score = np.mean(train_scores)
    val_mean_score = np.mean(val_scores)
    test_mean_score = np.mean(test_scores)

    return {
        'train_mean_score': train_mean_score,
        'val_mean_score': val_mean_score,
        'test_mean_score': test_mean_score
    }


def main():
    dwell_path = "saved_files/dwell_data.xlsx"
    flight_path = "saved_files/flight_data.xlsx"

    dwell_df = pd.read_excel(dwell_path).reset_index(drop=True).dropna()
    flight_df = pd.read_excel(flight_path).reset_index(drop=True).dropna()

    # dwell_df.drop(dwell_df.columns[0], inplace=True, axis=1)
    # flight_df.drop(flight_df.columns[0], inplace=True, axis=1)
    dwell_X = dwell_df[['dwell_times', 'current_key', 'last_key']]
    dwell_train, dwell_temp = train_test_split(dwell_X, test_size=0.4, random_state=42)
    dwell_val, dwell_test = train_test_split(dwell_temp, test_size=0.5, random_state=42)

    flight_X = flight_df[['flight_times', 'current_key', 'last_key']]
    flight_train, flight_temp = train_test_split(flight_X, test_size=0.4, random_state=42)
    flight_val, flight_test = train_test_split(flight_temp, test_size=0.5, random_state=42)

    dwell_df['dwell_times'] = dwell_df['dwell_times'] * 100
    flight_df['flight_times'] = flight_df['flight_times'] * 100

    X = dwell_df[['dwell_times', 'current_key', 'last_key']]

    dwell_svm_model = OneClassSVM(kernel='rbf', gamma='scale', nu=NU)
    dwell_svm_model.fit(dwell_train)
    dwell_svm_results = evaluate_model(dwell_svm_model, dwell_train, dwell_val, dwell_test, model_type="svm")
    print("Dwell SVM Model Mean Scores:", dwell_svm_results)

    with open('models/dwell_svm_model.pkl', 'wb') as file:
        pickle.dump(dwell_svm_model, file)

    dwell_iso_forest = IsolationForest(contamination=CONTAMINATION, random_state=42)
    dwell_iso_forest.fit(dwell_train)

    dwell_iso_results = evaluate_model(dwell_iso_forest, dwell_train, dwell_val, dwell_test,
                                       model_type="isolation_forest")
    print("Dwell Isolation Forest Model Mean Scores:", dwell_iso_results)

    with open('models/dwell_isolation_forest_model.pkl', 'wb') as file:
        pickle.dump(dwell_iso_forest, file)

    flight_svm_model = OneClassSVM(kernel='rbf', gamma='scale', nu=NU)
    flight_svm_model.fit(flight_train)

    flight_svm_results = evaluate_model(flight_svm_model, flight_train, flight_val, flight_test, model_type="svm")
    print("Flight SVM Model Mean Scores:", flight_svm_results)

    with open('models/flight_svm_model.pkl', 'wb') as file:
        pickle.dump(flight_svm_model, file)

    flight_iso_forest = IsolationForest(contamination=CONTAMINATION, random_state=42)
    flight_iso_forest.fit(flight_train)

    flight_iso_results = evaluate_model(flight_iso_forest, flight_train, flight_val, flight_test,
                                        model_type="isolation_forest")
    print("Flight Isolation Forest Model Mean Scores:", flight_iso_results)

    with open('models/flight_isolation_forest_model.pkl', 'wb') as file:
        pickle.dump(flight_iso_forest, file)


if __name__ == "__main__":
    main()
