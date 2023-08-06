import pandas

class TTR:
    def __init__(self, filename, group_by, punct_pos):
        self.filename = filename
        self.group_by = group_by
        self.punct_pos = punct_pos
        self.calculate_ttr()

    def calculate_ttr(self):
        # Get chunk

        # Filter out punctuation
        # If no group_by:
            # Get unique values of the 'lower' column
            # Add chunk.shape[0] to "tokens"
            # Add unique values to "types"
            # Calculate TTR based on type - tokens.
        # Else:
            # Parse the group_by argument value.
            # Create dictionary to hold data
            # Get unique values of the group_by columns + lower
            # For each group_by, add tokens and types to dictionary.
            # Calculate TTR for each key
        pass