import pickle
import pandas as pd


def main():
    dwell_path = "./saved_files/unauth_dwell_user_1.xlsx"
    flight_path = "./saved_files/unauth_flight_user_1.xlsx"

    dwell_df = pd.read_excel(dwell_path).tail(100)
    flight_df = pd.read_excel(flight_path).tail(100)

    dwell_df['dwell_times'] = dwell_df['dwell_times']*100
    flight_df['flight_times'] = flight_df['flight_times']*100

    X_dwell = dwell_df[['dwell_times', 'current_key', 'last_key']]

    with open("models/dwell_svm_model.pkl", 'rb') as f:
        dwell_svm_model = pickle.load(f)

    with open("models/dwell_isolation_forest_model.pkl", 'rb') as f:
        dwell_iso_forest = pickle.load(f)

    dwell_svm_scores = dwell_svm_model.decision_function(X_dwell)
    dwell_iso_scores = dwell_iso_forest.score_samples(X_dwell)

    dwell_svm_mean_score = dwell_svm_scores.mean()
    dwell_iso_mean_score = dwell_iso_scores.mean()

    print("Dwell SVM Mean Score:", dwell_svm_mean_score)
    print("Dwell Isolation Forest Mean Score:", dwell_iso_mean_score)

    X_flight = flight_df[['flight_times', 'current_key', 'last_key']]

    # Load flight models
    with open("models/flight_svm_model.pkl", 'rb') as f:
        flight_svm_model = pickle.load(f)

    with open("models/flight_isolation_forest_model.pkl", 'rb') as f:
        flight_iso_forest = pickle.load(f)

    flight_svm_scores = flight_svm_model.decision_function(X_flight)
    flight_iso_scores = flight_iso_forest.score_samples(X_flight)

    flight_svm_mean_score = flight_svm_scores.mean()
    flight_iso_mean_score = flight_iso_scores.mean()

    print("\nFlight SVM Mean Score:", flight_svm_mean_score)
    print("Flight Isolation Forest Mean Score:", flight_iso_mean_score)
    # with open("models/dwell_svm_model.pkl", 'rb') as f:
    #     dwell_svm_model = pickle.load(f)
    #
    # with open("models/dwell_isolation_forest_model.pkl", 'rb') as f:
    #     dwell_iso_forest = pickle.load(f)
    #
    # dwell_df['svm_prediction'] = dwell_svm_model.predict(X)
    # print(dwell_df['svm_prediction'])
    # dwell_df['svm_prediction'] = dwell_df['svm_prediction'].apply(lambda x: 'authorized' if x == 1 else 'unauthorized')
    #
    # dwell_df['iso_forest_prediction'] = dwell_iso_forest.predict(X)
    # dwell_df['iso_forest_prediction'] = dwell_df['iso_forest_prediction'].apply(
    #     lambda x: 'authorized' if x == 1 else 'unauthorized')
    #
    # svm_counts = dwell_df['svm_prediction'].value_counts()
    # print("SVM counts:")
    # print(svm_counts)
    # iso_forest_counts = dwell_df['iso_forest_prediction'].value_counts()
    # print("\nIsolation Forest counts:")
    # print(iso_forest_counts)
    #
    # X = flight_df[['flight_times', 'current_key', 'last_key']]
    #
    # with open("models/flight_svm_model.pkl", 'rb') as f:
    #     flight_svm_model = pickle.load(f)
    #
    # with open("models/flight_isolation_forest_model.pkl", 'rb') as f:
    #     flight_iso_forest = pickle.load(f)
    #
    # flight_df['svm_prediction'] = flight_svm_model.predict(X)
    # flight_df['svm_prediction'] = flight_df['svm_prediction'].apply(lambda x: 'authorized' if x == 1 else 'unauthorized')
    #
    # flight_df['iso_forest_prediction'] = flight_iso_forest.predict(X)
    # flight_df['iso_forest_prediction'] = flight_df['iso_forest_prediction'].apply(
    #     lambda x: 'authorized' if x == 1 else 'unauthorized')
    #
    # svm_counts = flight_df['svm_prediction'].value_counts()
    # print("\n----------\nSVM counts:")
    # print(svm_counts)
    # iso_forest_counts = flight_df['iso_forest_prediction'].value_counts()
    # print("\nIsolation Forest counts:")
    # print(iso_forest_counts)


if __name__ == "__main__":
    main()
