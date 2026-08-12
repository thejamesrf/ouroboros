#!/usr/bin/env python3
"""
Hidden Gods Game App
====================
Main entry point for the Hidden Gods TTRPG app.
Supports both CLI and web (Flask) modes.

Usage:
  CLI: python3 main.py [command] [args]
  Web: python3 main.py --web
"""

import argparse
import sys
from typing import Optional

from game import game_state, Character, Stat, RollOutcome
from game.session import session_manager
from game.moves import resolve_move, list_moves, get_move


# ============================================
# CLI COMMANDS
# ============================================

def cmd_roll(args):
    """Roll dice: roll [stat] [value]"""
    stat = None
    stat_value = 0
    
    if args.stat:
        try:
            stat = Stat[args.stat.upper()]
        except KeyError:
            print(f"Error: Unknown stat '{args.stat}'. Use Cool, Hard, Hot, Sharp, Weird, or Hx.")
            return
    
    if args.value:
        stat_value = int(args.value)
    
    result = game_state.roll_dice(stat, stat_value)
    stat_str = f"+{stat.value}{stat_value}" if stat else f"+{stat_value}" if stat_value else ""
    print(f"Rolled {result.dice[0]}+{result.dice[1]}{stat_str} = {result.final_value} ({result.outcome.value})")


def cmd_move(args):
    """Resolve a move: move <name> [character] [stat] [value]"""
    if len(args.name) < 1:
        print("Error: Move name required.")
        return
    
    move_name = " ".join(args.name)
    character_name = args.character if args.character else "Player"
    stat = None
    stat_value = 0
    
    if args.stat:
        try:
            stat = Stat[args.stat.upper()]
        except KeyError:
            print(f"Error: Unknown stat '{args.stat}'. Use Cool, Hard, Hot, Sharp, Weird, or Hx.")
            return
    
    if args.value:
        stat_value = int(args.value)
    
    # Get the move's default stat if not provided
    move = get_move(move_name)
    if move and not stat:
        stat = move.get("stat")
    
    outcome = resolve_move(move_name, character_name, stat_value, stat)
    print(outcome)


def cmd_anomaly(args):
    """Generate an anomaly: anomaly [layer]"""
    layer = args.layer if args.layer else None
    anomaly = game_state.generate_anomaly(layer)
    
    print(f"Anomaly: {anomaly.name}")
    print(f"  Layer: {anomaly.layer}")
    print(f"  Manifestation: {anomaly.manifestation}")
    print(f"  Clue: {anomaly.clue}")
    print(f"  Purpose: {anomaly.purpose}")
    print(f"  Risk: {anomaly.risk}")
    print(f"  God: {anomaly.god}")


def cmd_layer(args):
    """Generate a layer: layer"""
    layer = game_state.generate_layer()
    print(f"Layer: {layer.name}")
    print(f"  Theme: {layer.theme}")
    print(f"  Rules: {layer.rules}")
    print(f"  God: {layer.god}")


def cmd_god(args):
    """Generate a god: god"""
    god = game_state.generate_god()
    print(f"God: {god}")


def cmd_speak(args):
    """Navigator speaks: speak <message>"""
    from ontos-language.ONTOSplayground.tools.navigator import Navigator
    nav = Navigator()
    message = " ".join(args.message)
    print(nav.speak(message))


def cmd_ontos(args):
    """Navigator speaks in Ontos: ontos <message>"""
    from ontos-language.ONTOSplayground.tools.navigator import Navigator
    nav = Navigator()
    message = " ".join(args.message)
    print(nav.speak(message, as_ontos=True))


def cmd_session(args):
    """Manage sessions: session <start|end|info> [args]"""
    if args.action == "start":
        if not args.title:
            print("Error: Session title required.")
            return
        characters = args.characters.split(",") if args.characters else []
        layer = args.layer if args.layer else "Base Reality"
        session = session_manager.create_session(args.title, characters, layer)
        print(f"Started session: {session.id} ({session.title})")
        print(f"  Layer: {session.current_layer}")
        print(f"  Characters: {', '.join(session.characters)}")
    
    elif args.action == "end":
        session = session_manager.end_session()
        if session:
            print(f"Ended session: {session.id} ({session.title})")
            print(f"  Log entries: {len(session.log)}")
            print(f"  Anomalies encountered: {len(session.anomalies_encountered)}")
        else:
            print("No active session to end.")
    
    elif args.action == "info":
        summary = session_manager.get_session_summary()
        if "error" in summary:
            print(summary["error"])
        else:
            print(f"Session: {summary['title']} ({summary['id']})")
            print(f"  Date: {summary['date']}")
            print(f"  Layer: {summary['current_layer']}")
            print(f"  Characters: {', '.join(summary['characters'])}")
            print(f"  Anomalies: {len(summary['anomalies_encountered'])}")
            print(f"  Log entries: {summary['log_size']}")
    
    else:
        print("Error: Unknown session action. Use start, end, or info.")


