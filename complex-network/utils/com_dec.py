from sklearn.cluster import KMeans
import networkx as nx
from sklearn.metrics import silhouette_score, accuracy_score, normalized_mutual_info_score


class CommunityDetection:
    def __init__(self, graph: nx.Graph, embeddings_list: list[list]):
        """
        Initializes the CommunityDetection class.

        Parameters:
        graph (nx.Graph): The input graph for community detection.
        embeddings_list (list[list]): List of node embeddings (2D vectors).
        pre_labels（list）: Generated labels by K-means clustering
        """
        self.graph = graph
        self.embeddings_list = embeddings_list
        self.pre_labels = None

    def cluster(self):
        """
        Performs K-means clustering on a list of node embeddings.
        """
        Kmeans = KMeans(
            n_clusters=2,           # Number of clusters
            random_state=160,       # Random seed
            n_init=10,              # Number of initializations
            max_iter=300,           # Maximum number of iterations
            tol=1e-4,               # Tolerance for convergence
            algorithm='auto'        # K-means algorithm
        )  
        Kmeans.fit(self.embeddings_list)
        
        self.pre_labels = Kmeans.labels_
        

    def evaluate(self, true_labels: list):
        """
        Evaluate the model embeddings using silhouette score, accuracy, and normalized mutual information.

        Parameters:
        true_labels (list): True community labels for each node.

        Returns:
        tuple: Tuple containing silhouette score, accuracy, and NMI scores.
        """
        print("true labels =", true_labels)
        print("predicted labels=", self.pre_labels)
        # Compute silhouette score
        silhouette = silhouette_score(
            self.embeddings_list, self.pre_labels, metric='euclidean')

        # Compute accuracy
        accuracy = accuracy_score(true_labels, self.pre_labels)

        # Compute normalized mutual information
        nmi = normalized_mutual_info_score(true_labels, self.pre_labels)

        return silhouette, accuracy, nmi
