import sys
import pygame
import random
import time
from enum import Enum

class BattleshipHunter:
    """The AI hunter class for the Battleship game. Hunts for and targets ships on the board."""

    def __init__(self, _game_manager):

        self.game_manager = _game_manager
        # Create the empty board.
        self.create_board()
        # The ships that have not been sunk yet.
        self.ships = {
            ShipCell.DESTROYER : 2,
            ShipCell.SUBMARINE : 3,
            ShipCell.CRUISER : 3,
            ShipCell.BATTLESHIP : 4,
            ShipCell.CARRIER : 5,
        }
        # Ships that have been hit but not sunk.
        self.hits = {}
        # Number of shots that have hit a ship.
        self.shots_hit = 0
        # Total number of shots attempted.
        self.total_shots = 0

    def create_board(self):
        """Initializes an empty board, as the hunter has no information on the game so far."""
        self.board = [[ShipCell.EMPTY for _ in range(10)] for _ in range(10)]

    def set_mode(self, mode):
        """
        Sets the mode to either HUNTING or TARGETING.

        Parameters:
            mode (Mode): The new value for the mode variable.
        """
        Log.log("Switching mode to " + str(mode.name) + "...")
        self.mode = mode

    def take_turn(self):
        """
        Decides whether to go into hunting or targeting mode and returns result.

        If there are discovered ships that haven't been sunk, target. Otherwise, go into hunting
        mode and search for undiscovered ships. Return the resulting position.

        Returns:
            tuple: The position that is either being targeted or hunted.
        """
        # Task 1:

        # If there are hits on ships that haven't been sunk, return the result of the targeting
        # method.
        if len(self.hits):
            self.set_mode(Mode.TARGETING)
            return self.target_basic()
        # Otherwise, return the result of the hunting method.
        self.set_mode(Mode.HUNTING)
        return self.hunt_basic()

    def hunt_basic(self):
        """
        Hunts for undiscovered ships by finding and returning a possible position using the
        checkerboard method.

        Collects all empty cells that could contain a ship. Since all ships are two cells or more,
        we only should get every other cell. Then, randomly choose a cell from the available cells
        and return it.

        Returns:
            tuple: The choice position of the cell to hunt.
        """
        # Task 2:

        # Create a list of empty cells. Should go through all y values, then every other x value
        # starting at either 0 or 1, creating a checkerboard pattern.
        empty = []
        for y in range(len(self.board)):
            for x in range(y % 2, len(self.board[y]), 2):
                if self.board[y][x] == ShipCell.EMPTY:
                    empty.append((x, y))
        # Choose a random cell from the list.
        choice = random.choice(empty)
        # Return the chosen cell.
        return choice


    def on_miss(self, position):
        """
        Updates variables and statistics that need to be updated after a shot misses, including
        the board and statistics.

        Parameters:
            position (tuple): The position of the miss.
        """
        # Task 3.1:

        # Update the board with the miss.
        x, y = position
        self.board[y][x] = ShipCell.MISS
        # Update total shots.
        self.total_shots += 1

    def on_hit(self, ship, position):
        """
        Updates variables and statistics that need to be updated after a ship is hit.

        Updates the board and the hits dictionary with the ship, checks if the ship needs to be
        sunk, and adds the hit to the statistics. If the ship was undiscovered, add a new entry
        to the hits dictionary. Otherwise, update the ship's entry with the new hit.

        Parameters:
            ship (ShipCell): The ship that was hit.
            position (tuple): The position that the ship was hit at.
        """
        # Task 3.2:

        # Update the board with the hit ship.
        x, y = position
        self.board[y][x] = ship
        # If the ship has been hit before, add the hit to it's entry.
        if ship in self.hits:
            self.hits[ship].append(position)
        # Otherwise, create a new entry for the newly discovered ship.
        else:
            self.hits[ship] = [position]
        # Check if the ship needs to be sunk.
        if self.check_sink(ship):
            self.on_sink(ship)
        # Update statistics.
        self.shots_hit += 1
        self.total_shots += 1

    def in_bounds(self, position):
        """
        Checks if a position is within bounds of the board.

        Parameters:
            position (tuple): The position to check.
        Returns:
            bool: True if the position is within bounds of the board, False otherwise.
        """
        # Task 4.1:

        # Return true if both x and y are on the board.
        x, y = position
        return x >= 0 and y >= 0 and x < len(self.board[0]) and y < len(self.board)

        # Remove after adding your implementation.
        return False

    def is_empty(self, position):
        """
        Checks if a position on the board is currently empty.

        Paramters:
            position (tuple): The position to check.
        Returns:
            bool: True if the position is empty, False otherwise.
        """
        # Task 4.2:

        # Return true if the cell is empty.
        x, y = position
        return self.board[y][x] == ShipCell.EMPTY

    def target_basic(self):
        """
        Targets discovered ships by finding and returning a possible position of the next cell of the ship.

        Searches through current discovered ships, finds an empty adjacent cell to the ship, and
        returns its position.

        Returns:
            tuple: The choice position of the next cell of the ship to target.
        """
        # Task 4.3: Implement the basic targeting algorithm.

        # For each hit on the first ship in hits, check each adjacent cell. If it's in bounds and
        # empty, return that cell.
        first_ship = next(iter(self.hits))
        for hit in self.hits[first_ship]:
            x, y = hit
            for direction in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                direction_x, direction_y = direction
                choice = (x + direction_x, y + direction_y)
                if self.in_bounds(choice) and self.is_empty(choice):
                    return choice

    def check_sink(self, ship):
        """
        Checks if ship has been sunk or not.

        Parameters:
            ship (ShipCell): The cell of the ship to check.
        Returns:
            bool: True if the ship's hits >= its size, False otherwise.
        """
        # Task 5.1:

        # Return true if the number of hits on the ship is equal to or greater than the total
        # number of cells of that ship.
        return ship in self.hits and len(self.hits[ship]) >= self.ships[ship]
        # Remove after adding your implementation.
        return False

    def on_sink(self, ship):
        """
        When ship sinks, remove it from hits (because it can no longer be targeted), remove it from ships, and tell
        the game manager to update.

        Paramters:
            ship (ShipCell): the ship cell of the ship that has sunk.
        """
        # Task 5.2: Implement the algorithm for when a ship is sunk.

        # Remove the ship from the hits dictionary.
        self.hits.pop(ship)
        # Remove the ship from the ships dictionary.
        self.ships.pop(ship)
        # Tell the game manager to sink the ship.
        self.game_manager.sink_ship(ship)

    def can_fit_ship(self, position, size):
        """
        Checks if a ship of length size can fit either horizontally or vertically at position.

        Parameters:
            position (tuple): The position to check.
            size (int): The size of the ship.
        Returns:
            bool: True if the position can be fit on the ship, False otherwise.
        """
        # Task 6.1:

        # Check horizontally.
        # For all starting positions ((x - size + 1) to x).

            # If all the cells of the ship are in bounds of the board and empty...

                # Return result.

        # Check vertically.
        # For all starting positions((y - size + 1) to y).

            # If all the cells of the ship are in bounds of the board and empty...

                # Return result.

        # If all other checks were not successful, then this ship cannot be in this cell.

        # Remove after adding your implementation.
        return False

    def hunt_clusters(self):
        """
        Hunts for undiscovered ships by finding and returning a possible position for the largest ship remaining.

        Starts by getting the sizes of remaining ships to find the maximum size. Then, collects all
        empty cells that could contain that ship possibly horizontally or vertically. Finally, a
        cell is randomly chosen from the available cells.

        Returns:
            tuple: The choice position of the cell to hunt.
        """
        # Task 6.2

        # Get the sizes of the remaining ships.

        # Determine the maximum ship size using the max() function.

        # Gather empty cells that can hold a ship of the max ship size.

        # Choose a random cell from the list.

        # Return the chosen cell.

        # Remove after adding your implementation.
        return (0, 0)

    def get_space(self, position, orientation):
        """
        Returns the number of adjacent positions in a particular orientation.

        Parameters:
            position (tuple): The position to check around.
            orientation (Orientation): The orientation to check for.
        Returns:
            int: The number of adjacent positions in the given orientation.
        """
        # Task 7.1:

        # Make a list of directions based on the orientation.

        # Create a counter for the number of spaces available.

        # For each direction.

            # Create a variable to keep track how far away we currently are from the starting
            # position.

            # While the position in that direction and distance away is in bounds and empty.

                # Increment the counter.

                # Increment the distance.

        # Return the counter.

        # Remove after adding your implementation.
        return 1

    def target_fit(self):
        """
        Targets discovered ships by finding and returning a possible position of the next cell
        of the ship.

        Starts by going through all discovered ships and checking if the ship could fit in the
        adjacent cell and orientation.

        Returns:
            tuple: The choice position of the next cell of the ship to target.
        """
        # Task 7.2:

        # For each ship in the hits dictionary.

            # For each hit on that ship.

                # For each adjacent direction to that cell.

                    # Determine the adjacent cell in that direction.

                    # Determine whether the orientation would be HORIZONTAL or VERTICAL.

                    # If the adjacent cell can be targeted, and the ship can fit in that
                    # orientation, return the cell.

        # Remove after adding your implementation.
        return (0, 0)

    def target_directionally(self):
        """
        Targets discovered ships by finding and returning a possible position of the next cell
        of the ship.

        Starts by going through all the current discovered ships. If the ship has two or more hits, determines
        whether the ship's orientation and returns a position of an empty cell relative to that orientation.
        If the ship only has a single hit, returns the position of an empty cell that is adjacent
        to the ship cell that the ship could fit in.

        Returns:
            tuple: The choice position of the next cell of the ship to target.
        """
        # Task 8:

        # For each ship in the hits directory.

            # If the ship has more than two hits on it.

                # Get the positions of the first and second hits.

                # Calculate the direction of the ship using the sign() method.

                # For each hit on the ship.

                    # Determine the adjacent cell in the direction.

                    # If it can be hit, then return cell.

                    # Otherwise, determine the adjacent cell in the negative direction.

                    # If it can be hit, then return the cell.

        # If we look through all the cells and cannot target a ship directionally (no ships have
        # two hits). Then use the size-based targeting algorithm.

        # Remove after adding your implementation.
        return (0, 0)

    def sign(self, num):
        """
        Returns the 'sign' of a number.

        Parameters:
            num (int): The number to get the sign of.
        Returns:
            int: The sign of the number - 1 if num is positive, -1 if num is negative, 0 otherwise.
        """
        if num == 0:

            return num

        return -1 if num < 0 else 1

