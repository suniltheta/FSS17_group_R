import matplotlib.pyplot as plt
from sklearn.feature_selection import RFECV
import pandas as pd
from sklearn.model_selection import StratifiedKFold
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.metrics import accuracy_score
from imblearn.over_sampling import SMOTE
from sklearn.metrics import precision_score, f1_score, recall_score
from sklearn.model_selection import GridSearchCV
from datetime import datetime

# Load dataset in remove name.1 and version
#
# Convert bug to binary classification.
#
def process_dataset(path):
    df = pd.read_csv(path, header=0)
    df = df.drop('version', axis=1)
    df = df.drop('name', axis = 1)
    df = df.drop('name.1', axis=1) # Comment this line for prop data set
    df.bug = df.bug > 0
    return df

# Set below value {}
set_dataset = 6
dataset_path = [
    ["data/camel/camel-1.2.csv", "data/camel/camel-1.4.csv", "data/camel/camel-1.6.csv"],# 0
    ["data/ivy/ivy-1.1.csv", "data/ivy/ivy-1.4.csv", "data/ivy/ivy-2.0.csv"],# 1
    ["data/jedit/jedit-4.1.csv", "data/jedit/jedit-4.2.csv", "data/jedit/jedit-4.3.csv"],# 2
    ["data/log4j/log4j-1.0.csv", "data/log4j/log4j-1.1.csv", "data/log4j/log4j-1.2.csv"],# 3 good
    ["data/lucene/lucene-2.0.csv", "data/lucene/lucene-2.2.csv", "data/lucene/lucene-2.4.csv"],# 4 good
    ["data/poi/poi-1.5.csv", "data/poi/poi-2.0.csv", "data/poi/poi-2.5.csv", "data/poi/poi-3.0.csv"],# 5 great
        ["data/prop/prop-2.csv","data/prop/prop-3.csv", "data/prop/prop-4.csv", "data/prop/prop-5.csv"],# 6
    ["data/synapse/synapse-1.0.csv", "data/synapse/synapse-1.1.csv", "data/synapse/synapse-1.2.csv"],# 7
    ["data/velocity/velocity-1.4.csv", "data/velocity/velocity-1.5.csv", "data/velocity/velocity-1.6.csv"],# 8
    ["data/xalan/xalan-2.4.csv","data/xalan/xalan-2.5.csv", "data/xalan/xalan-2.6.csv"],# 9 good
    ["data/xerces/xerces-1.2.csv", "data/xerces/xerces-1.3.csv", "data/xerces/xerces-1.4.csv"]# 10
]

train_dataset1 = dataset_path[set_dataset][0]
train_dataset2 = dataset_path[set_dataset][1]
test_dataset = dataset_path[set_dataset][2]


# Load dataset
df = process_dataset(train_dataset1)
df.append(process_dataset(train_dataset2))

if (len(dataset_path[set_dataset]) > 3) :
    df.append(process_dataset(test_dataset))
    test_dataset = dataset_path[set_dataset][2]

# Load test dataset
test_df = process_dataset(test_dataset)

# Print dataset
print("* df.head()", df.head())

# Use all features
features = list(df.columns[:20])
print("* features:", features)

#Train decision tree.
dtSmote = DecisionTreeClassifier(random_state=99)

smote = SMOTE(random_state=23)
X, Y = SMOTE(kind="svm").fit_sample(df[features], df["bug"])
dtSmote.fit(X, Y)

test_predict = dtSmote.predict(test_df[features])
print("* Accuracy before feature selection", accuracy_score(test_df["bug"], test_predict))
export_graphviz(dtSmote, out_file='tree-un.dot', feature_names=features, impurity=False, class_names=["Bug", "Not a bug"])
f1_score_ds = f1_score(test_df["bug"], test_predict)

print('* F1 score before feature selection: {0:0.2f}'.format(
    f1_score_ds))
print(' * Precision before feature selection: {0:0.2f}'.format(precision_score(test_df["bug"], test_predict)))
print(' * Recall before feature selection: {0:0.2f}'.format(recall_score(test_df["bug"], test_predict)))

