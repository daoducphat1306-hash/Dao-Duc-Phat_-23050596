from flask import Blueprint, render_template, jsonify, request

from website.services.project_mip_service import run_project_mip_model


bai5_bp = Blueprint("bai5", __name__, url_prefix="/bai-5")


def parse_float(value, default):
    if value is None or value == "":
        return default

    if isinstance(value, (int, float)):
        return float(value)

    return float(str(value).replace(",", "."))


def parse_int(value, default):
    return int(parse_float(value, default))


@bai5_bp.route("/")
@bai5_bp.route("")
def page():
    return render_template("bai5_mip.html", active_page="bai5")


@bai5_bp.route("/api/run-model", methods=["POST"])
def run_model():
    try:
        params = request.get_json() or {}

        total_budget = parse_float(params.get("total_budget"), 80000)
        year12_budget = parse_float(params.get("year12_budget"), 40000)
        min_projects = parse_int(params.get("min_projects"), 7)
        max_projects = parse_int(params.get("max_projects"), 11)

        result = run_project_mip_model(
            total_budget=total_budget,
            year12_budget=year12_budget,
            min_projects=min_projects,
            max_projects=max_projects
        )

        if not result.get("success"):
            return jsonify({
                "success": False,
                "message": result.get("message", "Không giải được mô hình MIP chọn dự án")
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