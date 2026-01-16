"""Comprehensive unit tests for Hanoi Solitaire game logic."""

import pytest
from src.game import Card, Pile, HanoiGame


# ============================================================================
# Card Tests
# ============================================================================

def test_card_creation():
    """Test basic card creation with rank and suit."""
    card = Card("A", "hearts")
    assert card.rank == "A"
    assert card.suit == "hearts"


def test_card_value_ace():
    """Test that Ace has value 1."""
    ace = Card("A", "hearts")
    assert ace.value == 1


def test_card_value_numbers():
    """Test that number cards have correct values."""
    two = Card("2", "hearts")
    nine = Card("9", "hearts")
    assert two.value == 2
    assert nine.value == 9


def test_card_display_name_ace():
    """Test that Ace displays as 'Ace'."""
    ace = Card("A", "hearts")
    assert ace.display_name == "Ace"


def test_card_display_name_numbers():
    """Test that number cards display their rank."""
    two = Card("2", "hearts")
    nine = Card("9", "hearts")
    assert two.display_name == "2"
    assert nine.display_name == "9"


def test_card_comparisons():
    """Test card comparison operators."""
    ace = Card("A", "hearts")
    two = Card("2", "hearts")
    nine = Card("9", "hearts")

    # Less than
    assert ace < two
    assert two < nine
    assert ace < nine

    # Greater than
    assert nine > two
    assert two > ace
    assert nine > ace

    # Equality
    assert ace == Card("A", "diamonds")  # Same value, different suit
    assert not (ace == two)


def test_card_invalid_rank():
    """Test that invalid rank raises ValueError."""
    with pytest.raises(ValueError, match="Invalid rank"):
        Card("10", "hearts")  # Only 1-9 and A are valid


# ============================================================================
# Pile Tests
# ============================================================================

def test_pile_creation():
    """Test creating an empty pile."""
    pile = Pile()
    assert pile.is_empty()
    assert pile.size() == 0


def test_pile_push_pop():
    """Test pushing and popping cards from pile."""
    pile = Pile()
    card1 = Card("A", "hearts")
    card2 = Card("9", "hearts")

    pile.push(card1)
    pile.push(card2)

    assert pile.size() == 2
    assert pile.pop() == card2  # Last in, first out
    assert pile.size() == 1
    assert pile.pop() == card1
    assert pile.is_empty()


def test_pile_peek():
    """Test peeking at top card without removing it."""
    pile = Pile()
    card = Card("5", "hearts")

    pile.push(card)
    assert pile.peek() == card
    assert pile.size() == 1  # Card still there


def test_pile_is_empty():
    """Test empty pile detection."""
    pile = Pile()
    assert pile.is_empty()

    pile.push(Card("A", "hearts"))
    assert not pile.is_empty()

    pile.pop()
    assert pile.is_empty()


def test_pile_size():
    """Test pile size tracking."""
    pile = Pile()
    assert pile.size() == 0

    ranks = ["A", "2", "3", "4", "5"]
    for i, rank in enumerate(ranks):
        pile.push(Card(rank, "hearts"))
        assert pile.size() == i + 1


def test_pile_pop_empty_raises_error():
    """Test that popping from empty pile raises IndexError."""
    pile = Pile()
    with pytest.raises(IndexError, match="Cannot pop from empty pile"):
        pile.pop()


def test_pile_peek_empty_returns_none():
    """Test that peeking at empty pile returns None."""
    pile = Pile()
    assert pile.peek() is None


# ============================================================================
# HanoiGame Initialization Tests
# ============================================================================

def test_game_initialization():
    """Test that game initializes properly."""
    game = HanoiGame()
    assert game is not None
    assert game.suit == "hearts"
    assert game.move_count == 0
    assert game.move_history == []


def test_game_has_three_piles():
    """Test that game creates exactly three piles."""
    game = HanoiGame()
    assert len(game.piles) == 3
    assert all(isinstance(pile, Pile) for pile in game.piles)


