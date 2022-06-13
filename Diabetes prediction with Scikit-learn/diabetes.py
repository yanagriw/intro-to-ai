import pandas
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn import tree

column_names = ['pregnant', 'glucose', 'bp', 'skin', 'insulin', 'bmi', 'pedigree', 'age', 'label']
feature_columns = ['pregnant', 'glucose', 'bp', 'skin', 'insulin', 'bmi', 'pedigree', 'age']
df = pandas.read_csv("diabetes.csv")
df.columns = column_names

X = df[feature_columns]
y = df.label

X_train, X_test, y_train, y_test = train_test_split(X, y)

dec_tree = DecisionTreeClassifier(criterion = 'entropy', max_depth=5, min_samples_split=100, min_samples_leaf=50, max_leaf_nodes=8)
dec_tree= dec_tree.fit(X_train, y_train)

y_pred = dec_tree.predict(X_test)

print("Accuracy:", metrics.accuracy_score(y_test, y_pred))
print("Precision:", metrics.precision_score(y_test, y_pred))
print("Recall:", metrics.recall_score(y_test, y_pred))

tree.plot_tree(dec_tree, feature_names=feature_columns, filled=True)
plt.show()
