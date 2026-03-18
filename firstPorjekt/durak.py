import pygame
import sys
import random
from collections import namedtuple

# Constants for Card Visualization
CARD_WIDTH = 80
CARD_HEIGHT = 120
CARD_SPACING = 20
CARD_CORNER_RADIUS = 12
MARGIN = 30

BACKGROUND_COLOR = (0, 120, 0)
CARD_COLOR = (255, 255, 255)
CARD_BORDER_COLOR = (0, 0, 0)
TEXT_COLOR = (0, 0, 0)

WINDOW_WIDTH = 8 * (CARD_WIDTH + CARD_SPACING) + 2 * MARGIN
WINDOW_HEIGHT = 600

pygame.init()
pygame.font.init()
font = pygame.font.SysFont('Arial', 24, bold=True)
small_font = pygame.font.SysFont('Arial', 18)

Card = namedtuple('Card', ['rank', 'suit'])

class Deck:
    ranks = ['6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']

    suit_symbols = {
        'Hearts': '\u2665',
        'Diamonds': '\u2666',
        'Clubs': '\u2663',
        'Spades': '\u2660',
    }

    def __init__(self):
        self.cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, num=1):
        dealt_cards = self.cards[:num]
        self.cards = self.cards[num:]
        return dealt_cards

    def __len__(self):
        return len(self.cards)