### Used to run the game, do not modify past this line! ###
class ShipCell(Enum):
    """Class that links ship cells to their board symbols and written names."""
    EMPTY = ('~ ', 'Empty')
    MISS = ('X ', 'Miss')
    DESTROYER = ('D ', 'Destroyer')
    SUBMARINE = ('S ', 'Submarine')
    CRUISER = ('C ', 'Cruiser')
    BATTLESHIP = ('B ', 'Battleship')
    CARRIER = ('R ', 'Carrier')

    def __init__(self, symbol, description):

        self.symbol = symbol
        self.description = description


class Mode(Enum):
    """Enum constant for the search mode of the BattleshipHunter."""
    HUNTING = 0
    TARGETING = 1


class Orientation(Enum):
    """Enum constant for the orientation of the Battleship objects."""
    HORIZONTAL = 0
    VERTICAL = 1


class Log:
    """A helper class that provides static functions for outputting to the console and printing errors."""

    verbose = True

    @staticmethod
    def log(message=""):
        """
        Prints a given message to the console.

        Parameters:
            message (str): The message to print.
        """
        if Log.verbose:
            print(message)

    @staticmethod
    def display_board(board, name):
        """
        Prints a given board in the console in a nice format.

        Parameters:
            board (List[List[ShipCell]): A 2D list of the board.
            name (str): The name of the 'owner' of the board (such as "GAME", "HUNTER", etc).
        """
        if Log.verbose:

            print("\n" + "-" * 28)
            print("\t\t " + name + " BOARD")
            print("-" * 28)
            for row in board:
                print(" ".join(cell.symbol for cell in row))

            print("-" * 28)

