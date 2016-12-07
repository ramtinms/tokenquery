class Node:
    """
        Node is a container of one or many tokens or nodes
    """

    def __init__(self, children=[], label=""):
        self.children = children
        self.label = label

    def get_children():
        return self.children

    def get_label():
        return self.label

    def is_a_leaf():
        if self.children:
            return False
        return True

class Tree:
    """ to store a tree structure for tokens
    """

    # TODO from here
    def __init__(self, tree_id, tokens, nodes=[]):
        self.tree_id = tree_id
        self.tokens = tokens
        self.nodes = []



    def add_a_node(self):
        pass

    # def add_a_label(self, label_name, label_value):
    #     for counter, token in enumerate(self.tokens):
    #         if counter == 0:
    #             token.add_a_label(label_name+'~B', label_value)
    #         else:
    #             token.add_a_label(label_name+'~I', label_value)

    # def get_a_label(self, label_name):
    #     return self.tokens[0].get_a_label(label_name)

    # def get_text(self):
    #     if not self.tokens:
    #         return None
    #     return " ".join([token.get_text() for token in self.tokens])
