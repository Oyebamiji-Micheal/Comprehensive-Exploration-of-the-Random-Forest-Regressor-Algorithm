import streamlit as st
import pandas as pd
import joblib


def write_project_info():

    st.write("## Exploration of the Random Forest Regressor Algorithm") 

    st.write("""
        Predicting the ages of crabs while exploring the 
        random forest regressor algorithm in depth
    """
    )

    st.image("images/cover.jpeg")

    st.write("""
        ## About
        <p align="justify">
            Almost all of my past ML projects at one point or another use the Random Forest Algorithm.
            Perhaps, this is due to the fact that it is one of my favorite machine learning algorithms. My 
            first exposure to this algorithm was when I was trying to predict whether it will rain or not in 
            Australia using a dataset from <a href="https://www.kaggle.com/datasets/jsphyg/weather-dataset-rattle-package" style="text-decoration: None">Kaggle</a>. 
            Although I have a basic grasp of its functioning, I am eager to delve deeper into its fundamentals, understanding not just the "what" but the "why" behind its operations. My intention is to master its inner workings, gain insight into when and where to apply it, and grasp key interpretative elements. This app is a result of my camping in the <strong>Random Forest</strong>. Everything you need to know regarding this project including the documentation, notebook, dataset, etc. can be found in my repository on <a href="https://github.com/Oyebamiji-Micheal/Comprehensive-Exploration-of-the-Random-Forest-Regressor-Algorithm" target="_blank" style="text-decoration: None">Github</a>.</p>
    """, unsafe_allow_html=True)

    st.write("""**Made by Oyebamiji Micheal**""")


def take_user_inputs():
    st.sidebar.header("User Input Features")

    st.sidebar.write("<strong>1 foot = 30.48 cms</strong>", unsafe_allow_html=True)
    st.sidebar.write("<strong>1 pound = 16 ounces</strong>", unsafe_allow_html=True)

    sex = st.sidebar.selectbox(
        "**Sex: Gender of the Crab**", ("Male", "Female", "Indeterminate")
    )

    length = st.sidebar.number_input(
        "**Length**: Length of the Crab (in Feet)", step=None, min_value=0.001, max_value=10.0, value=0.1
    )

    diameter = st.sidebar.number_input(
        "**Diameter**: Diameter of the Crab (in Feet)", step=None, min_value=0.001, max_value=10.0, value=0.1
    )

    height = st.sidebar.number_input(
        "**Height**: Height of the Crab (in Feet)", step=None, min_value=0.001, max_value=10.00000, value=0.1
    )
    
    weight = st.sidebar.number_input(
        "**Weight**: Weight of the Crab (in ounces)", step=None, min_value=0.001, max_value=100.0, value=0.1
    )
    
    shucked_weight = st.sidebar.number_input(
        "**Shucked Weight**: Weight without the shell (in ounces)", step=None, min_value=0.001, max_value=100.0, value=0.1
    )

    viscera_weight = st.sidebar.number_input(
        "**Viscera Weight**: Weight that wraps around the abdominal organs deep inside body (in ounces)", step=None, min_value=0.001, max_value=100.0, value=0.1
    )

    shell_weight = st.sidebar.number_input(
        "**Shell Weight**: Weight of the shell (in ounces)", step=None, min_value=0.001, max_value=100.0, value=0.1
    )

    # Format inputs to training data representation
    mapping = {"Male": "M", "Female": "F", "Indeterminate": "I"}

    single_input = {
        "Sex": mapping[sex],
        "Length": length,
        "Diameter": diameter,
        "Height": height,
        "Weight": weight,
        "Shucked Weight": shucked_weight,
        "Viscera Weight": viscera_weight,
        "Shell Weight": shell_weight
    }

    return single_input


def predict_input(single_input):
    # Convert input into a pandas dataframe
    input_df = pd.DataFrame([single_input])

    model = joblib.load("crab_age_model.joblib")

    numeric_cols = model['numeric_cols']
    categorical_cols = model['categorical_cols']
    encoded_cols = model['encoded_cols']

    # Load fitted scaler and encoder
    scaler = model['scaler']
    encoder = model['encoder']
    
    # Load trained random forest model
    rf_model = model['rf_model']
    
    # Transform numeric columns
    input_df[numeric_cols] = scaler.transform(input_df[numeric_cols])
    
    # Encoded categorical columns
    encoded_data = encoder.transform(input_df[categorical_cols])
    
    input_df[encoded_cols] = encoded_data
    
    input_cols = list(numeric_cols) + list(encoded_cols)
    
    X_input = input_df[input_cols]
    
    prediction = rf_model.predict(X_input)
    
    prediction = prediction.round().astype(int)

    return prediction


if __name__ == "__main__":
    write_project_info()

    user_input = take_user_inputs()

    predict_crab_age = st.button("Predict Crab Age")

    if predict_crab_age:
        prediction = predict_input(user_input)
        
        st.write("Model = Random Forest")

        st.write(f"Predicted Crab Age = {prediction[0]} months")
