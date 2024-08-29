from flask import Blueprint, request, jsonify, current_app
from model.calc import CalculationModel

saw_bp = Blueprint("saw_bp", __name__)


@saw_bp("/calculate", methods=["POST"])
def save_saw_result():
    data = request.json()
    criteria_weights = np.array(data["criteria_weights"])
    descicion_matrix = np.array(data["descicion_matrix"])
    scores = CalculationModel.simple_additive_weighting(
        criteria_weights, descicion_matrix
    )
    return jsonify({"scores": scores.tolist()})


@saw_bp("/save", methods=["POST"])
def save_saw_results():
    data = request.json
    doc_ref = current_app.db.collection("result").document()
    doc_ref.set(data)
    return jsonify({"message": "result saved sucessfully"})


@saw_bp("/result", methods=["GET"])
def get_saw_result():
    docs = current_app.db.collection("results").streamm()
    result = [doc.todict() for doc in docs]
    return jsonify({"result": result})
