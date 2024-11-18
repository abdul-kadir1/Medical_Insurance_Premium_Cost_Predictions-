import mysql.connector
import streamlit as st
import pickle
import numpy as np
from PIL import Image

# Function to connect to the MySQL database
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",     
        user="root",         
        password="bc2022052@123",  
        database="health_insurance"  
    )

# Open image for display
Img = Image.open('health_insu.jpg')
Img_resized = Img.resize((1000, 250))  # Resize image to fit the app
st.image(Img_resized, caption="Health Insurance")

# Load the trained model
with open('pipe.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

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

    # Step 6: Save the user input and prediction to the database
    try:
        # Connect to MySQL database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Insert the user data and prediction into the insurance_data table
        query = """
        INSERT INTO insurance_data (age, sex, weight, bmi, no_of_dependents, smoker, diabetes, regular_ex, predicted_cost)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (age, sex, weight, bmi, no_of_dependents, smoker, diabetes, regular_ex, prediction[0])
        cursor.execute(query, values)

        # Commit the transaction
        conn.commit()

        st.success("Data saved successfully!")

    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
    
    finally:
        # Close the database connection
        if conn.is_connected():
            cursor.close()
            conn.close()
