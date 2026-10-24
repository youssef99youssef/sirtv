import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def open_and_extract(url):
  print("🚀 جاري إعداد المتصفح الوهمي لفتح الصفحة الجديدة...")

  options = Options()
  # options.add_argument("--headless") # اتركها معلقة لترى المتصفح يفتح أمامك

  driver = webdriver.Chrome(options=options)

  try:
    print(f"🔗 جاري فتح الرابط: {url}")
    driver.get(url)

    print("⏳ جاري الانتظار لتحميل محتوى البث والعنوان...")
    time.sleep(7)

    page_title = driver.title
    print(f"✅ عنوان الصفحة الظاهر للمباراة الجديدة: {page_title}")

    # استخراج توقيت المباراة من نص الصفحة باستخدام Regex للبحث عن تنسيق الساعات (مثال: 21:00)
    match_time = "غير محدد"
    try:
      body_text = driver.find_element("tag name", "body").text
      time_match = re.search(r"\b(\d{1,2}:\d{2})\b", body_text)
      if time_match:
        match_time = time_match.group(1)
        print(f"⏰ تم العثور على التوقيت بنجاح: {match_time}")
      else:
        print("⚠️ لم يتم العثور على توقيت في نص الصفحة.")
    except Exception as ex:
      print(f"⚠️ خطأ أثناء استخراج الوقت: {ex}")

    driver.save_screenshot("match_new_screenshot.png")
    print("📸 تم حفظ صورة للشاشة باسم match_new_screenshot.png بنجاح!")

  except Exception as e:
    print(f"❌ حدث خطأ: {e}")
  finally:
    driver.quit()
    print("🔒 تم إغلاق المتصفح.")


if __name__ == "__main__":
  new_url = "https://yassirtv.com/hard/2908c7d4425d87350.html?match=4789435"
  open_and_extract(new_url)