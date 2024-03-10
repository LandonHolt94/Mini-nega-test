from GameStatus_5120 import GameStatus

def minimax(game_state: GameStatus, depth: int, maximizingPlayer: bool, alpha=float('-inf'), beta=float('inf')):
    terminal = game_state.is_terminal()
    if depth == 0 or terminal:
        newScores = game_state.get_scores(terminal)
        return newScores, None

    if maximizingPlayer:
        value = float('-inf')
        best_move = None
        for move in game_state.get_possible_moves():
            child_state = game_state.get_next_state(move)
            child_value, _ = minimax(child_state, depth - 1, False, alpha, beta)
            if child_value > value:
                value = child_value
                best_move = move
            alpha = max(alpha, value)
            if alpha >= beta:
                break  # Beta cutoff
        return value, best_move
    else:
        value = float('inf')
        best_move = None
        for move in game_state.get_possible_moves():
            child_state = game_state.get_next_state(move)
            child_value, _ = minimax(child_state, depth - 1, True, alpha, beta)
            if child_value < value:
                value = child_value
                best_move = move
            beta = min(beta, value)
            if alpha >= beta:
                break  # Alpha cutoff
        return value, best_move

def negamax(game_status: GameStatus, depth: int, turn_multiplier: int, alpha=float('-inf'), beta=float('inf')):
    terminal = game_status.is_terminal()
    if depth == 0 or terminal:
        scores = game_status.get_negamax_scores(terminal)
        return turn_multiplier * scores, None

    value = float('-inf')
    best_move = None
    for move in game_status.get_possible_moves():
        child_state = game_status.get_next_state(move)
        child_value, _ = negamax(child_state, depth - 1, -turn_multiplier, -beta, -alpha)
        child_value = -child_value  # Negate the value for negamax
        if child_value > value:
            value = child_value
            best_move = move
        alpha = max(alpha, value)
        if alpha >= beta:
            break  # Beta cutoff
    return turn_multiplier * value, best_move