def test_game_creates_nine_cards():
    """Test that game creates exactly 9 cards total."""
    game = HanoiGame()
    total_cards = sum(pile.size() for pile in game.piles)
    assert total_cards == 9


def test_game_distributes_3_3_3():
    """Test that cards are distributed 3-3-3 across piles."""
    game = HanoiGame()
    assert game.piles[0].size() == 3
    assert game.piles[1].size() == 3
    assert game.piles[2].size() == 3


def test_game_move_count_starts_at_zero():
    """Test that move counter starts at 0."""
    game = HanoiGame()
    assert game.move_count == 0


def test_game_randomization():
    """Test that multiple games have different distributions."""
    # Create 10 games and check if they're not all identical
    games = [HanoiGame() for _ in range(10)]

    # Get top card values from each game
    top_cards = []
    for game in games:
        tops = tuple(pile.peek().value for pile in game.piles)
        top_cards.append(tops)

    # At least some games should have different top card configurations
    unique_configurations = len(set(top_cards))
    assert unique_configurations > 1, "Games should have random distributions"


# ============================================================================
# Move Validation Tests
# ============================================================================

def test_is_valid_move_smaller_on_larger():
    """Test that smaller card can be placed on larger card."""
    game = HanoiGame()

    # Manually set up a scenario: pile 0 has Ace (1) on top, pile 1 has 5 on top
    game.piles[0] = Pile()
    game.piles[0].push(Card("A", "hearts"))

    game.piles[1] = Pile()
    game.piles[1].push(Card("5", "hearts"))

    # Ace (1) on 5 should be valid
    assert game.is_valid_move(0, 1)


def test_is_valid_move_larger_on_smaller_invalid():
    """Test that larger card cannot be placed on smaller card."""
    game = HanoiGame()

    # pile 0 has 5 on top, pile 1 has Ace on top
    game.piles[0] = Pile()
    game.piles[0].push(Card("5", "hearts"))

    game.piles[1] = Pile()
    game.piles[1].push(Card("A", "hearts"))

    # 5 on Ace should be invalid
    assert not game.is_valid_move(0, 1)


def test_is_valid_move_to_empty_pile():
    """Test that any card can be moved to empty pile."""
    game = HanoiGame()

    # pile 0 has a card, pile 1 is empty
    game.piles[0] = Pile()
    game.piles[0].push(Card("5", "hearts"))

    game.piles[1] = Pile()

    # Should be valid to move to empty pile
    assert game.is_valid_move(0, 1)


def test_is_valid_move_from_empty_pile_invalid():
    """Test that moving from empty pile is invalid."""
    game = HanoiGame()

    # pile 0 is empty, pile 1 has a card
    game.piles[0] = Pile()

    game.piles[1] = Pile()
    game.piles[1].push(Card("5", "hearts"))

    # Should be invalid to move from empty pile
    assert not game.is_valid_move(0, 1)


def test_is_valid_move_same_pile_invalid():
    """Test that moving to the same pile is invalid."""
    game = HanoiGame()
    assert not game.is_valid_move(0, 0)
    assert not game.is_valid_move(1, 1)
    assert not game.is_valid_move(2, 2)


def test_is_valid_move_invalid_indices():
    """Test that invalid pile indices are rejected."""
    game = HanoiGame()

    # Negative indices
    assert not game.is_valid_move(-1, 0)
    assert not game.is_valid_move(0, -1)

    # Indices >= 3
    assert not game.is_valid_move(3, 0)
    assert not game.is_valid_move(0, 5)


# ============================================================================
# Move Execution Tests
# ============================================================================

def test_make_move_success():
    """Test successful move execution."""
    game = HanoiGame()

    # Set up: pile 0 has Ace, pile 1 has 5
    game.piles[0] = Pile()
    game.piles[0].push(Card("A", "hearts"))

    game.piles[1] = Pile()
    game.piles[1].push(Card("5", "hearts"))

    # Move should succeed
    result = game.make_move(0, 1)
    assert result is True


