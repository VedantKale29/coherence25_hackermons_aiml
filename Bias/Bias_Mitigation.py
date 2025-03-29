import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from aif360.datasets import StandardDataset
from aif360.algorithms.preprocessing import Reweighing
from aif360.metrics import BinaryLabelDatasetMetric
from aif360.algorithms.postprocessing import EqOddsPostprocessing

# Load dataset (Example Data)
data = pd.DataFrame({
    'Age': [25, 40, 30, 50, 45, 23, 29, 55, 35, 42],
    'Gender': ['Male', 'Female', 'Male', 'Female', 'Male', 'Female', 'Male', 'Female', 'Male', 'Female'],
    'Experience': [2, 10, 5, 15, 12, 1, 3, 20, 8, 11],
    'Hired': [1, 0, 1, 0, 1, 0, 1, 0, 1, 0]  # 1: Hired, 0: Not Hired
})

# Convert categorical Gender column to binary
data['Gender'] = data['Gender'].map({'Male': 1, 'Female': 0})

# Define privileged and unprivileged groups
privileged = [{'Gender': 1}]
unprivileged = [{'Gender': 0}]

# Convert to AIF360 dataset
aif_data = StandardDataset(
    data,
    label_name='Hired',
    favorable_classes=[1],
    protected_attribute_names=['Gender', 'Age'],
    privileged_classes=[[1], [30]]
)

# Analyze bias before mitigation
metric = BinaryLabelDatasetMetric(aif_data, unprivileged_groups=unprivileged, privileged_groups=privileged)
print(f"Statistical Parity Difference (Before Mitigation): {metric.statistical_parity_difference()}")
print(f"Disparate Impact (Before Mitigation): {metric.disparate_impact()}")

# Apply Reweighing to mitigate bias
rw = Reweighing(privileged_groups=privileged, unprivileged_groups=unprivileged)
reweighted_data = rw.fit_transform(aif_data)

# Convert back to dataframe
reweighted_df = reweighted_data.convert_to_dataframe()[0]
X = reweighted_df[['Age', 'Gender', 'Experience']]
y = reweighted_df['Hired']

# Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train Logistic Regression model
model = LogisticRegression()
model.fit(X_train_scaled, y_train)

# Evaluate model
preds = model.predict(X_test_scaled)
print("\nModel Accuracy After Bias Mitigation:", accuracy_score(y_test, preds))
print("\nClassification Report:")
print(classification_report(y_test, preds))

# Evaluate fairness after mitigation
aif_pred = aif_data.copy()
aif_pred.labels = preds.reshape(-1, 1)
metric_after = BinaryLabelDatasetMetric(aif_pred, unprivileged_groups=unprivileged, privileged_groups=privileged)
print(f"\nStatistical Parity Difference (After Mitigation): {metric_after.statistical_parity_difference()}")
print(f"Disparate Impact (After Mitigation): {metric_after.disparate_impact()}")
