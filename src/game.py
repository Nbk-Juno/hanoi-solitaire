import random

# Handle imports for both package and direct execution
try:
    from .constants import RANKS
except ImportError:
    from constants import RANKS


class Card:
    """Represents a playing card with a rank and suit."""

    def __init__(self, rank, suit="hearts"):
        if rank not in RANKS:
            raise ValueError(f"Invalid rank: {rank}")
        self.rank = rank
        self.suit = suit

    @property
    def value(self):
        """Returns the numeric value of the card (1-9)."""
        if self.rank == "A":
            return 1
        return int(self.rank)

    @property
    def display_name(self):
        """Returns the display name of the card."""
        return "Ace" if self.rank == "A" else self.rank

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value

    def __eq__(self, other):
        return self.value == other.value

    def __repr__(self):
        return f"Card({self.rank}, {self.suit})"

    def __str__(self):
        return f"{self.display_name} of {self.suit}"


class Pile:
    """Represents a pile (stack) of cards."""

    def __init__(self):
        self.cards = []

    def push(self, card):
        """Add a card to the top of the pile."""
        self.cards.append(card)

    def pop(self):
        """Remove and return the top card from the pile."""
        if self.is_empty():
            raise IndexError("Cannot pop from empty pile")
        return self.cards.pop()

    def peek(self):
        """Return the top card without removing it."""
        if self.is_empty():
            return None
        return self.cards[-1]

    def is_empty(self):
        """Check if the pile is empty."""
        return len(self.cards) == 0

    def size(self):
        """Return the number of cards in the pile."""
        return len(self.cards)

    def __repr__(self):
        return f"Pile({self.size()} cards)"

    def __str__(self):
        if self.is_empty():
            return "Empty pile"
        return f"Pile: {', '.join(str(card) for card in self.cards)}"


class HanoiGame:
    """Main game class that manages the Hanoi Solitaire game state."""

    def __init__(self, suit="hearts"):
        self.suit = suit
        self.piles = [Pile(), Pile(), Pile()]
        self.move_count = 0
        self.move_history = []
        self._initialize_game()

    def _initialize_game(self):
        """Initialize the game with 9 cards distributed randomly 3-3-3."""
        # Create 9 cards (Ace through 9)
        cards = [Card(rank, self.suit) for rank in RANKS]

        # Shuffle randomly
        random.shuffle(cards)

        # Distribute 3-3-3 to the three piles
        for i in range(3):
            for j in range(3):
                self.piles[i].push(cards[i * 3 + j])

    def reset(self):
        """Reset the game with a new random configuration."""
        # Clear all piles
        self.piles = [Pile(), Pile(), Pile()]
        self.move_count = 0
        self.move_history = []

        # Reinitialize with new random distribution
        self._initialize_game()

    def is_valid_move(self, from_pile_idx, to_pile_idx):
        """
        Check if a move from one pile to another is valid.

        Args:
            from_pile_idx: Index of source pile (0, 1, or 2)
            to_pile_idx: Index of destination pile (0, 1, or 2)

        Returns:
            bool: True if move is valid, False otherwise
        """
        # Check for valid pile indices
        if not (0 <= from_pile_idx <= 2 and 0 <= to_pile_idx <= 2):
            return False

        # Can't move to the same pile
        if from_pile_idx == to_pile_idx:
            return False

        from_pile = self.piles[from_pile_idx]
        to_pile = self.piles[to_pile_idx]

        # Can't move from empty pile
        if from_pile.is_empty():
            return False

        # Get the card to be moved (top of from_pile)
        moving_card = from_pile.peek()

        # Can always move to empty pile
        if to_pile.is_empty():
            return True

        # Can only place smaller card on larger card
        top_card = to_pile.peek()
        return moving_card < top_card

    def make_move(self, from_pile_idx, to_pile_idx):
        """
        Execute a move from one pile to another.

        Args:
            from_pile_idx: Index of source pile (0, 1, or 2)
            to_pile_idx: Index of destination pile (0, 1, or 2)

        Returns:
            bool: True if move was successful, False if move was invalid
        """
        # First validate the move
        if not self.is_valid_move(from_pile_idx, to_pile_idx):
            return False

        # Execute the move
        from_pile = self.piles[from_pile_idx]
        to_pile = self.piles[to_pile_idx]

        # Remove card from source pile
        card = from_pile.pop()

        # Add card to destination pile
        to_pile.push(card)

        # Increment move counter
        self.move_count += 1

        # Store move in history (for undo feature later)
        self.move_history.append((from_pile_idx, to_pile_idx))

        return True

    def is_game_won(self):
        """
        Check if the game is won.

        Game is won when all 9 cards are in a single pile,
        stacked in perfect descending order (9 at bottom, Ace at top).

        Returns:
            bool: True if game is won, False otherwise
        """
        # Find which pile has cards (should be exactly one with 9 cards)
        full_pile = None
        for pile in self.piles:
            if pile.size() == 9:
                full_pile = pile
            elif pile.size() > 0:
                # If any other pile has cards, game is not won
                return False

        # If no pile has 9 cards, game is not won
        if full_pile is None:
            return False

        # Check if cards are in perfect descending order
        # Cards should be [9, 8, 7, 6, 5, 4, 3, 2, 1] from bottom to top
        expected_values = [9, 8, 7, 6, 5, 4, 3, 2, 1]
        actual_values = [card.value for card in full_pile.cards]

        return actual_values == expected_values

    def undo(self):
        """
        Undo the last move.

        Returns:
            bool: True if undo was successful, False if no moves to undo
        """
        if not self.move_history:
            return False

        # Get last move
        from_pile_idx, to_pile_idx = self.move_history.pop()

        # Reverse the move (swap from and to)
        to_pile = self.piles[to_pile_idx]
        from_pile = self.piles[from_pile_idx]

        # Move card back
        card = to_pile.pop()
        from_pile.push(card)

        # Decrement move counter
        self.move_count -= 1

        return True

    def __repr__(self):
        return f"HanoiGame(moves={self.move_count})"

    def __str__(self):
        result = [f"Hanoi Solitaire - Moves: {self.move_count}\n"]
        for i, pile in enumerate(self.piles):
            result.append(f"Pile {i}: {pile}")
        return "\n".join(result)

