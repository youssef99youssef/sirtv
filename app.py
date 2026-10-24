import json
import os
import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


def process_match(url):
  print("🚀 جاري بدء فحص المباراة واستخراج كافة البيانات...")

  # إعداد المتصفح الخفي للعمل بسلاسة على السيرفرات والأتمتة
  options = Options()
  options.add_argument("--headless")
  options.add_argument("--no-sandbox")
  options.add_argument("--disable-dev-shm-usage")

  driver = webdriver.Chrome(options=options)

  try:
    driver.get(url)
    time.sleep(7)  # انتظار تحميل محتوى الصفحة بالكامل

    page_title = driver.title
    print(f"✅ عنوان الصفحة: {page_title}")

    # 1. استخراج التوقيت باستخدام Regex
    match_time = "غير محدد"
    try:
      body_text = driver.find_element(By.TAG_NAME, "body").text
      time_match = re.search(r"\b(\d{1,2}:\d{2})\b", body_text)
      if time_match:
        match_time = time_match.group(1)
        print(f"⏰ التوقيت المكتشف: {match_time}")
    except Exception as e:
      print(f"⚠️ ملاحظة حول التوقيت: {e}")

    # 2. الاستخراج الديناميكي لرابط البث الفعلي (iframe) ومفتاح الحماية (API Key)
    player_url = ""
    api_key = "غير محدد"
    try:
      iframe_element = driver.find_element(By.TAG_NAME, "iframe")
      player_src = iframe_element.get_attribute("src")
      if player_src:
        player_url = player_src
        print(f"🔗 تم استخراج رابط البث ديناميكياً: {player_url}")

        # استخراج مفتاح الـ API من رابط الـ iframe
        key_match = re.search(r"key=([a-zA-Z0-9]+)", player_src)
        if key_match:
          api_key = key_match.group(1)
          print(f"🔑 تم استخراج مفتاح الـ API بنجاح: {api_key}")
    except Exception as e:
      print(f"⚠️ تعذر استخراج الـ iframe ديناميكياً، جاري استخدام الرابط الاحتياطي: {e}")

    # استخراج معرف المباراة الأساسي
    match_id_search = re.search(r"match=(\d+)", url)
    if not match_id_search:
      print("❌ تعذر استخراج match_id من الرابط الأساسي.")
      return
    match_id = match_id_search.group(1)

    # إذا فشل الاستخراج الديناميكي لسبب ما، نعتمد على الرابط الافتراضي
    if not player_url:
      player_url = f"https://912acsss8af382.sirtv.top/playerv5.php?match={match_id}&key=9f39972b67d6ce22189507d008acwc26"

    # 3. استخراج أسماء الفرق والنتيجة من العنوان
    clean_title = page_title.split("|")[0].strip()
    home_team = "الفريق الأول"
    away_team = "الفريق الثاني"
    new_score = "VS"

    match_score_pattern = re.match(r"(.+?)\s+(\d+\s*-\s*\d+)\s+(.+)", clean_title)
    if match_score_pattern:
      home_team = match_score_pattern.group(1).strip()
      new_score = match_score_pattern.group(2).strip()
      away_team = match_score_pattern.group(3).strip()
    else:
      if "vs" in clean_title.lower():
        teams = re.split(r"\s+vs\s+", clean_title, flags=re.IGNORECASE)
        if len(teams) == 2:
          home_team = teams[0].strip()
          away_team = teams[1].strip()

    # 4. قراءة قاعدة البيانات الحالية لمقارنة الأرقام ورصد الأهداف
    database = []
    old_score = None

    if os.path.exists("matches_db.txt"):
      try:
        with open("matches_db.txt", "r", encoding="utf-8") as f:
          database = json.load(f)
      except Exception:
        database = []

    existing_match = next(
        (m for m in database if m.get("match_id") == match_id), None
    )
    if existing_match:
      old_score = existing_match.get("score")

    # 5. رصد تغير الأرقام والنتيجة
    if old_score != new_score:
      print(
          f"⚽ تم رصد تغير في النتيجة/الأرقام! من ({old_score}) إلى"
          f" ({new_score})"
      )
    else:
      print(f"🔄 النتيجة ثابتة دون تغير: {new_score}")

    # تجهيز حزمة بيانات المباراة المحدثة
    match_data = {
        "url": url,
        "match_id": match_id,
        "player_url": player_url,
        "api_key": api_key,
        "home_team": home_team,
        "away_team": away_team,
        "score": new_score,
        "time": match_time,
        "title": page_title,
    }

    # تحديث أو إضافة المباراة داخل القائمة
    exists_idx = next(
        (i for i, m in enumerate(database) if m.get("match_id") == match_id),
        None,
    )
    if exists_idx is not None:
      database[exists_idx] = match_data
    else:
      database.append(match_data)

    # حفظ قاعدة البيانات المحدثة
    with open("matches_db.txt", "w", encoding="utf-8") as f:
      json.dump(database, f, ensure_ascii=False, indent=4)

    # إعادة بناء واجهة index.html
    update_web_dashboard(database)

  except Exception as e:
    print(f"❌ حدث خطأ أثناء المعالجة: {e}")
  finally:
    driver.quit()
    print("🔒 تم إغلاق المتصفح بنجاح.")


