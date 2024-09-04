import numpy as np
from app.connection.connection import Connection
import json


class CalculationModel:
    def __init__(self) -> None:
        self.collection = Connection.get_collection("results")

    def simple_additive_weighting(
        self, criteria_weights, decision_matrix, criteria_types
    ) -> any:

        if len(criteria_weights) != decision_matrix.shape[1]:
            raise ValueError(
                "The number of criteria weights must match the number of columns in the decision matrix."
            )

        normalized_matrix = np.zeros_like(decision_matrix, dtype=float)
        for i, criterion_type in enumerate(criteria_types):
            if criterion_type == "cost":
                normalized_matrix[:, i] = (
                    decision_matrix[:, i].min() / decision_matrix[:, i]
                )
            elif criterion_type == "benefit":
                normalized_matrix[:, i] = (
                    decision_matrix[:, i] / decision_matrix[:, i].max()
                )

        weighted_matrix = normalized_matrix * criteria_weights
        scores = weighted_matrix.sum(axis=1)
        self.save_results(
            "simple_additive_weighting", criteria_weights, decision_matrix, scores
        )

        return scores

    def weighted_product(
        self, criteria_weights, decision_matrix, criteria_types
    ) -> any:

        if len(criteria_weights) != decision_matrix.shape[1]:
            raise ValueError(
                "The number of criteria weights must match the number of columns in the decision matrix."
            )

        powered_matrix = np.zeros_like(decision_matrix, dtype=float)
        for i, criterion_type in enumerate(criteria_types):
            if criterion_type == "cost":
                powered_matrix[:, i] = np.power(
                    1 / decision_matrix[:, i], criteria_weights[i]
                )
            elif criterion_type == "benefit":
                powered_matrix[:, i] = np.power(
                    decision_matrix[:, i], criteria_weights[i]
                )

        scores = powered_matrix.prod(axis=1)

        self.save_results("weighted_product", criteria_weights, decision_matrix, scores)

        return scores

    def save_results(
        self, method_name, criteria_weights, decision_matrix, scores
    ) -> None:
        """
        Save the results of the calculation in the database.
        """
        decision_matrix_str = json.dumps(decision_matrix.tolist())

        data = {
            "method": method_name,
            "criteria_weights": criteria_weights.tolist(),
            "decision_matrix": decision_matrix_str,
            "scores": scores.tolist(),
        }

        self.collection.add(data)

    def get_results(self):
        """
        Retrieve results from the database.
        """
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
