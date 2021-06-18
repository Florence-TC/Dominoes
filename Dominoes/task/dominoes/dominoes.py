import random

domino_set = []
player_pieces = []
computer_pieces = []
stock = []
domino_snake = []
status = ''

for number_1 in range(7):
    for number_2 in range(number_1, 7):
        domino_set.append([number_1, number_2])


def draw_pieces():
    global domino_set
    global player_pieces
    global computer_pieces
    global stock

    stock = domino_set
    player_pieces = random.sample(domino_set, 7)
    stock = [pieces for pieces in domino_set if pieces not in player_pieces]
    computer_pieces = random.sample(stock, 7)
    stock = [pieces for pieces in stock if pieces not in computer_pieces]


def start_game():
    global player_pieces
    global computer_pieces
    global domino_snake
    global status

    for i in range(6, -1, -1):
        if [i, i] in player_pieces:
            player_pieces.remove([i, i])
            domino_snake.append([i, i])
            status = "computer"
            break
        elif [i, i] in computer_pieces:
            computer_pieces.remove([i, i])
            domino_snake.append([i, i])
            status = "player"
            break


def display_board():
    string_snake = []
    string_snake_1 = []
    string_snake_2 = []

    print("=" * 70)
    print(f"Stock size: {len(stock)}")
    print(f"Computer pieces: {len(computer_pieces)}")
    print("\n")

    if len(domino_snake) <= 6:
        for domino in domino_snake:
            string_snake.append(str(domino))
        print("".join(string_snake))
    else:
        for j_1 in range(3):
            string_snake_1.append(str(domino_snake[j_1]))
        for j_2 in range(-3, 0, 1):
            string_snake_2.append(str(domino_snake[j_2]))
        print("".join(string_snake_1) + "..." + "".join(string_snake_2))

    print("\n")
    print("Your pieces:")
    for i in range(len(player_pieces)):
        print(f"{i + 1}:{player_pieces[i]}")
    print("\n")
    if status == "player":
        print("Status: It's your turn to make a move. Enter your command.")
    elif status == "computer":
        print("Status: Computer is about to make a move. Press Enter to continue...")


def player_move():
    global domino_snake
    global stock
    global player_pieces

    while True:
        piece = input()
        if not piece.lstrip('-').isdigit():
            print("Invalid input. Please try again.")
        else:
            int_piece = int(piece)
            if not -len(player_pieces) <= int_piece <= len(player_pieces):
                print("Invalid input. Please try again.")
            else:
                big_list_snake = []
                for domino in domino_snake:
                    big_list_snake.append(domino[0])
                    big_list_snake.append(domino[1])
                if int_piece < 0:
                    if player_pieces[-int_piece - 1][0] == big_list_snake[0]:
                        domino_snake.insert(0, player_pieces[-int_piece - 1][::-1])
                        del player_pieces[-int_piece - 1]
                    elif player_pieces[-int_piece - 1][1] == big_list_snake[0]:
                        domino_snake.insert(0, player_pieces[-int_piece - 1])
                        del player_pieces[-int_piece - 1]
                    else:
                        print("Illegal move. Please try again.")
                        player_move()
                    break
                elif int_piece > 0:
                    if player_pieces[int_piece - 1][0] == big_list_snake[-1]:
                        domino_snake.append(player_pieces[int_piece - 1])
                        del player_pieces[int_piece - 1]
                    elif player_pieces[int_piece - 1][1] == big_list_snake[-1]:
                        domino_snake.append(player_pieces[int_piece - 1][::-1])
                        del player_pieces[int_piece - 1]
                    else:
                        print("Illegal move. Please try again.")
                        player_move()
                    break
                elif int_piece == 0:
                    player_pieces.append(stock.pop())
                    break


def computer_move():
    global domino_snake
    global computer_pieces

    big_list_snake = []
    for domino in domino_snake:
        big_list_snake.append(domino[0])
        big_list_snake.append(domino[1])

    computer_list = []
    for domino in computer_pieces:
        computer_list.append(domino[0])
        computer_list.append(domino[1])

    snake_dict = {}
    for value in range(7):
        snake_dict[value] = big_list_snake.count(value) + computer_list.count(value)

    domino_scores = []
    for domino in computer_pieces:
        domino_scores.append(snake_dict[domino[0]] + snake_dict[domino[1]])

    for j in range(max(domino_scores)):
        for i in range(len(domino_scores)):
            if domino_scores[i] == max(domino_scores) - j:
                if computer_pieces[i][0] == big_list_snake[0]:
                    domino_snake.insert(0, computer_pieces[i][::-1])
                    del computer_pieces[i]
                    break
                elif computer_pieces[i][1] == big_list_snake[0]:
                    domino_snake.insert(0, computer_pieces[i])
                    del computer_pieces[i]
                    break
                elif computer_pieces[i][0] == big_list_snake[-1]:
                    domino_snake.append(computer_pieces[i])
                    del computer_pieces[i]
                    break
                elif computer_pieces[i][1] == big_list_snake[-1]:
                    domino_snake.append(computer_pieces[i][::-1])
                    del computer_pieces[i]
                    break
        else:
            continue
        break
    else:
        computer_pieces.append(stock.pop())


def test_snake():
    one_list_snake = []
    for domino in domino_snake:
        one_list_snake.append(domino[0])
        one_list_snake.append(domino[1])
    if one_list_snake[0] != one_list_snake[-1]:
        return True
    else:
        for number in range(1, 7):
            if one_list_snake.count(number) >= 8:
                return False
        return True


draw_pieces()
start_game()
while not domino_snake:
    draw_pieces()

while test_snake() and player_pieces and computer_pieces and stock:
    display_board()
    if status == "player":
        player_move()
        status = "computer"
    elif status == "computer":
        input()
        computer_move()
        status = "player"
else:
    if not test_snake() or not stock:
        print("Status: The game is over. It's a draw!")
    elif not player_pieces:
        display_board()
        print("Status: The game is over. You won!")
    elif not computer_pieces:
        display_board()
        print("Status: The game is over. The computer won!")