class GameManager:
    """Main game manager class."""

    def __init__(self):

        self.ships = {
            ShipCell.DESTROYER: Battleship("Destroyer", 2),
            ShipCell.SUBMARINE: Battleship("Submarine", 3),
            ShipCell.CRUISER: Battleship("Cruiser", 3),
            ShipCell.BATTLESHIP: Battleship("Battleship", 4),
            ShipCell.CARRIER: Battleship("Carrier", 5)
        }
        self.shots_hit = []
        self.total_shots = []
        self.accuracies = []
        self.hunt_fallbacks = []
        self.display = True
        self.manual = True

        Log.verbose = False

        self.ui = GameUI(self)
        self.game_num = 1

        self.run_game()

        # For accuracy testing.
        """for i in range(1000):

            self.run_game()
            self.game_num += 1

        print()
        print("Average Shots Hit: " + str(round(sum(self.shots_hit) / len(self.shots_hit), 4)))
        print("Average Total Shots: " + str(round(sum(self.total_shots) / len(self.total_shots), 4)))
        print("Average Accuracy: " + str(round(sum(self.accuracies) / len(self.accuracies), 4)))
        print("Average Hunt Fallbacks: " + str(round(sum(self.hunt_fallbacks) / len(self.hunt_fallbacks) * 100, 4)))"""

    def run_game(self):
        """Runs a single game of battleship."""
        # Place the ships on the board.
        self.place_ships()
        # Initialize the hunter.
        self.battleship_hunter = BattleshipHunter(self)

        Log.display_board(self.board, "GAME")
        # Main game loop.
        while self.ships_left() > 0:
            # Get the hunter's choice.
            call = self.battleship_hunter.take_turn()
            # If display is active, show on screen.
            if self.display:

                self.ui.run()
                time.sleep(0.04)
            # Check if the shot hit.
            result = self.check_hit(call)
            if result != ShipCell.MISS:

                self.battleship_hunter.on_hit(result, call)

            else:

                self.battleship_hunter.on_miss(call)

            Log.log()
            Log.display_board(self.board, "GAME")
            Log.log("Ships Left: " + str(self.ships_left()))
            # If manual is active, wait for the user's input.
            if self.manual:

                self.ui.get_next()
        # If display is active, show on screen one last time at the end of the game.
        if self.display:

            self.ui.run()
            if not self.manual:

                time.sleep(1.25)

        print(f"Game #{self.game_num} finished!")
        # Trigger the game over sequence.
        self.game_over()
        # If manual is active, wait until the user presses a button to continue to the next game.
        if self.manual:

            self.ui.get_next()

    def ships_left(self):
        """
        Counts the number of ships that have not sunk.

        Returns:
            int: The number of ships left.
        """
        return sum(1 for ship_cell, ship in self.ships.items() if not ship.sunk)

    def can_place(self, ship):
        """
        Checks if a ship can be placed.

        Parameters:
            ship (Battleship): The ship to be placed. Contains the position and orientation of the ship.
        Returns:
            bool: True if the ship can be placed, False otherwise.
        """

        dx, dy = (int(ship.orientation == Orientation.HORIZONTAL), int(ship.orientation == Orientation.VERTICAL))
        for i in range(ship.size):

            nx, ny = ship.position[0] + dx * i, ship.position[1] + dy * i
            # Check bounds or overlapping ship
            if not (0 <= nx < 10 and 0 <= ny < 10) or self.board[ny][nx] != ShipCell.EMPTY:

                return False

        return True

    def place_ship(self, ship, ship_cell):
        """Places ship on the board at its position."""
        dx, dy = (int(ship.orientation == Orientation.HORIZONTAL), int(ship.orientation == Orientation.VERTICAL))
        for i in range(ship.size):

            nx, ny = ship.position[0] + dx * i, ship.position[1] + dy * i
            self.board[ny][nx] = ship_cell

    def place_ships(self):
        """Generates the initial 10x10 game board and places all five ships."""
        self.board = [[ShipCell.EMPTY for _ in range(10)] for _ in range(10)]
        for ship_cell, ship in self.ships.items():

            placed = False
            while not placed:

                ship.set_orientation(random.choice(list(Orientation)))
                ship.set_position((random.randint(0, 9), random.randint(0, 9)))
                if self.can_place(ship):

                    self.place_ship(ship, ship_cell)
                    ship.hits = 0
                    ship.sunk = False
                    placed = True

    def check_hit(self, position):
        """
        Checks if position would hit a ship.

        Parameters:
            position (tuple): The position to check for a hit.
        Returns:
            ShipCell: The ID of the ShipCell hit.
        """
        Log.log(str(self.board[0][0]))
        if self.board[position[1]][position[0]] != ShipCell.EMPTY:

            return self.board[position[1]][position[0]]

        return ShipCell.MISS

    def sink_ship(self, ship):
        """
        Sinks a ship.

        Parameters:
            ship (ShipCell): The key of the ship that has sunk.
        """
        self.ships[ship].set_sunk(True)

    def game_over(self):
        """Updates the overall stats after completing a game."""
        Log.log("Game Over!")
        Log.display_board(self.battleship_hunter.board, "HUNTER")
        Log.display_board(self.board, "GAME")
        Log.log()
        Log.log("Accuracy: " + str(self.battleship_hunter.shots_hit) + " / " + str(self.battleship_hunter.total_shots) +
                " (" + str(round(float(self.battleship_hunter.shots_hit) /
                                 float(self.battleship_hunter.total_shots) *
                                 100, 2)) + "%)")
        self.shots_hit.append(self.battleship_hunter.shots_hit)
        self.total_shots.append(self.battleship_hunter.total_shots)
        self.accuracies.append(float(self.battleship_hunter.shots_hit) /
                               float(self.battleship_hunter.total_shots) * 100)


