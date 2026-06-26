from flask import Blueprint, render_template, jsonify, request

from website.services.qlearning_policy_service import run_qlearning_policy_model


bai11_bp = Blueprint("bai11", __name__, url_prefix="/bai-11")


def parse_float(value, default):
    if value is None or value == "":
        return default

    if isinstance(value, (int, float)):
        return float(value)

    return float(str(value).replace(",", "."))


def parse_int(value, default):
    return int(parse_float(value, default))


@bai11_bp.route("/")
@bai11_bp.route("")
def page():
    return render_template("bai11_qlearning.html", active_page="bai11")


@bai11_bp.route("/api/run-model", methods=["POST"])
def run_model():
    try:
        params = request.get_json() or {}

        episodes = parse_int(params.get("episodes"), 10000)
        alpha = parse_float(params.get("alpha"), 0.10)
        gamma = parse_float(params.get("gamma"), 0.95)
        eps_start = parse_float(params.get("eps_start"), 1.0)
        eps_end = parse_float(params.get("eps_end"), 0.05)
        eps_decay_episodes = parse_int(params.get("eps_decay_episodes"), 5000)
        eval_episodes = parse_int(params.get("eval_episodes"), 300)
        seed = parse_int(params.get("seed"), 42)

        result = run_qlearning_policy_model(
            episodes=episodes,
            alpha=alpha,
            gamma=gamma,
            eps_start=eps_start,
            eps_end=eps_end,
            eps_decay_episodes=eps_decay_episodes,
            eval_episodes=eval_episodes,
            seed=seed
        )

        if not result.get("success"):
            return jsonify({
                "success": False,
                "message": result.get("message", "Không chạy được mô hình Q-learning")
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