def test_make_move_increments_counter():
    """Test that move counter increments after valid move."""
    game = HanoiGame()

    # Set up valid move scenario
    game.piles[0] = Pile()
    game.piles[0].push(Card("A", "hearts"))

    game.piles[1] = Pile()
    game.piles[1].push(Card("5", "hearts"))

    initial_count = game.move_count
    game.make_move(0, 1)

    assert game.move_count == initial_count + 1


def test_make_move_updates_piles():
    """Test that piles are updated correctly after move."""
    game = HanoiGame()

    # Set up: pile 0 has Ace, pile 1 has 5
    ace = Card("A", "hearts")
    five = Card("5", "hearts")

    game.piles[0] = Pile()
    game.piles[0].push(ace)

    game.piles[1] = Pile()
    game.piles[1].push(five)

    # Execute move
    game.make_move(0, 1)

    # Verify state
    assert game.piles[0].is_empty()
    assert game.piles[1].size() == 2
    assert game.piles[1].peek() == ace  # Ace should be on top


def test_make_move_stores_history():
    """Test that move history is recorded."""
    game = HanoiGame()

    # Set up valid move scenario
    game.piles[0] = Pile()
    game.piles[0].push(Card("A", "hearts"))

    game.piles[1] = Pile()

    # Execute move
    game.make_move(0, 1)

    # Verify history
    assert len(game.move_history) == 1
    assert game.move_history[0] == (0, 1)


def test_make_move_invalid_returns_false():
    """Test that invalid move returns False."""
    game = HanoiGame()

    # Set up invalid move: larger on smaller
    game.piles[0] = Pile()
    game.piles[0].push(Card("9", "hearts"))

    game.piles[1] = Pile()
    game.piles[1].push(Card("A", "hearts"))

    # Move should fail
    result = game.make_move(0, 1)
    assert result is False


def test_make_move_invalid_no_state_change():
    """Test that invalid move doesn't change game state."""
    game = HanoiGame()

    # Set up invalid move
    game.piles[0] = Pile()
    game.piles[0].push(Card("9", "hearts"))

    game.piles[1] = Pile()
    game.piles[1].push(Card("A", "hearts"))

    # Record initial state
    initial_count = game.move_count
    initial_pile0_size = game.piles[0].size()
    initial_pile1_size = game.piles[1].size()

    # Attempt invalid move
    game.make_move(0, 1)

    # Verify no changes
    assert game.move_count == initial_count
    assert game.piles[0].size() == initial_pile0_size
    assert game.piles[1].size() == initial_pile1_size


# ============================================================================
# Reset Tests
# ============================================================================

def test_reset_clears_piles():
    """Test that reset creates new pile configuration."""
    game = HanoiGame()

    # Make some moves
    for from_idx in range(3):
        for to_idx in range(3):
            if game.is_valid_move(from_idx, to_idx):
                game.make_move(from_idx, to_idx)
                break

    # Reset and verify all piles have cards again
    game.reset()

    total_cards = sum(pile.size() for pile in game.piles)
    assert total_cards == 9


def test_reset_resets_move_count():
    """Test that reset clears move counter."""
    game = HanoiGame()

    # Make a move
    for from_idx in range(3):
        for to_idx in range(3):
            if game.is_valid_move(from_idx, to_idx):
                game.make_move(from_idx, to_idx)
                break

    # Reset
    game.reset()

    assert game.move_count == 0


def test_reset_clears_history():
    """Test that reset clears move history."""
    game = HanoiGame()

    # Make a move
    for from_idx in range(3):
        for to_idx in range(3):
            if game.is_valid_move(from_idx, to_idx):
                game.make_move(from_idx, to_idx)
                break

    # Verify history exists
    assert len(game.move_history) > 0

    # Reset
    game.reset()

    assert len(game.move_history) == 0


