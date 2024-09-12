import sys
import os
from typing import List

# Adiciona o diretório 'DC-UFSCar-ES2-202401-Grupo3' ao PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import gamble.models as g


if __name__ == "__main__":
    while True:
        game_input = input("Selecione um jogo para jogar (BLACKJACK, BACARA): ")

        if game_input.upper() not in ["BLACKJACK", "BACARA"]:
            print("Selecione uma opção válida (BLACKJACK ou BACARA): ")
        else:
            break

    if game_input.upper() == "BLACKJACK":
        cards = g.BlackJackCard()
        players: List[g.BlackJackPlayer] = []

        qtd_players = int(input("Digite a quantidade de jogadores: "))

        for i in range(qtd_players):
            nome = input(f"Digite o nome do jogador {i + 1}: ")

            while True:
                try:
                    aposta = int(input(f"Digite a aposta do jogador {i}: "))
                    break
                except Exception:
                    print("Digite uma aposta válida")

            players.append(g.BlackJackPlayer(nome, aposta))

        game = g.BlackJackGame(players)
        game.start_game()

    elif game_input.upper() == "BACARA":
        # aposta = float(input("Digite o valor da sua aposta: "))
        
        game = g.BaccaratGame()
        resultado = game.play_game()

        print(resultado)
