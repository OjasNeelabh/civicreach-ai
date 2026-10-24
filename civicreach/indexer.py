"""
Semantic & Statutory Legal Indexer for CivicReach AI
Trains on Indian statutory database, BNS/IPC mappings, and plain-language legal definitions.
"""

import math
import re
from typing import List, Dict, Any, Tuple

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False


class LegalSearchIndexer:
    def __init__(self, laws: List[Dict[str, Any]]):
        self.laws = laws
        self.corpus = []
        self.doc_ids = []
        self.vectorizer = None
        self.tfidf_matrix = None
        self._build_index()

    def _tokenize(self, text: str) -> List[str]:
        """Simple multilingual whitespace and punctuation tokenizer."""
        return re.findall(r"[\w\u0900-\u097F\u0980-\u09FF\u0B80-\u0BFF]+", text.lower())

    def _build_index(self):
        """Constructs text corpus from laws and fits TF-IDF model."""
        self.corpus = []
        self.doc_ids = []

        for law in self.laws:
            t = law.get("title", {})
            p = law.get("plain_language", {})
            a = law.get("rights_and_actions", {})
            
            # Aggregate all multi-language terms, act names, and legacy IPC/CrPC numbers
            doc_text = " ".join([
                law.get("id", ""),
                law.get("act", ""),
                law.get("section", ""),
                law.get("legacy_ref", ""),
                " ".join(t.values()),
                " ".join(law.get("keywords", [])),
                law.get("description", ""),
                " ".join(p.values()),
                " ".join(a.values())
            ])
            self.corpus.append(doc_text)
            self.doc_ids.append(law.get("id"))

        if SKLEARN_AVAILABLE and len(self.corpus) > 0:
            self.vectorizer = TfidfVectorizer(token_pattern=r"(?u)\b\w+\b")
            self.tfidf_matrix = self.vectorizer.fit_transform(self.corpus)

    def search(self, query: str, top_k: int = 4) -> List[Tuple[Dict[str, Any], float]]:
        """Searches indexed Indian laws using TF-IDF or keyword frequency."""
        if not query.strip() or not self.laws:
            return [(law, 1.0) for law in self.laws[:top_k]]

        query_clean = query.strip().lower()

        # Method 1: Sklearn Vector Similarity
        if SKLEARN_AVAILABLE and self.vectorizer is not None and self.tfidf_matrix is not None:
            try:
                query_vec = self.vectorizer.transform([query_clean])
                sims = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
                
                # Boost if exact section or keyword match
                results = []
                for idx, score in enumerate(sims):
                    law = self.laws[idx]
                    boost = 0.0
                    
                    # Boost exact section numbers (e.g. "341", "420", "39a", "145", "173")
                    sec = law.get("section", "").lower()
                    legacy = law.get("legacy_ref", "").lower()
                    if any(term in query_clean for term in [sec, legacy]) and len(query_clean) > 2:
                        boost += 0.5
                    
                    # Boost keyword matches
                    for kw in law.get("keywords", []):
                        if kw.lower() in query_clean:
                            boost += 0.3
                            
                    results.append((law, float(score + boost)))

                results.sort(key=lambda x: x[1], reverse=True)
                return results[:top_k]
            except Exception:
                pass

        # Method 2: Pure Python Fallback (BM25-style keyword overlap)
        tokens = set(self._tokenize(query_clean))
        results = []
        for law in self.laws:
            score = 0.0
            doc_text = " ".join([
                law.get("act", ""),
                law.get("section", ""),
                law.get("legacy_ref", ""),
                " ".join(law.get("title", {}).values()),
                " ".join(law.get("keywords", [])),
                " ".join(law.get("plain_language", {}).values())
            ]).lower()
            doc_tokens = self._tokenize(doc_text)

            for token in tokens:
                count = doc_tokens.count(token)
                if count > 0:
                    score += 1.0 + math.log(count)

            if score > 0:
                results.append((law, score))

        results.sort(key=lambda x: x[1], reverse=True)
        if not results:
            return [(law, 0.5) for law in self.laws[:top_k]]
        return results[:top_k]