def cmd_character(args):
    """Manage characters: character <create|list|show> [args]"""
    if args.action == "create":
        if not args.name or not args.player or not args.archetype:
            print("Error: name, player, and archetype required.")
            return
        
        character = Character(
            name=args.name,
            player=args.player,
            archetype=args.archetype,
            secondary_archetype=args.secondary_archetype,
            stats={},
            moves=[],
            hx={},
            ifs_parts=args.ifs_parts.split(",") if args.ifs_parts else []
        )
        
        # Set stats from arguments
        for stat_name in ["cool", "hard", "hot", "sharp", "weird"]:
            stat_value = getattr(args, stat_name, 0)
            if stat_value:
                character.stats[Stat[stat_name.upper()]] = stat_value
        
        game_state.add_character(character)
        print(f"Created character: {character.name}")
        print(f"  Player: {character.player}")
        print(f"  Archetype: {character.archetype}")
        if character.secondary_archetype:
            print(f"  Secondary: {character.secondary_archetype}")
        print(f"  IFS Parts: {', '.join(character.ifs_parts)}")
        print(f"  Stats: {', '.join([f'{s.value}{v}' for s, v in character.stats.items()])}")
    
    elif args.action == "list":
        if not game_state.characters:
            print("No characters created yet.")
            return
        for name, character in game_state.characters.items():
            print(f"- {name} ({character.archetype}), played by {character.player}")
    
    elif args.action == "show":
        if not args.name:
            print("Error: Character name required.")
            return
        character = game_state.get_character(args.name)
        if not character:
            print(f"Error: Character '{args.name}' not found.")
            return
        
        print(f"Character: {character.name}")
        print(f"  Player: {character.player}")
        print(f"  Archetype: {character.archetype}")
        if character.secondary_archetype:
            print(f"  Secondary: {character.secondary_archetype}")
        print(f"  IFS Parts: {', '.join(character.ifs_parts)}")
        print(f"  Stats: {', '.join([f'{s.value}{v}' for s, v in character.stats.items()])}")
        print(f"  Moves: {', '.join(character.moves)}")
        print(f"  Equipment: {', '.join(character.equipment)}")
        print(f"  Notes: {character.notes}")
    
    else:
        print("Error: Unknown character action. Use create, list, or show.")


def cmd_moves(args):
    """List moves: moves [archetype]"""
    archetype = args.archetype if args.archetype else None
    moves = list_moves(archetype)
    
    if not moves:
        print("No moves found.")
        return
    
    print(f"Moves {'for ' + archetype if archetype else ''}:")
    for move in moves:
        move_data = get_move(move)
        stat = move_data.get("stat", "Unknown")
        print(f"  - {move} ({stat.value})")


def cmd_navigator(args):
    """Navigator commands: navigator <speak|ontos|roll|move> [args]"""
    from ontos-language.ONTOSplayground.tools.navigator import Navigator
    nav = Navigator()
    
    if args.action == "speak":
        message = " ".join(args.message)
        print(nav.speak(message))
    
    elif args.action == "ontos":
        message = " ".join(args.message)
        print(nav.speak(message, as_ontos=True))
    
    elif args.action == "roll":
        stat = None
        stat_value = 0
        if args.stat:
            try:
                stat = Stat[args.stat.upper()]
            except KeyError:
                print(f"Error: Unknown stat '{args.stat}'.")
                return
        if args.value:
            stat_value = int(args.value)
        result = nav.roll_dice(stat, stat_value)
        print(f"Rolled {result.final_value} ({result.outcome.value})")
    
    elif args.action == "move":
        if not args.move_name:
            print("Error: Move name required.")
            return
        stat = None
        stat_value = 0
        if args.stat:
            try:
                stat = Stat[args.stat.upper()]
            except KeyError:
                print(f"Error: Unknown stat '{args.stat}'.")
                return
        if args.value:
            stat_value = int(args.value)
        outcome = nav.resolve_move(args.move_name, stat, stat_value)
        print(outcome)
    
    else:
        print("Error: Unknown navigator action. Use speak, ontos, roll, or move.")


