import networkx as nx
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from utils.logger import Logger
from utils.error_handler import ErrorHandler

class PredictiveModeling:
    def __init__(self, graph_structure):
        self.graph = graph_structure
        self.logger = Logger("PredictiveModeling")
        self.error_handler = ErrorHandler()

    def prepare_link_prediction_data(self):
        try:
            G = self.graph.to_networkx()
            edges = list(G.edges())
            non_edges = list(nx.non_edges(G))
            
            X = []
            y = []
            
            for edge in edges:
                X.append(self._extract_features(G, edge[0], edge[1]))
                y.append(1)
            
            for non_edge in non_edges[:len(edges)]:  # Balance the dataset
                X.append(self._extract_features(G, non_edge[0], non_edge[1]))
                y.append(0)
            
            return X, y
        except Exception as e:
            self.error_handler.handle_error(e, "Error preparing link prediction data")
            return None, None

    def _extract_features(self, G, node1, node2):
        common_neighbors = len(list(nx.common_neighbors(G, node1, node2)))
        jaccard_coefficient = list(nx.jaccard_coefficient(G, [(node1, node2)]))[0][2]
        adamic_adar_index = list(nx.adamic_adar_index(G, [(node1, node2)]))[0][2]
        preferential_attachment = list(nx.preferential_attachment(G, [(node1, node2)]))[0][2]
        return [common_neighbors, jaccard_coefficient, adamic_adar_index, preferential_attachment]

    def train_link_prediction_model(self):
        try:
            X, y = self.prepare_link_prediction_data()
            if X is None or y is None:
                return None
            
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            model = LogisticRegression()
            model.fit(X_train, y_train)
            
            y_pred = model.predict(X_test)
            
            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred)
            recall = recall_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)
            
            self.logger.info(f"Link Prediction Model Performance: Accuracy={accuracy:.2f}, Precision={precision:.2f}, Recall={recall:.2f}, F1={f1:.2f}")
            
            return model
        except Exception as e:
            self.error_handler.handle_error(e, "Error training link prediction model")
            return None

    def predict_new_links(self, model, top_n=10):
        try:
            G = self.graph.to_networkx()
            non_edges = list(nx.non_edges(G))
            
            predictions = []
            for non_edge in non_edges:
                features = self._extract_features(G, non_edge[0], non_edge[1])
                prob = model.predict_proba([features])[0][1]
                predictions.append((non_edge[0], non_edge[1], prob))
            
            predictions.sort(key=lambda x: x[2], reverse=True)
            return predictions[:top_n]
        except Exception as e:
            self.error_handler.handle_error(e, "Error predicting new links")
            return []