from flask import Blueprint, render_template, jsonify

from website.services.topsis_region_service import run_topsis_region_model


bai6_bp = Blueprint("bai6", __name__, url_prefix="/bai-6")


@bai6_bp.route("/")
@bai6_bp.route("")
def page():
    return render_template("bai6_topsis.html", active_page="bai6")


@bai6_bp.route("/api/run-model", methods=["POST"])
def run_model():
    try:
        result = run_topsis_region_model()

        if not result.get("success"):
            return jsonify({
                "success": False,
                "message": result.get("message", "Không chạy được mô hình TOPSIS")
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