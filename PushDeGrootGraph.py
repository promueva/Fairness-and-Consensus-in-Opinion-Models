import networkx as nx
import random

class PushDeGrootGraph(nx.DiGraph):

    def __init__(self, n, ops=[]):
        p = 0.1
        G = nx.fast_gnp_random_graph(n, p, directed=True)
        while not nx.is_strongly_connected(G):
            G = nx.fast_gnp_random_graph(n, p, directed=True)
        super().__init__(G)
        
        letters = 'abcdefghijklmnopqrstuvwxyz'
        self.labels = {}
        self.alphabet = []
        for n, edge in enumerate(self.edges):
            label = letters[n] if len(self.edges) < len(letters) else "%d_%d" % edge
            self.edges[edge]['label'] = label
            self.labels[label] = edge
            self.alphabet.append(label)
        self.set_initial_opinions(ops)
        
        self.pos = nx.spring_layout(self)
        
    def set_initial_opinions(self, ops=[]):
        self.opinion = {}
        for node in self:
            if node < len(ops):
                self.opinion[node] = ops[node]
            else:
                self.opinion[node] = random.random()

    def draw(self):
        labels_with_opinions = {n:"%.2f \n %d" % (s,n) for n, s in self.opinion.items()}
        nx.draw_networkx_nodes(self, self.pos, margins=0.1)
        nx.draw_networkx_edges(self, self.pos)
        nx.draw_networkx_labels(self, self.pos,  labels=labels_with_opinions, verticalalignment="baseline")
        nx.draw_networkx_edge_labels(self, self.pos, nx.get_edge_attributes(self, "label"))

    
    def make_call(self, edge):
        caller, callee = edge
        if not nx.is_path(self, [caller, callee]):
            raise Exception("edge " + str(edge) + " does not exist")
        self.opinion[callee] = (self.opinion[callee] + self.opinion[caller]) * 0.5
    
    def execute_word(self, word, Check=None): # word is a list of edge labels to be used in consecutive calls
        if Check is not None:
            test = Check(self)
        for t, e in enumerate(word):
            self.make_call(self.labels[e])
            if Check is not None:
                test.check(t)
        if Check is not None:
            return test.terminate()

