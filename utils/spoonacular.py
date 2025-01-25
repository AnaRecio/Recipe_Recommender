import requests

def fetch_recipes(api_key, ingredients, diet=None, meal_type=None):
    url = "https://api.spoonacular.com/recipes/findByIngredients"
    params = {
        "ingredients": ingredients,
        "number": 10,
        "apiKey": api_key
    }
    if diet:
        params["diet"] = diet 
    if meal_type:
        params["type"] = meal_type 
    try:
            response = requests.get(url, params=params)  # Make the API call
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.json()  # Return the JSON response
    except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch recipes: {str(e)}")
    
def fetch_recipe_details(api_key, recipe_id):
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
    params = {"apiKey": api_key}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch recipe details: {response.status_code}")

