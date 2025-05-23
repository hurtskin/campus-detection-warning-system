import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from gensim.models import Word2Vec
from sklearn.manifold import TSNE  # Dimension Reduction Tool
from sklearn.preprocessing import StandardScaler


def random_walk(graph: nx.Graph, start_node: int, walk_length: int) -> list:
    """
    Performs a random walk of a given length starting from a specified node in the graph.

    Parameters:
    graph (networkx.Graph): The input graph.
    start_node (int): The starting node for the random walk.
    walk_length (int): The desired length of the random walk.

    Returns:
    list: A list of nodes representing the sequence of the random walk.
    """
    np.random.seed(42)  # Set a random seed for reproducibility
    walk = [start_node]
    while len(walk) < walk_length:
        cur = walk[-1]
        neighbors = list(graph.neighbors(cur))
        if len(neighbors) > 0:
            walk.append(np.random.choice(neighbors))
        else:
            break
    return walk


def generate_walks(graph: nx.Graph, num_walks: int, walk_length: int) -> list:
    """
    Generates multiple random walks from each node in the graph.

    Parameters:
    graph (networkx.Graph): The input graph on which random walks will be performed.
    num_walks (int): The number of random walks to start from each node.
    walk_length (int): The desired length of each random walk.

    Returns:
    list: A list of lists, where each inner list represents a sequence of nodes visited in a random walk.
    """
    walks = []  # Initialize an empty list to store the walks
    nodes = list(graph.nodes())  # Get a list of all nodes in the graph
    
    for _ in range(num_walks):
        # Shuffle the nodes to ensure random start order
        np.random.shuffle(nodes)
        for node in nodes:
            # Perform a random walk from the current node and add it to the list
            walks.append(random_walk(graph, node, walk_length))

    # Convert the input sequences from integer to string as Word2Vec requires the input to be of string type.
    sentences = [list(map(str, walk)) for walk in walks]
    return sentences


class DeepWalk:
    def __init__(self, graph, num_walks, walk_length):
        """
        Initializes the DeepWalk instance with a graph, number of walks, and walk length.
        
        Attributes:
        graph (networkx.Graph): The input graph.
        w2v_model: The Word2Vec model for learning embeddings.
        _embeddings (dict): A dictionary to store node embeddings.
        sentences (list): A list to store random walk sequences.
        """
        self.graph = graph
        self.w2v_model = None
        self._embeddings = {}
        self.sentences = generate_walks(graph, num_walks, walk_length)

    def train(self, embed_size=300, window_size=10, min_count=0, sg=1, hs=0, negative=10, epochs=50, workers=4, seed=42, **kwargs):
        """
        Trains a Word2Vec model on the generated random walks.
        
        Parameters:
        embed_size (int): Dimension of the node embeddings.
        window_size (int): Maximum distance between the current and predicted node within a sentence.
        min_count (int): Ignores all nodes with total frequency lower than this.
        sg (int): Training algorithm: 1 for skip-gram; otherwise CBOW.
        hs (int): If 1, hierarchical softmax will be used for model training.
        negative (int): Number of negative samples to use for training.
        epochs (int): Number of iterations (epochs) over the corpus.
        workers (int): Number of worker threads to use for training.
        seed (int): Seed for the random number generator.
        kwargs: Additional arguments for the Word2Vec model.
        
        Returns:
        model (Word2Vec): Trained Word2Vec model.
        """
        kwargs["sentences"] = self.sentences  # Random walk sequences
        kwargs["vector_size"] = embed_size  # Size of the embedding vectors
        kwargs["window"] = window_size  # Max distance between current and predicted node
        kwargs["min_count"] = min_count  # Minimum node frequency
        kwargs["sg"] = sg  # Skip-gram if 1, else CBOW
        kwargs["hs"] = hs  # Hierarchical softmax
        kwargs["negative"] = negative  # Number of negative samples
        kwargs["epochs"] = epochs  # Number of training iterations
        kwargs["workers"] = workers  # Number of worker threads
        kwargs["seed"] = seed  # Random seed

        print("Learning embedding vectors...")
        model = Word2Vec(**kwargs)  # Train Word2Vec model
        print("Learning embedding vectors done!")

        self.w2v_model = model
        return model

    def get_embeddings(self):
        """
        Retrieves the embeddings for all nodes in the graph.
        
        Returns:
        dict: A dictionary with nodes as keys and their embeddings as values.
        """
        if self.w2v_model is None:
            print("Model not trained")
            return {}

        for node in self.graph.nodes():
            self._embeddings[str(node)] = self.w2v_model.wv[str(node)]

        return self._embeddings
