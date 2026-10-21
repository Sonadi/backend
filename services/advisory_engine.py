
import os

from dotenv import load_dotenv
from groq import Groq

from services.knowledge_base import collection


load_dotenv()

SUPPORTED_LANGUAGES = {"en", "si", "ta"}

LANGUAGE_NAMES = {
    "en": "English",
    "si": "Sinhala",
    "ta": "Tamil",
}

# Fixed, reviewed translations for farmer-facing messages.
TEXT = {
    "en": {
        "report_title": "CINNAMON WHITE ROOT ROT - ADVISORY REPORT",
        "risk_assessment": "RISK ASSESSMENT",
        "advisory": "ADVISORY",
        "input_conditions": "SENSOR CONDITIONS",
        "soil_ph": "Soil pH",
        "soil_moisture": "Soil moisture",
        "temperature": "Temperature",
        "confidence": "Model confidence",
        "ph_optimal": "Optimal",
        "ph_suboptimal": "Outside preferred range",
        "critical": "Critical",
        "high": "High",
        "medium": "Medium",
        "low": "Low",
        "knowledge": "KNOWLEDGE BASE INSIGHTS",
        "fallback": "AI advice is unavailable. Showing rule-based guidance.",
        "low_message": "The model indicates low risk. Continue routine monitoring and maintain good field drainage.",
        "medium_message": "The model indicates medium risk. Inspect plants regularly and address drainage or other abnormal conditions.",
        "high_message": "The model indicates high risk. Inspect affected plants promptly and consult an agricultural officer.",
        "actions_title": "Immediate Actions",
        "preventive_title": "Preventive Measures",
        "monitoring_title": "Monitoring Plan",
        "disclaimer_title": "Important notice",
        "disclaimer": "This is a decision-support estimate, not a confirmed diagnosis. Consult an agricultural officer before applying treatments.",
        "high_actions": [
            "Inspect plants and root zones for possible disease symptoms.",
            "Check field drainage and correct waterlogging where present.",
            "Avoid unnecessary irrigation when the soil is already excessively wet.",
            "Consult an agricultural officer if disease symptoms are observed.",
        ],
        "medium_actions": [
            "Inspect plants for yellowing, wilting, or other unusual symptoms.",
            "Check soil moisture and field drainage.",
            "Record sensor readings and observe changes over time.",
            "Consult an agricultural officer if symptoms appear or worsen.",
        ],
        "low_actions": [
            "Continue routine monitoring of plants and sensor readings.",
            "Maintain good field drainage.",
            "Check plants periodically for unusual symptoms.",
        ],
        "preventive": [
            "Use healthy planting material from a reliable source.",
            "Maintain appropriate field drainage.",
            "Monitor soil pH, moisture, and temperature regularly.",
            "Remove and handle suspected infected plant material according to agricultural guidance.",
            "Seek advice from an agricultural officer when disease is suspected.",
        ],
        "monitor_high": "Inspect plants frequently. Review sensor readings and drainage after rainfall. Seek agricultural advice promptly if symptoms are present.",
        "monitor_medium": "Inspect plants at least weekly and review sensor readings. Increase inspection frequency if conditions worsen.",
        "monitor_low": "Inspect plants monthly and keep records of sensor readings and plant health.",
        "unknown": "The risk category could not be identified. Consult an agricultural officer.",
    },

    "si": {
        "report_title": "කුරුඳු සුදු මුල් කුණුවීමේ රෝගය - උපදේශන වාර්තාව",
        "risk_assessment": "රෝග අවදානම් තක්සේරුව",
        "advisory": "උපදෙස්",
        "input_conditions": "සංවේදක දත්ත",
        "soil_ph": "පාංශු pH අගය",
        "soil_moisture": "පාංශු තෙතමනය",
        "temperature": "උෂ්ණත්වය",
        "confidence": "ආකෘතියේ විශ්වාස මට්ටම",
        "ph_optimal": "සුදුසු පරාසය",
        "ph_suboptimal": "සුදුසු පරාසයෙන් පිටත",
        "critical": "අතිශය අවදානම්",
        "high": "ඉහළ",
        "medium": "මධ්‍යම",
        "low": "අඩු",
        "knowledge": "දැනුම් පදනමේ තොරතුරු",
        "fallback": "AI උපදෙස් ලබාගත නොහැක. නීති මත පදනම් වූ උපදෙස් පෙන්වයි.",
        "low_message": "ආකෘතිය අනුව රෝග අවදානම අඩුය. සාමාන්‍ය නිරීක්ෂණය දිගටම කරගෙන යමින් වගා බිමේ හොඳ ජලවහනයක් පවත්වා ගන්න.",
        "medium_message": "ආකෘතිය අනුව රෝග අවදානම මධ්‍යම මට්ටමක පවතී. පැළ නිතිපතා පරීක්ෂා කර ජලවහනය සහ අසාමාන්‍ය තත්ත්ව පිළිබඳ අවධානය යොමු කරන්න.",
        "high_message": "ආකෘතිය අනුව රෝග අවදානම ඉහළය. පැළ සහ මුල් ප්‍රදේශ ඉක්මනින් පරීක්ෂා කර කෘෂිකර්ම නිලධාරියෙකුගෙන් උපදෙස් ලබා ගන්න.",
        "actions_title": "වහාම ගත යුතු ක්‍රියාමාර්ග",
        "preventive_title": "රෝග වැළැක්වීමේ ක්‍රියාමාර්ග",
        "monitoring_title": "නිරීක්ෂණ සැලැස්ම",
        "disclaimer_title": "වැදගත් දැනුම්දීම",
        "disclaimer": "මෙය තීරණ ගැනීමට සහාය වන අවදානම් ඇස්තමේන්තුවක් මිස තහවුරු කළ රෝග නිර්ණයක් නොවේ. ප්‍රතිකාර යෙදීමට පෙර කෘෂිකර්ම නිලධාරියෙකුගෙන් උපදෙස් ලබා ගන්න.",
        "high_actions": [
            "රෝග ලක්ෂණ තිබේදැයි පැළ සහ මුල් ප්‍රදේශ පරීක්ෂා කරන්න.",
            "වගා බිමේ ජලවහනය පරීක්ෂා කර ජලය රැඳී තිබේ නම් එය නිවැරදි කරන්න.",
            "පස අධික ලෙස තෙත් නම් අනවශ්‍ය ජල සැපයීමෙන් වළකින්න.",
            "රෝග ලක්ෂණ දක්නට ලැබේ නම් කෘෂිකර්ම නිලධාරියෙකුගෙන් උපදෙස් ලබා ගන්න.",
        ],
        "medium_actions": [
            "කොළ කහ වීම, මැලවීම හෝ වෙනත් අසාමාන්‍ය ලක්ෂණ සඳහා පැළ පරීක්ෂා කරන්න.",
            "පාංශු තෙතමනය සහ වගා බිමේ ජලවහනය පරීක්ෂා කරන්න.",
            "සංවේදක අගයන් සටහන් කර කාලයත් සමඟ සිදුවන වෙනස්කම් නිරීක්ෂණය කරන්න.",
            "රෝග ලක්ෂණ ඇති වුවහොත් හෝ වැඩි වුවහොත් කෘෂිකර්ම නිලධාරියෙකුගෙන් උපදෙස් ලබා ගන්න.",
        ],
        "low_actions": [
            "පැළ සහ සංවේදක දත්ත නිතිපතා නිරීක්ෂණය කරන්න.",
            "වගා බිමේ හොඳ ජලවහනයක් පවත්වා ගන්න.",
            "අසාමාන්‍ය ලක්ෂණ සඳහා පැළ වරින් වර පරීක්ෂා කරන්න.",
        ],
        "preventive": [
            "විශ්වාසදායක මූලාශ්‍රයකින් ලබාගත් නිරෝගී රෝපණ ද්‍රව්‍ය භාවිත කරන්න.",
            "වගා බිමේ සුදුසු ජලවහනයක් පවත්වා ගන්න.",
            "පාංශු pH අගය, තෙතමනය සහ උෂ්ණත්වය නිතිපතා නිරීක්ෂණය කරන්න.",
            "රෝගී බවට සැක කරන පැළ ද්‍රව්‍ය කෘෂිකර්ම උපදෙස් අනුව ඉවත් කර කළමනාකරණය කරන්න.",
            "රෝගයක් ඇති බවට සැකයක් ඇත්නම් කෘෂිකර්ම නිලධාරියෙකුගෙන් උපදෙස් ලබා ගන්න.",
        ],
        "monitor_high": "පැළ නිතර පරීක්ෂා කරන්න. වර්ෂාවෙන් පසු සංවේදක අගයන් සහ ජලවහනය පරීක්ෂා කරන්න. රෝග ලක්ෂණ ඇත්නම් ඉක්මනින් කෘෂිකර්ම උපදෙස් ලබා ගන්න.",
        "monitor_medium": "අවම වශයෙන් සතියකට වරක් පැළ පරීක්ෂා කර සංවේදක අගයන් සමාලෝචනය කරන්න. තත්ත්වය නරක අතට හැරේ නම් පරීක්ෂණ වාර ගණන වැඩි කරන්න.",
        "monitor_low": "මාසිකව පැළ පරීක්ෂා කර සංවේදක අගයන් සහ පැළවල සෞඛ්‍ය තත්ත්වය සටහන් කරන්න.",
        "unknown": "අවදානම් මට්ටම හඳුනාගත නොහැකි විය. කෘෂිකර්ම නිලධාරියෙකුගෙන් උපදෙස් ලබා ගන්න.",
    },

    "ta": {
        "report_title": "இலவங்கப்பட்டை வெள்ளை வேர் அழுகல் - ஆலோசனை அறிக்கை",
        "risk_assessment": "நோய் அபாய மதிப்பீடு",
        "advisory": "ஆலோசனை",
        "input_conditions": "சென்சார் தரவுகள்",
        "soil_ph": "மண்ணின் pH அளவு",
        "soil_moisture": "மண்ணின் ஈரப்பதம்",
        "temperature": "வெப்பநிலை",
        "confidence": "மாதிரியின் நம்பிக்கை அளவு",
        "ph_optimal": "உகந்த வரம்பு",
        "ph_suboptimal": "உகந்த வரம்பிற்கு வெளியே",
        "critical": "மிகவும் அபாயகரமான",
        "high": "அதிகம்",
        "medium": "நடுத்தரம்",
        "low": "குறைவு",
        "knowledge": "அறிவுத் தளத் தகவல்கள்",
        "fallback": "AI ஆலோசனையைப் பெற முடியவில்லை. விதி அடிப்படையிலான வழிகாட்டுதல் காட்டப்படுகிறது.",
        "low_message": "மாதிரியின் கணிப்பின்படி நோய் அபாயம் குறைவாக உள்ளது. வழக்கமான கண்காணிப்பைத் தொடரவும்; வயலில் நல்ல நீர்வடிகாலைப் பராமரிக்கவும்.",
        "medium_message": "மாதிரியின் கணிப்பின்படி நோய் அபாயம் நடுத்தரமாக உள்ளது. செடிகளைத் தொடர்ந்து பரிசோதித்து நீர்வடிகால் மற்றும் அசாதாரண நிலைகளைக் கவனிக்கவும்.",
        "high_message": "மாதிரியின் கணிப்பின்படி நோய் அபாயம் அதிகமாக உள்ளது. செடிகளையும் வேர் பகுதிகளையும் விரைவாகப் பரிசோதித்து விவசாய அதிகாரியிடம் ஆலோசனை பெறவும்.",
        "actions_title": "உடனடி நடவடிக்கைகள்",
        "preventive_title": "தடுப்பு நடவடிக்கைகள்",
        "monitoring_title": "கண்காணிப்புத் திட்டம்",
        "disclaimer_title": "முக்கிய அறிவிப்பு",
        "disclaimer": "இது முடிவெடுப்பதற்கான அபாய மதிப்பீடு மட்டுமே; உறுதிப்படுத்தப்பட்ட நோய் கண்டறிதல் அல்ல. சிகிச்சைகளைப் பயன்படுத்துவதற்கு முன் விவசாய அதிகாரியிடம் ஆலோசனை பெறவும்.",
        "high_actions": [
            "நோய் அறிகுறிகள் உள்ளனவா என செடிகளையும் வேர் பகுதிகளையும் பரிசோதிக்கவும்.",
            "வயலின் நீர்வடிகாலைச் சரிபார்த்து நீர் தேங்கியிருந்தால் சரிசெய்யவும்.",
            "மண் ஏற்கனவே அதிக ஈரப்பதத்துடன் இருந்தால் தேவையற்ற நீர்ப்பாசனத்தைத் தவிர்க்கவும்.",
            "நோய் அறிகுறிகள் காணப்பட்டால் விவசாய அதிகாரியிடம் ஆலோசனை பெறவும்.",
        ],
        "medium_actions": [
            "இலைகள் மஞ்சளாதல், வாடுதல் அல்லது பிற அசாதாரண அறிகுறிகள் உள்ளனவா எனப் பரிசோதிக்கவும்.",
            "மண்ணின் ஈரப்பதத்தையும் வயலின் நீர்வடிகாலையும் சரிபார்க்கவும்.",
            "சென்சார் அளவுகளைப் பதிவு செய்து காலப்போக்கில் ஏற்படும் மாற்றங்களைக் கவனிக்கவும்.",
            "அறிகுறிகள் தோன்றினாலோ மோசமடைந்தாலோ விவசாய அதிகாரியிடம் ஆலோசனை பெறவும்.",
        ],
        "low_actions": [
            "செடிகளையும் சென்சார் அளவுகளையும் வழக்கமாகக் கண்காணிக்கவும்.",
            "வயலில் நல்ல நீர்வடிகாலைப் பராமரிக்கவும்.",
            "அசாதாரண அறிகுறிகள் உள்ளனவா என செடிகளை அவ்வப்போது பரிசோதிக்கவும்.",
        ],
        "preventive": [
            "நம்பகமான மூலத்திலிருந்து பெறப்பட்ட ஆரோக்கியமான நடவுப் பொருட்களைப் பயன்படுத்தவும்.",
            "வயலில் பொருத்தமான நீர்வடிகாலைப் பராமரிக்கவும்.",
            "மண்ணின் pH, ஈரப்பதம் மற்றும் வெப்பநிலையைத் தொடர்ந்து கண்காணிக்கவும்.",
            "நோய் தொற்றியிருக்கலாம் எனச் சந்தேகிக்கப்படும் தாவரப் பொருட்களை விவசாய வழிகாட்டுதலின்படி அகற்றவும்.",
            "நோய் இருப்பதாகச் சந்தேகித்தால் விவசாய அதிகாரியிடம் ஆலோசனை பெறவும்.",
        ],
        "monitor_high": "செடிகளை அடிக்கடி பரிசோதிக்கவும். மழைக்குப் பிறகு சென்சார் அளவுகளையும் நீர்வடிகாலையும் சரிபார்க்கவும். அறிகுறிகள் இருந்தால் விரைவாக விவசாய ஆலோசனை பெறவும்.",
        "monitor_medium": "வாரத்திற்கு குறைந்தது ஒருமுறை செடிகளைப் பரிசோதித்து சென்சார் அளவுகளை மதிப்பாய்வு செய்யவும். நிலைமை மோசமடைந்தால் பரிசோதனைகளை அதிகரிக்கவும்.",
        "monitor_low": "மாதந்தோறும் செடிகளைப் பரிசோதித்து சென்சார் அளவுகளையும் தாவர ஆரோக்கியத்தையும் பதிவு செய்யவும்.",
        "unknown": "அபாய நிலையை அடையாளம் காண முடியவில்லை. விவசாய அதிகாரியிடம் ஆலோசனை பெறவும்.",
    },
}