class GameUI:
    """Class that manages the UI display of the game, including the Battleship board and stats."""

    def __init__(self, _game_manager):

        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Battleship")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.cell_size = 40  # Size of each grid cell
        self.margin = 50  # Margin around the grid
        self.game_manager = _game_manager
        # Colors for each ShipCell.
        self.colors = {
            ShipCell.EMPTY: (250, 250, 250),  # Light Grey
            ShipCell.MISS: (50, 50, 50),  # Dark Grey
            ShipCell.DESTROYER: (0, 200, 0),  # Green
            ShipCell.CARRIER: (0, 0, 200),  # Blue
            ShipCell.CRUISER: (200, 0, 200),  # Purple
            ShipCell.BATTLESHIP: (0, 200, 200),  # Teal
            ShipCell.SUBMARINE: (200, 200, 0)  # Yellow
        }

    def draw_board(self, board):
        """Draws the board and fills in the cells."""
        for y, row in enumerate(board):

            for x, cell in enumerate(row):

                rect = pygame.Rect(
                    self.margin + x * self.cell_size,
                    self.margin + 20 + y * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )
                # Sets the color of this cell and draws it.
                color = self.colors[cell]
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)  # Black grid lines

    def draw_stats(self):
        """Displays game stats."""
        # Draw the game number.
        text = self.font.render(f"Game #{self.game_manager.game_num}", True, (255, 255, 255))
        self.screen.blit(text, (10, 10))
        # Draw the stats.
        text = self.font.render(
            f"Shots: {self.game_manager.battleship_hunter.total_shots} | " +
            f"Hits: {self.game_manager.battleship_hunter.shots_hit} | " +
            f"Accuracy: {round((self.game_manager.battleship_hunter.shots_hit / max(1, self.game_manager.battleship_hunter.total_shots)) * 100, 2)}%",
            True,
            (255, 255, 255)
        )
        self.screen.blit(text, (10, 40))

    def handle_events(self):
        """Handles user input."""
        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:

                    pygame.quit()
                    sys.exit()

                elif event.key == pygame.K_m:

                    self.game_manager.manual = not self.game_manager.manual

            if event.type == pygame.QUIT:

                pygame.quit()
                sys.exit()

    def display(self):
        """Updates the screen with the current board and stats."""
        self.screen.fill((0, 0, 0))  # Clear the screen
        self.draw_board(self.game_manager.battleship_hunter.board)
        self.draw_stats()
        pygame.display.flip()

    def run(self):
        """Takes user input and updates the screen as needed."""
        self.handle_events()
        self.display()
        self.clock.tick(60)

    def get_next(self):
        """Awaits user input before moving on to the next step in the game."""
        next_input = False
        while not next_input:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_ESCAPE:

                        pygame.quit()
                        sys.exit()

                    elif event.key == pygame.K_m:

                        self.game_manager.manual = not self.game_manager.manual
                        return

                    else:

                        next_input = True