# ============================================
# WEB API (Flask)
# ============================================

def run_web_api():
    """Run the Flask web API."""
    from flask import Flask, request, jsonify
    from werkzeug.middleware.dispatcher import DispatcherMiddleware
    from werkzeug.serving import run_simple
    
    app = Flask(__name__)
    
    # API Routes
    @app.route("/api/roll", methods=["GET"])
    def api_roll():
        stat = request.args.get("stat")
        value = int(request.args.get("value", 0))
        
        stat_enum = None
        if stat:
            try:
                stat_enum = Stat[stat.upper()]
            except KeyError:
                return jsonify({"error": f"Unknown stat: {stat}"}), 400
        
        result = game_state.roll_dice(stat_enum, value)
        return jsonify({
            "dice": result.dice,
            "total": result.total,
            "stat": stat,
            "stat_value": value,
            "final_value": result.final_value,
            "outcome": result.outcome.value
        })
    
    @app.route("/api/move", methods=["GET"])
    def api_move():
        move_name = request.args.get("name")
        character = request.args.get("character", "Player")
        stat = request.args.get("stat")
        value = int(request.args.get("value", 0))
        
        if not move_name:
            return jsonify({"error": "Move name required"}), 400
        
        stat_enum = None
        if stat:
            try:
                stat_enum = Stat[stat.upper()]
            except KeyError:
                return jsonify({"error": f"Unknown stat: {stat}"}), 400
        
        outcome = resolve_move(move_name, character, value, stat_enum)
        return jsonify({"outcome": outcome})
    
    @app.route("/api/anomaly", methods=["GET"])
    def api_anomaly():
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
    
    @app.route("/api/layer", methods=["GET"])
    def api_layer():
        layer = game_state.generate_layer()
        return jsonify({
            "name": layer.name,
            "theme": layer.theme,
            "rules": layer.rules,
            "god": layer.god
        })
    
    @app.route("/api/navigator/speak", methods=["GET"])
    def api_navigator_speak():
        from ontos-language.ONTOSplayground.tools.navigator import Navigator
        nav = Navigator()
        message = request.args.get("message", "")
        response = nav.speak(message)
        return jsonify({"response": response})
    
    @app.route("/api/navigator/ontos", methods=["GET"])
    def api_navigator_ontos():
        from ontos-language.ONTOSplayground.tools.navigator import Navigator
        nav = Navigator()
        message = request.args.get("message", "")
        response = nav.speak(message, as_ontos=True)
        return jsonify({"response": response})
    
    @app.route("/api/session/start", methods=["POST"])
    def api_session_start():
        data = request.get_json()
        title = data.get("title", "Untitled Session")
        characters = data.get("characters", [])
        layer = data.get("layer", "Base Reality")
        
        session = session_manager.create_session(title, characters, layer)
        return jsonify({
            "id": session.id,
            "title": session.title,
            "date": session.date,
            "current_layer": session.current_layer,
            "characters": session.characters
        })
    
    @app.route("/api/session/end", methods=["POST"])
    def api_session_end():
        session = session_manager.end_session()
        if session:
            return jsonify({
                "id": session.id,
                "title": session.title,
                "log_entries": len(session.log),
                "anomalies_encountered": len(session.anomalies_encountered)
            })
        return jsonify({"error": "No active session"}), 400
    
    @app.route("/api/session/info", methods=["GET"])
    def api_session_info():
        summary = session_manager.get_session_summary()
        if "error" in summary:
            return jsonify(summary), 404
        return jsonify(summary)
    
    # Serve static files (for future frontend)
    @app.route("/")
    def index():
        return "Hidden Gods Game API. Use /api/ endpoints."
    
    # Run the app
    print("Starting Hidden Gods web API on http://localhost:5000")
    run_simple("localhost", 5000, app, use_reloader=True, use_debugger=True)


# ============================================
# MAIN
# ============================================

