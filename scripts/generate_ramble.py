import google.generativeai as genai
import os
import json
import random
from datetime import datetime
import sys

# --- Danh sách seed_words giữ nguyên ---
seed_words = [
    "mây", "cà phê", "tắc đường", "giấc mơ", "con mèo", "wifi", "cái ghế",
    "âm nhạc", "màu xanh", "vì sao", "cuốn sách", "ổ bánh mì", "cơn mưa",
    "đôi dép", "bóng đèn", "cái cây", "điện thoại", "cửa sổ", "kẹo mút",
    # ... (thêm các từ khác nếu có) ...
]

# --- Đường dẫn file JSON (Đảm bảo đúng với workflow) ---
# Ví dụ: Lưu ở thư mục gốc
# file_path = "daily_ramble.json"
# Ví dụ: Lưu trong thư mục _data
file_path = "data/daily_ramble.json"

# --- Đọc nội dung cũ (NẾU CÓ) ---
previous_ramble = "Không có nội dung cũ." # Giá trị mặc định
try:
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            old_data = json.load(f)
            if 'ramble' in old_data:
                previous_ramble = old_data['ramble']
                print(f"Loaded previous ramble (first 50 chars): {previous_ramble[:50]}...")
            else:
                print("Previous JSON found, but no 'ramble' key.")
    else:
        print(f"Previous data file not found at {file_path}. First run?")
except Exception as read_err:
    print(f"Warning: Could not read or parse previous data file: {read_err}", file=sys.stderr)
    # Không thoát chương trình, chỉ cảnh báo và tiếp tục với giá trị mặc định

# --- Bắt đầu phần chính ---
try:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("API key not found in environment variables.")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    daily_seed_word = random.choice(seed_words)

    # --- Xây dựng prompt HOÀN CHỈNH (bao gồm nội dung cũ) ---
    prompt = f"""
### Nhiệm vụ: Sáng tạo Độc thoại Nội tâm Hỗn loạn Đầy Năng lượng

**Mục tiêu:** Viết một đoạn độc thoại nội tâm ngắn (khoảng 150-250 từ) thể hiện góc nhìn của một nhân vật có các đặc điểm sau:

1.  **Năng lượng Cực Cao & Bất ổn:** ... (Giữ nguyên) ...
2.  **Lạc quan Phi lý Trí (Toxic Positivity Kiểu Hài Hước):** ... (Giữ nguyên) ...
3.  **Tư duy Hỗn loạn & Nhảy cóc (Stream of Consciousness):** ... (Giữ nguyên) ...
4.  **Ngôn ngữ "Vietglish" Sáng tạo:** ... (Giữ nguyên các ví dụ) ...
5.  **Chốt hạ bằng một Lời Khuyên "Chân Lý" Ngớ Ngẩn:** ***Gần cuối*** đoạn độc thoại (khoảng 1-2 câu cuối), hãy đưa ra ***MỘT*** lời khuyên ... (Như đã sửa ở trên) ...
6.  **Giọng điệu & Phong cách:** ... (Giữ nguyên các ví dụ) ...
7.  **Yếu tố THEN CHỐT - Từ khóa Ngẫu nhiên:** Hôm nay, hãy để từ khóa **'{daily_seed_word}'** xuất hiện một cách bất ngờ ... (Giữ nguyên) ...
8, Nếu có dùng gì thì hãy lấy xung quanh những công việc IT, ví dụ hôm nay tôi fixx bug hay là hôm nay tôi phải gặp sếp để báo cáo chẳng hạn,....
---
**BỐI CẢNH QUAN TRỌNG - Nội dung ngày hôm qua:**

*Đây là nội dung đã được tạo ngày hôm trước.không được lặp lại câu đầu tiên hay những từ đã được viết trong đoạn văn trước Vui lòng **TRÁNH LẶP LẠI** ý tưởng, cấu trúc câu hoặc các chi tiết cụ thể quá giống với đoạn này khi tạo nội dung cho hôm nay:*

"{previous_ramble}"
---

**LƯU Ý QUAN TRỌNG:**
* **KHÔNG** cần bắt đầu bằng ... (Giữ nguyên) ...
* Ví dụ về giọng điệu ... (Giữ nguyên) ...

**Hãy bắt đầu dòng suy nghĩ hỗn loạn nhưng đầy lạc quan MỚI MẺ cho hôm nay!**
"""

    # Gọi Gemini API
    print(f"Generating content with seed word: {daily_seed_word} and previous context.")
    response = model.generate_content(prompt)
    ramble_text = response.text.strip()
    print(f"Generated text: {ramble_text[:100]}...")

    # Chuẩn bị dữ liệu để lưu
    today_date = datetime.now().strftime("%Y-%m-%d")
    data = {"date": today_date, "seed_word": daily_seed_word, "ramble": ramble_text}

    # Ghi file JSON (tạo thư mục nếu chưa có)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Successfully updated {file_path}")

except Exception as e:
    print(f"An error occurred: {e}", file=sys.stderr)
    sys.exit(1)