def _language(code: str) -> str:
    return code if code in SUPPORTED_LANGUAGES else "en"


def _text(language: str, key: str) -> str:
    return TEXT[_language(language)][key]


def _build_rag_query(ph, moisture, temp, risk):
    terms = []

    if ph < 4.5 or ph > 7.0:
        terms.append("critical soil pH stress root rot")
    elif ph < 5.5:
        terms.append("acidic soil pH fungal growth")
    elif ph <= 6.5:
        terms.append("optimal pH cinnamon cultivation recommendations")
    else:
        terms.append("slightly alkaline soil pH")

    if moisture > 60:
        terms.append("high soil moisture waterlogging drainage")
    elif moisture >= 45:
        terms.append("high soil moisture fungal pathogen growth")
    elif moisture >= 30:
        terms.append("soil moisture medium risk early warning")
    else:
        terms.append("low soil moisture dry conditions")

    if temp > 30:
        terms.append("high temperature heat stress")
    elif temp >= 25:
        terms.append("warm humid temperature fungal growth")
    elif temp >= 23:
        terms.append("moderate temperature disease monitoring")
    else:
        terms.append("cool temperature conditions")

    return (
        f"{risk} cinnamon white root rot prevention management "
        + " ".join(terms)
    )


def _get_immediate_actions(risk, ph, moisture, temp, language):
    key = _language(language)

    if risk == "high":
        actions = list(TEXT[key]["high_actions"])
    elif risk == "medium":
        actions = list(TEXT[key]["medium_actions"])
    else:
        actions = list(TEXT[key]["low_actions"])

    # Add translated condition-specific guidance.
    if moisture > 60:
        extra = {
            "en": "Soil moisture is very high. Check drainage and avoid unnecessary irrigation.",
            "si": "පාංශු තෙතමනය ඉතා ඉහළය. ජලවහනය පරීක්ෂා කර අනවශ්‍ය ජල සැපයීමෙන් වළකින්න.",
            "ta": "மண்ணின் ஈரப்பதம் மிகவும் அதிகமாக உள்ளது. நீர்வடிகாலைச் சரிபார்த்து தேவையற்ற நீர்ப்பாசனத்தைத் தவிர்க்கவும்.",
        }
        actions.insert(0, extra[key])

    if ph < 5.5:
        extra = {
            "en": "Soil pH is below 5.5. Ask an agricultural officer about suitable soil amendments.",
            "si": "පාංශු pH අගය 5.5 ට අඩුය. සුදුසු පාංශු සංශෝධක පිළිබඳ කෘෂිකර්ම නිලධාරියෙකුගෙන් උපදෙස් ලබා ගන්න.",
            "ta": "மண்ணின் pH அளவு 5.5-க்கு குறைவாக உள்ளது. பொருத்தமான மண் திருத்தப் பொருட்கள் குறித்து விவசாய அதிகாரியிடம் ஆலோசனை பெறவும்.",
        }
        actions.append(extra[key])

    if temp > 30:
        extra = {
            "en": "Temperature is high. Observe plants for heat stress and maintain suitable soil cover.",
            "si": "උෂ්ණත්වය ඉහළය. උෂ්ණත්ව ආතතියේ ලක්ෂණ නිරීක්ෂණය කර සුදුසු පාංශු ආවරණයක් පවත්වා ගන්න.",
            "ta": "வெப்பநிலை அதிகமாக உள்ளது. வெப்ப அழுத்த அறிகுறிகளைக் கவனித்து பொருத்தமான மண் மூடாக்கைப் பராமரிக்கவும்.",
        }
        actions.append(extra[key])

    return actions


