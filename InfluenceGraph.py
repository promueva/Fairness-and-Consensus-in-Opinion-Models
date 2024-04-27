import networkx as nx
import random
import numpy as np
import matplotlib.pyplot as plt

class InfluenceGraph(nx.DiGraph):

    def __init__(self, n, ops=[], keep_history=True, G=None, edge_labels = 'abcdefghijklmnopqrstuvwxyz', influence_fn=lambda self,e: 0.5):
        if G is None:    
            p = 0.1
            G = nx.fast_gnp_random_graph(n, p, directed=True)
            while not nx.is_strongly_connected(G):
                G = nx.fast_gnp_random_graph(n, p, directed=True)
        super().__init__(G)
        
        self.labels = {}
        self.alphabet = []
        for n, edge in enumerate(self.edges):
            label = edge_labels[n] if len(self.edges) <= len(edge_labels) else "%d_%d" % edge
            self.edges[edge]['label'] = label
            self.labels[label] = edge
            self.alphabet.append(label)
        self.set_initial_opinions(ops)
        self.influence_fn = influence_fn
        self.keep_history = keep_history
        if self.keep_history:
            self.history = [[*self.opinion.values()]]
        
        self.pos = nx.spring_layout(self)
        
    def set_initial_opinions(self, ops=[]):
        self.opinion = {}
        for i,node in enumerate(self):
            if i < len(ops):
                self.opinion[node] = ops[i]
            else:
                self.opinion[node] = random.random()

    def draw(self):
        labels_with_opinions = {n:"%.2f \n %d" % (s,n) for n, s in self.opinion.items()}
        nx.draw_networkx_nodes(self, self.pos, margins=0.1)
        nx.draw_networkx_edges(self, self.pos, connectionstyle='arc3,rad=0.2')
        nx.draw_networkx_labels(self, self.pos,  labels=labels_with_opinions, verticalalignment="baseline")
        nx.draw_networkx_edge_labels(self, self.pos, nx.get_edge_attributes(self, "label"), connectionstyle='arc3,rad=0.2')

    def plot_opinion_evolution(self):
        history = np.transpose(self.history)

        fig, ax = plt.subplots()
        plt.ylim((-0.1,1.1))

        plt.xlabel("Time")
        plt.ylabel("Opinion value")

        for i, data in enumerate(history):
            ax.plot(data,  label=f"{i+1}")
        return fig

    def execute_edge(self, edge):
        caller, callee = edge
        if not nx.is_path(self, [caller, callee]):
            raise Exception("edge " + str(edge) + " does not exist")
        self.opinion[callee] = self.opinion[callee] + (self.opinion[caller] - self.opinion[callee]) * self.influence_fn(self,edge)
        if self.keep_history:
            self.history.append([*self.opinion.values()])
    
    def execute_word(self, word, Check=None): # word is a list of edge labels to be used in consecutive calls
        if Check is not None:
            test = Check(self)
        for t, e in enumerate(word):
            self.execute_edge(self.labels[e])
