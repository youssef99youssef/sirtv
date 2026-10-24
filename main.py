import requests
import urllib3

# إيقاف تحذيرات الـ SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://yassirtv.com/"
}

# قائمة المباريات مع المعرفات الأساسية وأسماء الفرق للتحقق من التطابق
matches_data = [
    {
        "team_left_ar": "الاتحاد", "team_left_en": "Al Ittihad",
        "team_right_ar": "الدرعية", "team_right_en": "Al Diriyah",
        "league_ar": "الدوري السعودي", "league_en": "Saudi League",
        "status": "'45", "score": "1 - 0",
        "base_id": "478944"
    },
    {
        "team_left_ar": "الأهلي", "team_left_en": "Al Ahli SC",
        "team_right_ar": "الخليج", "team_right_en": "Al Khaleej",
        "league_ar": "الدوري السعودي", "league_en": "Saudi League",
        "status": "لم تبدأ بعد", "score": "18:00",
        "base_id": "478945"
    },
    {
        "team_left_ar": "القادسية", "team_left_en": "Al Qadsiah",
        "team_right_ar": "الهلال", "team_right_en": "Al Hilal",
        "league_ar": "الدوري السعودي", "league_en": "Saudi League",
        "status": "لم تبدأ بعد", "score": "18:00",
        "base_id": "478946"
    },
    {
        "team_left_ar": "الرجاء الرياضي", "team_left_en": "Raja Casablanca",
        "team_right_ar": "إل كانيمي", "team_right_en": "El Kanemi",
        "league_ar": "كأس الكونفيدرالية", "league_en": "CAF Confederation Cup",
        "status": "لم تبدأ بعد", "score": "20:00",
        "base_id": "478947"
    },
    {
        "team_left_ar": "الزمالك", "team_left_en": "Zamalek",
        "team_right_ar": "أبر", "team_right_en": "APR",
        "league_ar": "دوري أبطال أفريقيا", "league_en": "CAF Champions League",
        "status": "لم تبدأ بعد", "score": "17:00",
        "base_id": "478948"
    },
    {
        "team_left_ar": "أهلي طرابلس", "team_left_en": "Al Ahly Tripoli",
        "team_right_ar": "ويلوالو", "team_right_en": "Welwalo Adigrat",
        "league_ar": "كأس الكونفيدرالية", "league_en": "CAF Confederation Cup",
        "status": "لم تبدأ بعد", "score": "17:00",
        "base_id": "478949"
    },
    {
        "team_left_ar": "بيراميدز", "team_left_en": "Pyramids",
        "team_right_ar": "المريخ بانتيو", "team_right_en": "EL Merriekh Bentiu",
        "league_ar": "دوري أبطال أفريقيا", "league_en": "CAF Champions League",
        "status": "لم تبدأ بعد", "score": "17:00",
        "base_id": "478950"
    },
    {
        "team_left_ar": "يعقوب المنصور", "team_left_en": "Yacoub El Mansour",
        "team_right_ar": "البطولة 2", "team_right_en": "Botola 2",
        "league_ar": "القسم الثاني", "league_en": "Botola 2",
        "status": "لم تبدأ بعد", "score": "17:00",
        "base_id": "478951"
    },
    {
        "team_left_ar": "اتحاد تواركة", "team_left_en": "Union Touarga",
        "team_right_ar": "البطولة الاحترافية", "team_right_en": "Botola Pro",
        "league_ar": "البطولة الاحترافية", "league_en": "Botola Pro",
        "status": "لم تبدأ بعد", "score": "18:00",
        "base_id": "478952"
    }
]

html_matches_cards = ""

print("جاري فحص النطاق (من 40 إلى 50) والتحقق من تطابق أسماء الفرق...")

