import numpy as np


class CalculationModel:
    @staticmethod
    def simple_additive_weighting(criteria_weights, decision_matrix):
        if criteria_weights.shape[0] != decision_matrix.shape[1]:
            raise ValueError(
                "The number of criteria weights must match the number of columns in the decision matrix."
            )

        normalized_matrix = decision_matrix / decision_matrix.sum(axis=0)
        weighted_matrix = normalized_matrix * criteria_weights
        scores = weighted_matrix.sum(axis=1)
        return scores

    @staticmethod
    def weighted_product(criteria_weights, decision_matrix):
        if criteria_weights.shape[0] != decision_matrix.shape[1]:
            raise ValueError(
                "The number of criteria weights must match the number of columns in the decision matrix."
            )

        normalized_matrix = decision_matrix / decision_matrix.sum(axis=0)
        powered_matrix = np.power(normalized_matrix, criteria_weights)
        scores = powered_matrix.prod(axis=1)
        return scores
