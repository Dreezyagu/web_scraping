import requests
from bs4 import BeautifulSoup as bs
import matplotlib.pyplot as plt

recipes = []

# Loop through the 50 pages to load the contents individually
for i in range(1,51):
  r = requests.get(f"https://www.skinnytaste.com/recipe-index/?_paged={i}")
  soup = bs(r.text, 'html.parser')

  # Get all meals on a page
  meals = soup.find_all('h2', class_="entry-title")
  for meal in meals:
    title = meal.text
    url = meal.find('a')['href']

    # Load the meal page
    if url:
      meal_request = requests.get(url)
      meal_soup = bs(meal_request.text, 'html.parser')

      # Get meals calories count
      meal_calories = meal_soup.find('span', class_="recipe-meta-value value-calories")
      if meal_calories:
        calories = meal_calories.text
      else:
        calories = "Cals: N/A"

      # Get meal summary
      summary = meal_soup.find('p')
      
      # Get meal personal points
      personal_points = meal_soup.find('span', class_="recipe-meta-value recipe-ww-pp icon")
      if personal_points:
        personal_point = personal_points.text
      else:
        personal_point = "N/A"

      # Get meal recipe keys and put them in a list
      recipe_keys = meal_soup.find('ul', class_="cat-icons post-icons")
      if recipe_keys:
        recipe_key_items = recipe_keys.find_all('li')
        key_list = []
        for key in recipe_key_items:
          key_list.append(key.text)
        recipe_key = key_list
      else:
        recipe_key = "N/A"

      # Get the image of the meal
      recipe_figure = meal_soup.find('figure', class_="wp-block-image size-full")
      if recipe_figure:
        recipe_image = recipe_figure.find('img')['src']
      else:
        recipe_image = "N/A"
      


      # Add all relevant recipe details to a list of dictionaries
      if recipe_key != "N/A" and calories != "Cals: N/A" and personal_point != "N/A":
        recipes.append({"title": title, "image": recipe_image, "calories": float(calories[6:]), "personal_points": float(personal_point), "summary": summary.text, "recipe_key": recipe_key})

# Declaring dictionaries to be used to generate the charts
recipe_key_frequency_map = {}
personal_points_frequency_map = {}
personal_points_frequency_map_sorted = {}
calories_frequency_map = {"0-100": 0, "101-200": 0, "201-300":0, "301-400":0, "401-500":0, "500+":0}

for recipe in recipes:

  #this goes through the recipe keys. If a key doesn’t exist, it sets the key and value to 1. If it exists, it increments the key value by +1
  for key in recipe["recipe_key"]:
    if key in recipe_key_frequency_map:
      recipe_key_frequency_map[key] += 1
    else:
      recipe_key_frequency_map[key] = 1
  #the same implementation as above for personal points
  personal_point = int(recipe["personal_points"])
  if personal_point:
    if personal_point in personal_points_frequency_map:
      personal_points_frequency_map[personal_point] += 1
    else:
      personal_points_frequency_map[personal_point] = 1

  # a match(switch) function to increment calorie ranges to appropriately
  calorie = recipe["calories"];
  if calorie:
    match calorie :
      case num if calorie <= 100:
        calories_frequency_map["0-100"] += 1
      case num if calorie <= 200:
        calories_frequency_map["101-200"] += 1
      case num if calorie <= 300:
        calories_frequency_map["201-300"] += 1
      case num if calorie <= 400:
        calories_frequency_map["301-400"] += 1
      case num if calorie <= 500:
        calories_frequency_map["401-500"] += 1
      case num if calorie > 500:
        calories_frequency_map["500+"] += 1

recipe_fig, recipe_ax = plt.subplots()
calories_fig, calories_ax = plt.subplots()
personal_points_fig, personal_points_ax = plt.subplots()

#setting calories chart. Calories range against frequency
calories_ax.bar(calories_frequency_map.keys(), calories_frequency_map.values())
calories_ax.set_xlabel("Calories")
calories_ax.set_ylabel("Frequency")
calories_ax.set_title("Frequency of Calories")

