# black jack in python with pygame!
import copy
import random
import pygame

pygame.init()

ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
suits = ['♥', '♦', '♣', '♠']
one_deck = [rank + suit for rank in ranks for suit in suits]
decks = 4

WIDTH = 600
HEIGHT = 900
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Pygame Blackjack!')

fps = 60
timer = pygame.time.Clock()
font = pygame.font.SysFont('arial', 44)
smaller_font = pygame.font.SysFont('arial', 36)

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
natural_blackjack = False

balance = 1000
current_bet = 0
betting_active = True
game_over = False

dealer_draw_time = 0

results = [
    '',
    'PLAYER BUSTED',
    'PLAYER WINS!',
    'DEALER WINS',
    'TIE GAME'
]


def get_rank(card):
    return card[:-1]
# [dn] waarom niet gewoon card[0] en card[1]?
def get_suit(card):
    return card[-1]


def get_suit_color(card):
    suit = get_suit(card)

    # [dn] de symbolen gebruiken is leuk, maar hier zie je meteen het probleem: je moet ze ook kunnen typen (sneller als copy pasten)
    # een sneller alternatief is letters: ['c', 's', 'h', 'd']
    if suit == '♥' or suit == '♦':
        return 'red'

    return 'black'


def deal_cards(current_hand, current_deck):
    card = random.randint(0, len(current_deck) - 1)
    current_hand.append(current_deck[card])
    current_deck.pop(card)
    return current_hand, current_deck


def calculate_score(hand):
    hand_score = 0
    aces_count = 0

    for card in hand:
        rank = get_rank(card)

        if rank in ['J', 'Q', 'K']:
            hand_score += 10
        elif rank == 'A':
            hand_score += 11
            aces_count += 1
        else:
            hand_score += int(rank)

    while hand_score > 21 and aces_count > 0:
        hand_score -= 10
        aces_count -= 1 # [dn] waarom? aces_count is nergens gebruikt

    return hand_score


def draw_labels():
    dealer_label = smaller_font.render('DEALER', True, 'white')
    player_label = smaller_font.render('PLAYER', True, 'white')

    screen.blit(dealer_label, (70, 130))
    screen.blit(player_label, (70, 430))


def draw_scores(player, dealer):
    if reveal_dealer:
        dealer_score_text = font.render(f'Score: {dealer}', True, 'white')
        screen.blit(dealer_score_text, (350, 205))

    player_score_text = font.render(f'Score: {player}', True, 'white')
    screen.blit(player_score_text, (350, 505))


def draw_single_card(card, x, y, border_color):
    pygame.draw.rect(screen, (30, 30, 30), [x + 6, y + 6, 120, 220], 0, 5)
    pygame.draw.rect(screen, 'white', [x, y, 120, 220], 0, 5)

    rank = get_rank(card)
    suit = get_suit(card)
    card_color = get_suit_color(card)

    screen.blit(font.render(rank, True, card_color), (x + 8, y + 5))
    screen.blit(smaller_font.render(suit, True, card_color), (x + 10, y + 55))

    screen.blit(smaller_font.render(suit, True, card_color), (x + 78, y + 135))
    screen.blit(font.render(rank, True, card_color), (x + 72, y + 170))

    pygame.draw.rect(screen, border_color, [x, y, 120, 220], 5, 5)


def draw_hidden_card(x, y):
    pygame.draw.rect(screen, (30, 30, 30), [x + 6, y + 6, 120, 220], 0, 5)
    pygame.draw.rect(screen, 'white', [x, y, 120, 220], 0, 5)

    pygame.draw.rect(screen, 'blue', [x + 15, y + 15, 90, 190], 0, 5)
    pygame.draw.rect(screen, 'white', [x + 25, y + 25, 70, 170], 3, 5)

    hidden_text = smaller_font.render('???', True, 'white')
    hidden_rect = hidden_text.get_rect(center=(x + 60, y + 110))
    screen.blit(hidden_text, hidden_rect)

    pygame.draw.rect(screen, 'blue', [x, y, 120, 220], 5, 5)