# Feature selection
# Create the RFE object and compute a cross-validated score.
# The "accuracy" scoring is proportional to the number of correct
# classifications. We are using F1 scoring.
timeStart = datetime.now()
rfecv = RFECV(estimator=dtSmote, step=1, cv=StratifiedKFold(n_splits=5),
              scoring='f1')
rfecv.fit(df[features], df["bug"])
print ("\n* Time taken for feature selection : %d" % (datetime.now() - timeStart).seconds)
print("Optimal number of features : %d" % rfecv.n_features_)
print ("* Optimal features ", rfecv.ranking_)
# Plot number of features VS. cross-validation scores
# plt.figure()
# plt.xlabel("Number of features selected")
# plt.ylabel("Cross validation score (nb of correct classifications)")
# plt.plot(range(1, len(rfecv.grid_scores_) + 1), rfecv.grid_scores_)
# plt.show()

selected_feature = []

for i in range(len(features)):
    if rfecv.ranking_[i] == 1:
        selected_feature.append(features[i])

print ("* New selected feature ", selected_feature)

#dt.fit(df[features], df["bug"])
new_data = pd.DataFrame(X, columns=features)

paramgrid = {"max_depth":[3,4], "max_leaf_nodes" : range(4,8,1), "min_samples_split": range(3,25,1), "criterion": ["gini", "entropy"]}

#Cross validation 5 splits
cross_validation = StratifiedKFold(n_splits=5)
timeStart = datetime.now()
grid_search = GridSearchCV(DecisionTreeClassifier(), param_grid = paramgrid,
                          cv = cross_validation, scoring= "f1")

grid_search.fit(df[selected_feature], df["bug"])
print ("\n* Time taken for grid search : %d" % (datetime.now() - timeStart).seconds)
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
test_predict_fs = dtSmote.predict(test_df[selected_feature])
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
timeStart = datetime.now()
rf = RandomForestClassifier(n_jobs=-1, random_state=0)
rfecv = RFECV(estimator=rf, step=1, cv=StratifiedKFold(n_splits=5),
              scoring='f1')
rfecv.fit(df[features], df["bug"])
print ("\n* Time taken for feature selection : %d" % (datetime.now() - timeStart).seconds)

print("Optimal number of features : %d" % rfecv.n_features_)
print ("* Optimal features ", rfecv.ranking_)
# Plot number of features VS. cross-validation scores
# plt.figure()
# plt.xlabel("Number of features selected")
# plt.ylabel("Cross validation score (nb of correct classifications)")
# plt.plot(range(1, len(rfecv.grid_scores_) + 1), rfecv.grid_scores_)
# plt.show()

selected_feature = []

for i in range(len(features)):
    if rfecv.ranking_[i] == 1:
        selected_feature.append(features[i])

print ("* New selected feature ", selected_feature)
new_data = pd.DataFrame(X, columns=features)

#Param tuning
param_grid = {
    "n_estimators"      : range(50, 150, 10),
    "max_features"      : ["auto", "sqrt", "log2"],
    "min_samples_split" : range(2,20,1)
}


#Cross validation 5 splits
cross_validation = StratifiedKFold(n_splits=5)

grid_search = GridSearchCV(RandomForestClassifier(n_jobs=-1), param_grid = param_grid,
                          cv = cross_validation, scoring= "f1")
#Fit
grid_search.fit(df[selected_feature], df["bug"])
print ("\n* Time taken for grid search : %d" % (datetime.now() - timeStart).seconds)
print (grid_search.best_params_)
#Predict
rf = RandomForestClassifier(n_estimators = grid_search.best_params_.get("n_estimators"),
                            max_features = grid_search.best_params_.get("max_features"),
                            min_samples_split= grid_search.best_params_.get("min_samples_split")
                           );

rf.fit(new_data[selected_feature], Y)
test_predict = rf.predict(test_df[selected_feature])
print "Best Score: {}".format(grid_search.best_score_)
print "Best params: {}".format(grid_search.best_params_)

print "\n"
print("* Accuracy: ", accuracy_score(test_df["bug"], test_predict))
print("* F1 Score: ", f1_score(test_df["bug"], test_predict))
print("* Precision: ", precision_score(test_df["bug"], test_predict))
print("* Recall: ", recall_score(test_df["bug"], test_predict))
