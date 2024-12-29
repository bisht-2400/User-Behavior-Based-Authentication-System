import pickle


def predict(x_dwell, x_flight) -> tuple:
    with (open('models/dwell_isolation_forest_model.pkl', 'rb') as di,
          open('models/dwell_svm_model.pkl', 'rb') as ds,
          open('models/flight_isolation_forest_model.pkl', 'rb') as fi,
          open('models/flight_svm_model.pkl', 'rb') as fs):

        dwell_iso_model = pickle.load(di)
        dwell_svm_model = pickle.load(ds)
        flight_iso_model = pickle.load(fi)
        flight_svm_model = pickle.load(fs)
        dwell_svm_scores = dwell_svm_model.decision_function(x_dwell)
        dwell_iso_scores = dwell_iso_model.score_samples(x_dwell)
        dwell_svm_mean_score = dwell_svm_scores.mean()
        dwell_iso_mean_score = dwell_iso_scores.mean()

        flight_svm_scores = flight_svm_model.decision_function(x_flight)
        flight_iso_scores = flight_iso_model.score_samples(x_flight)

        flight_svm_mean_score = flight_svm_scores.mean()
        flight_iso_mean_score = flight_iso_scores.mean()

        predict_score = dwell_svm_mean_score, dwell_iso_mean_score, flight_svm_mean_score, flight_iso_mean_score
        return predict_score


# def main():
#     dwell_path = "./saved_files/unauth_dwell_data_2.xlsx"
#     flight_path = "./saved_files/unauth_flight_data_2.xlsx"
#
#     dwell_df = pd.read_excel(dwell_path).tail(100)
#     flight_df = pd.read_excel(flight_path).tail(100)
#
#     dwell_df['dwell_times'] = dwell_df['dwell_times']*100
#     flight_df['flight_times'] = flight_df['flight_times']*100
#
#     X_dwell = dwell_df[['dwell_times', 'current_key', 'last_key']]
#
#     with open("models/dwell_svm_model.pkl", 'rb') as f:
#         dwell_svm_model = pickle.load(f)
#
#     with open("models/dwell_isolation_forest_model.pkl", 'rb') as f:
#         dwell_iso_forest = pickle.load(f)
#
#     dwell_svm_scores = dwell_svm_model.decision_function(X_dwell)
#     dwell_iso_scores = dwell_iso_forest.score_samples(X_dwell)
#
#     dwell_svm_mean_score = dwell_svm_scores.mean()
#     dwell_iso_mean_score = dwell_iso_scores.mean()
#
#     print("Dwell SVM Mean Score:", dwell_svm_mean_score)
#     print("Dwell Isolation Forest Mean Score:", dwell_iso_mean_score)
#
#     X_flight = flight_df[['flight_times', 'current_key', 'last_key']]
#
#     # Load flight models
#     with open("models/flight_svm_model.pkl", 'rb') as f:
#         flight_svm_model = pickle.load(f)
#
#     with open("models/flight_isolation_forest_model.pkl", 'rb') as f:
#         flight_iso_forest = pickle.load(f)
#
#     flight_svm_scores = flight_svm_model.decision_function(X_flight)
#     flight_iso_scores = flight_iso_forest.score_samples(X_flight)
#
#     flight_svm_mean_score = flight_svm_scores.mean()
#     flight_iso_mean_score = flight_iso_scores.mean()
#
#     print("\nFlight SVM Mean Score:", flight_svm_mean_score)
#     print("Flight Isolation Forest Mean Score:", flight_iso_mean_score)
#
#
# if __name__ == "__main__":
#     main()
