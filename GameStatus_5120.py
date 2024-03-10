# -*- coding: utf-8 -*-

class GameStatus:

    def __init__(self, board_state, turn_O):
        self.board_state = board_state
        self.turn_O = turn_O
        self.oldScores = 0
        self.winner = ""

    def is_terminal(self):
        # Check if any cell is empty with the value 0
        for row in self.board_state:
            if 0 in row:
                return False
        # If no empty cells, check the winner
        scores = self.get_scores(True)
        if scores > 0:
            self.winner = "Human"
        elif scores < 0:
            self.winner = "AI"
        else:
            self.winner = "Draw"
        return True

    def get_scores(self, terminal):
        rows = len(self.board_state)
        cols = len(self.board_state[0])
        scores = 0
        check_point = 3 if terminal else 2

        # Check rows
        for i in range(rows):
            for j in range(cols - check_point + 1):
                triplet = self.board_state[i][j:j + check_point]
                scores += self.calculate_score(triplet)

        # Check columns
        for j in range(cols):
            for i in range(rows - check_point + 1):
                triplet = [self.board_state[i + k][j] for k in range(check_point)]
                scores += self.calculate_score(triplet)

        # Check diagonals
        for i in range(rows - check_point + 1):
            for j in range(cols - check_point + 1):
                # Check diagonal \
                triplet = [self.board_state[i + k][j + k] for k in range(check_point)]
                scores += self.calculate_score(triplet)
                # Check diagonal /
                triplet = [self.board_state[i + k][j + check_point - 1 - k] for k in range(check_point)]
                scores += self.calculate_score(triplet)

        return scores

    def calculate_score(self, triplet):
        if triplet.count(1) == 3:
            return 1
        elif triplet.count(-1) == 3:
            return -1
        else:
            return 0

    def get_negamax_scores(self, terminal):
    # Use the same logic as get_scores
     rows = len(self.board_state)
     cols = len(self.board_state[0])
     scores = 0
     check_point = 3 if terminal else 2

    # Check rows
     for i in range(rows):
        for j in range(cols - check_point + 1):
            triplet = self.board_state[i][j:j + check_point]
            scores += self.calculate_score(triplet)

    # Check columns
     for j in range(cols):
        for i in range(rows - check_point + 1):
            triplet = [self.board_state[i + k][j] for k in range(check_point)]
            scores += self.calculate_score(triplet)

    # Check diagonals
     for i in range(rows - check_point + 1):
        for j in range(cols - check_point + 1):
            # Check diagonal \
            triplet = [self.board_state[i + k][j + k] for k in range(check_point)]
            scores += self.calculate_score(triplet)
            # Check diagonal /
            triplet = [self.board_state[i + k][j + check_point - 1 - k] for k in range(check_point)]
            scores += self.calculate_score(triplet)

    # Negate the total score
     return -scores

    def get_possible_moves(self):
        moves = []
        for i in range(len(self.board_state)):
            for j in range(len(self.board_state[0])):
                if self.board_state[i][j] == 0:
                    moves.append((i, j))
        return moves

    def get_next_state(self, move):
        new_board_state = [row[:] for row in self.board_state]
        x, y = move[0], move[1]
        new_board_state[x][y] = 1 if self.turn_O else -1
        return GameStatus(new_board_state, not self.turn_O)