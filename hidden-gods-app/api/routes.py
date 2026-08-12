"""
API Routes for Hidden Gods
"""
from flask import Blueprint, request, jsonify
from werkzeug.exceptions import BadRequest
from game import game_state, Stat
from game.session import session_manager
from game.moves import resolve_move, list_moves, get_move

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.route("/roll", methods=["GET"])
def roll_dice():
    stat_name = request.args.get("stat")
    value = request.args.get("value", default=0, type=int)
    stat = None
    if stat_name:
        try:
            stat = Stat[stat_name.upper()]
        except KeyError:
            raise BadRequest(f"Unknown stat: {stat_name}")
    result = game_state.roll_dice(stat, value)
    return jsonify({
        "dice": result.dice,
        "total": result.total,
        "stat": stat_name,
        "stat_value": value,
        "final_value": result.final_value,
        "outcome": result.outcome.value
    })


@api_bp.route("/move", methods=["GET"])
def resolve_move_endpoint():
    move_name = request.args.get("name")
    character = request.args.get("character", "Player")
    stat_name = request.args.get("stat")
    value = request.args.get("value", default=0, type=int)
    if not move_name:
        raise BadRequest("Move name required.")
    stat = None
    if stat_name:
        try:
            stat = Stat[stat_name.upper()]
        except KeyError:
            raise BadRequest(f"Unknown stat: {stat_name}")
    outcome = resolve_move(move_name, character, value, stat)
    return jsonify({"outcome": outcome})


@api_bp.route("/anomaly", methods=["GET"])
def generate_anomaly():
    layer = request.args.get("layer")
    anomaly = game_state.generate_anomaly(layer)
    return jsonify({
        "name": anomaly.name,
        "layer": anomaly.layer,
        "manifestation": anomaly.manifestation,
        "clue": anomaly.clue,
        "purpose": anomaly.purpose,
        "risk": anomaly.risk,
        "god": anomaly.god
    })


@api_bp.route("/layer", methods=["GET"])
def generate_layer():
    layer = game_state.generate_layer()
    return jsonify({"name": layer.name, "theme": layer.theme, "rules": layer.rules, "god": layer.god})


@api_bp.route("/god", methods=["GET"])
def generate_god():
    god = game_state.generate_god()
    return jsonify({"god": god})


@api_bp.route("/navigator/speak", methods=["GET"])
def navigator_speak():
    from ontos-language.ONTOSplayground.tools.navigator import Navigator
    nav = Navigator()
    message = request.args.get("message", "")
    return jsonify({"response": nav.speak(message)})


@api_bp.route("/navigator/ontos", methods=["GET"])
def navigator_ontos():
    from ontos-language.ONTOSplayground.tools.navigator import Navigator
    nav = Navigator()
    message = request.args.get("message", "")
    return jsonify({"response": nav.speak(message, as_ontos=True)})


@api_bp.route("/session/start", methods=["POST"])
def start_session():
    data = request.get_json() or {}
    session = session_manager.create_session(
        data.get("title", "Untitled Session"),
        data.get("characters", []),
        data.get("layer", "Base Reality")
    )
    return jsonify({
        "id": session.id,
        "title": session.title,
        "date": session.date,
        "current_layer": session.current_layer,
        "characters": session.characters
    })


@api_bp.route("/session/end", methods=["POST"])
def end_session():
    session = session_manager.end_session()
    if session:
        return jsonify({
            "id": session.id,
            "title": session.title,
            "log_entries": len(session.log),
            "anomalies_encountered": len(session.anomalies_encountered)
        })
    raise BadRequest("No active session")


@api_bp.route("/session/info", methods=["GET"])
def session_info():
    summary = session_manager.get_session_summary()
    if "error" in summary:
        raise BadRequest(summary["error"])
    return jsonify(summary)


@api_bp.route("/moves", methods=["GET"])
def list_moves_endpoint():
    archetype = request.args.get("archetype")
    moves = list_moves(archetype)
    move_list = [{"name": m, "stat": get_move(m).get("stat", Stat.COOL).value} for m in moves]
    return jsonify({"moves": move_list})
