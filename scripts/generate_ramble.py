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
    prompt = f"""Mục tiêu: Viết một đoạn độc thoại nội tâm ngắn (khoảng 150-250 từ) thể hiện góc nhìn của một nhân vật với các đặc điểm đã mô tả, nhưng phải đảm bảo sự khác biệt hoàn toàn so với nội dung ngày hôm qua ({previous_ramble}). Tập trung vào việc tạo ra một mạch suy nghĩ, cách diễn đạt và tình huống mới lạ.

Năng lượng Cực Cao & Bất ổn: Vẫn là cốt lõi, nhưng biểu hiện theo cách khác (VD: không phải là sự phấn khích bề ngoài, mà là dòng suy nghĩ dồn dập, không ngừng nghỉ bên trong).
Lạc quan Phi lý Trí (Toxic Positivity Kiểu Hài Hước): Tìm một góc độ mới để thể hiện sự lạc quan này, có thể liên quan đến tình huống cụ thể trong độc thoại.
Tư duy Hỗn loạn & Nhảy cóc (Stream of Consciousness): Cấu trúc dòng suy nghĩ phải khác hôm qua. Thay vì liệt kê, có thể là những câu hỏi dồn dập, những liên tưởng xa vời, sự tự ngắt lời...
Ngôn ngữ "Vietglish" Sáng tạo: Dùng các từ/cụm từ Vietglish khác hoặc kết hợp chúng theo cách mới. Tránh lặp lại y hệt các ví dụ đã dùng nhiều lần.
Chốt hạ bằng một Lời Khuyên "Chân Lý" Ngớ Ngẩn: Vẫn giữ yêu cầu này, đặt gần cuối, chỉ MỘT lời khuyên duy nhất, nhưng nội dung lời khuyên phải khác và có vẻ "sâu sắc" một cách hài hước.
Giọng điệu & Phong cách: Hướng đến sự tự nhiên hơn trong sự hỗn loạn, có thể thêm chút tự giễu hoặc hoang mang nhẹ.
Yếu tố THEN CHỐT - Từ khóa Ngẫu nhiên: Từ khóa hôm nay là '{daily_seed_word}'. Hãy để nó xen vào một cách bất ngờ, nhưng có thể liên kết (dù chỉ là mong manh) với dòng suy nghĩ trước đó hoặc sau đó.
BỐI CẢNH QUAN TRỌNG - Nội dung ngày hôm qua:

Nội dung đã tạo ngày hôm qua là {previous_ramble}. Tuyệt đối không lặp lại câu mở đầu, các ý tưởng chính, cấu trúc câu hay cách dùng từ đặc trưng của đoạn văn này. Phải tạo ra một trải nghiệm đọc hoàn toàn khác biệt.
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