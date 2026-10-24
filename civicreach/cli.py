"""
Command-Line Interface (CLI) for CivicReach AI
Allows querying Indian penal codes, decrypting court notices, and screening NALSA eligibility from terminal.
"""

import argparse
import json
import sys

# Ensure UTF-8 output on Windows consoles to prevent cp1252 UnicodeEncodeError
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from .legal_engine import LegalEngine
from .server import start_server

def main():
    parser = argparse.ArgumentParser(
        description="CivicReach AI — Indian Public Services & Legal Aid CLI Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m civicreach search "bail under bnss" --lang hi
  python -m civicreach decrypt "Court summons SDM Section 145 CrPC" --lang hi
  python -m civicreach aid --woman --income 120000 --lang en
  python -m civicreach serve --port 8000
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # Command 1: search
    search_parser = subparsers.add_parser("search", help="Search Indian laws and penal codes")
    search_parser.add_argument("query", type=str, help="Legal topic, crime, or section to query")
    search_parser.add_argument("--lang", type=str, default="en", choices=["en", "hi", "bn", "mr", "ta"], help="Output language")

    # Command 2: decrypt
    decrypt_parser = subparsers.add_parser("decrypt", help="Demystify court summons, police notice, or hospital bill")
    decrypt_parser.add_argument("text", type=str, help="Text of the notice to decrypt")
    decrypt_parser.add_argument("--lang", type=str, default="en", choices=["en", "hi", "bn", "mr", "ta"], help="Output language")

    # Command 3: aid
    aid_parser = subparsers.add_parser("aid", help="Check Section 12 NALSA free legal aid eligibility")
    aid_parser.add_argument("--woman", action="store_true", help="Applicant is a woman or child")
    aid_parser.add_argument("--scst", action="store_true", help="Applicant is SC or ST")
    aid_parser.add_argument("--pwd", action="store_true", help="Applicant is a person with disability")
    aid_parser.add_argument("--custody", action="store_true", help="Applicant is in custody / undertrial")
    aid_parser.add_argument("--income", type=float, default=0.0, help="Annual household income in INR")
    aid_parser.add_argument("--state", type=str, default="default", help="Indian State name")
    aid_parser.add_argument("--lang", type=str, default="en", choices=["en", "hi", "bn", "mr", "ta"], help="Output language")

    # Command 4: serve
    serve_parser = subparsers.add_parser("serve", help="Start the web server and REST API")
    serve_parser.add_argument("--host", type=str, default="0.0.0.0", help="Host address")
    serve_parser.add_argument("--port", type=int, default=8000, help="Port number")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    engine = LegalEngine()

    if args.command == "search":
        results = engine.search(args.query, lang=args.lang)
        print(f"\n🔍 Found {len(results)} relevant Indian statutory records for '{args.query}' [{args.lang.upper()}]:\n")
        for i, res in enumerate(results, 1):
            print(f"[{i}] {res['act']} — {res['section']}")
            print(f"    Title: {res['title']}")
            print(f"    Plain Meaning: {res['plain_language']}")
            print(f"    Next Action: {res['rights_and_actions']}")
            print(f"    Free Legal Aid: {'Yes (NALSA Guaranteed)' if res['free_legal_aid_applicable'] else 'No'}\n")

    elif args.command == "decrypt":
        result = engine.decrypt_notice(args.text, lang=args.lang)
        print(f"\n📜 Kanoon Samjho Notice Decryption [{args.lang.upper()}]:")
        print(f"    Type: {result['detected_type']}")
        print(f"    Status: {result['panic_reduction']}")
        print(f"    Plain Meaning: {result['plain_meaning']}")
        print(f"    Immediate Action: {result['action_steps']}")
        print(f"    Governing Law: {result['relevant_statute']}\n")

    elif args.command == "aid":
        data = {
            "is_woman_or_child": args.woman,
            "is_sc_st": args.scst,
            "is_pwd": args.pwd,
            "is_custody": args.custody,
            "annual_income": args.income,
            "state": args.state
        }
        res = engine.check_nalsa_eligibility(data, lang=args.lang)
        print(f"\n⚖️  NALSA Section 12 Free Legal Aid Eligibility Result:")
        print(f"    Status: {res['status']}")
        print(f"    Certificate ID: {res['certificate_id']}")
        print(f"    Summary: {res['summary']}")
        print(f"    Action: {res['action']}")
        print(f"    Helpline: {res['helpline']}\n")

    elif args.command == "serve":
        start_server(host=args.host, port=args.port)

if __name__ == "__main__":
    main()