class Battleship:
    """Battleship class to hold the orientation, position, and status of ships on the board."""

    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.orientation = Orientation.HORIZONTAL
        self.position = (0, 0)
        self.hits = 0
        self.sunk = False

    def get_sunk(self):
        """
        Gets whether the ship is sunk or not.

        Returns:
            bool: The value of the sunk variable.
        """
        return self.sunk

    def set_sunk(self, sunk):
        """
        Updates the sunk variable of the ship to a boolean value.

        Parameters:
            sunk (bool): The new value for the sunk variable.
        """

        self.sunk = sunk

    def get_orientation(self):
        """
        Gets the orientation of the ship.

        Returns:
            Orientation: The orientation enum value of the orientation variable.
        """

        return self.orientation

    def set_orientation(self, orientation):
        """
        Updates the orientation variable of the ship either to HORIZONTAL or VERTICAL.

        Parameters:
            orientation (Orientation): The new orientation of the ship.
        """
        self.orientation = orientation

    def get_position(self):
        """
        Gets the position of the ship.

        Returns:
            (tuple): The value of the position variable.
        """

        return self.position

    def set_position(self, position):
        """
        Updates the position variable of the ship.

        Parameters:
            position (tuple): The new position.
        """
        self.position = position

    def hit(self):
        """Adds to hits count and updates the sunk variable if necessary."""
        self.hits += 1
        if self.hits >= self.size:
            self.sunk = True

# Entry point of the program.
if __name__ == '__main__':

    game_manager = GameManager()