#setting personal points chart. Personal points against frequency
personal_points_ax.bar(personal_points_frequency_map.keys(), personal_points_frequency_map.values())
personal_points_ax.set_xlabel("Personal Points")
personal_points_ax.set_ylabel("Frequency")
personal_points_ax.set_title("Frequency of Personal Points")

#setting recipe key chart. Keys against frequency
recipe_ax.bar(recipe_key_frequency_map.keys(), recipe_key_frequency_map.values())
recipe_ax.set_xlabel("Recipe Key")
recipe_ax.set_ylabel("Frequency")
recipe_ax.set_title("Frequency of Recipe Keys")

plt.show()

# prompt: a function that takes a calories range and return recipes that fall in that range
def get_recipes_by_calories(min_calories, max_calories):
  """
  Returns a list of recipes that fall within a specified calorie range.

  Args:
    min_calories: The minimum calorie value for the range.
    max_calories: The maximum calorie value for the range.

  Returns:
    A list of dictionaries, where each dictionary represents a recipe 
    that falls within the specified calorie range.
  """
  matching_recipes = []
  for recipe in recipes:
    if min_calories <= recipe["calories"] <= max_calories:
      matching_recipes.append(recipe)
  return matching_recipes

minimuim_calories = input('Input minimum calorie\n')
maximum_calories = input('Input maximum calorie\n')

try:
    float(minimuim_calories)
except ValueError:
    print("This is not a number")

try:
    float(maximum_calories)
except ValueError:
    print("This is not a number") 

recipes_in_range1 = get_recipes_by_calories(float(minimuim_calories), float(maximum_calories))

# Print the titles of the recipes found.
for recipe in recipes_in_range1:
  print(recipe)

if(len(recipe) == 0):
  print("No recipe found!")

# prompt: a function that takes a calories range and return recipes that fall in that range
def get_recipes_by_calories(min_calories, max_calories):
  """
  Returns a list of recipes that fall within a specified calorie range.

  Args:
    min_calories: The minimum calorie value for the range.
    max_calories: The maximum calorie value for the range.

  Returns:
    A list of dictionaries, where each dictionary represents a recipe 
    that falls within the specified calorie range.
  """
  matching_recipes = []
  for recipe in recipes:
    if min_calories <= recipe["calories"] <= max_calories:
      matching_recipes.append(recipe)
  return matching_recipes

minimuim_calories = input('Input minimum calorie\n')
maximum_calories = input('Input maximum calorie\n')

try:
    float(minimuim_calories)
except ValueError:
    print("This is not a number")

try:
    float(maximum_calories)
except ValueError:
    print("This is not a number") 

recipes_in_range1 = get_recipes_by_calories(float(minimuim_calories), float(maximum_calories))

# Print the titles of the recipes found.
for re in recipes_in_range1:
  print(re)

if(len(recipes_in_range1) == 0):
  print("No recipe found!")


# prompt: a function that takes a calories range and return recipes that fall in that range
def get_recipes_by_points(min_points, max_points):
  """
  Returns a list of recipes that fall within a specified personal points range.

  Args:
    min_calories: The minimum point value for the range.
    max_calories: The maximum point value for the range.

  Returns:
    A list of dictionaries, where each dictionary represents a recipe 
    that falls within the specified personal points.
  """
  matching_recipes = []
  for recipe in recipes:
    if min_points <= recipe["personal_points"] <= max_points:
      matching_recipes.append(recipe)
  return matching_recipes


minimuim_points = input('Input minimum points:\n')
maximum_points = input('Input maximum points:\n')

try:
    float(minimuim_points)
except ValueError:
    print("This is not a number")

try:
    float(maximum_points)
except ValueError:
    print("This is not a number") 

recipes_in_range2 = get_recipes_by_points(float(minimuim_points), float(maximum_points))

# Print the titles of the recipes found.
for re in recipes_in_range2:
  print(re)

if(len(recipes_in_range2) == 0):
  print("No recipe found!")