import sys
import os

# Adiciona o diretório 'x' ao caminho de importação
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Agora você pode importar os módulos do diretório 'gamble'
from gamble import models as g
from gamble import Player
from typing import List

def main():
    # Criando um jogador com saldo inicial de 100
    player = Player(balance=400)

    # Criando o jogo e passando o jogador
    game = g.BaccaratGame(player)

    # Loop principal do jogo
    while True:
        # Exibindo o saldo atual
        print(f"\nSaldo atual: {player.balance}")

        # Verificando se o jogador tem saldo suficiente
        if player.balance <= 0:
            print("Você ficou sem saldo. O jogo acabou.")
            break

        # Receber o valor da aposta
        try:
            bet_amount = float(input("Digite o valor da sua aposta: "))
            if bet_amount > player.balance:
                print("Aposta maior que o saldo disponível. Tente novamente.")
                continue
        except ValueError:
            print("Valor de aposta inválido. Tente novamente.")
            continue

        # Escolher em quem apostar (Player, Banker ou Tie)
        bet_on = input("Aposte em Player, Banker ou Tie: ").capitalize()

        # Verificando se a aposta é válida
        if bet_on not in ["Player", "Banker", "Tie"]:
            print("Escolha inválida. Tente novamente.")
            continue

        # Jogador faz a aposta
        try:
            player.place_bet(bet_amount, bet_on)
        except ValueError as e:
            print(e)
            continue

        # Jogando o jogo
        result = game.play_game()
        print(result)

        # Pergunta se o jogador deseja continuar
        keep_playing = input("Deseja jogar outra rodada? (s/n): ").lower()
        if keep_playing != 's':
            print("Obrigado por jogar!")
            break

        # Reiniciar o jogo
        game.reset_game()

if __name__ == "__main__":
    main()