def main():
    parser = argparse.ArgumentParser(description="Hidden Gods Game App")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Roll command
    roll_parser = subparsers.add_parser("roll", help="Roll dice")
    roll_parser.add_argument("stat", nargs="?", help="Stat to add (Cool, Hard, Hot, Sharp, Weird, Hx)")
    roll_parser.add_argument("value", nargs="?", type=int, help="Stat value (e.g., 1 for +1)")
    
    # Move command
    move_parser = subparsers.add_parser("move", help="Resolve a move")
    move_parser.add_argument("name", nargs="+", help="Move name (e.g., Open Your Brain)")
    move_parser.add_argument("character", nargs="?", help="Character name")
    move_parser.add_argument("stat", nargs="?", help="Stat to use")
    move_parser.add_argument("value", nargs="?", type=int, help="Stat value")
    
    # Anomaly command
    anomaly_parser = subparsers.add_parser("anomaly", help="Generate an anomaly")
    anomaly_parser.add_argument("layer", nargs="?", help="Layer name (e.g., Debug)")
    
    # Layer command
    subparsers.add_parser("layer", help="Generate a layer")
    
    # God command
    subparsers.add_parser("god", help="Generate a god")
    
    # Speak command
    speak_parser = subparsers.add_parser("speak", help="Navigator speaks")
    speak_parser.add_argument("message", nargs="+", help="Message to the Navigator")
    
    # Ontos command
    ontos_parser = subparsers.add_parser("ontos", help="Navigator speaks in Ontos")
    ontos_parser.add_argument("message", nargs="+", help="Message to the Navigator")
    
    # Session command
    session_parser = subparsers.add_parser("session", help="Manage sessions")
    session_parser.add_argument("action", choices=["start", "end", "info"], help="Session action")
    session_parser.add_argument("title", nargs="?", help="Session title (for start)")
    session_parser.add_argument("characters", nargs="?", help="Comma-separated character names (for start)")
    session_parser.add_argument("layer", nargs="?", help="Starting layer (for start)")
    
    # Character command
    char_parser = subparsers.add_parser("character", help="Manage characters")
    char_parser.add_argument("action", choices=["create", "list", "show"], help="Character action")
    char_parser.add_argument("name", nargs="?", help="Character name")
    char_parser.add_argument("player", nargs="?", help="Player name")
    char_parser.add_argument("archetype", nargs="?", help="Primary archetype")
    char_parser.add_argument("secondary_archetype", nargs="?", help="Secondary archetype")
    char_parser.add_argument("ifs_parts", nargs="?", help="Comma-separated IFS parts")
    char_parser.add_argument("--cool", type=int, default=0, help="Cool stat value")
    char_parser.add_argument("--hard", type=int, default=0, help="Hard stat value")
    char_parser.add_argument("--hot", type=int, default=0, help="Hot stat value")
    char_parser.add_argument("--sharp", type=int, default=0, help="Sharp stat value")
    char_parser.add_argument("--weird", type=int, default=0, help="Weird stat value")
    
    # Moves command
    moves_parser = subparsers.add_parser("moves", help="List moves")
    moves_parser.add_argument("archetype", nargs="?", help="Filter by archetype")
    
    # Navigator command
    nav_parser = subparsers.add_parser("navigator", help="Navigator commands")
    nav_parser.add_argument("action", choices=["speak", "ontos", "roll", "move"], help="Navigator action")
    nav_parser.add_argument("message", nargs="*", help="Message (for speak/ontos)")
    nav_parser.add_argument("stat", nargs="?", help="Stat (for roll/move)")
    nav_parser.add_argument("value", nargs="?", type=int, help="Stat value (for roll/move)")
    nav_parser.add_argument("move_name", nargs="?", help="Move name (for move)")
    
    # Web mode
    parser.add_argument("--web", action="store_true", help="Run in web mode (Flask API)")
    
    args = parser.parse_args()
    
    if args.web:
        run_web_api()
    elif args.command == "roll":
        cmd_roll(args)
    elif args.command == "move":
        cmd_move(args)
    elif args.command == "anomaly":
        cmd_anomaly(args)
    elif args.command == "layer":
        cmd_layer(args)
    elif args.command == "god":
        cmd_god(args)
    elif args.command == "speak":
        cmd_speak(args)
    elif args.command == "ontos":
        cmd_ontos(args)
    elif args.command == "session":
        cmd_session(args)
    elif args.command == "character":
        cmd_character(args)
    elif args.command == "moves":
        cmd_moves(args)
    elif args.command == "navigator":
        cmd_navigator(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