def test_reset_creates_new_distribution():
    """Test that reset creates a new random distribution."""
    game = HanoiGame()

    # Get initial configuration
    initial_config = []
    for pile in game.piles:
        cards_values = [card.value for card in pile.cards]
        initial_config.append(tuple(cards_values))
    initial_config = tuple(initial_config)

    # Reset multiple times and check for at least one different configuration
    different_found = False
    for _ in range(10):
        game.reset()

        new_config = []
        for pile in game.piles:
            cards_values = [card.value for card in pile.cards]
            new_config.append(tuple(cards_values))
        new_config = tuple(new_config)

        if new_config != initial_config:
            different_found = True
            break

    assert different_found, "Reset should create new random distributions"


# ============================================================================
# Win Condition Tests
# ============================================================================

def test_is_game_won_perfect_sequence():
    """Test that game is won with perfect descending sequence in one pile."""
    game = HanoiGame()

    # Clear piles and set up winning condition
    game.piles = [Pile(), Pile(), Pile()]

    # Create perfect sequence: 9 at bottom, Ace at top
    winning_ranks = ["9", "8", "7", "6", "5", "4", "3", "2", "A"]
    for rank in winning_ranks:
        game.piles[0].push(Card(rank, "hearts"))

    assert game.is_game_won()


def test_is_game_won_wrong_order():
    """Test that game is not won if cards are in wrong order."""
    game = HanoiGame()

    # Clear piles and set up wrong order
    game.piles = [Pile(), Pile(), Pile()]

    # Wrong order: Ace at bottom, 9 at top
    wrong_ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9"]
    for rank in wrong_ranks:
        game.piles[0].push(Card(rank, "hearts"))

    assert not game.is_game_won()


def test_is_game_won_cards_split_across_piles():
    """Test that game is not won if cards are split across multiple piles."""
    game = HanoiGame()

    # Set up cards split across piles (even if some are in correct order)
    game.piles = [Pile(), Pile(), Pile()]

    # Pile 0 has some cards in correct order
    for rank in ["9", "8", "7", "6", "5"]:
        game.piles[0].push(Card(rank, "hearts"))

    # Pile 1 has remaining cards
    for rank in ["4", "3", "2", "A"]:
        game.piles[1].push(Card(rank, "hearts"))

    assert not game.is_game_won()


def test_is_game_won_incomplete_pile():
    """Test that game is not won if pile doesn't have all 9 cards."""
    game = HanoiGame()

    # Clear piles and set up incomplete sequence
    game.piles = [Pile(), Pile(), Pile()]

    # Only 5 cards in correct order
    for rank in ["9", "8", "7", "6", "5"]:
        game.piles[0].push(Card(rank, "hearts"))

    assert not game.is_game_won()


def test_is_game_won_correct_count_wrong_order():
    """Test that having 9 cards in one pile isn't enough - order matters."""
    game = HanoiGame()

    # Clear piles
    game.piles = [Pile(), Pile(), Pile()]

    # 9 cards but shuffled order
    shuffled_ranks = ["5", "9", "2", "7", "A", "8", "3", "6", "4"]
    for rank in shuffled_ranks:
        game.piles[0].push(Card(rank, "hearts"))

    assert not game.is_game_won()


def test_is_game_won_empty_game():
    """Test that empty game is not won."""
    game = HanoiGame()

    # Clear all piles
    game.piles = [Pile(), Pile(), Pile()]

    assert not game.is_game_won()


def test_is_game_won_initial_state():
    """Test that newly initialized game is not won."""
    game = HanoiGame()

    # Random 3-3-3 distribution should never be a winning state
    assert not game.is_game_won()


def test_is_game_won_after_moves():
    """Test win detection after making moves (integration test)."""
    game = HanoiGame()

    # Manually set up a near-win scenario and complete it
    game.piles = [Pile(), Pile(), Pile()]

    # Set up: pile 0 has 9,8,7,6,5,4,3,2 and pile 1 has Ace
    for rank in ["9", "8", "7", "6", "5", "4", "3", "2"]:
        game.piles[0].push(Card(rank, "hearts"))

    game.piles[1].push(Card("A", "hearts"))

    # Not won yet
    assert not game.is_game_won()

    # Make winning move
    game.make_move(1, 0)

    # Now should be won
    assert game.is_game_won()


