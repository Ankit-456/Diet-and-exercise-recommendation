from flask import Flask, request, render_template
import random

app = Flask(__name__)

# Predefined recommendations

breakfasts = {
    "North Indian": ["Aloo paratha", "Poha", "Fruit juice"],
    "South Indian": ["Dosa", "Idli", "Vada"],
    "Chinese": ["Greek Yogurt with Nuts"],
    "Both": ["Fruit Salad", "Oatmeal with Berries", "Avocado Toast", "Smoothie Bowl", "Veggie Omelette",
             "Greek Yogurt with Nuts"]
}

lunches = {
    "North Indian": ["Chickpea Salad", "Grilled Chicken Wrap"],
    "South Indian": ["Vegetable Soup", "Pasta Primavera"],
    "Chinese": ["Falafel Sandwich"],
    "Both": ["Chickpea Salad", "Grilled Chicken Wrap", "Vegetable Soup", "Pasta Primavera", "Falafel Sandwich"]
}

dinners = {
    "North Indian": ["Grilled Vegetables", "Quinoa Salad"],
    "South Indian": ["Veggie Stir Fry", "Lentil Soup"],
    "Chinese": ["Stuffed Peppers"],
    "Both": ["Grilled Vegetables", "Quinoa Salad", "Veggie Stir Fry", "Lentil Soup", "Stuffed Peppers"]
}

# Workouts classified by age and disease
workouts = {
    "young_healthy": ["Morning Yoga", "Light Jogging", "Cycling", "Strength training"],
    "middle_aged_healthy": ["Evening Walk", "Light Jogging", "Stretching Exercises", "Cycling", "Strength training"],
    "senior_healthy": ["Morning Yoga", "Evening Walk", "Stretching Exercises", "Meditation", "Light Jogging"],
    "young_disease": ["Morning Yoga", "Evening Walk", "Stretching Exercises", "Meditation","Light Jogging"],
    "middle_aged_disease": ["Morning Yoga", "Evening Walk", "Stretching Exercises", "Meditation"],
    "senior_disease": ["Morning Yoga", "Evening Walk", "Stretching Exercises", "Meditation"]
}

# Function to generate recommendations based on user preferences
def generate_recommendations(input_data):
    age = input_data.get('age', 25)
    disease = input_data.get('disease', 'None')
    food_type = input_data.get('food_preferences', 'Both')

    # Determine the appropriate workout category based on age and disease
    if age < 30:
        if disease == 'None':
            workout_category = 'young_healthy'
        else:
            workout_category = 'young_disease'
    elif 30 <= age < 50:
        if disease == 'None':
            workout_category = 'middle_aged_healthy'
        else:
            workout_category = 'middle_aged_disease'
    else:
        if disease == 'None':
            workout_category = 'senior_healthy'
        else:
            workout_category = 'senior_disease'

    recommendations = {
        "breakfasts": random.sample(breakfasts.get(food_type, breakfasts["Both"]), 3),
        "lunches": random.sample(lunches.get(food_type, lunches["Both"]), 3),
        "dinners": random.sample(dinners.get(food_type, dinners["Both"]), 3),
        "workouts": random.sample(workouts.get(workout_category, workouts["young_healthy"]), 3)
    }
    return recommendations

# Function to calculate BMI
def calculate_bmi(weight, height):
    height_m = height / 100  # Convert height from cm to meters
    bmi = weight / (height_m ** 2)
    return round(bmi, 2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    # Get user input
    age = float(request.form['age'])
    gender = request.form['gender']
    weight = float(request.form['weight'])
    height = float(request.form['height'])
    veg_or_nonveg = request.form['veg_or_nonveg']
    disease = request.form['disease']
    food_preferences = request.form['food_preferences']  # Ensure this field matches the HTML form field name

    # Calculate BMI
    bmi = calculate_bmi(weight, height)

    # Generate recommendations
    recommendations = generate_recommendations({
        'age': age,
        'gender': gender,
        'weight': weight,
        'height': height,
        'veg_or_nonveg': veg_or_nonveg,
        'disease': disease,
        'food_preferences': food_preferences
    })

    return render_template('index.html', recommendations=recommendations, bmi=bmi)

if __name__ == '__main__':
    app.run(debug=True)
