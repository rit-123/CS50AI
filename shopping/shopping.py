import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    evidence = list()
    labels = list()
    with open(filename, "r") as file:
        # curr_evidence = list()
        # evidence.append(curr_evidence)
        bool  = {"TRUE": 1, "FALSE": 0}
        months = {"Jan": 0, "Feb": 1, "Mar": 2, "Apr": 3, "May": 4, "June": 5, "Jul": 6, "Aug": 7, "Sep": 8, "Oct": 9, "Nov": 10, "Dec": 11}
        visitor_type = {"Returning_Visitor": 1, "New_Visitor": 0, "Other": 0}
        reader = csv.DictReader(file)
        for row in reader:
            # row is a dictionary of each of the fields
            labels.append(bool[row["Revenue"]])
            curr_evidence = list()

            # appending all the evidence
            for field in row:
                if field == "Revenue":
                    continue
                if field == "Administrative" or field == "Informational" or field == "ProductRelated" or field == "OperatingSystems" or field == "Browser" or field == "Region" or field == "TrafficType":
                    curr_evidence.append(int(row[field]))
                    continue
                if field == "Month":
                    curr_evidence.append(months[row[field]])
                    continue
                if field == "Weekend":
                    curr_evidence.append(bool[row[field]])
                    continue
                if field == "VisitorType":
                    curr_evidence.append(visitor_type[row[field]])
                    continue
                if field == "Administrative_Duration" or field == "Informational_Duration" or field == "ProductRelated_Duration" or field == "BounceRates" or field == "ExitRates" or field == "PageValues" or field == "SpecialDay":
                    curr_evidence.append(float(row[field]))
                    continue
            evidence.append(curr_evidence)
    return (evidence, labels)
            

def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence,labels)
    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    correct_positive_counter = 0
    correct_negative_counter = 0
    incorrect_positive_counter = 0
    incorrect_negative_counter = 0
    
    for i in range(len(labels)):
        # positive result
        if labels[i] == 1:
            if labels[i] == predictions[i]:
                correct_positive_counter += 1
            else:
                incorrect_positive_counter += 1
        # negative result
        if labels[i] == 0:
            if labels[i] == predictions[i]:
                correct_negative_counter += 1
            else:
                incorrect_negative_counter += 1
    sensitivity = correct_positive_counter/(correct_positive_counter + incorrect_positive_counter)
    specificity = correct_negative_counter/(correct_negative_counter + incorrect_negative_counter)
    return (sensitivity,specificity)


if __name__ == "__main__":
    main()
