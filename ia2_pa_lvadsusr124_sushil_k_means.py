# -*- coding: utf-8 -*-
"""IA2-PA-LVADSUSR124-SUSHIL-k-means

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1j7oeMCD1pIc9xlDIRuDmtiGEcAiERwh9
"""

import pandas as pd
import warnings as wr
wr.filterwarnings('ignore')
data= pd.read_csv("https://raw.githubusercontent.com/Deepsphere-AI/LVA-Batch4-Assessment/main/Mall_Customers.csv")
data.head()

# # Handle missing values and outliers
nulls = data.isnull().sum()
print(nulls)

from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.impute import SimpleImputer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt

scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(data.iloc[:, 2:])


imputer = SimpleImputer(strategy='mean')
imputed_data = imputer.fit_transform(scaled_data)

# # imputed_data
# data.dropna(inplace=True)

#a Data exploration and preprocessing



# Feature engineering - calculate the ratio of spending to income
data['SpendingtoIncomeRatio'] = data['Spending Score (1-100)'] / data['Annual Income (k$)']
data

#b Determining the optimal number of clusters using elbow method
sse = []
k_rng=(1,11)

for i in k_rng:
    kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42)
    kmeans.fit(imputed_data)
    sse.append(kmeans.inertia_)

plt.plot(k_rng,sse)
plt.title('Elbow Method')
plt.xlabel('Number of Clusters(K)')
plt.ylabel('Sum of squared error()')
plt.show()

#bUsing silhouette score for validation
silhouette_scores = []
for i in range(2, 11):
    kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42)
    kmeans.fit(imputed_data)
    silhouette_scores.append(silhouette_score(imputed_data, kmeans.labels_))

plt.plot(range(2, 11), silhouette_scores)
plt.title('Silhouette Score')
plt.xlabel('Number of Clusters')
plt.ylabel('Silhouette Score')
plt.show()

#c Applying K-Means clustering algorithm
k = 5
kmeans = KMeans(n_clusters=k, init='k-means++', random_state=42)
data['Cluster'] = kmeans.fit_predict(imputed_data)
data

#d Cluster center
cluster_centers = kmeans.cluster_centers_
cluster_centers_df = pd.DataFrame(cluster_centers,columns=data.columns[4:])
print("Cluster Centers:")
print(cluster_centers_df)

# Cluster analysis - cluster profiling
cluster_profiles = data.groupby('Cluster').mean()
print(cluster_profiles)

# Visualizing clusters
plt.scatter(data['Annual Income (k$)'], data['Spending Score (1-100)'], c=data['Cluster'], cmap='viridis', alpha=0.5)
plt.scatter(cluster_profiles['Annual Income (k$)'], cluster_profiles['Spending Score (1-100)'], marker='x', c='red', s=200, label='Cluster Center')
plt.title('Customer Segmentation')
plt.xlabel('Annual Income (k$)')
plt.ylabel('Spending Score (1-100)')
plt.legend()
plt.show()

