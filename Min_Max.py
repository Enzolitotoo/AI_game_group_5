class Tree:
    def __init__(self, state, move=None, parent=None, is_max=True):
        self.state = state
        self.parent = parent
        self.move = move
        self.is_max = is_max  # True = Max (impaire), False = Min (paire)
        self.children = []

    def add_child(self, move, child_node):
        self.children.append(child_node)

    def possible_moves(self):
        number = self.state['number']
        return [i for i in range(2, 6) if number % i == 0]

    def Minmax_leaf_value(self):
        """Définit la valeur minimax d'un nœud terminal en gardant des scores positifs."""
        if self.state['score'] % 2 == 0:  # Si le score est pair, c'est Min qui joue
            Final_score = self.state['score'] - self.state['Bank']
        else:  # Si impair, choix de Max
            Final_score = self.state['score'] + self.state['Bank']
        if Final_score % 2 == 0:
            self.state['MinMax_ana'] = -1
        else:
            self.state['MinMax_ana'] = 1

    def expand(self, depth=0, max_depth=10):
        """Développe l'arbre en appliquant Minimax."""
        if depth >= max_depth:
            return

        possible_moves = self.possible_moves()

        if not possible_moves:  # Feuille atteinte
            self.Minmax_leaf_value()
            return

        for i in possible_moves:
            numbr = self.state['number'] // i
            new_state = {
                'number': numbr,
                'score': self.state['score'],
                'Bank': self.state['Bank'],
                'MinMax_ana': 0
            }

            if numbr % 10 == 5 or numbr % 10 == 0:
                new_state['Bank'] += 1
            if numbr % 2 == 0:
                new_state['score'] = new_state['score'] - 1  # Empêcher les négatifs
            if numbr % 2 == 1:
                new_state['score'] += 1

            child_node = Tree(new_state, move=i, parent=self, is_max=not self.is_max)
            self.add_child(i, child_node)
            child_node.expand(depth=depth + 1, max_depth=max_depth)

        # Appliquer Minimax en remontant la meilleure valeur
        if self.is_max:
            self.state['MinMax_ana'] = max(child.state['MinMax_ana'] for child in self.children)
        else:
            self.state['MinMax_ana'] = min(child.state['MinMax_ana'] for child in self.children)

    def best_move(self):
        # Recherche le meilleur mouvement en fonction de la valeur MinMax des enfants
        if self.is_max:
            best_child = max(self.children, key=lambda child: child.state['MinMax_ana'])
        else:
            best_child = min(self.children, key=lambda child: child.state['MinMax_ana'])
        return best_child.move
