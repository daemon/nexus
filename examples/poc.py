import nexus

def main():
  api = nexus.load("https://api.uwaterloo.ca/v2/")
  api = api(key="a9916c2386dca2b31013969b43dcc98b")
  print(api.foodservices.menu_json.get_json())
  food_endpoint = api.foodservices[2017][1]
  print(food_endpoint.menu_json.get_json())
  print(food_endpoint.notes_json.get_json())

main()