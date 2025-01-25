import os
import streamlit as st
from dotenv import load_dotenv
from utils.spoonacular import fetch_recipes, fetch_recipe_details

# Load API key
load_dotenv()
API_KEY = os.getenv("SPOONACULAR_API_KEY")

# Main Content
st.title("Smart Food Recipe Recommender 🍳")
st.subheader("Find recipes based on the ingredients you have!")


ingredients = st.text_area("Enter your ingredients (comma-separated):", placeholder="e.g., chicken, tomatoes, basil")

diet = st.selectbox(
    "Select a dietary preference (optional):",
    ["None", "Vegetarian", "Vegan", "Gluten Free"]
)
if diet == "None":
    diet = None

meal_type = st.selectbox(
    "Select a meal type (optional):",
    ["None", "Breakfast", "Lunch", "Dinner", "Snack", "Dessert"]
)
if meal_type == "None":
    meal_type = None


# Recipe Fetch and Display Logic
if st.button("Find Recipes"):
    if not ingredients.strip():
        st.error("Please enter some ingredients!")
    else:
        try:
            recipes = fetch_recipes(API_KEY, ingredients, diet, meal_type)
            if not recipes:
                st.warning("No recipes found!")
            else:
                # Filter and display recipes with <= 3 missing ingredients
                filtered_recipes = [
                    recipe for recipe in recipes if len(recipe["missedIngredients"]) <= 3
                ]

                if not filtered_recipes:
                    st.warning("No recipes found with 3 or fewer missing ingredients!")
                else:
                    for recipe in filtered_recipes:
                        with st.expander(recipe["title"]):
                            st.image(recipe["image"], width=200)
                            st.write(f"**Used Ingredients:** {[ing['name'] for ing in recipe['usedIngredients']]}")
                            st.write(f"**Missing Ingredients:** {[ing['name'] for ing in recipe['missedIngredients']]}")

                            # Fetch and display detailed recipe info
                            details = fetch_recipe_details(API_KEY, recipe["id"])
                            if 'nutrition' in details and 'nutrients' in details['nutrition']:
                                calories = details['nutrition']['nutrients'][0]['amount']
                                st.write(f"**Calories:** {calories} kcal")
                            else:
                                st.write("**Calories:** Not available")

                            st.write(f"**Preparation Time:** {details['readyInMinutes']} minutes")
                            st.markdown(f"[View Full Recipe](https://spoonacular.com/recipes/{recipe['title'].replace(' ', '-')}-{recipe['id']})")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")


