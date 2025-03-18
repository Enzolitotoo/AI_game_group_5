class Tree_A:
    def __init__(self, state, move=None, parent=None, is_max=True):
        self.state = state
        self.parent = parent
        self.move = move
        self.is_max = is_max  # True = Max (impair), False = Min (pair)
        self.children = []

    def add_child(self, move, child_node):
        self.children.append(child_node)

    def possible_moves(self):
        number = self.state['number']
        return [i for i in range(2, 6) if number % i == 0]

    def Minmax_leaf_value(self):
        # MinMax Value definition
        if self.state['score'] % 2 == 0:  # Si le score est pair, c'est Min qui joue
            Final_score = self.state['score'] - self.state['Bank']
        else:  # Si impair, choix de Max
            Final_score = self.state['score'] + self.state['Bank']
        
        self.state['MinMax_ana'] = 1 if Final_score % 2 == 1 else -1

    def expand(self, alpha=float('-inf'), beta=float('inf')):
        possible_moves = self.possible_moves()

        if not possible_moves:  # Reached leaf
            self.Minmax_leaf_value()
            return self.state['MinMax_ana']

        if self.is_max:
            max_eval = float('-inf')  # Negative infinite value
            for i in possible_moves:
                new_state = self.new_state_g(i)
                child_node = Tree_A(new_state, move=i, parent=self, is_max=False)
                self.add_child(i, child_node)
                eval_value = child_node.expand(alpha, beta)
                max_eval = max(max_eval, eval_value)
                alpha = max(alpha, eval_value)
                
                if max_eval == 1:
                    break
                
                if beta <= alpha:
                    break
                
            self.state['MinMax_ana'] = max_eval
            return max_eval
        
        else:
            min_eval = float('inf')  # Positive infinite value
            for i in possible_moves:
                new_state = self.new_state_g(i)
                child_node = Tree_A(new_state, move=i, parent=self, is_max=True)
                self.add_child(i, child_node)
                eval_value = child_node.expand(alpha, beta)
                min_eval = min(min_eval, eval_value)
                beta = min(beta, eval_value)
                
                if min_eval == -1:
                    break
                
                if beta <= alpha:
                    break
                
            self.state['MinMax_ana'] = min_eval
            return min_eval

    def new_state_g(self, move):
        if move == 0:
            raise ValueError("Division par zéro détectée dans new_state_g()")
        
        numbr = self.state['number'] // move
        new_state = {
            'number': numbr,
            'score': self.state['score'],
            'Bank': self.state['Bank'],
            'MinMax_ana': 0
        }

        if numbr % 10 == 5 or numbr % 10 == 0:
            new_state['Bank'] += 1
        if numbr % 2 == 0:
            new_state['score'] = new_state['score'] - 1 # Empêcher les négatifs
        if numbr % 2 == 1:
            new_state['score'] += 1
        
        return new_state

    def best_move(self):
        if not self.children:
            return None  # Aucun mouvement possible
        
        if self.is_max:
            best_child = max(self.children, key=lambda child: child.state['MinMax_ana'])
        else:
            best_child = min(self.children, key=lambda child: child.state['MinMax_ana'])
        
        return best_child.move

    def print_tree(self, level=0):
        """
        Prints the current node and all its children recursively.
        """
        print(f"{'  ' * level}State: {self.state}, Move: {self.move}, MinMax_ana: {self.state['MinMax_ana']}")
        for child in self.children:
            child.print_tree(level + 1)
    
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

# Example usage:

# Define the initial state for the tree
initial_state = Tree_A.create_initial_state(start_number=42680, start_score=0, start_bank=0)

# Create the root node of the tree
root = Tree_A(initial_state)

# Expand the tree from the root node
root.expand()

# Print the tree structure
root.print_tree()
