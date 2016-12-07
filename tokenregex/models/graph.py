import re

class Edge:
    def __init__(self, edge_label):
        self.edge_label = edge_label

class Graph:
    """ Graph of tokens 
    """

    def __init__(self, graph_id, tokens):
        self.graph_id = graph_id
        self.tokens = tokens
        self.edges = []

    def add_an_edge():
        self.edges.append()


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

