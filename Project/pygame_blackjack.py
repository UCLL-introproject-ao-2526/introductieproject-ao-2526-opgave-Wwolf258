# black jack in python with pygame!
import copy
import random
import pygame

pygame.init()

# game variables
cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
one_deck = 4 * cards
decks = 4

WIDTH = 600
HEIGHT = 900
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Pygame Blackjack!')

fps = 60
timer = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 44)
smaller_font = pygame.font.Font('freesansbold.ttf', 36)

active = False
records = [0, 0, 0]

player_score = 0
dealer_score = 0
initial_deal = False

my_hand = []
dealer_hand = []

outcome = 0
reveal_dealer = False
hand_active = False
add_score = False

results = ['', 'PLAYER BUSTED o_O', 'Player WINS! :)', 'DEALER WINS :(', 'TIE GAME...']

# uitbreiding: coins en bets
balance = 1000
current_bet = 0
betting_active = True


def deal_cards(current_hand, current_deck):
    card = random.randint(0, len(current_deck) - 1)
    current_hand.append(current_deck[card])
    current_deck.pop(card)
    return current_hand, current_deck


def draw_scores(player, dealer):
    screen.blit(font.render(f'Score[{player}]', True, 'white'), (350, 400))
    if reveal_dealer:
        screen.blit(font.render(f'Score[{dealer}]', True, 'white'), (350, 100))


def draw_cards(player, dealer, reveal):
    for i in range(len(player)):
        pygame.draw.rect(screen, 'white', [70 + (70 * i), 460 + (5 * i), 120, 220], 0, 5)
        screen.blit(font.render(player[i], True, 'black'), (75 + 70 * i, 465 + 5 * i))
        screen.blit(font.render(player[i], True, 'black'), (75 + 70 * i, 635 + 5 * i))
        pygame.draw.rect(screen, 'red', [70 + (70 * i), 460 + (5 * i), 120, 220], 5, 5)

    for i in range(len(dealer)):
        pygame.draw.rect(screen, 'white', [70 + (70 * i), 160 + (5 * i), 120, 220], 0, 5)

        if i != 0 or reveal:
            screen.blit(font.render(dealer[i], True, 'black'), (75 + 70 * i, 165 + 5 * i))
            screen.blit(font.render(dealer[i], True, 'black'), (75 + 70 * i, 335 + 5 * i))
        else:
            screen.blit(font.render('???', True, 'black'), (75 + 70 * i, 165 + 5 * i))
            screen.blit(font.render('???', True, 'black'), (75 + 70 * i, 335 + 5 * i))

        pygame.draw.rect(screen, 'blue', [70 + (70 * i), 160 + (5 * i), 120, 220], 5, 5)


def calculate_score(hand):
    hand_score = 0
    aces_count = hand.count('A')

    for i in range(len(hand)):
        for j in range(8):
            if hand[i] == cards[j]:
                hand_score += int(hand[i])

        if hand[i] in ['10', 'J', 'Q', 'K']:
            hand_score += 10
        elif hand[i] == 'A':
            hand_score += 11

    if hand_score > 21 and aces_count > 0:
        for i in range(aces_count):
            if hand_score > 21:
                hand_score -= 10

    return hand_score


def draw_balance():
    balance_text = smaller_font.render(f'Balance: ${balance}', True, 'gold')
    bet_text = smaller_font.render(f'Bet: ${current_bet}', True, 'gold')

    screen.blit(balance_text, (20, 20))
    screen.blit(bet_text, (20, 60))


def draw_betting_buttons():
    button_list = []

    bet10 = pygame.draw.rect(screen, 'white', [50, 720, 120, 60], 0, 5)
    pygame.draw.rect(screen, 'black', [50, 720, 120, 60], 3, 5)
    screen.blit(smaller_font.render('+10', True, 'black'), (75, 735))
    button_list.append(bet10)

    bet50 = pygame.draw.rect(screen, 'white', [200, 720, 120, 60], 0, 5)
    pygame.draw.rect(screen, 'black', [200, 720, 120, 60], 3, 5)
    screen.blit(smaller_font.render('+50', True, 'black'), (225, 735))
    button_list.append(bet50)

    deal = pygame.draw.rect(screen, 'green', [380, 720, 170, 60], 0, 5)
    pygame.draw.rect(screen, 'white', [380, 720, 170, 60], 3, 5)
    screen.blit(smaller_font.render('DEAL', True, 'white'), (420, 735))
    button_list.append(deal)

    return button_list


