
import streamlit as st
import anthropic
import google.generativeai as genai

# Access API keys from Streamlit Secrets
claude_api_key = st.secrets["claude"]["api_key"]
gemini_api_key = st.secrets["gemini"]["api_key"]

# Ensure API keys are provided
if not claude_api_key or not gemini_api_key:
    st.sidebar.warning("API keys are missing. Please set them in the environment variables.")
    st.stop()

# Configure Google Gemini API
genai.configure(api_key=gemini_api_key)

# Initialize Claude AI client
claude_client = anthropic.Anthropic(api_key=claude_api_key)

def generate_diet_plan(claude_client, fasting_sugar, pre_meal_sugar, post_meal_sugar, preferences):
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
    nutritional_info = genai.GenerativeModel('gemini-1.5-flash').generate(
        prompt=f"Provide detailed nutritional information for the following meal plan:\n{meal_plan}",
        max_tokens=500
    ).output.strip()  # Strip unnecessary spaces/newlines

    # Google Gemini: Generate Expert Insights
    expert_insights = genai.GenerativeModel('gemini-1.5-flash').generate(
        prompt=f"Explain how the following meal plan helps in managing diabetes:\n{meal_plan}",
        max_tokens=500
    ).output.strip()  # Strip unnecessary spaces/newlines

    return meal_plan, nutritional_info, expert_insights

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
