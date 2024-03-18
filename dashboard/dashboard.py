import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
def load_data():
    return pd.read_csv('cleaned_data.csv')

# Load rfm_data
def load_rfm_data():
    return pd.read_csv('rfm_data.csv')

data = load_data()
rfm_data = load_rfm_data()

# Merge data
merged_data = pd.merge(data, rfm_data, on='customer_unique_id')

# Sidebar
analysis_choice = st.sidebar.selectbox('Select Analysis', ['Top 10 Customer States', 'Top 10 Product Categories', 'Frequency Distribution', 'Monetary Distribution', 'Customer Segmentation'], index=0)

# Main content
st.title('Sales Analysis Dashboard')

if analysis_choice == 'Top 10 Customer States':
    st.header('Top 10 Customer States by Frequency')
    state_frequency = merged_data.groupby('customer_state')['customer_id'].nunique().nlargest(10)
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = ['lightgrey' if state != state_frequency.idxmax() else 'lightblue' for state in state_frequency.index]
    sns.barplot(y=state_frequency.values, x=state_frequency.index, palette=colors, ax=ax)  # Tukar posisi x dan y
    plt.xlabel('Customer State')  # Label x menjadi Customer State
    plt.ylabel('Frequency')  # Label y menjadi Frequency
    plt.xticks(rotation=45)
    st.pyplot(fig)

elif analysis_choice == 'Top 10 Product Categories':
    st.header('Top 10 Best Selling Product Categories')
    category_counts = merged_data['product_category_name'].value_counts().head(10)
    palette = ['lightgray' if cat != category_counts.idxmax() else 'lightblue' for cat in category_counts.index]
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(x=category_counts.values, y=category_counts.index, palette='viridis', ax=ax)
    plt.xlabel('Frequency')
    plt.ylabel('Product Category')
    st.pyplot(fig)

elif analysis_choice == 'Frequency Distribution':
    st.header('Distribution of Purchasing Frequency')
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(merged_data['Frequency'], bins=20, kde=True, color='lightgreen', ax=ax)
    plt.xlabel('Purchasing Frequency')
    plt.ylabel('Frequency')
    st.pyplot(fig)

elif analysis_choice == 'Monetary Distribution':
    st.header('Distribution of Monetary Value')
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(merged_data['Monetary'], bins=20, kde=True, color='salmon', ax=ax)
    plt.xlabel('Monetary Value')
    plt.ylabel('Frequency')
    st.pyplot(fig)

elif analysis_choice == 'Customer Segmentation':
    st.header('Customer Segmentation')
    most_frequent_segment = merged_data['Segment'].value_counts().idxmax()
    colors = ['lightgray' if seg != most_frequent_segment else 'lightblue' for seg in merged_data['Segment'].unique()]
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.countplot(y='Segment', data=merged_data, order=merged_data['Segment'].value_counts().index, palette=colors, ax=ax)
    plt.xlabel('Number of Customers')
    plt.ylabel('Segment')
    st.pyplot(fig)
