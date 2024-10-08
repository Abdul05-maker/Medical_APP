import streamlit as st
import anthropic
import google.generativeai as genai

# Retrieve the API keys from secrets
claude_api_key = st.secrets["claude"]["api_key"]
gemini_api_key = st.secrets["gemini"]["api_key"]

# Initialize the Claude client with the API key
claude_client = anthropic.Anthropic(api_key=claude_api_key)

# Configure Google Gemini API
genai.configure(api_key=gemini_api_key)

# Initialize the Gemini model once
gemini_model = genai.GenerativeModel('gemini-1.5-flash')

def generate_diet_plan(claude_client, fasting_sugar, pre_meal_sugar, post_meal_sugar, preferences):
    try:
        # Claude AI: Generate Meal Plan
        claude_message = claude_client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=1000,
            temperature=0.7,
            system="You are a world-class nutritionist. Provide a personalized meal plan for a diabetic patient.",
            messages=[
                {
                    "role": "user",
                    "content": f"""
                    Create a personalized meal plan for a diabetic patient with the following details:
                    Fasting Sugar Level: {fasting_sugar} mg/dL
                    Pre-Meal Sugar Level: {pre_meal_sugar} mg/dL
                    Post-Meal Sugar Level: {post_meal_sugar} mg/dL
                    Dietary Preferences: {preferences}
                    """
                }
            ]
        )
        meal_plan = claude_message.content.strip()  # Strip unnecessary spaces/newlines

        # Google Gemini: Generate Nutritional Information
        nutritional_info = gemini_model.generate(
            prompt=f"Provide detailed nutritional information for the following meal plan:\n{meal_plan}",
            max_tokens=500
        ).output.strip()  # Strip unnecessary spaces/newlines

        # Google Gemini: Generate Expert Insights
        expert_insights = gemini_model.generate(
            prompt=f"Explain how the following meal plan helps in managing diabetes:\n{meal_plan}",
            max_tokens=500
        ).output.strip()  # Strip unnecessary spaces/newlines

        return meal_plan, nutritional_info, expert_insights

    except Exception as e:
        st.error(f"An error occurred: {e}")
        return "Error generating meal plan", "Error generating nutritional info", "Error generating expert insights"

# Sidebar Inputs with Enter Buttons
st.sidebar.header("Input Your Details")

fasting_sugar = st.sidebar.number_input("Fasting Sugar Level", min_value=0, max_value=500, step=1)
pre_meal_sugar = st.sidebar.number_input("Pre-Meal Sugar Level", min_value=0, max_value=500, step=1)
post_meal_sugar = st.sidebar.number_input("Post-Meal Sugar Level", min_value=0, max_value=500, step=1)
preferences = st.sidebar.text_input("Personal Preferences", "e.g., low-carb, vegetarian")

if st.sidebar.button("Generate Meal Plan"):
    meal_plan, nutritional_info, expert_insights = generate_diet_plan(claude_client, fasting_sugar, pre_meal_sugar, post_meal_sugar, preferences)

    # Main Screen Output
    st.title("Diabetic Diet Meal Planner")

    # Section: Personalized Meal Plan from Claude AI
    st.subheader("📋 Personalized Meal Plan")
    st.markdown(meal_plan)

    # Section: Nutritional Information from Google Gemini
    st.subheader("🍽 Nutritional Information")
    st.markdown(nutritional_info)

    # Section: Expert Insights from Google Gemini
    st.subheader("🔍 Expert Insights")
    st.markdown(expert_insights)

# Disclaimer at the End of the App
st.markdown("#### Disclaimer")
st.write("This AI-powered tool is for informational purposes only and does not replace professional medical advice. Please consult with your healthcare provider for personalized medical guidance.")
