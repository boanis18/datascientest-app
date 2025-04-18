import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split

# Load dataset
df = pd.read_csv("train.csv")

st.title("Titanic : Binary Classification Project")
st.sidebar.title("Table of Contents")
pages = ["Exploration", "Data Visualization", "Modelling"]
page = st.sidebar.radio("Go to", pages)

# Exploration Page
if page == pages[0]:
    st.write("### Presentation of Data")
    st.dataframe(df.head())
    st.write(df.shape)
    st.dataframe(df.describe())

    if st.checkbox("Show NA"):
        st.dataframe(df.isna().sum())

# Data Visualization Page
elif page == pages[1]:
    st.write("### Data Visualization")

    fig = plt.figure()
    sns.countplot(x='Survived', data=df)
    st.pyplot(fig)

    fig = plt.figure()
    sns.countplot(x='Sex', data=df)
    plt.title("Distribution of the Passengers' Gender")
    st.pyplot(fig)

    fig = plt.figure()
    sns.countplot(x='Pclass', data=df)
    plt.title("Distribution of the Passengers' Class")
    st.pyplot(fig)

    fig = sns.displot(x='Age', data=df)
    plt.title("Distribution of the Passengers' Age")
    st.pyplot(fig)

    fig = plt.figure()
    sns.countplot(x='Survived', hue='Sex', data=df)
    st.pyplot(fig)

    fig = sns.catplot(x='Pclass', y='Survived', data=df, kind='point')
    st.pyplot(fig)

    fig = sns.lmplot(x='Age', y='Survived', hue="Pclass", data=df)
    st.pyplot(fig)

    num_df = df.select_dtypes(include=['number'])
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(num_df.corr(), ax=ax, annot=True, fmt=".2f", cmap="coolwarm")
    st.pyplot(fig)

# Modelling Page
elif page == pages[2]:
    st.write("### Modelling")

    # Preprocessing
    df = df.drop(['PassengerId', 'Name', 'Ticket', 'Cabin'], axis=1)
    y = df['Survived']
    X_cat = df[['Pclass', 'Sex', 'Embarked']]
    X_num = df[['Age', 'Fare', 'SibSp', 'Parch']]

    for col in X_cat.columns:
        X_cat[col] = X_cat[col].fillna(X_cat[col].mode()[0])
    for col in X_num.columns:
        X_num[col] = X_num[col].fillna(X_num[col].median())

    X_cat_scaled = pd.get_dummies(X_cat, columns=X_cat.columns)
    X = pd.concat([X_cat_scaled, X_num], axis=1)

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Classifier function
    def prediction(classifier):
        if classifier == 'Random Forest':
            clf = RandomForestClassifier()
        elif classifier == 'SVC':
            clf = SVC()
        elif classifier == 'Logistic Regression':
            clf = LogisticRegression()
        clf.fit(X_train, y_train)
        return clf

    # Evaluation function
    def scores(clf, choice):
        if choice == 'Accuracy':
            return clf.score(X_test, y_test)
        elif choice == 'Confusion matrix':
            return confusion_matrix(y_test, clf.predict(X_test))

    choice = ['Random Forest', 'SVC', 'Logistic Regression']
    option = st.selectbox('Choice of the model', choice)
    st.write('The chosen model is:', option)

    clf = prediction(option)

    display = st.radio('What do you want to show?', ('Accuracy', 'Confusion matrix'))
    if display == 'Accuracy':
        st.write(scores(clf, display))
    elif display == 'Confusion matrix':
        st.dataframe(scores(clf, display))