for match in matches_data:
    discovered_link = None
    
    # فحص نطاق المعرفات لكل مباراة (من 40 إلى 50)
    for i in range(40, 51):
        match_id = f"{match['base_id']}{i}"
        target_url = f"https://yassirtv.com/hard/2908c7d4425d87350.html?match={match_id}"
        
        try:
            response = requests.get(target_url, headers=headers, verify=False, timeout=5)
            if response.status_code == 200:
                page_content = response.text
                
                # شرط التطابق: هل محتوى الصفحة يحتوي على اسم الفريق (عربي أو إنجليزي)؟
                if match['team_left_en'].lower() in page_content.lower() or match['team_left_ar'] in page_content:
                    print(id_msg := f"[✔] تطابق تام للمباراة ({match['team_left_ar']}) عبر المعرف: {match_id}")
                    discovered_link = target_url
                    break
                else:
                    print(f"[-] المعرف {match_id} متاح لكن أسماء الفرق غير مطابقة، جاري المرور للرابط التالي...")
            else:
                print(f"[x] المعرف {match_id} غير متاح")
        except Exception as e:
            print(f"[!] خطأ في الاتصال بالمعرف {match_id}: {e}")

    # تحديد شكل زر البث بناءً على نتيجة التحقق من التطابق
    if discovered_link:
        btn_html = f'<a href="{discovered_link}" target="_blank" class="watch-btn">مشاهدة البث</a>'
    else:
        btn_html = '<span class="watch-btn disabled-btn" title="البث غير متوفر حالياً">غير متوفر</span>'

    # بناء كود البطاقة ديناميكياً
    html_matches_cards += f"""
        <div class="match-card">
            <div class="team left" title="{match['team_left_ar']} / {match['team_left_en']}">
                {match['team_left_ar']} <br><span style="font-size: 11px; color: #7f8c8d; font-weight: normal;">{match['team_left_en']}</span>
            </div>
            <div class="match-info">
                <div class="match-status">{match['status']}</div>
                <div class="score-time">{match['score']}</div>
                <div class="league" title="{match['league_en']}">{match['league_ar']} / {match['league_en']}</div>
                {btn_html}
            </div>
            <div class="team right" title="{match['team_right_ar']} / {match['team_right_en']}">
                {match['team_right_ar']} <br><span style="font-size: 11px; color: #7f8c8d; font-weight: normal;">{match['team_right_en']}</span>
            </div>
        </div>
    """

# تجميع قالب الـ HTML النهائي
full_html = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>مباريات الفرق والبطولات الكبرى - بث مباشر</title>
    <style>
        body {{ font-family: Tahoma, sans-serif; background-color: #f8f9fa; color: #333; margin: 0; padding: 15px; direction: rtl; }}
        .container {{ max-width: 800px; margin: auto; }}
        h1 {{ text-align: center; color: #2c3e50; font-size: 22px; margin-bottom: 20px; }}
        .match-card {{ background: #fff; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); padding: 12px 15px; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center; border: 1px solid #e9ecef; }}
        .team {{ width: 30%; font-weight: bold; font-size: 15px; color: #2c3e50; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
        .team.left {{ text-align: right; }}
        .team.right {{ text-align: left; }}
        .match-info {{ width: 30%; text-align: center; }}
        .match-status {{ font-size: 13px; font-weight: bold; color: #c0392b; margin-bottom: 2px; }}
        .score-time {{ font-size: 18px; font-weight: bold; color: #2c3e50; margin-bottom: 2px; }}
        .league {{ font-size: 11px; color: #7f8c8d; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
        .watch-btn {{ display: inline-block; background-color: #2980b9; color: white; text-decoration: none; padding: 6px 12px; font-size: 12px; font-weight: bold; border-radius: 6px; cursor: pointer; margin-top: 6px; transition: background 0.2s; }}
        .watch-btn:hover {{ background-color: #2471a3; }}
        .disabled-btn {{ background-color: #95a5a6; cursor: not-allowed; pointer-events: none; }}
        .footer {{ text-align: center; margin-top: 25px; font-size: 12px; color: #95a5a6; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>مباريات الفرق والبطولات الكبرى (بث مباشر)</h1>
        {html_matches_cards}
    </div>
    <div class="footer">
        تم التحديث تلقائياً على مدار الساعة عبر الفحص الذكي لمحتوى الروابط
    </div>
</body>
</html>
"""

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(full_html)

print("تم فحص جميع المباريات والتحقق من تطابق الأسماء وتحديث ملف index.html بنجاح!")