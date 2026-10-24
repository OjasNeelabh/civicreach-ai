"""
NALSA Section 12 Free Legal Aid Eligibility Engine
Evaluates statutory criteria under Section 12 of the Legal Services Authorities Act, 1987 & Article 39A.
"""

from typing import Dict, Any

STATE_INCOME_LIMITS = {
    "default": 150000,
    "delhi": 300000,
    "maharashtra": 300000,
    "karnataka": 300000,
    "tamil_nadu": 300000,
    "west_bengal": 150000,
    "bihar": 150000,
    "uttar_pradesh": 150000
}

class NALSAScreener:
    @staticmethod
    def evaluate(data: Dict[str, Any], lang: str = "en") -> Dict[str, Any]:
        """
        Evaluates eligibility under Section 12 of the Legal Services Authorities Act, 1987.
        Criteria:
        a) Member of Scheduled Caste or Scheduled Tribe
        b) Victim of trafficking in human beings or begar
        c) A woman or a child
        d) A person with disability (RPwD Act 2016)
        e) A person under circumstances of underserved want (mass disaster, ethnic violence, flood, drought)
        f) An industrial workman
        g) In custody (including protective custody or undertrial)
        h) Annual income below prescribed threshold (default ₹1,50,000 / ₹3,00,000 in higher income states)
        """
        is_woman_or_child = bool(data.get("is_woman_or_child", False))
        is_sc_st = bool(data.get("is_sc_st", False))
        is_pwd = bool(data.get("is_pwd", False))
        is_custody = bool(data.get("is_custody", False))
        is_workman = bool(data.get("is_workman", False))
        
        income = float(data.get("annual_income", 0))
        state = str(data.get("state", "default")).lower().replace(" ", "_")
        income_ceiling = STATE_INCOME_LIMITS.get(state, STATE_INCOME_LIMITS["default"])
        
        income_eligible = income <= income_ceiling

        qualifying_clauses = []
        if is_woman_or_child:
            qualifying_clauses.append("Section 12(c): Woman or Child")
        if is_sc_st:
            qualifying_clauses.append("Section 12(a): Member of Scheduled Caste or Scheduled Tribe")
        if is_pwd:
            qualifying_clauses.append("Section 12(d): Person with Disability (RPwD Act)")
        if is_custody:
            qualifying_clauses.append("Section 12(g): Person in Custody / Undertrial")
        if is_workman:
            qualifying_clauses.append("Section 12(f): Industrial Workman")
        if income_eligible and not (is_woman_or_child or is_sc_st or is_pwd or is_custody or is_workman):
            qualifying_clauses.append(f"Section 12(h): Annual Income below State Limit (₹{income_ceiling:,})")

        eligible = len(qualifying_clauses) > 0 or income_eligible

        # Localized explanations
        messages = {
            "en": {
                "status": "Eligible for 100% Free Legal Aid" if eligible else "Standard Legal Aid / Nominal Tele-Law",
                "summary": "You are legally entitled to a government advocate and exemption from court fees under Article 39A of the Constitution of India and Section 12 of the Legal Services Authorities Act, 1987." if eligible else "You do not meet automatic fee waiver criteria, but you are entitled to Tele-Law consultation at your local CSC for ₹30.",
                "action": "Present this certificate to your District Legal Services Authority (DLSA) Front Office or visit your local village Common Services Center (CSC)."
            },
            "hi": {
                "status": "100% मुफ्त सरकारी कानूनी सहायता के पात्र" if eligible else "सुलभ टेली-लॉ विधिक सलाह",
                "summary": "आप भारत के संविधान के अनुच्छेद 39A एवं विधिक सेवा प्राधिकरण अधिनियम 1987 की धारा 12 के तहत निःशुल्क सरकारी वकील व कोर्ट फीस माफी के पूर्ण हकदार हैं।" if eligible else "आप मुफ्त वकील के स्वतः पात्र नहीं हैं, परंतु मात्र ₹30 में गांव के सीएससी केंद्र से टेली-लॉ परामर्श ले सकते हैं।",
                "action": "इस पात्रता पर्ची को जिला विधिक सेवा प्राधिकरण (DLSA) कोर्ट में दिखाएं या नजदीकी सीएससी केंद्र जाएं।"
            },
            "bn": {
                "status": "১০০% বিনামূল্যে সরকারি আইনি সহায়তার যোগ্য" if eligible else "সুলভ টেলি-ল আইনি পরামর্শ",
                "summary": "আপনি ভারতীয় সংবিধানের অনুচ্ছেদ 39A এবং আইনি সেবা কর্তৃপক্ষ আইন 1987 এর ধারা 12 অনুযায়ী বিনামূল্যে সরকারি উকিল পাওয়ার অধিকারী।" if eligible else "আপনি সিএসসি কেন্দ্র থেকে মাত্র ৩০ টাকায় আইনজীবীর পরামর্শ নিতে পারেন।",
                "action": "আপনার জেলা আদালতের ডিএলএসএ (DLSA) হেল্পডেস্কে যোগাযোগ করুন।"
            },
            "mr": {
                "status": "१००% मोफत सरकारी कायदेशीर मदतीसाठी पात्र" if eligible else "सुलभ टेलि-लॉ सल्ला",
                "summary": "तुम्ही भारतीय राज्यघटनेच्या कलम ३९A आणि विधी सेवा प्राधिकरण कायदा १९८७ च्या कलम १२ अन्वये मोफत सरकारी वकिलाचे हक्कदार आहात." if eligible else "तुम्ही स्थानिक सीएससी केंद्रावरून ३० रुपयांत टेलि-लॉ सल्ला घेऊ शकता.",
                "action": "जिल्हा विधी सेवा प्राधिकरण (DLSA) कार्यालयात जाऊन हा दाखला सादर करा."
            },
            "ta": {
                "status": "100% இலவச அரசு சட்ட உதவி பெற தகுதியானவர்" if eligible else "டெலி-லா சட்ட ஆலோசனை",
                "summary": "இந்திய அரசியலமைப்பு சட்டப்பிரிவு 39A மற்றும் சட்ட சேவைகள் அதிகார சட்டம் 1987 பிரிவு 12-ன் கீழ் நீங்கள் முற்றிலும் இலவச அரசு வழக்கறிஞர் பெற உரிமை உண்டு." if eligible else "நீங்கள் அருகிலுள்ள CSC மையத்தில் ₹30 கட்டணத்தில் டெலி-லா மூலம் சட்ட ஆலோசனை பெறலாம்.",
                "action": "மாவட்ட சட்ட சேவைகள் ஆணையத்தின் (DLSA) முன் மேசையை அணுகவும்."
            }
        }

        lang_data = messages.get(lang, messages["en"])

        return {
            "eligible": eligible,
            "certificate_id": f"CR-NALSA-2026-{abs(hash(str(data))) % 100000:05d}",
            "clauses": qualifying_clauses,
            "status": lang_data["status"],
            "summary": lang_data["summary"],
            "action": lang_data["action"],
            "helpline": "15100 (NALSA National Toll-Free)",
            "telelaw_portal": "tele-law.in"
        }
