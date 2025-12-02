from pokemon_cli.pokemon.moves import Movedex
from pokemon_cli.pokemon.pokemon import Pokedex


def main() -> None:
    print("Hello from pokemon-cli!")
    dex = Pokedex()
    bulbasaur = dex.get_pokemon("Bulbasaur")
    print(bulbasaur)
    bulbasaur.base_stats.hp = 1000
    print(bulbasaur)
    friend = dex.get_pokemon("Bulbasaur")
    print(friend)

    movedex = Movedex()
    print(movedex.get_move("pound"))
    print(movedex.get_move("karate choP"))