def update_web_dashboard(matches):
  matches_html = ""
  for match in matches:
    player_url = match.get("player_url")
    home = match.get("home_team", "")
    away = match.get("away_team", "")
    score = match.get("score", "VS")
    match_time = match.get("time", "غير محدد")
    teams_display = f"{home} 🆚 {away}" if away else home

    matches_html += f"""
        <div class="match-card" onclick="loadPlayer('{player_url}', '{teams_display}', '{score}')">
            <div class="teams">{teams_display}</div>
            <div class="time-box">⏰ توقيت المباراة: {match_time}</div>
            <div class="score-box">{score}</div>
            <span class="btn-watch">مشاهدة البث المباشر</span>
        </div>
        """

  html_content = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>منصة بث المباريات المباشرة</title>
    <style>
        body {{ background-color: #0a0e27; color: #fff; font-family: sans-serif; padding: 20px; }}
        .container {{ max-width: 1100px; margin: 0 auto; }}
        h1 {{ text-align: center; color: #ff80c0; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; }}
        .match-card {{ background: #1a1f3a; border: 1px solid #7877c6; border-radius: 16px; padding: 20px; text-align: center; cursor: pointer; transition: transform 0.2s; }}
        .match-card:hover {{ transform: translateY(-5px); }}
        .teams {{ font-size: 18px; font-weight: bold; margin-bottom: 8px; }}
        .time-box {{ font-size: 13px; color: #fbbf24; margin-bottom: 10px; }}
        .score-box {{ font-size: 18px; color: #38bdf8; font-weight: bold; background: rgba(56, 189, 248, 0.1); padding: 6px; border-radius: 8px; }}
        .btn-watch {{ display: block; background: #7877c6; color: #fff; padding: 8px; border-radius: 8px; margin-top: 10px; }}
        .player-wrapper {{ position: relative; width: 100%; padding-top: 56.25%; background: #000; display: none; margin-top: 20px; border-radius: 16px; overflow: hidden; }}
        iframe {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0; }}
        #active-title {{ text-align: center; margin-top: 20px; color: #22c55e; font-weight: bold; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>منصة بث المباريات المباشرة</h1>
        <div class="grid">{matches_html}</div>
        <div id="active-title"></div>
        <div class="player-wrapper" id="playerWrapper">
            <iframe id="mainPlayer" src="" allowfullscreen scrolling="no"></iframe>
        </div>
    </div>
    <script>
        function loadPlayer(url, title, score) {{
            document.getElementById('mainPlayer').src = url;
            document.getElementById('playerWrapper').style.display = 'block';
            document.getElementById('active-title').innerText = "جاري عرض: " + title + " (" + score + ")";
        }}
    </script>
</body>
</html>
"""
  with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)


if __name__ == "__main__":
  target_url = (
      "https://yassirtv.com/hard/2908c7d4425d87350.html?match=4789435"
  )
  process_match(target_url)