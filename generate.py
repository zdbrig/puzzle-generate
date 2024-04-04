import chess
import chess.engine
import random

def generate_random_position():
    board = chess.Board()
    num_moves = random.randint(10, 50)
    for _ in range(num_moves):
        legal_moves = list(board.legal_moves)
        if legal_moves:
            move = random.choice(legal_moves)
            board.push(move)
        else:
            break
    return board

def evaluate_position(board, engine, depth):
    result = engine.play(board, chess.engine.Limit(depth=depth))
    score = result.info["score"].relative.score()
    return score

def has_single_solution(board, engine, depth, num_moves):
    for _ in range(num_moves):
        result = engine.play(board, chess.engine.Limit(depth=depth))
        if result.move is None:
            return False
        board.push(result.move)
        legal_moves = list(board.legal_moves)
        if len(legal_moves) > 1:
            for move in legal_moves:
                if move != result.move:
                    board.push(move)
                    score = evaluate_position(board, engine, depth)
                    board.pop()
                    if score is not None and (score >= 200 or score <= -200):
                        return False
    return True

def find_awesome_puzzle(engine, depth):
    while True:
        board = generate_random_position()
        score = evaluate_position(board, engine, depth)
        if score is not None and (score >= 200 or score <= -200):
            result = engine.play(board, chess.engine.Limit(depth=depth))
            if result.move is not None:
                board.push(result.move)
                score_after_move = evaluate_position(board, engine, depth)
                if score_after_move is not None and abs(score_after_move) < 200:
                    if has_single_solution(board.copy(), engine, depth, 5):
                        board.pop()
                        return board, result.move
                board.pop()
        board.reset()

def main():
    engine = chess.engine.SimpleEngine.popen_uci("/usr/local/bin/stockfish")
    depth = 18
    puzzle_board, solution_move = find_awesome_puzzle(engine, depth)
    print("Awesome Chess Puzzle:")
    print(puzzle_board)
    print("White to play and win/draw.")
    print("Solution:")
    print(solution_move)
    engine.quit()

if __name__ == "__main__":
    main()
