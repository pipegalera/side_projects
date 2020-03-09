"""
@author: Pipe Galera

When the Titanic sank, 1502 of the 2224 passengers and crew were killed.
One of the main reasons for this high level of casualties was the lack of
lifeboats on this self-proclaimed "unsinkable" ship.

Those that have seen the movie know that some individuals were more likely to
survive the sinking (lucky Rose) than others (poor Jack).
"""

# Import modules
%reset
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
from sklearn import tree, svm
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split, GridSearchCV
import os


# Figures inline and set visualization style
%matplotlib inline
sns.set()

# Load data
os.chdir("C:/Users/fgm.si/Documents/GitHub/side_projects/titanic")
features = pd.read_csv('out_data/data_eng.csv')
submission = pd.read_csv('out_data/submission.csv')
label_data = pd.read_csv('raw_data/train.csv')
unlabel_data = pd.read_csv('raw_data/test.csv')

# Identifying data
X_train = features[418:]
y_train = label_data.Survived
X_test = features[:418]

#################################
# First baseline: none survived #
#################################
submission["Survived"] = 0
submission.shape

submission.to_csv('C:/Users/fgm.si/Documents/GitHub/side_projects/titanic/predictions/no_survivors.csv', index = False)

###################################
# Second baseline: women survived #
###################################
number_women_survived = label_data[label_data.Sex == "female"].Survived.sum()
number_women = label_data[label_data.Sex == "female"].PassengerId.count()
number_women_survived / number_women

number_men_survived = label_data[label_data.Sex == "male"].Survived.sum()
number_men = label_data[label_data.Sex == "male"].PassengerId.count()
number_men_survived / number_men

submission['Survived'] = X_test.Sex # The first 891 rows are unlabel data
submission.shape

submission.to_csv('C:/Users/fgm.si/Documents/GitHub/side_projects/titanic/predictions/women_survived.csv', index = False)

##########################
# DecisionTreeClassifier #
##########################

X = X_train.values
y = y_train.values

DecisionTreeClassifier = tree.DecisionTreeClassifier(max_depth = 3)
DecisionTreeClassifier.fit(X, y)
y_pred = DecisionTreeClassifier.predict(X_test)


submission["Survived"] = y_pred
submission.to_csv('C:/Users/fgm.si/Documents/GitHub/side_projects/titanic/predictions/DecisionTreeClassifier.csv', index=False)
# 77,9

###########################
# Visualizing overfitting #
###########################

# Selecting hyperparameter to avoid overfitting
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.33)

dep = np.arange(1,9)
train_accuracy = np.empty(len(dep))
test_accuracy = np.empty(len(dep))
dep

for i,k in enumerate(dep):
    clf = tree.DecisionTreeClassifier(max_depth=k)
    clf.fit(X_train, y_train)
    train_accuracy[i] = clf.score(X_train, y_train)
    test_accuracy[i] = clf.score(X_test, y_test)

plt.title('clf: Varying depth of tree')
plt.plot(dep, train_accuracy, label = 'Training Accuracy')
plt.plot(dep, test_accuracy, label = 'Testing Accuracy')
plt.legend()
plt.xlabel('Depth of tree')
plt.ylabel('Accuracy')
plt.show()

# Split again
X_train = features[418:]
y_train = label_data.Survived
X_test = features[:418]

##############################
# DecisionTreeClassifier 2.0 #
##############################

# Tree
X = X_train.values
y = y_train.values

# Using GridSearch to select the best dept of the tree
dep = np.arange(1,9)
param_grid = {'max_depth' : dep}

DecisionTreeClassifier = tree.DecisionTreeClassifier()
DecisionTreeClassifier_cv = GridSearchCV(DecisionTreeClassifier, param_grid= param_grid)
DecisionTreeClassifier_cv.fit(X, y)

print("Best cccuracy " + str(DecisionTreeClassifier_cv.best_score_) + " reached with " + str(DecisionTreeClassifier_cv.best_params_) )

y_pred = DecisionTreeClassifier_cv.predict(X_test)

submission["Survived"] = y_pred
submission.to_csv('C:/Users/fgm.si/Documents/GitHub/side_projects/titanic/predictions/DecisionTreeClassifier_cv.csv', index=False)
# 83,3