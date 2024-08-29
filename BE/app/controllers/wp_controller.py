from flask import Blueprint, request, jsonify, current_app
from models.calculation_model import CalculationModel
import numpy as np

wp_bp = Blueprint("wp_bp", __name__)


@wp_bp.route("/calculate", methods=["POST"])
def calculate_wp():
    data = request.json
    criteria_weights = np.array(data["criteria_weights"])
    decision_matrix = np.array(data["decision_matrix"])

    try:
        scores = CalculationModel.weighted_product(criteria_weights, decision_matrix)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify({"scores": scores.tolist()})


@wp_bp.route("/save", methods=["POST"])
def save_wp_results():
    data = request.json
    doc_ref = current_app.db.collection("results").document()
    doc_ref.set(data)

    return jsonify({"message": "Results saved successfully."})


@wp_bp.route("/results", methods=["GET"])
def get_wp_results():
    docs = current_app.db.collection("results").stream()
    results = [doc.to_dict() for doc in docs]

    return jsonify({"results": results})
