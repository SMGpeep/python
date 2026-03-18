import pygame
import sys
from collections import namedtuple
import random

# ------- Constants for Card Visualization -------
CARD_WIDTH = 80
CARD_HEIGHT = 120
CARD_SPACING = 20
CARD_CORNER_RADIUS = 12
MARGIN = 30

BACKGROUND_COLOR = (0, 120, 0)
CARD_COLOR = (255, 255, 255)
CARD_BORDER_COLOR = (0, 0, 0)
TEXT_COLOR = (0, 0, 0)

WINDOW_WIDTH = 5 * (CARD_WIDTH + CARD_SPACING) + 2 * MARGIN
WINDOW_HEIGHT = 480

pygame.init()
pygame.font.init()
font = pygame.font.SysFont('Arial', 24, bold=True)

Card = namedtuple('Card', ['rank', 'suit'])

class Deck:
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
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

    def __repr__(self):
        return f"Deck({self.cards})"

def draw_card(surface, card, x, y):
    # Draw card body
    pygame.draw.rect(surface, CARD_COLOR, (x, y, CARD_WIDTH, CARD_HEIGHT), border_radius=CARD_CORNER_RADIUS)
    pygame.draw.rect(surface, CARD_BORDER_COLOR, (x, y, CARD_WIDTH, CARD_HEIGHT), 2, border_radius=CARD_CORNER_RADIUS)
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

def visualize_deck_with_pygame():
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Deck Visualizer')
    clock = pygame.time.Clock()
    deck = Deck()
    deck.shuffle()
    dealt = []
    run = True

    instructions_font = pygame.font.SysFont('Arial', 22)
    small_font = pygame.font.SysFont('Arial', 18)
    instructions = [
        'Space: Deal 5 More Cards',
        'R: Shuffle Deck',
        'Esc/Quit: Exit',
    ]

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                if event.key == pygame.K_SPACE:
                    # Deal 5, append to dealt
                    if len(deck) > 0:
                        dealt.extend(deck.deal(min(5, len(deck))))
                if event.key == pygame.K_r:
                    # Reset and shuffle
                    deck = Deck()
                    deck.shuffle()
                    dealt = []

        screen.fill(BACKGROUND_COLOR)

        # Draw instructions
        for i, text in enumerate(instructions):
            inst_surf = instructions_font.render(text, True, (255, 255, 255))
            screen.blit(inst_surf, (MARGIN, 12 + 28 * i))

        # Draw dealt cards
        y_offset = 120
        dealt_to_draw = dealt[-5:]  # Only show the last 5 dealt
        for i, card in enumerate(dealt_to_draw):
            x = MARGIN + i * (CARD_WIDTH + CARD_SPACING)
            y = y_offset
            draw_card(screen, card, x, y)

        # If deck has cards left, show a deck representation
        remaining = len(deck)
        deck_text = f"Cards Left: {remaining}"
        dt_surf = small_font.render(deck_text, True, (255,255,255))
        screen.blit(dt_surf, (WINDOW_WIDTH - 160, y_offset + CARD_HEIGHT + 12))

        # Deck pile - back of card
        if remaining > 0:
            x = WINDOW_WIDTH // 2 - CARD_WIDTH // 2
            y = WINDOW_HEIGHT - CARD_HEIGHT - 62
            # Make a stack visualization
            for i in range(min(4, remaining)):
                ox = x + 2*i
                oy = y + 2*i
                pygame.draw.rect(
                    screen,
                    (50, 50, 120),
                    (ox, oy, CARD_WIDTH, CARD_HEIGHT),
                    border_radius=CARD_CORNER_RADIUS
                )
                pygame.draw.rect(
                    screen,
                    (10, 10, 40),
                    (ox, oy, CARD_WIDTH, CARD_HEIGHT),
                    3,
                    border_radius=CARD_CORNER_RADIUS
                )
            back_text = small_font.render("Deck", True, (200, 200, 255))
            screen.blit(back_text, (x + 10, y + CARD_HEIGHT // 2 - 9))

        pygame.display.flip()
        clock.tick(30)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    visualize_deck_with_pygame()