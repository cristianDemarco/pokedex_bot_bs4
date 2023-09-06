import requests
import sys
import os
import random
import re

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Classes.pokemon import Pokemon

class PokemonAPI:
    
    def __init__(self) -> None:
        self.data = None
        self.species_data = None

    def get_api_data(self, pokemon : str = "Undefined", variety : int = 0) -> None:
        variety = int(variety)
        species_data_response = requests.get(f"https://pokeapi.co/api/v2/pokemon-species/{pokemon}")
        
        if species_data_response.status_code == 200:
            self.species_data = species_data_response.json()
            
        if variety > len(self.species_data["varieties"]) - 1:
            variety = 0
                    
        pokemon_variety = self.species_data["varieties"][variety]["pokemon"]["name"]

        data_response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_variety}")
        
        if data_response.status_code == 200:
            self.data = data_response.json()

    def elaborate_api_data(self, variety) -> None:

        name = self.data["name"].capitalize().split("-", 1)[0]
        
        id = str(self.species_data["id"])

        photo = self.data["sprites"]["other"]["official-artwork"]["front_default"]
        photo_link = photo.replace("PokeAPI/sprites", "cristianDemarco/PokeAPI_sprites")

        types = []
        
        for type in self.data["types"]:
            type_link = type["type"]["url"]
            data_response = requests.get(type_link).json()
            for element in data_response["names"]:
                if element["language"]["name"] == "it":
                    types.append(element["name"])
                    break

        types = ", ".join(types)

        warning = ""
        descriptions = self.species_data["flavor_text_entries"]

        descriptions_set = set(description["flavor_text"] for description in descriptions if description["language"]["name"] == "it")

        if len(descriptions_set) == 0:
            descriptions_set = set(description["flavor_text"] for description in descriptions if description["language"]["name"] == "en")
            warning = "La descrizione non è disponbile in italiano.\n"

        description = warning + " ".join(random.choice(list(descriptions_set)).split())

        generation = self.species_data["generation"]["url"]
        pattern = r"/generation/(\d+)/"
        generation = re.search(pattern, generation).group(1)
        is_legendary = self.species_data["is_legendary"]
        is_legendary = self.species_data["is_mythical"]
        number_of_varieties = len(self.species_data["varieties"])


        return Pokemon(name, id, generation, is_legendary, photo_link, types, description, 0 if int(variety) > number_of_varieties - 1 else variety)        
            

    