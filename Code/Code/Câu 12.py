from flask import Blueprint, render_template, jsonify, request

from website.services.aideom_integrated_service import run_aideom_integrated_model


bai12_bp = Blueprint("bai12", __name__, url_prefix="/bai-12")


def parse_float(value, default):
    if value is None or value == "":
        return default

    if isinstance(value, (int, float)):
        return float(value)

    return float(str(value).replace(",", "."))


@bai12_bp.route("/")
@bai12_bp.route("")
def page():
    return render_template("bai12_integrated.html", active_page="bai12")


@bai12_bp.route("/api/run-model", methods=["POST"])
def run_model():
    try:
        params = request.get_json() or {}

        annual_budget = parse_float(params.get("annual_budget"), 1000)

        result = run_aideom_integrated_model(
            annual_budget=annual_budget
        )

        if not result.get("success"):
            return jsonify({
                "success": False,
                "message": result.get("message", "Không chạy được mô hình AIDEOM-VN tích hợp")
            }), 500

        return jsonify({
            "success": True,
            "data": result
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500