def draw_cards(player, dealer, reveal):
    for i in range(len(player)):
        card_x = 70 + (70 * i)
        card_y = 460 + (5 * i)
        draw_single_card(player[i], card_x, card_y, 'red')

    for i in range(len(dealer)):
        card_x = 70 + (70 * i)
        card_y = 165 + (5 * i)

        if i != 0 or reveal:
            draw_single_card(dealer[i], card_x, card_y, 'blue')
        else:
            draw_hidden_card(card_x, card_y)


def draw_balance():
    screen.blit(smaller_font.render(f'Balance: ${balance}', True, 'gold'), (20, 20))
    screen.blit(smaller_font.render(f'Bet: ${current_bet}', True, 'gold'), (20, 60))

    title_text = smaller_font.render('CASINO BLACKJACK', True, 'gold')
    title_rect = title_text.get_rect(center=(WIDTH // 2, 105))
    screen.blit(title_text, title_rect)


def draw_chip(x, y, amount, color):
    pygame.draw.circle(screen, color, (x, y), 35)
    pygame.draw.circle(screen, 'white', (x, y), 35, 4)
    pygame.draw.circle(screen, 'black', (x, y), 25, 2)

    text = smaller_font.render(amount, True, 'white')
    text_rect = text.get_rect(center=(x, y))
    screen.blit(text, text_rect)

    return pygame.Rect(x - 35, y - 35, 70, 70)


def draw_betting_buttons():
    button_list = []

    # [dn] als je vaak dezelfde waardes ziet (vooral 715, maar ook 770, 30, 55), steek ze in een variabele
    # dan hebben ze een naam en kan je ze op 1 plaats aanpassen
    button_list.append(draw_chip(70, 715, '+10', 'red'))
    button_list.append(draw_chip(160, 715, '+50', 'blue'))
    button_list.append(draw_chip(260, 715, '+100', 'purple'))
    button_list.append(draw_chip(375, 715, '+500', 'black'))

    clear = pygame.draw.rect(screen, 'white', [30, 770, 150, 55], 0, 5)
    pygame.draw.rect(screen, 'black', [30, 770, 150, 55], 3, 5)
    screen.blit(smaller_font.render('CLEAR', True, 'black'), (45, 780))
    button_list.append(clear)

    all_in = pygame.draw.rect(screen, 'white', [205, 770, 150, 55], 0, 5)
    pygame.draw.rect(screen, 'black', [205, 770, 150, 55], 3, 5)
    screen.blit(smaller_font.render('ALL IN', True, 'black'), (215, 780))
    button_list.append(all_in)

    deal = pygame.draw.rect(screen, 'green', [380, 770, 170, 55], 0, 5)
    pygame.draw.rect(screen, 'white', [380, 770, 170, 55], 3, 5)
    screen.blit(smaller_font.render('DEAL', True, 'white'), (420, 780))
    button_list.append(deal)

    return button_list


def draw_game():
    button_list = []

    if active and outcome == 0 and not game_over:
        hit = pygame.draw.rect(screen, 'white', [0, 700, 300, 100], 0, 5)
        pygame.draw.rect(screen, 'green', [0, 700, 300, 100], 3, 5)
        screen.blit(font.render('HIT ME', True, 'black'), (55, 735))
        button_list.append(hit)

        stand = pygame.draw.rect(screen, 'white', [300, 700, 300, 100], 0, 5)
        pygame.draw.rect(screen, 'green', [300, 700, 300, 100], 3, 5)
        screen.blit(font.render('STAND', True, 'black'), (355, 735))
        button_list.append(stand)

    if outcome != 0 and not game_over:
        # [dn] zelfde opmerking met je kleuren: je kan highlight = 'gold' gebruiken
        # als je de kleur dan ooit wilt aanpassen 
        result_box = pygame.draw.rect(screen, 'black', [110, 135, 380, 60], 0, 8)
        pygame.draw.rect(screen, 'gold', [110, 135, 380, 60], 3, 8)

        result_text = font.render(results[outcome], True, 'white')
        result_rect = result_text.get_rect(center=result_box.center)
        screen.blit(result_text, result_rect)

        new_hand = pygame.draw.rect(screen, 'white', [150, 720, 300, 80], 0, 5)
        pygame.draw.rect(screen, 'green', [150, 720, 300, 80], 3, 5)
        screen.blit(font.render('NEW HAND', True, 'black'), (175, 740))
        button_list.append(new_hand)

    if game_over:
        game_over_box = pygame.draw.rect(screen, 'black', [120, 315, 360, 90], 0, 8)
        pygame.draw.rect(screen, 'gold', [120, 315, 360, 90], 4, 8)

        game_over_text = font.render('GAME OVER', True, 'white')
        game_over_rect = game_over_text.get_rect(center=game_over_box.center)
        screen.blit(game_over_text, game_over_rect)

        restart = pygame.draw.rect(screen, 'white', [150, 720, 300, 80], 0, 5)
        pygame.draw.rect(screen, 'green', [150, 720, 300, 80], 3, 5)
        screen.blit(font.render('RESTART', True, 'black'), (175, 740))
        button_list.append(restart)

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
    # [dn] hier zie je al meteen dat het wel heel veel variabelen zijn die je gaat gebruiken
    # later in de methode zijn er ook veel geneste blokken (if/else/while's)
    # de beste manier om dit overzichtelijk te houden 
    global active, initial_deal, game_deck
    global my_hand, dealer_hand, outcome
    global hand_active, reveal_dealer, add_score
    global dealer_score, player_score, betting_active
    global paid_out, dealer_draw_time, natural_blackjack

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
    natural_blackjack = False

    dealer_score = 0
    player_score = 0
    dealer_draw_time = 0


run = True

while run:
    timer.tick(fps)
    screen.fill((0, 90, 40))

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

        draw_labels()
        draw_cards(my_hand, dealer_hand, reveal_dealer)
        draw_scores(player_score, dealer_score)

        if hand_active and len(my_hand) == 2 and player_score == 21:
            natural_blackjack = True
            outcome = 2
            hand_active = False
            reveal_dealer = True

            if add_score:
                records[0] += 1
                add_score = False

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

    if betting_active and not active and not game_over:
        betting_buttons = draw_betting_buttons()

    buttons = draw_game()

    if outcome != 0 and not paid_out:
        if outcome == 2:
            if natural_blackjack:
                balance += int(current_bet * 1.5)
            else:
                balance += current_bet

        elif outcome == 1 or outcome == 3:
            balance -= current_bet

        paid_out = True

        if balance <= 0 and outcome != 0:
            balance = 0
            game_over = True
            betting_active = False
            reveal_dealer = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONUP:

            if game_over:
                # [dn] hier kan je wat indentatie sparen door game_over ook in de if hieronder te steken
                if len(buttons) > 0 and buttons[0].collidepoint(event.pos):
                    # [dn] ook al gebruik je het maar 1 keer, het zou properder zijn als je dit bovenaan definieert 
                    balance = 1000 
                    current_bet = 0
                    outcome = 0
                    records = [0, 0, 0]

                    active = False
                    betting_active = True
                    game_over = False

                    reveal_dealer = False
                    hand_active = False
                    paid_out = False
                    natural_blackjack = False

                    my_hand = []
                    dealer_hand = []

            elif betting_active and not active:
                # [dn] deze blok kan wat properder door te loopen over de buttons
                # de actie (de code in de (if collidepoint) kan een array wan lamda's zijn,
                # of je maakt een struct (button, lambda)
                if betting_buttons[0].collidepoint(event.pos):
                    if balance >= current_bet + 10:
                        current_bet += 10

                elif betting_buttons[1].collidepoint(event.pos):
                    if balance >= current_bet + 50:
                        current_bet += 50

                elif betting_buttons[2].collidepoint(event.pos):
                    if balance >= current_bet + 100:
                        current_bet += 100

                elif betting_buttons[3].collidepoint(event.pos):
                    if balance >= current_bet + 500:
                        current_bet += 500

                elif betting_buttons[4].collidepoint(event.pos):
                    current_bet = 0

                elif betting_buttons[5].collidepoint(event.pos):
                    current_bet = balance

                elif betting_buttons[6].collidepoint(event.pos):
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
                    paid_out = False
                    natural_blackjack = False
                    my_hand = []
                    dealer_hand = []

    pygame.display.flip()

pygame.quit()
