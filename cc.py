import numpy as np
from typing import Tuple, List

class ChessCrypt:
    def __init__(self, box_size: int = 16):
        """
        Initialize ChessCrypt with configurable S-Box size.
        
        Args:
            box_size: Size of one side of the square S-Box (default 16 for 256 values)
        """
        self.box_size = box_size
        self.sbox = np.arange(box_size * box_size).reshape(box_size, box_size)
        
        # Initial positions for pieces
        self.king_pos = (0, 0)
        self.knight_pos = (box_size//2, box_size//2)
        self.bishop_pos = (box_size-1, box_size-1)

    def _get_knight_moves(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Calculate all valid knight moves from current position."""
        moves = [
            (pos[0] + 2, pos[1] + 1), (pos[0] + 2, pos[1] - 1),
            (pos[0] - 2, pos[1] + 1), (pos[0] - 2, pos[1] - 1),
            (pos[0] + 1, pos[1] + 2), (pos[0] + 1, pos[1] - 2),
            (pos[0] - 1, pos[1] + 2), (pos[0] - 1, pos[1] - 2)
        ]
        # Filter valid moves within board boundaries with cyclic wrapping
        return [(x % self.box_size, y % self.box_size) for x, y in moves]

    def _get_king_moves(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Calculate all valid king moves from current position."""
        moves = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                moves.append(((pos[0] + dx) % self.box_size, 
                            (pos[1] + dy) % self.box_size))
        return moves

    def _get_bishop_moves(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Calculate all valid bishop moves from current position."""
        moves = []
        for direction in [(1,1), (1,-1), (-1,1), (-1,-1)]:
            curr_x, curr_y = pos
            for _ in range(self.box_size):
                curr_x = (curr_x + direction[0]) % self.box_size
                curr_y = (curr_y + direction[1]) % self.box_size
                moves.append((curr_x, curr_y))
        return moves

    def _swap_positions(self, pos1: Tuple[int, int], pos2: Tuple[int, int]):
        """Swap values in the S-Box at given positions."""
        self.sbox[pos1[0]][pos1[1]], self.sbox[pos2[0]][pos2[1]] = \
            self.sbox[pos2[0]][pos2[1]], self.sbox[pos1[0]][pos1[1]]

    def generate_sbox(self, iterations: int = 1000) -> np.ndarray:
        """
        Generate the S-Box using chess piece movements.
        
        Args:
            iterations: Number of movement iterations to perform
            
        Returns:
            Generated S-Box as a numpy array
        """
        for _ in range(iterations):
            # Move knight
            knight_moves = self._get_knight_moves(self.knight_pos)
            new_knight_pos = knight_moves[np.random.randint(len(knight_moves))]
            self._swap_positions(self.knight_pos, new_knight_pos)
            self.knight_pos = new_knight_pos

            # Move king
            king_moves = self._get_king_moves(self.king_pos)
            new_king_pos = king_moves[np.random.randint(len(king_moves))]
            self._swap_positions(self.king_pos, new_king_pos)
            self.king_pos = new_king_pos

            # Move bishop
            bishop_moves = self._get_bishop_moves(self.bishop_pos)
            new_bishop_pos = bishop_moves[np.random.randint(len(bishop_moves))]
            self._swap_positions(self.bishop_pos, new_bishop_pos)
            self.bishop_pos = new_bishop_pos

        return self.sbox

    def substitute(self, input_byte: int) -> int:
        """
        Perform substitution using the generated S-Box.
        
        Args:
            input_byte: Input byte value to substitute
            
        Returns:
            Substituted byte value
        """
        row = input_byte // self.box_size
        col = input_byte % self.box_size
        return int(self.sbox[row][col])

    def get_sbox_stats(self) -> dict:
        """Calculate and return statistical properties of the S-Box."""
        flat_sbox = self.sbox.flatten()
        
        # Check bijectivity
        is_bijective = len(np.unique(flat_sbox)) == len(flat_sbox)
        
        # Calculate basic statistics
        stats = {
            'is_bijective': is_bijective,
            'min_value': int(np.min(flat_sbox)),
            'max_value': int(np.max(flat_sbox)),
            'mean_value': float(np.mean(flat_sbox)),
            'std_dev': float(np.std(flat_sbox))
        }
        
        return stats

def main():
    # Example usage
    crypto = ChessCrypt(box_size=16)  # 16x16 S-Box for 256 values
    sbox = crypto.generate_sbox(iterations=1000)
    
    # Print S-Box statistics
    stats = crypto.get_sbox_stats()
    print("S-Box Statistics:")
    for key, value in stats.items():
        print(f"{key}: {value}")
    
    # Example substitution
    input_byte = 123
    output_byte = crypto.substitute(input_byte)
    print(f"\nExample substitution:")
    print(f"Input byte: {input_byte}")
    print(f"Output byte: {output_byte}")

if __name__ == "__main__":
    main()