# ============================================================================
# Undo Tests
# ============================================================================

def test_undo_reverses_move():
    """Test that undo reverses a move correctly."""
    game = HanoiGame()

    # Set up known state
    game.piles = [Pile(), Pile(), Pile()]
    game.piles[0].push(Card("5", "hearts"))
    game.piles[1].push(Card("9", "hearts"))

    # Make a move
    game.make_move(0, 1)

    # Verify move happened
    assert game.piles[0].is_empty()
    assert game.piles[1].size() == 2
    assert game.piles[1].peek().rank == "5"

    # Undo the move
    result = game.undo()

    # Verify undo worked
    assert result is True
    assert game.piles[0].size() == 1
    assert game.piles[0].peek().rank == "5"
    assert game.piles[1].size() == 1
    assert game.piles[1].peek().rank == "9"


def test_undo_decrements_counter():
    """Test that undo decrements the move counter."""
    game = HanoiGame()

    # Set up and make a move
    game.piles = [Pile(), Pile(), Pile()]
    game.piles[0].push(Card("A", "hearts"))
    game.piles[1].push(Card("5", "hearts"))

    game.make_move(0, 1)
    move_count_after_move = game.move_count

    # Undo
    game.undo()

    # Verify counter decremented
    assert game.move_count == move_count_after_move - 1


def test_undo_updates_history():
    """Test that undo removes move from history."""
    game = HanoiGame()

    # Set up and make moves
    game.piles = [Pile(), Pile(), Pile()]
    game.piles[0].push(Card("A", "hearts"))
    game.piles[1].push(Card("5", "hearts"))

    game.make_move(0, 1)
    game.make_move(1, 2)

    # Verify history has 2 moves
    assert len(game.move_history) == 2

    # Undo once
    game.undo()

    # Verify history has 1 move
    assert len(game.move_history) == 1
    assert game.move_history[0] == (0, 1)


def test_undo_empty_history_returns_false():
    """Test that undo returns False when there are no moves to undo."""
    game = HanoiGame()

    # Clear history
    game.move_history = []

    # Try to undo
    result = game.undo()

    # Should return False
    assert result is False


def test_multiple_undos():
    """Test that multiple undos work in sequence."""
    game = HanoiGame()

    # Set up
    game.piles = [Pile(), Pile(), Pile()]
    game.piles[0].push(Card("9", "hearts"))
    game.piles[0].push(Card("5", "hearts"))
    game.piles[0].push(Card("A", "hearts"))

    # Make 3 moves
    game.make_move(0, 1)  # Move A to pile 1
    game.make_move(0, 2)  # Move 5 to pile 2
    game.make_move(1, 2)  # Move A to pile 2

    # State after moves:
    # Pile 0: [9]
    # Pile 1: []
    # Pile 2: [5, A]
    assert game.piles[0].size() == 1
    assert game.piles[1].size() == 0
    assert game.piles[2].size() == 2
    assert game.move_count == 3

    # Undo first move (reverse: A from pile 2 to pile 1)
    result1 = game.undo()
    assert result1 is True
    assert game.piles[2].size() == 1
    assert game.piles[1].size() == 1
    assert game.piles[1].peek().rank == "A"
    assert game.move_count == 2

    # Undo second move (reverse: 5 from pile 2 to pile 0)
    result2 = game.undo()
    assert result2 is True
    assert game.piles[2].size() == 0
    assert game.piles[0].size() == 2
    assert game.piles[0].peek().rank == "5"
    assert game.move_count == 1

    # Undo third move (reverse: A from pile 1 to pile 0)
    result3 = game.undo()
    assert result3 is True
    assert game.piles[1].size() == 0
    assert game.piles[0].size() == 3
    assert game.piles[0].peek().rank == "A"
    assert game.move_count == 0
