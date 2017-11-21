import matplotlib.pyplot as plt
from sklearn.feature_selection import RFECV
import pandas as pd
from sklearn.model_selection import StratifiedKFold
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.metrics import accuracy_score
from imblearn.over_sampling import SMOTE
from sklearn.metrics import precision_score, f1_score, recall_score
from sklearn.model_selection import GridSearchCV

# Load dataset in remove name.1 and version
#
# Convert bug to binary classification.
#
def process_dataset(path):
    df = pd.read_csv(path, header=0)
    df = df.drop('version', axis=1)
    df = df.drop('name', axis = 1)
    df = df.drop('name.1', axis=1)
    df.bug = df.bug > 0
    return df

# Load dataset
df = process_dataset("data/velocity-1.4.csv")
df.append(process_dataset("data/velocity-1.5.csv"))

# Load test dataset
test_df = process_dataset("data/velocity-1.6.csv")

# Print dataset
print("* df.head()", df.head())

# Use all features
features = list(df.columns[:20])
print("* features:", features)

#Train decision tree.
dtSmote = DecisionTreeClassifier(min_samples_split=20, random_state=99)

smote = SMOTE(random_state=23)
X, Y = SMOTE(kind="svm").fit_sample(df[features], df["bug"])
dtSmote.fit(X, Y)

test_predict = dtSmote.predict(test_df[features])
print("* Accuracy before feature selection", accuracy_score(test_df["bug"], test_predict))
export_graphviz(dtSmote, out_file='tree-un.dot', feature_names=features, impurity=False, class_names=["Bug", "Not a bug"])
f1_score_ds = f1_score(test_df["bug"], test_predict)

print('* F1 score before feature selection: {0:0.2f}'.format(
    f1_score_ds))

# Feature selection
# Create the RFE object and compute a cross-validated score.
# The "accuracy" scoring is proportional to the number of correct
# classifications. We are using F1 scoring.
rfecv = RFECV(estimator=dtSmote, step=1, cv=StratifiedKFold(10),
              scoring='f1')
rfecv.fit(X, Y)

print("Optimal number of features : %d" % rfecv.n_features_)
print ("* Optimal features ", rfecv.ranking_)
# Plot number of features VS. cross-validation scores
plt.figure()
plt.xlabel("Number of features selected")
plt.ylabel("Cross validation score (nb of correct classifications)")
plt.plot(range(1, len(rfecv.grid_scores_) + 1), rfecv.grid_scores_)
plt.show()

selected_feature = []

for i in range(len(features)):
    if rfecv.ranking_[i] == 1:
        selected_feature.append(features[i])

print ("* New selected feature ", selected_feature)

#dt.fit(df[features], df["bug"])
new_data = pd.DataFrame(X, columns=features)

paramgrid = {"max_depth":[3,4], "max_leaf_nodes" : range(4,8,1), "min_samples_split": range(3,25,1), "criterion": ["gini", "entropy"]}

#Cross validation 10 splits
cross_validation = StratifiedKFold(10)

grid_search = GridSearchCV(DecisionTreeClassifier(), param_grid = paramgrid,
                          cv = cross_validation, scoring= "f1")

grid_search.fit(new_data[selected_feature], Y)

print "Best Score: {}".format(grid_search.best_score_)
print "Best params: {}".format(grid_search.best_params_)

print "\nTraining new model with tuned params \n"
#Use new params found by grid search
dtSmote = DecisionTreeClassifier(min_samples_split= grid_search.best_params_.get("min_samples_split"),
                                 max_leaf_nodes= grid_search.best_params_.get("max_leaf_nodes"),
                                 criterion=grid_search.best_params_.get("criterion"),
                                 max_depth=grid_search.best_params_.get("max_depth"))

dtSmote.fit(new_data[selected_feature], Y)

# Predict
test_predict_fs = grid_search.predict(test_df[selected_feature])
print("* Accuracy with feature selection & param tuning", accuracy_score(test_df["bug"], test_predict_fs))

f1_score_ds_fs = f1_score(test_df["bug"], test_predict_fs)

print(' * F1 score: {0:0.2f}'.format(f1_score_ds_fs))
print(' * Precision: {0:0.2f}'.format(precision_score(test_df["bug"], test_predict_fs)))
print(' * Recall: {0:0.2f}'.format(recall_score(test_df["bug"], test_predict_fs)))



# Plot the dot file which can be used to visualize the dataset.
export_graphviz(dtSmote, out_file='tree.dot', feature_names=selected_feature, impurity=False, class_names=["Bug", "Not a bug"])

# Start of Random Forest
print "\n\n Random Forest \n"
from sklearn.ensemble import RandomForestClassifier

rf = RandomForestClassifier(n_jobs=2, random_state=0)
rf.fit(X, Y)

test_predict = rf.predict(test_df[features])

print("* Accuracy before feature selection", accuracy_score(test_df["bug"], test_predict))
print("* F1 Score before feature selection", f1_score(test_df["bug"], test_predict))
print("* Precision before feature selection", precision_score(test_df["bug"], test_predict))
print("* Recall before feature selection", recall_score(test_df["bug"], test_predict))

print ("\nFeature Selection\n")
rf = RandomForestClassifier(n_jobs=2, random_state=0)
rfecv = RFECV(estimator=rf, step=1, cv=StratifiedKFold(10),
              scoring='f1')
rfecv.fit(X, Y)

print("Optimal number of features : %d" % rfecv.n_features_)
print ("* Optimal features ", rfecv.ranking_)
# Plot number of features VS. cross-validation scores
plt.figure()
plt.xlabel("Number of features selected")
plt.ylabel("Cross validation score (nb of correct classifications)")
plt.plot(range(1, len(rfecv.grid_scores_) + 1), rfecv.grid_scores_)
plt.show()

selected_feature = []

for i in range(len(features)):
    if rfecv.ranking_[i] == 1:
        selected_feature.append(features[i])

print ("* New selected feature ", selected_feature)
new_data = pd.DataFrame(X, columns=features)

#Param tuning
param_grid = {
    "n_estimators"      : [10,20,30, 100, 200],
    "max_features"      : ["auto", "sqrt", "log2"],
    "min_samples_split" : [2,4,8],
    "bootstrap": [True, False],
}

#Cross validation 10 splits
cross_validation = StratifiedKFold(10)

grid_search = GridSearchCV(RandomForestClassifier(), param_grid = param_grid,
                          cv = cross_validation, scoring= "f1")
#Fit
grid_search.fit(new_data[selected_feature], Y)

#Predict
test_predict = grid_search.predict(test_df[selected_feature])
print "Best Score: {}".format(grid_search.best_score_)
print "Best params: {}".format(grid_search.best_params_)

print "\n"
print("* Accuracy: ", accuracy_score(test_df["bug"], test_predict))
print("* F1 Score: ", f1_score(test_df["bug"], test_predict))
print("* Precision: ", precision_score(test_df["bug"], test_predict))
print("* Recall: ", recall_score(test_df["bug"], test_predict))

