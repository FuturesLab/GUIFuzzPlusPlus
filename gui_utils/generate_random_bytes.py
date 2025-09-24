"""
Script used to generate a file with n random bytes

Example usage python3 generate_random_bytes.py 100 seed
"""

import os
import sys

def generate_random_bytes(n, output_file):
    try:
        # Generate n random bytes
        random_bytes = os.urandom(n)
        
        # Write the bytes to the output file
        with open(output_file, 'wb') as f:
            f.write(random_bytes)
        print(f"Generated {n} random bytes and saved to {output_file}.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <n> <output_file>")
        sys.exit(1)
    
    try:
        n = int(sys.argv[1])
        output_file = sys.argv[2]

        if n < 0:
            raise ValueError("Number of bytes must be non-negative.")
        
        generate_random_bytes(n, output_file)

    except ValueError as ve:
        print(f"Invalid input: {ve}")
