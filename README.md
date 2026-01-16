# Hanoi Solitaire

A GUI-based card game implementing Hanoi Solitaire, built for [boot.dev's Back-End Developer course](https://boot.dev).

## Rules

Using 9 cards (Ace through 9), move all cards to a single pile in descending order (9 at bottom, Ace at top).
- Move one card at a time
- Only top cards can be moved
- Smaller cards can only go on larger cards or empty piles

## How to Run

```bash
git clone https://github.com/yourusername/hanoi-solitaire.git
cd hanoi-solitaire
uv run python src/main.py
```

## Run Tests

```bash
uv run pytest tests/
```
