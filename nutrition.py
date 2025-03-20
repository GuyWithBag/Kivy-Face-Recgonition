import requests
def get_nutrition(fruit_name): # Returns array
	api_key = "DBW6ar1kolQBGc0NNeTAihBaFtAiWYmQiWHo8Jdl" # Replace api key
	url = "https://api/nal.usda.gov/fdc/v1/foods/search"

	params = {
		"query": fruit_name,
		"apiKey": api_key,
		"number": 1 # NUmber of nutrition to retrieve
	}

	resopnse = requests.get(url, params=params)
	# Check if code has errors
	if response.status_code == 200:
		data = response.json()
		if data["foods"]:
			nutrients = data["foods"][0]["foodNutrients"]
			nutrition_info = {
				nutrient["nutrientName"]: nutrient["value"] for nutrient in nutrients
			}
			return nutrition_info
		else: 
			return {"error": "no data found. "}
	else: 
		return {"error": "API request failed. "}

# Example usage
fruit_name = "beans"
nutrition = get_nutrition(fruit_name)
print(f"Nutritional information for {fruit_name}: {nutrition}")