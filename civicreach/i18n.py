"""
Multilingual Localization Engine for CivicReach AI
Supports English (default) + Top Major Indian Languages: Hindi (हिन्दी), Bengali (বাংলা), Marathi (मराठी), and Tamil (தமிழ்).
"""

SUPPORTED_LANGUAGES = {
    "en": {"name": "English", "native": "English", "code": "en-IN"},
    "hi": {"name": "Hindi", "native": "हिन्दी", "code": "hi-IN"},
    "bn": {"name": "Bengali", "native": "বাংলা", "code": "bn-IN"},
    "mr": {"name": "Marathi", "native": "मराठी", "code": "mr-IN"},
    "ta": {"name": "Tamil", "native": "தமிழ்", "code": "ta-IN"}
}

MESSAGES = {
    "en": {
        "title": "CivicReach AI — Indian Public Services & Free Legal Aid Portal",
        "tagline": "NALSA & Tele-Law Partner | GIGW 3.0 & WCAG 2.2 AAA Accessible",
        "article_39a_banner": "<strong>Article 39A:</strong> 100% Free Government Legal Aid for women, children, SC/ST, and families with income under ₹1.5 Lakh.",
        "search_placeholder": "Search any law, crime, right, dispute (e.g., 'cheating', 'land dispute', 'domestic violence', 'bail')...",
        "search_btn": "Search Law",
        "tab_laws": "Legal Rights & Penal Codes",
        "tab_decrypt": "Kanoon Samjho (Notice Decryptor)",
        "tab_nalsa": "Free Legal Aid Screener (Sec 12)",
        "tab_telelaw": "Tele-Law / Lawyer Connect",
        "listen_btn": "Listen (Voice)",
        "high_contrast_btn": "High Contrast (7:1+)",
        "easy_read_btn": "Easy Read",
        "voice_active": "Voice Guidance Active",
        "sec12_eligible": "100% Guaranteed Free Legal Representation under Section 12, Legal Services Authorities Act, 1987.",
        "sec12_ineligible": "You can still access subsidized Tele-Law consultation at your village CSC for a nominal ₹30 fee.",
        "dlsa_helpline": "NALSA National Helpline: 15100 | Tele-Law: 14455"
    },
    "hi": {
        "title": "सिविक-रीच एआई — भारतीय नागरिक सहायता एवं मुफ्त कानूनी अधिकार पोर्टल",
        "tagline": "NALSA एवं टेली-लॉ भागीदार | GIGW 3.0 एवं WCAG 2.2 AAA सुगम्य",
        "article_39a_banner": "<strong>अनुच्छेद 39A:</strong> महिलाओं, बच्चों, SC/ST और ₹1.5 लाख से कम आय वाले परिवारों के लिए 100% मुफ्त सरकारी वकील।",
        "search_placeholder": "किसी भी कानून, अपराध या अधिकार की खोज करें (जैसे: 'धोखाधड़ी', 'जमीन विवाद', 'दहेज', 'जमानत')...",
        "search_btn": "कानून खोजें",
        "tab_laws": "कानूनी अधिकार व भारतीय संहिता",
        "tab_decrypt": "कानून समझो (नोटिस वाचक)",
        "tab_nalsa": "मुफ्त वकील पात्रता जांच (धारा 12)",
        "tab_telelaw": "टेली-लॉ / वकील संपर्क",
        "listen_btn": "बोलकर सुनें (Voice)",
        "high_contrast_btn": "हाई कंट्रास्ट (7:1+)",
        "easy_read_btn": "सरल पाठ (Easy Read)",
        "voice_active": "आवाज मार्गदर्शन सक्रिय है",
        "sec12_eligible": "बधाई! विधिक सेवा प्राधिकरण अधिनियम 1987 की धारा 12 के तहत आप 100% मुफ्त सरकारी वकील पाने के हकदार हैं।",
        "sec12_ineligible": "आप अपने नजदीकी सीएससी (CSC) केंद्र पर केवल ₹30 में टेली-लॉ विधिक सलाह प्राप्त कर सकते हैं।",
        "dlsa_helpline": "NALSA राष्ट्रीय हेल्पलाइन: 15100 | टेली-लॉ: 14455"
    },
    "bn": {
        "title": "সিভিকরিচ এআই — ভারতীয় নাগরিক অধিকার ও বিনামূল্যে আইনি সহায়তা পোর্টাল",
        "tagline": "NALSA ও টেলি-ল অংশীদার | GIGW 3.0 ও WCAG 2.2 AAA উপযোগী",
        "article_39a_banner": "<strong>ধারা 39A:</strong> মহিলা, শিশু, SC/ST এবং ₹1.5 লক্ষের কম আয়ের ব্যক্তিদের জন্য 100% বিনামূল্যে সরকারি আইনজীবী।",
        "search_placeholder": "যেকোনো আইন বা অপরাধ অনুসন্ধান করুন (যেমন: 'প্রতারণা', 'জমির বিরোধ', 'পারিবারিক নির্যাতন', 'জামিন')...",
        "search_btn": "আইন খুঁজুন",
        "tab_laws": "আইনি অধিকার ও দণ্ডবিধি",
        "tab_decrypt": "আইন সহজীকরণ (নোটিশ বিশ্লেষক)",
        "tab_nalsa": "বিনামূল্যে উকিল পাওয়ার যোগ্যতা (ধারা ১২)",
        "tab_telelaw": "টেলি-ল / আইনজীবীর সাথে যোগাযোগ",
        "listen_btn": "শুনে নিন (Voice)",
        "high_contrast_btn": "হাই কনট্রাস্ট (7:1+)",
        "easy_read_btn": "সহজ পাঠ (Easy Read)",
        "voice_active": "ভয়েস গাইডেন্স চালু আছে",
        "sec12_eligible": "অভিনন্দন! আইনি সেবা কর্তৃপক্ষ আইন ১৯৮৭ এর ধারা ১২ অনুসারে আপনি ১০০% বিনামূল্যে সরকারি আইনজীবী পাওয়ার যোগ্য।",
        "sec12_ineligible": "আপনি মাত্র ৩০ টাকায় নিকটস্থ সিএসসি কেন্দ্র থেকে টেলি-ল পরামর্শ নিতে পারেন।",
        "dlsa_helpline": "NALSA জাতীয় হেল্পলাইন: 15100 | টেলি-ল: 14455"
    },
    "mr": {
        "title": "सिविकरीच एआय — भारतीय नागरिक कल्याण व मोफत कायदेशीर मदत पोर्टल",
        "tagline": "NALSA व टेलि-लॉ भागीदार | GIGW 3.0 व WCAG 2.2 AAA सुलभ",
        "article_39a_banner": "<strong>अनुच्छेद 39A:</strong> महिला, बालके, SC/ST आणि ₹1.5 लाखांपेक्षा कमी उत्पन्न असणाऱ्यांसाठी 100% मोफत सरकारी वकील.",
        "search_placeholder": "कोणताही कायदा किंवा गुन्हा शोधा (उदा. 'फसवणूक', 'जमीन वाद', 'कौटुंबिक हिंसाचार', 'जामीन')...",
        "search_btn": "कायदा शोधा",
        "tab_laws": "कायदेशीर अधिकार व दंड संहिता",
        "tab_decrypt": "कायदा समजून घ्या (नोटीस वाचक)",
        "tab_nalsa": "मोफत वकील पात्रता चाचणी (कलम १२)",
        "tab_telelaw": "टेलि-लॉ / वकील संपर्क",
        "listen_btn": "ऐका (Voice)",
        "high_contrast_btn": "हाय कॉन्ट्रास्ट (7:1+)",
        "easy_read_btn": "सोपे वाचन (Easy Read)",
        "voice_active": "आवाज मार्गदर्शन सुरू आहे",
        "sec12_eligible": "अभिनंदन! विधी सेवा प्राधिकरण कायदा १९८७ च्या कलम १२ नुसार तुम्ही १००% मोफत सरकारी वकिलासाठी पात्र आहात.",
        "sec12_ineligible": "तुम्ही जवळच्या सीएससी केंद्रावर केवळ ३० रुपयांत टेलि-लॉ कायदेशीर सल्ला घेऊ शकता.",
        "dlsa_helpline": "NALSA राष्ट्रीय हेल्पलाइन: १५१०० | टेलि-लॉ: १४४५५"
    },
    "ta": {
        "title": "சிவிக்-ரீச் ஏஐ — இந்திய குடிமக்கள் நலன் மற்றும் இலவச சட்ட உதவி தளம்",
        "tagline": "NALSA & டெலி-லா கூட்டாளர் | GIGW 3.0 & WCAG 2.2 AAA அணுகல்தன்மை",
        "article_39a_banner": "<strong>சட்டப்பிரிவு 39A:</strong> பெண்கள், குழந்தைகள், SC/ST மற்றும் ₹1.5 லட்சத்திற்கும் குறைவான வருமானம் உள்ளவர்களுக்கு 100% இலவச அரசு வழக்கறிஞர்.",
        "search_placeholder": "சட்டம் அல்லது குற்றத்தைத் தேடுங்கள் (எ.கா. 'மோசடி', 'நிலத் தகராறு', 'குடும்ப வன்முறை', 'ஜாமீன்')...",
        "search_btn": "சட்டம் தேடு",
        "tab_laws": "சட்ட உரிமைகள் & தண்டனைச் சட்டம்",
        "tab_decrypt": "சட்டம் அறிவோம் (நோட்டீஸ் விளக்கம்)",
        "tab_nalsa": "இலவச வழக்கறிஞர் தகுதி (பிரிவு 12)",
        "tab_telelaw": "டெலி-லா / வழக்கறிஞர் இணைப்பு",
        "listen_btn": "கேட்க (Voice)",
        "high_contrast_btn": "அதிக மாறுபாடு (7:1+)",
        "easy_read_btn": "எளிய வாசிப்பு (Easy Read)",
        "voice_active": "குரல் வழிகாட்டுதல் செயலில் உள்ளது",
        "sec12_eligible": "வாழ்த்துகள்! சட்ட சேவைகள் அதிகார சட்டம் 1987 பிரிவு 12-ன் கீழ் நீங்கள் 100% இலவச அரசு வழக்கறிஞர் பெற தகுதியானவர்.",
        "sec12_ineligible": "அருகிலுள்ள CSC மையத்தில் வெறும் ₹30 கட்டணத்தில் டெலி-லா மூலம் சட்ட ஆலோசனை பெறலாம்.",
        "dlsa_helpline": "NALSA தேசிய உதவி எண்: 15100 | டெலி-லா: 14455"
    }
}

def get_text(key: str, lang: str = "en") -> str:
    """Retrieve localized message string with fallback to English."""
    lang_dict = MESSAGES.get(lang, MESSAGES["en"])
    return lang_dict.get(key, MESSAGES["en"].get(key, key))