def _get_monitoring_plan(risk, language):
    key = _language(language)

    if risk == "high":
        return _text(key, "monitor_high")
    if risk == "medium":
        return _text(key, "monitor_medium")
    return _text(key, "monitor_low")


def _get_disclaimer(confidence, language):
    key = _language(language)
    message = _text(key, "disclaimer")

    if confidence < 0.6:
        warnings = {
            "en": " Model confidence is low; verify the result with an agricultural officer.",
            "si": " ආකෘතියේ විශ්වාස මට්ටම අඩුය; ප්‍රතිඵලය කෘෂිකර්ම නිලධාරියෙකු සමඟ තහවුරු කර ගන්න.",
            "ta": " மாதிரியின் நம்பிக்கை அளவு குறைவாக உள்ளது; முடிவை விவசாய அதிகாரியுடன் உறுதிப்படுத்தவும்.",
        }
        message += warnings[key]

    return message


def _generate_rule_based_report(
    ph, moisture, temp, risk, confidence, retrieved_passages, language
):
    key = _language(language)
    risk_key = risk if risk in ("low", "medium", "high") else "unknown"

    message_key = {
        "low": "low_message",
        "medium": "medium_message",
        "high": "high_message",
    }.get(risk_key)

    message = (
        _text(key, message_key)
        if message_key
        else _text(key, "unknown")
    )

    ph_label = (
        _text(key, "ph_optimal")
        if 5.5 <= ph <= 6.5
        else _text(key, "ph_suboptimal")
    )

    if moisture > 60:
        moisture_label = _text(key, "critical")
    elif moisture >= 45:
        moisture_label = _text(key, "high")
    elif moisture >= 30:
        moisture_label = _text(key, "medium")
    else:
        moisture_label = _text(key, "low")

    if temp > 30:
        temperature_label = _text(key, "critical")
    elif temp >= 25:
        temperature_label = _text(key, "high")
    elif temp >= 23:
        temperature_label = _text(key, "medium")
    else:
        temperature_label = _text(key, "low")

    report = (
        f"{_text(key, 'report_title')}\n\n"
        f"{_text(key, 'risk_assessment')}: "
        f"{_text(key, risk_key) if risk_key in ('low', 'medium', 'high') else _text(key, 'unknown')}\n\n"
        f"{_text(key, 'advisory')}:\n{message}\n\n"
        f"{_text(key, 'input_conditions')}\n"
        f"{_text(key, 'soil_ph')}: {ph} ({ph_label})\n"
        f"{_text(key, 'soil_moisture')}: {moisture}% ({moisture_label})\n"
        f"{_text(key, 'temperature')}: {temp}°C ({temperature_label})\n"
        f"{_text(key, 'confidence')}: {confidence * 100:.1f}%\n"
    )

    # Keep retrieved passages in their original language for traceability.
    if retrieved_passages:
        report += f"\n{_text(key, 'knowledge')}\n"
        for index, document in enumerate(retrieved_passages, 1):
            report += f"\n[{index}] {document.strip()[:350]}\n"

    return report


