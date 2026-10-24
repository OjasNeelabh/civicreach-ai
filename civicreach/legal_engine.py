"""
Core Legal Engine for CivicReach AI
Performs multilingual statutory query reasoning, document notice decryption, and case routing.
"""

import re
from typing import Dict, Any, List
from .database import LegalDatabase
from .indexer import LegalSearchIndexer
from .nalsa_screener import NALSAScreener
from .i18n import get_text

class LegalEngine:
    def __init__(self):
        self.db = LegalDatabase()
        self.indexer = LegalSearchIndexer(self.db.get_all_laws())

    def search(self, query: str, lang: str = "en") -> List[Dict[str, Any]]:
        """Searches Indian laws and formats output in the requested language."""
        results = self.indexer.search(query, top_k=5)
        formatted = []
        for law, score in results:
            t = law.get("title", {})
            p = law.get("plain_language", {})
            a = law.get("rights_and_actions", {})
            
            formatted.append({
                "id": law.get("id"),
                "act": law.get("act"),
                "section": law.get("section"),
                "legacy_ref": law.get("legacy_ref"),
                "category": law.get("category"),
                "title": t.get(lang, t.get("en", "")),
                "plain_language": p.get(lang, p.get("en", "")),
                "rights_and_actions": a.get(lang, a.get("en", "")),
                "free_legal_aid_applicable": law.get("free_legal_aid_applicable", True),
                "relevance_score": round(score, 3)
            })
        return formatted

    def decrypt_notice(self, text: str, lang: str = "en") -> Dict[str, Any]:
        """
        Analyzes court summons, police notices, or hospital bills,
        translates complex legalese into 4th-grade plain language,
        and identifies statutory rights.
        """
        clean_text = text.lower()

        # Notice Category 1: SDM Court Land / Boundary Inquiry (BNSS 168 / CrPC 145)
        if any(w in clean_text for w in ["145", "168", "sdm", "sub-divisional", "land dispute", "zamini vivad", "khesra", "khata", "boundary", "zameen"]):
            law = self.db.get_law_by_id("BNSS-SEC-168")
            return {
                "detected_type": "Executive Magistrate Land Inquiry Notice (BNSS Sec 168 / CrPC 145)",
                "panic_reduction": {
                    "en": "DO NOT PANIC: This is NOT an arrest warrant or eviction order.",
                    "hi": "घबराएं नहीं: यह कोई गिरफ्तारी वारंट या बेदखली का आदेश नहीं है।",
                    "bn": "আতঙ্কিত হবেন না: এটি কোনো গ্রেপ্তারি পরোয়ানা বা উচ্ছেদের আদেশ নয়।",
                    "mr": "घाबरू नका: हा अटकेचा वॉरंट किंवा घर खाली करण्याचा आदेश नाही.",
                    "ta": "பயப்பட வேண்டாம்: இது கைது வாரண்ட் அல்லது வெளியேற்ற உத்தரவு அல்ல."
                }.get(lang, "DO NOT PANIC: This is NOT an arrest warrant."),
                "plain_meaning": law.get("plain_language", {}).get(lang, law.get("plain_language", {}).get("en")),
                "action_steps": law.get("rights_and_actions", {}).get(lang, law.get("rights_and_actions", {}).get("en")),
                "relevant_statute": "Section 168 BNSS / Section 12 Legal Services Authorities Act",
                "free_lawyer_available": True
            }

        # Notice Category 2: Hospital PM-JAY Ayushman Denial
        elif any(w in clean_text for w in ["ayushman", "pmjay", "hospital", "deposit", "45000", "billing", "surgery", "admit"]):
            law = self.db.get_law_by_id("PMJAY-ACT-2018")
            return {
                "detected_type": "Hospital Cashless Healthcare Violation (PM-JAY)",
                "panic_reduction": {
                    "en": "WARNING: Demanding cash deposits for covered treatment is illegal under PM-JAY regulations.",
                    "hi": "सावधान: आयुष्मान भारत के तहत अस्पताल का अग्रिम नकदी मांगना कानूनन अवैध है।",
                    "bn": "সতর্কবার্তা: আয়ুষ্মান প্রকল্পের অধীনে টাকা দাবি করা সম্পূর্ণ বেআইনি।",
                    "mr": "सावधान: आयुष्मान योजनेअंतर्गत पैसे मागणे कायद्याने बेकायदेशीर आहे.",
                    "ta": "எச்சரிக்கை: ஆயுஷ்மான் திட்டத்தின் கீழ் முன்கூட்டியே பணம் கேட்பது சட்டவிரோதமானது."
                }.get(lang, "WARNING: Cash deposits are illegal under PM-JAY."),
                "plain_meaning": law.get("plain_language", {}).get(lang, law.get("plain_language", {}).get("en")),
                "action_steps": law.get("rights_and_actions", {}).get(lang, law.get("rights_and_actions", {}).get("en")),
                "relevant_statute": "Ayushman Bharat PM-JAY Rules & Clinical Establishments Act",
                "free_lawyer_available": True
            }

        # Notice Category 3: Cheating / Financial Fraud
        elif any(w in clean_text for w in ["420", "318", "cheating", "fraud", "dhoka", "scam", "forgery"]):
            law = self.db.get_law_by_id("BNS-SEC-318")
            return {
                "detected_type": "Criminal Cheating & Property Deceit (BNS Sec 318 / IPC 420)",
                "panic_reduction": {
                    "en": "Action Needed: Fraud is a non-bailable crime punishable by up to 7 years imprisonment.",
                    "hi": "कार्यवाही आवश्यक: धोखाधड़ी 7 साल की जेल वाला गंभीर गैर-जमानती अपराध है।",
                    "bn": "পদক্ষেপ প্রয়োজন: প্রতারণা একটি ৭ বছর পর্যন্ত কারাদণ্ডযোগ্য অপরাধ।",
                    "mr": "तातडीने कृती करा: फसवणूक हा ७ वर्षांच्या शिक्षेस पात्र अजामीनपात्र गुन्हा आहे.",
                    "ta": "நடவடிக்கை தேவை: மோசடி என்பது 7 ஆண்டுகள் வரை சிறைத்தண்டனைக்குரிய குற்றமாகும்."
                }.get(lang, "Action Needed: Fraud is punishable by up to 7 years."),
                "plain_meaning": law.get("plain_language", {}).get(lang, law.get("plain_language", {}).get("en")),
                "action_steps": law.get("rights_and_actions", {}).get(lang, law.get("rights_and_actions", {}).get("en")),
                "relevant_statute": "BNS Section 318(4) / IT Act Section 66D",
                "free_lawyer_available": True
            }

        # Default Notice Parser
        else:
            return {
                "detected_type": "General Legal Document / Court Notice",
                "panic_reduction": {
                    "en": "Read carefully: You are entitled to free government counsel under Article 39A.",
                    "hi": "ध्यानपूर्वक पढ़ें: अनुच्छेद 39A के तहत आपको मुफ्त सरकारी वकील पाने का पूर्ण अधिकार है।",
                    "bn": "মনোযোগ সহকারে পড়ুন: আপনি সংবিধানের অনুচ্ছেদ 39A অনুযায়ী বিনামূল্যে উকিল পেতে পারেন।",
                    "mr": "काळजीपूर्वक वाचा: राज्यघटनेच्या कलम ३९A अन्वये तुम्हाला मोफत वकिलाचा अधिकार आहे.",
                    "ta": "கவனமாகப் படியுங்கள்: பிரிவு 39A-ன் கீழ் உங்களுக்கு இலவச அரசு வழக்கறிஞர் உரிமை உண்டு."
                }.get(lang, "You are entitled to free legal aid."),
                "plain_meaning": {
                    "en": "The notice requests your presence or information. Do not ignore it.",
                    "hi": "इस नोटिस में आपकी उपस्थिति या जानकारी मांगी गई है। इसे अनदेखा न करें।",
                    "bn": "এই নোটিশে আপনার উপস্থিতি চাওয়া হয়েছে। এটি অবহেলা করবেন না।",
                    "mr": "या नोटीसमध्ये तुमची उपस्थिती मागितली आहे. याकडे दुर्लक्ष करू नका.",
                    "ta": "இந்த நோட்டீஸ் உங்கள் வருகையைக் கோருகிறது. இதை புறக்கணிக்காதீர்கள்."
                }.get(lang, "The notice requests your presence."),
                "action_steps": {
                    "en": "Visit your District Legal Services Authority (DLSA) with your Aadhaar card and this notice.",
                    "hi": "आधार कार्ड और इस नोटिस को लेकर सीधे जिला विधिक सेवा प्राधिकरण (DLSA) जाएं।",
                    "bn": "আধার কার্ড ও নোটিশটি নিয়ে সরাসরি জেলা লিগ্যাল সার্ভিসেস অথরিটিতে (DLSA) যান।",
                    "mr": "आधार कार्ड आणि ही नोटीस घेऊन थेट DLSA कार्यालयात जा.",
                    "ta": "ஆதார் அட்டை மற்றும் இந்த நோட்டீசுடன் மாவட்ட சட்ட சேவைகள் ஆணையத்தை அணுகவும்."
                }.get(lang, "Visit your local DLSA."),
                "relevant_statute": "Article 39A, Constitution of India & Legal Services Authorities Act",
                "free_lawyer_available": True
            }

    def check_nalsa_eligibility(self, data: Dict[str, Any], lang: str = "en") -> Dict[str, Any]:
        """Wrapper for NALSA Section 12 criteria evaluation."""
        return NALSAScreener.evaluate(data, lang=lang)
