import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

# Handle imports for both package and direct execution
try:
    from .game import HanoiGame
except ImportError:
    from game import HanoiGame


class HanoiGUI:
    """Tkinter GUI for Hanoi Solitaire game."""

    def __init__(self, root):
        self.root = root
        self.game = HanoiGame()

        # Configuration
        self.CARD_WIDTH = 140
        self.CARD_HEIGHT = 190
        self.PILE_X_POSITIONS = [150, 350, 550]  # X positions for 3 piles
        self.PILE_Y = 180  # Y position for pile area
        self.CARD_STACK_OFFSET = 35  # Pixels to offset stacked cards

        # Drag state
        self.dragged_items = []  # List of canvas item IDs being dragged
        self.drag_source_pile = None
        self.drag_offset_x = 0
        self.drag_offset_y = 0

        # Load card images
        self.card_images = {}
        self._load_card_images()

        self._setup_ui()
        self._draw_game_state()

    def _load_card_images(self):
        """Load all card images from assets folder."""
        # Get the project root directory (go up from src/)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        assets_path = os.path.join(project_root, "assets", "images", "Heart Suit")

        # Mapping of card ranks to filenames
        card_files = {
            "A": "card_hearts_A.png",
            "2": "card_hearts_02.png",
            "3": "card_hearts_03.png",
            "4": "card_hearts_04.png",
            "5": "card_hearts_05.png",
            "6": "card_hearts_06.png",
            "7": "card_hearts_07.png",
            "8": "card_hearts_08.png",
            "9": "card_hearts_09.png",
            "empty": "card_empty.png"
        }

        # Load and resize each card image
        for rank, filename in card_files.items():
            filepath = os.path.join(assets_path, filename)
            if os.path.exists(filepath):
                img = Image.open(filepath)
                img = img.resize((self.CARD_WIDTH, self.CARD_HEIGHT), Image.Resampling.LANCZOS)
                self.card_images[rank] = ImageTk.PhotoImage(img)

    def _setup_ui(self):
        """Create all UI elements."""
        # Title label
        title_label = tk.Label(
            self.root,
            text="Hanoi Solitaire",
            font=("Arial", 24, "bold"),
            bg="#1a472a",
            fg="white"
        )
        title_label.pack(pady=10)

        # Move counter
        self.move_label = tk.Label(
            self.root,
            text="Moves: 0",
            font=("Arial", 14),
            bg="#1a472a",
            fg="white"
        )
        self.move_label.pack()

        # Game canvas (card display area)
        self.canvas = tk.Canvas(
            self.root,
            width=850,
            height=550,
            bg="#2d5a3d"
        )
        self.canvas.pack(pady=20)

        # Bind mouse events for drag-and-drop
        self.canvas.bind("<Button-1>", self._on_mouse_press)
        self.canvas.bind("<B1-Motion>", self._on_mouse_motion)
        self.canvas.bind("<ButtonRelease-1>", self._on_mouse_release)

        # Bottom panel with buttons
        button_frame = tk.Frame(self.root, bg="#1a472a")
        button_frame.pack(pady=10)

        new_game_btn = tk.Button(
            button_frame,
            text="New Game",
            command=self._new_game,
            font=("Arial", 12, "bold"),
            width=12,
            bg="#4CAF50",
            fg="black",
            activebackground="#45a049",
            activeforeground="black"
        )
        new_game_btn.pack(side=tk.LEFT, padx=10)

        undo_btn = tk.Button(
            button_frame,
            text="Undo",
            command=self._undo_move,
            font=("Arial", 12, "bold"),
            width=12,
            bg="#ff9800",
            fg="black",
            activebackground="#e68900",
            activeforeground="black"
        )
        undo_btn.pack(side=tk.LEFT, padx=10)

    def _draw_game_state(self):
        """Render current game state on canvas."""
        self.canvas.delete("all")  # Clear canvas

        # Draw pile labels
        for i, x in enumerate(self.PILE_X_POSITIONS):
            self.canvas.create_text(
                x + self.CARD_WIDTH // 2,
                self.PILE_Y - 30,
                text=f"Pile {i + 1}",
                font=("Arial", 14, "bold"),
                fill="white"
            )

        # Draw cards in each pile
        for pile_idx, pile in enumerate(self.game.piles):
            x = self.PILE_X_POSITIONS[pile_idx]

            if pile.is_empty():
                # Draw empty card placeholder
                if "empty" in self.card_images:
                    self.canvas.create_image(
                        x, self.PILE_Y,
                        image=self.card_images["empty"],
                        anchor="nw",
                        tags="placeholder"
                    )
            else:
                # Draw all cards in the pile
                for card_idx, card in enumerate(pile.cards):
                    y = self.PILE_Y + card_idx * self.CARD_STACK_OFFSET
                    self._draw_card(x, y, card, pile_idx, card_idx)

        # Update move counter
        self.move_label.config(text=f"Moves: {self.game.move_count}")

    def _draw_card(self, x, y, card, pile_idx, card_idx):
        """Draw a single card at position (x, y) using card image."""
        # Get the card image
        if card.rank in self.card_images:
            self.canvas.create_image(
                x, y,
                image=self.card_images[card.rank],
                anchor="nw",
                tags=("card", f"pile_{pile_idx}", f"card_{card_idx}")
            )

    def _on_mouse_press(self, event):
        """Handle mouse press - start dragging if on top card."""
        # Find which item was clicked
        items = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)
        if not items:
            return

        # Get the topmost item
        item_id = items[-1]
        tags = self.canvas.gettags(item_id)

        # Check if clicked on a card
        if "card" not in tags:
            return

        # Parse pile index from tags
        pile_tags = [t for t in tags if t.startswith("pile_")]
        if not pile_tags:
            return

        pile_idx = int(pile_tags[0].split("_")[1])

        # Check if this is the top card of the pile
        pile = self.game.piles[pile_idx]
        if pile.is_empty():
            return

        card_tags = [t for t in tags if t.startswith("card_")]
        if not card_tags:
            return

        card_idx = int(card_tags[0].split("_")[1])

        if card_idx != pile.size() - 1:
            return  # Not the top card

        # Find all items (rectangle, text, suit) that make up this card
        self.dragged_items = []
        for canvas_item in self.canvas.find_all():
            item_tags = self.canvas.gettags(canvas_item)
            if f"pile_{pile_idx}" in item_tags and f"card_{card_idx}" in item_tags:
                self.dragged_items.append(canvas_item)

        if not self.dragged_items:
            return

        # Start dragging
        self.drag_source_pile = pile_idx

        # Calculate offset from card's top-left corner
        main_rect = self.dragged_items[0]
        coords = self.canvas.coords(main_rect)
        self.drag_offset_x = event.x - coords[0]
        self.drag_offset_y = event.y - coords[1]

        # Raise all card items to top layer
        for item in self.dragged_items:
            self.canvas.tag_raise(item)

    def _on_mouse_motion(self, event):
        """Handle mouse motion - move dragged card."""
        if not self.dragged_items:
            return

        # Calculate new position
        new_x = event.x - self.drag_offset_x
        new_y = event.y - self.drag_offset_y

        # Get current position of the first item (rectangle)
        main_rect = self.dragged_items[0]
        old_coords = self.canvas.coords(main_rect)
        old_x = old_coords[0]
        old_y = old_coords[1]

        # Calculate delta
        dx = new_x - old_x
        dy = new_y - old_y

        # Move all items by the delta
        for item in self.dragged_items:
            self.canvas.move(item, dx, dy)

    def _on_mouse_release(self, event):
        """Handle mouse release - attempt to place card."""
        if not self.dragged_items:
            return

        # Determine which pile the card was dropped on
        drop_pile_idx = None
        for i, x in enumerate(self.PILE_X_POSITIONS):
            if x <= event.x <= x + self.CARD_WIDTH + 100:  # Add some margin
                drop_pile_idx = i
                break

        # Attempt the move
        if drop_pile_idx is not None:
            move_successful = self.game.make_move(self.drag_source_pile, drop_pile_idx)

            if move_successful:
                # Check for win
                if self.game.is_game_won():
                    messagebox.showinfo(
                        "Congratulations!",
                        f"You won in {self.game.move_count} moves!"
                    )
            # If move failed, card will just return to original position

        # Reset drag state
        self.dragged_items = []
        self.drag_source_pile = None

        # Redraw entire game state (resets card positions)
        self._draw_game_state()

    def _new_game(self):
        """Start a new game with random distribution."""
        self.game.reset()
        self._draw_game_state()

    def _undo_move(self):
        """Undo the last move."""
        success = self.game.undo()

        if not success:
            messagebox.showinfo("Undo", "No moves to undo!")
        else:
            self._draw_game_state()