def _generate_llm_report(
    ph, moisture, temp, risk, confidence, retrieved_passages, language
):
    key = _language(language)
    context = "\n\n".join(retrieved_passages or [])

    prompt = f"""
You are an agricultural advisory assistant specializing in
Ceylon cinnamon and White Root Rot disease.

Write the entire farmer-facing report in {LANGUAGE_NAMES[key]}.
Use natural, clear language suitable for Sri Lankan cinnamon farmers.

Sensor values:
- Soil pH: {ph}
- Soil moisture: {moisture}%
- Soil temperature: {temp} degrees Celsius
- Predicted risk: {risk}
- Model confidence: {confidence * 100:.1f}%

Retrieved agricultural knowledge:
{context}

Instructions:
1. Explain the predicted risk.
2. Give practical immediate actions supported by the context.
3. Give preventive recommendations supported by the context.
4. Explain what to monitor next.
5. Translate headings and explanations into {LANGUAGE_NAMES[key]}.
6. Keep sensor values and confidence numbers unchanged.
7. Do not invent treatments, dosages, or unsupported agricultural facts.
8. Make clear that a model prediction is not a confirmed diagnosis.
9. Do not claim that disease is confirmed solely from sensor readings.
10. Keep the report concise and understandable.
"""

    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is not configured")

    client = Groq(api_key=api_key)

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": (
                    "Follow the requested output language exactly. "
                    "Prioritize safe, evidence-based agricultural guidance."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
        max_tokens=700,
    )

    content = response.choices[0].message.content
    if not content or not content.strip():
        raise RuntimeError("Groq returned an empty advisory report")

    return content.strip()


