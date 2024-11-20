# ChessCrypt
My implementation(s) of [ChessCrypt](https://doi.org/10.1038/s41598-024-77927-0), focusing on the core S-Box generation algorithm using chess piece movements for cryptographic strength.

## Python
I've implemented ChessCrypt in Python with the following key features:

1. S-Box Generation using chess piece movements:
   - Knight: Moves in L-shape pattern with cyclic wrapping
   - King: Moves one step in any direction
   - Bishop: Moves diagonally any number of steps

2. Core functionality:
   - Configurable S-Box size (default 16x16 for 256 values)
   - Random chess piece movements with cyclic wrapping
   - Value swapping based on piece movements
   - Substitution using the generated S-Box

3. Statistical Analysis:
   - Bijectivity checking
   - Basic statistical properties calculation

4. Clean, typed, and documented code following Python best practices

To use ChessCrypt, you can create an instance and generate an S-Box:

```python
crypto = ChessCrypt()
sbox = crypto.generate_sbox()
output = crypto.substitute(input_byte)
```

![image](https://github.com/user-attachments/assets/ca1165fe-d3c6-421f-82a0-e2c92ab7c46d)


### Citation
Banga, A., Iqbal, N., Ikram, A. et al. ChessCrypt: enhancing wireless communication security in smart cities through dynamically generated S-Box with chess-based nonlinearity. Sci Rep 14, 28205 (2024). [https://doi.org/10.1038/s41598-024-77927-0](https://doi.org/10.1038/s41598-024-77927-0)
