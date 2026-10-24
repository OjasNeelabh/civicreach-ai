"""
Database Loader and SQLite Repository for CivicReach AI
Manages statutory definitions, BNS/IPC mappings, and case notice templates.
"""

import json
import os
import sqlite3
from typing import List, Dict, Any, Optional

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "indian_laws.json")
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "civicreach.sqlite")

class LegalDatabase:
    def __init__(self, json_path: str = DATA_PATH, db_path: str = DB_PATH):
        self.json_path = json_path
        self.db_path = db_path
        self.laws: List[Dict[str, Any]] = []
        self._load_data()
        self._sync_sqlite()

    def _load_data(self):
        if os.path.exists(self.json_path):
            with open(self.json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.laws = data.get("laws", [])
        else:
            self.laws = []

    def _sync_sqlite(self):
        """Syncs JSON records into a lightweight local SQLite database for fast queries."""
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS indian_laws (
                id TEXT PRIMARY KEY,
                category TEXT,
                act TEXT,
                section TEXT,
                legacy_ref TEXT,
                title_en TEXT,
                title_hi TEXT,
                title_bn TEXT,
                title_mr TEXT,
                title_ta TEXT,
                keywords TEXT,
                description TEXT,
                plain_en TEXT,
                plain_hi TEXT,
                plain_bn TEXT,
                plain_mr TEXT,
                plain_ta TEXT,
                actions_en TEXT,
                actions_hi TEXT,
                actions_bn TEXT,
                actions_mr TEXT,
                actions_ta TEXT,
                free_legal_aid INTEGER
            )
        """)

        for law in self.laws:
            t = law.get("title", {})
            p = law.get("plain_language", {})
            a = law.get("rights_and_actions", {})
            cur.execute("""
                INSERT OR REPLACE INTO indian_laws VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                law.get("id"),
                law.get("category"),
                law.get("act"),
                law.get("section"),
                law.get("legacy_ref", ""),
                t.get("en", ""), t.get("hi", ""), t.get("bn", ""), t.get("mr", ""), t.get("ta", ""),
                ",".join(law.get("keywords", [])),
                law.get("description", ""),
                p.get("en", ""), p.get("hi", ""), p.get("bn", ""), p.get("mr", ""), p.get("ta", ""),
                a.get("en", ""), a.get("hi", ""), a.get("bn", ""), a.get("mr", ""), a.get("ta", ""),
                1 if law.get("free_legal_aid_applicable") else 0
            ))
        conn.commit()
        conn.close()

    def get_all_laws(self) -> List[Dict[str, Any]]:
        return self.laws

    def get_law_by_id(self, law_id: str) -> Optional[Dict[str, Any]]:
        for law in self.laws:
            if law.get("id") == law_id:
                return law
        return None
