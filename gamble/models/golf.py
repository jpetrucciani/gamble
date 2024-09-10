"""
golf related games
"""

YARDS = (
    332,
    410,
    357,
    148,
    431,
    519,
    338,
    405,
    283,
    515,
    348,
    148,
    446,
    348,
    380,
    431,
    217,
    389,
)
PAR = (4, 4, 4, 3, 4, 5, 4, 4, 4, 5, 4, 3, 4, 4, 4, 4, 3, 4)
HANDICAP = (15, 3, 5, 17, 1, 9, 11, 7, 13, 6, 16, 18, 2, 14, 8, 4, 12, 10)
HCC_DATA = zip(YARDS, PAR, HANDICAP, strict=True)


class Hole:
    """
    a golf hole object
    """

    def __init__(self, tee: int, yards: int, par: int, handicap: int) -> None:
        """
        hole constructor

        Args:
            tee: the tee number for this hole
            yards: the number of yards from tee to hole
            par: the par for this hole
            handicap: the handicap value for this hole
        """
        self.tee = tee
        self.yards = yards
        self.par = par
        self.handicap = handicap


class Course:
    """
    a golf course object

    Args:
        name: the name of this golf course
        holes: a list of holes in this golf course
    """

    def __init__(self, name: str, holes: list[Hole]) -> None:
        self.name = name
        self.holes = sorted(holes, key=lambda hole: hole.tee)
        self.yards = sum(x.yards for x in self.holes)
        self.par = sum(x.par for x in self.holes)
        self.front = self.holes[:9]
        self.back = self.holes[9:]


class Player:
    """
    a golf player object

    Args:
        name: the name of the player
        handicap: the handicap of the player
    """

    def __init__(self, name: str, handicap: int) -> None:
        self.name = name
        self.handicap = handicap


class Group:
    """
    A golf group object

    Args:
        course: the course that this group is playing
        players: the list of players in this group
    """

    def __init__(self, course: Course, players: list[Player]) -> None:
        self.course = course
        self.players = players
        self.scores = {player.name: [None] * len(course.holes) for player in players}

    def add_score(self, player_name: str, hole_index: int, score: int):
        """
        Adiciona o score de um jogador para um buraco específico.
        
        Args:
            player_name: Nome do jogador
            hole_index: O número do buraco (começando em 1)
            score: A pontuação do jogador para esse buraco
        """
        if player_name in self.scores:
            self.scores[player_name][hole_index - 1] = score

    def get_total_score(self, player_name: str) -> int:
        """
        Calcula o total de pontos para o jogador.
        
        Args:
            player_name: Nome do jogador
        Returns:
            int: Pontuação total do jogador
        """
        return sum(score for score in self.scores[player_name] if score is not None)

    def display_scores(self):
        """
        Mostra os scores de cada jogador buraco a buraco e o total.
        """
        for player in self.players:
            print(f"Scores for {player.name}:")
            for hole_index, score in enumerate(self.scores[player.name], start=1):
                if score is not None:
                    print(f"  Hole {hole_index}: {score}")
                else:
                    print(f"  Hole {hole_index}: No score")
            total_score = self.get_total_score(player.name)
            print(f"  Total Score: {total_score}\n")

    def declare_winner(self):
        """
        Compara os scores totais dos jogadores e declara o vencedor (menor score).
        """
        scores = {player.name: self.get_total_score(player.name) for player in self.players}
        winner = min(scores, key=scores.get)
        print(f"The winner is {winner} with a score of {scores[winner]}!")





HOLES = [Hole(index + 1, x[0], x[1], x[2]) for index, x in enumerate(HCC_DATA)]
HCC = Course("Hillcrest", HOLES)

import unittest

class TestGolfGame(unittest.TestCase):
    
    def test_course_setup(self):
        course = HCC
        self.assertEqual(course.yards, 6445)
        self.assertEqual(course.par, 71)

    def test_add_and_display_scores(self):
        # Setup
        player1 = Player("John", 10)
        player2 = Player("Alice", 15)
        group = Group(HCC, [player1, player2])

        # Adiciona scores para múltiplos buracos
        group.add_score("John", 1, 4)
        group.add_score("John", 2, 5)
        group.add_score("John", 3, 4)
        group.add_score("John", 4, 3)
        group.add_score("Alice", 1, 3)
        group.add_score("Alice", 2, 5)
        group.add_score("Alice", 3, 4)
        group.add_score("Alice", 4, 3)

        # Verifica se os scores foram adicionados corretamente
        self.assertEqual(group.scores["John"][0], 4)
        self.assertEqual(group.scores["John"][1], 5)
        self.assertEqual(group.scores["John"][2], 4)
        self.assertEqual(group.scores["John"][3], 3)
        self.assertEqual(group.scores["Alice"][0], 3)
        self.assertEqual(group.scores["Alice"][1], 5)
        self.assertEqual(group.scores["Alice"][2], 4)
        self.assertEqual(group.scores["Alice"][3], 3)

        # Verifica a pontuação total
        self.assertEqual(group.get_total_score("John"), 16)
        self.assertEqual(group.get_total_score("Alice"), 15)

        # Exibe os scores
        group.display_scores()

        # Declara o vencedor
        group.declare_winner()

if __name__ == "__main__":
    unittest.main()

