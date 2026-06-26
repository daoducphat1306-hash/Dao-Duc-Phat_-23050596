from flask import Blueprint, render_template, jsonify, request

from website.services.stochastic_sp_service import run_stochastic_sp_model


bai10_bp = Blueprint("bai10", __name__, url_prefix="/bai-10")


def parse_float(value, default):
    if value is None or value == "":
        return default

    if isinstance(value, (int, float)):
        return float(value)

    return float(str(value).replace(",", "."))


@bai10_bp.route("/")
@bai10_bp.route("")
def page():
    return render_template("bai10_stochastic.html", active_page="bai10")


@bai10_bp.route("/api/run-model", methods=["POST"])
def run_model():
    try:
        params = request.get_json() or {}

        budget_first = parse_float(params.get("budget_first"), 65000)
        budget_second = parse_float(params.get("budget_second"), 15000)
        ai_h_ratio = parse_float(params.get("ai_h_ratio"), 0.5)

        result = run_stochastic_sp_model(
            budget_first=budget_first,
            budget_second=budget_second,
            ai_h_ratio=ai_h_ratio
        )

        if not result.get("success"):
            return jsonify({
                "success": False,
                "message": result.get("message", "Không chạy được mô hình stochastic programming")
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