from flask import Blueprint, request, jsonify, current_app
from models.calculation_model import CalculationModel
import numpy as np

saw_bp = Blueprint("saw_bp", __name__)


@saw_bp.route("/calculate", methods=["POST"])
def calculate_saw():
    data = request.json
    criteria_weights = np.array(data["criteria_weights"])
    decision_matrix = np.array(data["decision_matrix"])

    try:
        scores = CalculationModel.simple_additive_weighting(
            criteria_weights, decision_matrix
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify({"scores": scores.tolist()})


@saw_bp.route("/save", methods=["POST"])
def save_saw_results():
    data = request.json
    doc_ref = current_app.db.collection("results").document()
    doc_ref.set(data)

    return jsonify({"message": "Results saved successfully."})


@saw_bp.route("/results", methods=["GET"])
def get_saw_results():
    docs = current_app.db.collection("results").stream()
    results = [doc.to_dict() for doc in docs]

    return jsonify({"results": results})
