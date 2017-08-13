import nexus

def main():
  # UWaterloo OpenData API
  # Demonstrates basic usage
  api = nexus.load("https://api.uwaterloo.ca/v2/")
  api = api(key="a9916c2386dca2b31013969b43dcc98b")
  print(api.foodservices.menu_json.get_json())
  food_endpoint = api.foodservices[2017][1]
  print(food_endpoint.menu_json.get_json())
  print(food_endpoint.notes_json.get_json())

  # Google Maps directions
  # Demonstrates sticky parameters
  api = nexus.load("https://maps.googleapis.com/maps/api")
  api = api(key="PUT KEY HERE", mode="transit") # mode and key persist
  transit_endpoint = api.directions(origin="University of Waterloo") # origin persists
  transit_endpoint.json.get_json(params=dict(destination="345 King St N"))

main()