class Tree:
    # This part defines the data structure
    def __init__(self, state, move=None, parent=None, is_max=True):
        self.state = state  # state = state because a child inherits its state from its parent and then modifies it
        self.parent = parent  # to remember who is the parent of the node that is being expanded
        self.move = move  # To remember which move has been made to get to the state
        self.is_max = is_max  # True = Max (odd), False = Min (even)
        self.children = []  # List the children of the current node

    def add_child(self, move, child_node):
        self.children.append(child_node)  # Add the node into the list of children of the current node

    def possible_moves(self):
        number = self.state['number']
        return [i for i in range(2, 6) if number % i == 0]  # Define the possible moves that can be made from a node

    def Minmax_leaf_value(self):
        # MinMax Value definition
        if self.state['score'] % 2 == 0:  # If the score is even, then the Final score is score - Bank and the opposite if the score is odd
            Final_score = self.state['score'] - self.state['Bank']
        else:  # if odd then add the bank to the score
            Final_score = self.state['score'] + self.state['Bank']
        if Final_score % 2 == 0:
            self.state['MinMax_ana'] = -1  # determine who wins if it's odd then a +1 (for the first player) value is given
        else:
            self.state['MinMax_ana'] = 1  # determine who wins if it's odd then a -1 (for the second player) value is given

    def expand(self, depth=0, max_depth=10):
        """Expand the tree applying Minimax."""
        if depth >= max_depth:
            return

        possible_moves = self.possible_moves()

        if not possible_moves:  # Reached leaf
            self.Minmax_leaf_value()
            return

        for i in possible_moves:  # Main difference with the alpha-beta pruning, we give the value of the new state in the expand function
            numbr = self.state['number'] // i  # Definition of the state
            new_state = {
                'number': numbr,
                'score': self.state['score'],
                'Bank': self.state['Bank'],
                'MinMax_ana': 0
            }

            if numbr % 10 == 5 or numbr % 10 == 0:
                new_state['Bank'] += 1
            if numbr % 2 == 0:
                new_state['score'] = new_state['score'] - 1
            if numbr % 2 == 1:
                new_state['score'] += 1

            child_node = Tree(new_state, move=i, parent=self, is_max=not self.is_max)
            self.add_child(i, child_node)
            child_node.expand(depth=depth + 1, max_depth=max_depth)

        # Apply MinMax
        if self.is_max:
            self.state['MinMax_ana'] = max(child.state['MinMax_ana'] for child in self.children)
        else:
            self.state['MinMax_ana'] = min(child.state['MinMax_ana'] for child in self.children)

    def best_move(self):
        # Look for the best move depending on the value of MinMax for the children
        if self.is_max:
            best_child = max(self.children, key=lambda child: child.state['MinMax_ana'])
        else:
            best_child = min(self.children, key=lambda child: child.state['MinMax_ana'])
        return best_child.move

    @staticmethod
    def create_initial_state(start_number=10, start_score=0, start_bank=0):
        """
        Creates the initial state for the game.
        """
        return {
            'number': start_number,
            'score': start_score,
            'Bank': start_bank,
            'MinMax_ana': 0
        }

    def print_tree(self, level=0):
        """
        Prints the tree structure in a readable way.
        """
        indent = "  " * level
        move = f"Move: {self.move}" if self.move is not None else "Root"
        minmax_value = f"MinMax Value: {self.state['MinMax_ana']}"
        print(f"{indent}{move} - {minmax_value} (Score: {self.state['score']}, Bank: {self.state['Bank']}, Number: {self.state['number']})")

        # Recursively print children
        for child in self.children:
            child.print_tree(level + 1)


# Example usage:

# Define the initial state for the tree
initial_state = Tree.create_initial_state(start_number=40, start_score=-1, start_bank=1)

# Create the root node of the tree
root = Tree(initial_state)

# Expand the tree from the root node
root.expand()

# Print the entire tree structure
root.print_tree()
