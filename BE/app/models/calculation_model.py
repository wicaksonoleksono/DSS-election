import numpy as np
from app.connection.connection import Connection
import json


class CalculationModel:
    def __init__(self) -> None:
        self.collection = Connection.get_collection("results")

    def simple_additive_weighting(self, criteria_weights, decision_matrix) -> any:
        if criteria_weights.shape[0] != decision_matrix.shape[1]:
            raise ValueError(
                "The number of criteria weights must match the number of columns in the decision matrix."
            )
        normalized_matrix = decision_matrix / decision_matrix.sum(axis=0)
        weighted_matrix = normalized_matrix * criteria_weights
        scores = weighted_matrix.sum(axis=1)

        self.save_results(
            "simple_additive_weighting", criteria_weights, decision_matrix, scores
        )

        return scores

    def weighted_product(self, criteria_weights, decision_matrix) -> any:
        if criteria_weights.shape[0] != decision_matrix.shape[1]:
            raise ValueError(
                "The number of criteria weights must match the number of columns in the decision matrix."
            )

        normalized_matrix = decision_matrix / decision_matrix.sum(axis=0)
        powered_matrix = np.power(normalized_matrix, criteria_weights)
        scores = powered_matrix.prod(axis=1)

        self.save_results("weighted_product", criteria_weights, decision_matrix, scores)

        return scores

    def save_results(
        self, method_name, criteria_weights, decision_matrix, scores
    ) -> None:
        decision_matrix_str = json.dumps(decision_matrix.tolist())

        data = {
            "method": method_name,
            "criteria_weights": criteria_weights.tolist(),
            "decision_matrix": decision_matrix_str,
            "scores": scores.tolist(),
        }

        self.collection.add(data)

    def get_results(self):
        docs = self.collection.stream()
        results = []
        for doc in docs:
            data = doc.to_dict()
            if "decision_matrix" in data:
                try:
                    data["decision_matrix"] = json.loads(data["decision_matrix"])
                except json.JSONDecodeError:
                    data["decision_matrix"] = None
            else:
                data["decision_matrix"] = None
            results.append(data)
        return results
