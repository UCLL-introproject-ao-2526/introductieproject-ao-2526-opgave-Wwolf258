# black jack in python with pygame!
import copy
import random
import pygame

pygame.init()

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
paid_out = False

balance = 1000
current_bet = 0
betting_active = True

dealer_draw_time = 0

results = [
    '',
    'PLAYER BUSTED',
    'PLAYER WINS!',
    'DEALER WINS',
    'TIE GAME'
]


def deal_cards(current_hand, current_deck):
    card = random.randint(0, len(current_deck) - 1)
    current_hand.append(current_deck[card])
    current_deck.pop(card)
    return current_hand, current_deck


def calculate_score(hand):
    hand_score = 0
    aces_count = hand.count('A')

    for card in hand:
        if card in ['J', 'Q', 'K']:
            hand_score += 10
        elif card == 'A':
            hand_score += 11
        else:
            hand_score += int(card)

    while hand_score > 21 and aces_count > 0:
        hand_score -= 10
        aces_count -= 1

    return hand_score


def draw_scores(player, dealer):
    screen.blit(font.render(f'Score: {player}', True, 'white'), (330, 400))

    if reveal_dealer:
        screen.blit(font.render(f'Score: {dealer}', True, 'white'), (330, 100))


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


def draw_balance():
    screen.blit(smaller_font.render(f'Balance: ${balance}', True, 'gold'), (20, 20))
    screen.blit(smaller_font.render(f'Bet: ${current_bet}', True, 'gold'), (20, 60))


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


def draw_game():
    button_list = []

    if active and outcome == 0:
        hit = pygame.draw.rect(screen, 'white', [0, 700, 300, 100], 0, 5)
        pygame.draw.rect(screen, 'green', [0, 700, 300, 100], 3, 5)
        screen.blit(font.render('HIT ME', True, 'black'), (55, 735))
        button_list.append(hit)

        stand = pygame.draw.rect(screen, 'white', [300, 700, 300, 100], 0, 5)
        pygame.draw.rect(screen, 'green', [300, 700, 300, 100], 3, 5)
        screen.blit(font.render('STAND', True, 'black'), (355, 735))
        button_list.append(stand)

    if outcome != 0:
        screen.blit(font.render(results[outcome], True, 'white'), (120, 25))

        new_hand = pygame.draw.rect(screen, 'white', [150, 720, 300, 80], 0, 5)
        pygame.draw.rect(screen, 'green', [150, 720, 300, 80], 3, 5)
        screen.blit(font.render('NEW HAND', True, 'black'), (175, 740))
        button_list.append(new_hand)

    score_text = smaller_font.render(
        f'Wins: {records[0]}   Losses: {records[1]}   Draws: {records[2]}',
        True,
        'white'
    )
    screen.blit(score_text, (15, 840))

    return button_list


def determine_outcome(player, dealer):
    if player > 21:
        return 1
    elif dealer > 21:
        return 2
    elif player > dealer:
        return 2
    elif dealer > player:
        return 3
    else:
        return 4


def start_new_round():
    global active, initial_deal, game_deck
    global my_hand, dealer_hand, outcome
    global hand_active, reveal_dealer, add_score
    global dealer_score, player_score, betting_active
    global paid_out, dealer_draw_time

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
    paid_out = False

    dealer_score = 0
    player_score = 0
    dealer_draw_time = 0


run = True

while run:
    timer.tick(fps)
    screen.fill('black')

    betting_buttons = []
    buttons = []

    if initial_deal:
        for i in range(2):
            my_hand, game_deck = deal_cards(my_hand, game_deck)
            dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
        initial_deal = False

    if active:
        player_score = calculate_score(my_hand)
        dealer_score = calculate_score(dealer_hand)

        draw_cards(my_hand, dealer_hand, reveal_dealer)
        draw_scores(player_score, dealer_score)

        if reveal_dealer and outcome == 0:
            now = pygame.time.get_ticks()

            if dealer_score < 17:
                if now - dealer_draw_time > 700:
                    dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
                    dealer_draw_time = now
            else:
                outcome = determine_outcome(player_score, dealer_score)

                if add_score:
                    if outcome == 2:
                        records[0] += 1
                    elif outcome == 1 or outcome == 3:
                        records[1] += 1
                    else:
                        records[2] += 1

                    add_score = False

        if hand_active and player_score >= 21:
            hand_active = False
            reveal_dealer = True
            dealer_draw_time = pygame.time.get_ticks()

    draw_balance()

    if betting_active and not active:
        betting_buttons = draw_betting_buttons()

    buttons = draw_game()

    if outcome != 0 and not paid_out:
        if outcome == 2:
            balance += current_bet
        elif outcome == 1 or outcome == 3:
            balance -= current_bet

        paid_out = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONUP:

            if betting_active and not active:
                if betting_buttons[0].collidepoint(event.pos):
                    if balance >= current_bet + 10:
                        current_bet += 10

                elif betting_buttons[1].collidepoint(event.pos):
                    if balance >= current_bet + 50:
                        current_bet += 50

                elif betting_buttons[2].collidepoint(event.pos):
                    if current_bet > 0:
                        start_new_round()

            elif active and outcome == 0:
                if len(buttons) >= 2:
                    if buttons[0].collidepoint(event.pos) and player_score < 21 and hand_active:
                        my_hand, game_deck = deal_cards(my_hand, game_deck)

                    elif buttons[1].collidepoint(event.pos):
                        hand_active = False
                        reveal_dealer = True
                        dealer_draw_time = pygame.time.get_ticks()

            elif outcome != 0:
                if buttons[0].collidepoint(event.pos):
                    active = False
                    betting_active = True
                    current_bet = 0
                    outcome = 0
                    reveal_dealer = False
                    hand_active = False
                    my_hand = []
                    dealer_hand = []

    pygame.display.flip()

pygame.quit()