def draw_game(act, record, result):
    button_list = []

    if act:
        hit = pygame.draw.rect(screen, 'white', [0, 700, 300, 100], 0, 5)
        pygame.draw.rect(screen, 'green', [0, 700, 300, 100], 3, 5)
        hit_text = font.render('HIT ME', True, 'black')
        screen.blit(hit_text, (55, 735))
        button_list.append(hit)

        stand = pygame.draw.rect(screen, 'white', [300, 700, 300, 100], 0, 5)
        pygame.draw.rect(screen, 'green', [300, 700, 300, 100], 3, 5)
        stand_text = font.render('STAND', True, 'black')
        screen.blit(stand_text, (355, 735))
        button_list.append(stand)

        score_text = smaller_font.render(f'Wins: {record[0]}   Losses: {record[1]}   Draws: {record[2]}', True, 'white')
        screen.blit(score_text, (15, 840))

    if result != 0:
        screen.blit(font.render(results[result], True, 'white'), (15, 25))

    return button_list


def check_endgame(hand_act, deal_score, play_score, result, totals, add):
    if not hand_act and deal_score >= 17:
        if play_score > 21:
            result = 1
        elif deal_score < play_score <= 21 or deal_score > 21:
            result = 2
        elif play_score < deal_score <= 21:
            result = 3
        else:
            result = 4

        if add:
            if result == 1 or result == 3:
                totals[1] += 1
            elif result == 2:
                totals[0] += 1
            else:
                totals[2] += 1
            add = False

    return result, totals, add


# main game loop
run = True

while run:
    timer.tick(fps)
    screen.fill('black')

    betting_buttons = []

    if initial_deal:
        for i in range(2):
            my_hand, game_deck = deal_cards(my_hand, game_deck)
            dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
        initial_deal = False

    if active:
        player_score = calculate_score(my_hand)
        draw_cards(my_hand, dealer_hand, reveal_dealer)

        if reveal_dealer:
            dealer_score = calculate_score(dealer_hand)
            if dealer_score < 17:
                dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)

        draw_scores(player_score, dealer_score)

    buttons = draw_game(active, records, outcome)
    draw_balance()

    if betting_active and not active:
        betting_buttons = draw_betting_buttons()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONUP:

            if not active:

                if betting_active:

                    if betting_buttons[0].collidepoint(event.pos):
                        if balance >= current_bet + 10:
                            current_bet += 10

                    elif betting_buttons[1].collidepoint(event.pos):
                        if balance >= current_bet + 50:
                            current_bet += 50

                    elif betting_buttons[2].collidepoint(event.pos):

                        if current_bet > 0:
                            active = True
                            initial_deal = True

                            game_deck = copy.deepcopy(decks * one_deck)

                            my_hand = []
                            dealer_hand = []

                            outcome = 0
                            hand_active = True
                            reveal_dealer = False
                            add_score = True

                            betting_active = False

            else:
                if len(buttons) >= 2:
                    if buttons[0].collidepoint(event.pos) and player_score < 21 and hand_active:
                        my_hand, game_deck = deal_cards(my_hand, game_deck)

                    elif buttons[1].collidepoint(event.pos) and not reveal_dealer:
                        reveal_dealer = True
                        hand_active = False

    if hand_active and player_score >= 21:
        hand_active = False
        reveal_dealer = True

    outcome, records, add_score = check_endgame(
        hand_active,
        dealer_score,
        player_score,
        outcome,
        records,
        add_score
    )

    pygame.display.flip()

pygame.quit()