def get_advisory(
    ph: float,
    moisture: float,
    temp: float,
    risk: str,
    confidence: float,
    language: str = "en",
):
    language = _language(language)
    risk = risk.strip().lower()

    query = _build_rag_query(ph, moisture, temp, risk)

    # Retrieval failures should not prevent a fallback advisory.
    try:
        results = collection.query(
            query_texts=[query],
            n_results=4,
            include=["documents", "metadatas", "distances"],
        )

        retrieved_passages = (
            (results.get("documents") or [[]])[0] or []
        )
        metadatas = (results.get("metadatas") or [[]])[0] or []

        sources = sorted({
            metadata.get("source", "Unknown source")
            for metadata in metadatas
            if isinstance(metadata, dict)
        })

    except Exception as exc:
        print(f"Knowledge retrieval failed: {exc}")
        retrieved_passages = []
        sources = []

    try:
        report = _generate_llm_report(
            ph,
            moisture,
            temp,
            risk,
            confidence,
            retrieved_passages,
            language,
        )
        ai_available = True

    except Exception as exc:
        print(f"Groq advisory generation failed: {exc}")
        report = (
            f"{_text(language, 'fallback')}\n\n"
            + _generate_rule_based_report(
                ph,
                moisture,
                temp,
                risk,
                confidence,
                retrieved_passages,
                language,
            )
        )
        ai_available = False

    key = _language(language)

    preventive_measures = list(TEXT[key]["preventive"])

    return {
        "language": language,
        "ai_available": ai_available,
        "input_conditions": {
            "soil_pH": ph,
            "soil_moisture_percent": moisture,
            "temperature_c": temp,
            "risk_level": risk,
            "model_confidence": round(confidence, 3),
        },
        "retrieved_passages": retrieved_passages,
        "sources": sources,
        "report": report,
        "immediate_actions": _get_immediate_actions(
            risk, ph, moisture, temp, language
        ),
        "preventive_measures": preventive_measures,
        "monitoring_plan": _get_monitoring_plan(risk, language),
        "disclaimer": _get_disclaimer(confidence, language),
    }