def draw_card(surface, card, x, y, highlight=False):
    # Draw card body
    color = CARD_COLOR
    bordercol = (255, 215, 0) if highlight else CARD_BORDER_COLOR
    pygame.draw.rect(surface, color, (x, y, CARD_WIDTH, CARD_HEIGHT), border_radius=CARD_CORNER_RADIUS)
    pygame.draw.rect(surface, bordercol, (x, y, CARD_WIDTH, CARD_HEIGHT), 3 if highlight else 2, border_radius=CARD_CORNER_RADIUS)
    # Draw rank
    rank_surface = font.render(card.rank, True, TEXT_COLOR)
    surface.blit(rank_surface, (x + 8, y + 6))
    # Draw suit
    symbol = Deck.suit_symbols[card.suit]
    symbol_color = (220, 0, 0) if card.suit in ("Hearts", "Diamonds") else (0, 0, 0)
    suit_surface = font.render(symbol, True, symbol_color)
    surface.blit(suit_surface, (x + CARD_WIDTH - 28, y + 6))
    # Draw center suit
    center_surface = font.render(symbol, True, symbol_color)
    cs_rect = center_surface.get_rect(center=(x + CARD_WIDTH // 2, y + CARD_HEIGHT // 2))
    surface.blit(center_surface, cs_rect)

def card_less(card1, card2, trump_suit):
    """Returns True if card1 < card2 for Durak rules, given trump_suit."""
    if card1.suit == card2.suit:
        return Deck.ranks.index(card1.rank) < Deck.ranks.index(card2.rank)
    elif card1.suit == trump_suit and card2.suit != trump_suit:
        return False
    elif card1.suit != trump_suit and card2.suit == trump_suit:
        return True
    else:
        return False

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def add_cards(self, cards):
        self.hand.extend(cards)

    def remove_card(self, card):
        self.hand.remove(card)

    def has_cards(self):
        return len(self.hand) > 0

    def lowest_trump(self, trump_suit):
        # Used to determine the first attacker if needed
        trump_cards = [c for c in self.hand if c.suit == trump_suit]
        return min(trump_cards, key=lambda c: Deck.ranks.index(c.rank)) if trump_cards else None

def sort_hand(hand, trump):
    """Sort hand: non-trump by suit, then trump by rank at the end."""
    def key(card):
        suit_value = (1 if card.suit == trump else 0)
        return (suit_value, Deck.suits.index(card.suit), Deck.ranks.index(card.rank))
    return sorted(hand, key=key)

def setup_game(player_num=2):
    deck = Deck()
    deck.shuffle()
    players = [Player("You"), Player("Computer")]
    for player in players:
        player.add_cards(deck.deal(6))
    trump_card = deck.cards[-1] if deck.cards else None
    trump_suit = trump_card.suit if trump_card else random.choice(Deck.suits)
    return deck, players, trump_suit, trump_card

def next_player_idx(idx, player_count):
    return (idx + 1) % player_count

def find_attacker(players, trump_suit):
    # Attacker: player with lowest trump
    lowest = None
    attacker_idx = 0
    for i, player in enumerate(players):
        lt = player.lowest_trump(trump_suit)
        if lt and (lowest is None or card_less(lt, lowest, trump_suit)):
            lowest = lt
            attacker_idx = i
    return attacker_idx

def valid_attack_cards(hand, table):
    # Can play any card matching a rank on table, or any card if table is empty
    attackers = hand[:]
    if not table:
        return attackers
    ranks_on_table = set(card.rank for pair in table for card in pair if card)
    return [c for c in hand if c.rank in ranks_on_table]

def valid_defend_cards(hand, attack_card, trump):
    # Must beat attack card or use trump
    valids = []
    for c in hand:
        if c.suit == attack_card.suit and Deck.ranks.index(c.rank) > Deck.ranks.index(attack_card.rank):
            valids.append(c)
        elif c.suit == trump and attack_card.suit != trump:
            valids.append(c)
    return valids

def refill_hand(deck, players, start_idx):
    # In order from attacker onward, refill hands to 6 if possible
    for i in range(len(players)):
        idx = (start_idx + i) % len(players)
        player = players[idx]
        need = 6 - len(player.hand)
        if need > 0:
            player.add_cards(deck.deal(need))

def render_durak_game(screen, players, deck, table, trump_suit, trump_card, attacker_idx, defender_idx, selected_card, status, player_view_idx=0):
    screen.fill(BACKGROUND_COLOR)
    info_font = pygame.font.SysFont('Arial', 21)
    # Draw trump card and label
    suit_symbol = Deck.suit_symbols[trump_suit]
    tc_text = f"Trump: {trump_suit} {suit_symbol}"
    tc_surf = info_font.render(tc_text, True, (255, 255, 255))
    screen.blit(tc_surf, (MARGIN, 12))

    # Deck size
    d_text = f"Cards Left In Deck: {len(deck)}"
    d_surf = small_font.render(d_text, True, (255, 255, 255))
    screen.blit(d_surf, (WINDOW_WIDTH - 270, 18))
    
    # Draw trump card
    if trump_card:
        draw_card(screen, trump_card, WINDOW_WIDTH - MARGIN - CARD_WIDTH, MARGIN, highlight=True)

    # Draw computer's hand (back only)
    comp_x = MARGIN
    comp_y = 70
    n_comp = len(players[1].hand)
    for i in range(n_comp):
        # All back
        pygame.draw.rect(
            screen,
            (50, 50, 120),
            (comp_x + i * (CARD_WIDTH // 3), comp_y, CARD_WIDTH, CARD_HEIGHT),
            border_radius=CARD_CORNER_RADIUS
        )
        pygame.draw.rect(
            screen,
            (10, 10, 40),
            (comp_x + i * (CARD_WIDTH // 3), comp_y, CARD_WIDTH, CARD_HEIGHT),
            3,
            border_radius=CARD_CORNER_RADIUS
        )

    comp_txt = small_font.render(f"Computer ({n_comp})", True, (200, 200, 240))
    screen.blit(comp_txt, (comp_x, comp_y - 20))

    # Draw play area (table)
    tb_x = MARGIN
    tb_y = 260
    spacing = CARD_WIDTH + 20
    for idx, (atk, df) in enumerate(table):
        x = tb_x + idx * spacing
        if atk:
            draw_card(screen, atk, x, tb_y)
        if df:
            draw_card(screen, df, x + 35, tb_y + 24, highlight=True)

    # Draw your hand
    player = players[0]
    hand = sort_hand(player.hand, trump_suit)
    p_x = MARGIN
    p_y = WINDOW_HEIGHT - CARD_HEIGHT - 55
    for i, card in enumerate(hand):
        hl = (card == selected_card)
        draw_card(screen, card, p_x + i * (CARD_WIDTH + CARD_SPACING), p_y, highlight=hl)

    you_txt = small_font.render(f"You ({len(player.hand)})", True, (200, 220, 255))
    screen.blit(you_txt, (p_x, p_y - 22))

    # Draw instructions/status
    instructions = [
        'Space: End turn / Pass',
        'Click on your cards to play.',
        'ESC: Quit'
    ]
    for i, text in enumerate(instructions):
        inst_surf = small_font.render(text, True, (225,225,225))
        screen.blit(inst_surf, (MARGIN, WINDOW_HEIGHT - 34 - 22 * i))

    # Status zone
    stat_surf = info_font.render(status, True, (238,246,84))
    screen.blit(stat_surf, (MARGIN, tb_y - 40))

def main():
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Durak')
    clock = pygame.time.Clock()
    deck, players, trump_suit, trump_card = setup_game()
    n_players = 2
    table = [] # List of (attack_card, defense_card) pairs
    attacker_idx = find_attacker(players, trump_suit)
    defender_idx = next_player_idx(attacker_idx, n_players)

    # Game state
    status = "Your move! You attack."
    attack_mode = True  # True: attack phase, False: defend phase
    selected_card = None
    finished = False

    while True:
        # Handle Game End
        if not players[0].has_cards() and not len(deck):
            status = "You win! Press ESC to quit."
            finished = True
        elif not players[1].has_cards() and not len(deck):
            status = "Computer wins! Press ESC to quit."
            finished = True

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()
                if finished:
                    continue
                if event.key == pygame.K_SPACE:
                    # Space = End turn / Pass / Take
                    if attack_mode:
                        # Cannot end attack if table empty
                        if table:
                            attack_mode = False
                            status = "Defend!"
                    else:
                        # Defender chooses to take cards
                        # Defender picks up all cards on table; no defense
                        taking_player = players[defender_idx]
                        for pair in table:
                            if pair[0]:
                                taking_player.add_cards([pair[0]])
                            if pair[1]:
                                taking_player.add_cards([pair[1]])
                        table = []
                        # Refill
                        refill_hand(deck, players, attacker_idx)
                        # Roles don't change: defender stays defender next
                        attack_mode = True
                        # If hands empty, victory handled at loop top
                        status = "Your move!" if attacker_idx == 0 else "Computer attacks!"
                        selected_card = None
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not finished:
                mx, my = pygame.mouse.get_pos()
                # Only the player can click cards: attack or defend
                hand = sort_hand(players[0].hand, trump_suit)
                # Find if click is on a card
                p_y = WINDOW_HEIGHT - CARD_HEIGHT - 55
                card_clicked = None
                for i, card in enumerate(hand):
                    x = MARGIN + i * (CARD_WIDTH + CARD_SPACING)
                    rect = pygame.Rect(x, p_y, CARD_WIDTH, CARD_HEIGHT)
                    if rect.collidepoint(mx, my):
                        card_clicked = card
                        break
                if card_clicked and not finished:
                    if attack_mode and attacker_idx == 0:
                        # Your turn to attack
                        valids = valid_attack_cards(hand, table)
                        if card_clicked in valids:
                            table.append((card_clicked, None))
                            players[0].remove_card(card_clicked)
                            status = "Attack card played. Space to end attack or add more."
                    # If defending and you are defender
                    elif not attack_mode and defender_idx == 0:
                        # Find card to defend (first undefended)
                        for idx, (atk, df) in enumerate(table):
                            if atk and not df:
                                attack_card = atk
                                break
                        else:
                            attack_card = None
                        if attack_card:
                            valids = valid_defend_cards(hand, attack_card, trump_suit)
                            if card_clicked in valids:
                                table[idx] = (attack_card, card_clicked)
                                players[0].remove_card(card_clicked)
                                status = "Defended! Space to end turn or defend another."
                                # If all pairs defended and table full, end turn automatically soon

        # --- Computer AI Logic ---
        if not finished:
            # Computer's turn to attack
            if attack_mode and attacker_idx == 1 and (not table or len(table) < 6):
                comp = players[1]
                # Find allowed attack cards
                valids = valid_attack_cards(comp.hand, table)
                if valids:
                    # Play the lowest
                    play = sorted(valids, key=lambda c: (c.suit != trump_suit, Deck.ranks.index(c.rank)))[0]
                    table.append((play, None))
                    comp.remove_card(play)
                    status = "Computer attacks!"
                    pygame.time.delay(500)
                else:
                    # End attack
                    attack_mode = False
                    status = "Your move to defend!"
                    pygame.time.delay(600)
            # Computer's turn to defend
            elif not attack_mode and defender_idx == 1:
                comp = players[1]
                made_defense = False
                for idx, (atk, df) in enumerate(table):
                    if atk and not df:
                        valids = valid_defend_cards(comp.hand, atk, trump_suit)
                        if valids:
                            play = sorted(valids, key=lambda c: (c.suit != trump_suit, Deck.ranks.index(c.rank)))[0]
                            table[idx] = (atk, play)
                            comp.remove_card(play)
                            made_defense = True
                            status = "Computer defends!"
                            pygame.time.delay(600)
                        # else: can't defend, will have to take
                # Check if all pairs are defended or defender can't defend
                all_defended = all(atk and df for atk, df in table)
                defender_can_defend_more = False
                for atk, df in table:
                    if atk and not df:
                        if valid_defend_cards(comp.hand, atk, trump_suit):
                            defender_can_defend_more = True
                if all_defended or not defender_can_defend_more:
                    # Table is resolved: discard all and refill
                    table = []
                    refill_hand(deck, players, attacker_idx)
                    # Roles switch: defender becomes attacker
                    attacker_idx, defender_idx = defender_idx, attacker_idx
                    attack_mode = True
                    status = "Your move!" if attacker_idx == 0 else "Computer attacks!"
                    pygame.time.delay(900)
        # If attack is over and all pairs are defended, clean up table & switch roles
        if not attack_mode and not finished:
            all_defended = all(atk and df for atk, df in table)
            defender_has_cards = players[defender_idx].has_cards()
            if all_defended:
                table = []
                refill_hand(deck, players, attacker_idx)
                attacker_idx, defender_idx = defender_idx, attacker_idx
                attack_mode = True
                status = "Your move!" if attacker_idx == 0 else "Computer attacks!"
                selected_card = None

        # Render
        render_durak_game(screen, players, deck, table, trump_suit, trump_card, attacker_idx, defender_idx, selected_card, status)

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()

