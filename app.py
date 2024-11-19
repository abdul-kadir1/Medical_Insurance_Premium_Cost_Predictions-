# import sklearn
import streamlit as st
import pickle
import numpy as np
from PIL import Image

  

# Open image for display
Img = Image.open('health_insu.jpg')
Img_resized = Img.resize((1000, 250))  # Resize image to fit the app
st.image(Img_resized, caption="Health Insurance")

# Load the trained model
with open('pipe.pkl', 'rb') as model_file:
    model = pickle.dumps(model_file)

# Set up title and description
st.title('Health Insurance Cost Prediction Model')
st.write('Enter your details below to get Insurance amount.')

# Step 1: Get user input using Streamlit's widgets
age = st.number_input('Age', min_value=18, max_value=100, value=30)
sex = st.number_input('Sex (1 for Male, 0 for Female)', min_value=0, max_value=1, value=0)
weight = st.number_input('Weight (kg)', min_value=30, max_value=200, value=70)
bmi = st.number_input('BMI', min_value=10, max_value=50, value=25)
no_of_dependents = st.number_input('Number of Dependents', min_value=0, max_value=10, value=2)
smoker = st.number_input('Smoker (1 for Yes, 0 for No)', min_value=0, max_value=1, value=0)
diabetes = st.number_input('Diabetes (1 for Yes, 0 for No)', min_value=0, max_value=1, value=0)
regular_ex = st.number_input('Regular Exercise (1 for Yes, 0 for No)', min_value=0, max_value=1, value=0)

# Step 2: Prepare the input features for prediction
user_input = np.array([[age, sex, weight, bmi, no_of_dependents, smoker, diabetes, regular_ex]])

# Step 3: Add a button to trigger the prediction
if st.button('Predict'):
    st.write("The Details You Entered -")
    st.markdown(f"""
                age: {age}
                sex: {sex}
                weight: {weight}
                bmi: {bmi}
                no_of_dependents: {no_of_dependents}
                smoker: {smoker}
                diabetes: {diabetes}
                regular_ex: {regular_ex}
                """)

    # Step 4: Make a prediction using the loaded model
    prediction = model.predict(user_input)

    # Step 5: Display the prediction result
    st.write(f'Insurance Cost: {prediction[0]}')





