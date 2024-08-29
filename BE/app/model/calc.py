import numpy


class CalculationModel:
    @staticmethod
    def simple_additive_weighting(criteria_weights, descision_matrix):
        nomralized_matrix = descision_matrix / descision_matrix.sum(axis=0)
        weighted_matrix = nomralized_matrix * criteria_weights
        scores = weighted_matrix.sum(axis=1)
        return scores

    @staticmethod
    def weighted_products(criteria_weights, descision_matrix):
        normalize_matrix = descision_matrix / descision_matrix.sum(axis=0)
        powered_matrix = np.power(normalize_matrix, criteria_weights)
        scores = powered_matrix.prod(axis=1)
        return scores
