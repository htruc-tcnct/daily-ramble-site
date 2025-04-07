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
Nhiệm vụ: Hãy hóa thân và viết một đoạn độc thoại nội tâm ngắn (khoảng 150-250 từ) của một nhân vật mà tâm trí họ giống như một trình duyệt web mở 50 tab cùng lúc, nhạc nhảy bật volume max, và vừa uống liền 3 ly cà phê đậm. Đoạn độc thoại này cần phản ánh sự ảnh hưởng tinh tế từ từ khóa của ngày hôm đó.

Yêu cầu về "Chất liệu" bên trong:

Nhịp điệu Nền Tảng: Vẫn là suy nghĩ dồn dập, không đi theo đường thẳng, nhảy ý liên tục, câu chữ như đang "nhảy múa". Đây là cốt lõi không đổi.
"Filter" Lạc Quan (Kiểu Hài): Vẫn giữ lăng kính tích cực hơi lố, biến mọi thứ thành "tín hiệu vũ trụ" hoặc cơ hội "level up" một cách hài hước.
Ngôn ngữ "Hybrid" Tự Nhiên: Tiếp tục sử dụng Vietglish đời thường, sáng tạo ("OMG", "seriously?", "chốt đơn", "on top", "deadline dí", "so deep", "flex", "vibe"...).
Ảnh Hưởng Tinh Tế Từ Từ Khóa ({daily_seed_word}): Đây là điểm mới quan trọng:
Cảm nhận 'Năng Lượng' Từ Khóa: Hãy xem xét ý nghĩa, sắc thái, hoặc cảm giác mà {daily_seed_word} gợi ra.
Điều Chỉnh Phong Cách Nhẹ Nhàng: Để 'năng lượng' này thoáng ảnh hưởng đến giọng điệu hoặc dòng suy nghĩ. Ví dụ:
Nếu từ khóa là "yên bình", có thể có một khoảnh khắc suy tư ngắn, một câu hỏi về sự tĩnh lặng xen giữa mớ hỗn độn (nhưng rồi nhanh chóng bị dòng khác cuốn đi).
Nếu từ khóa là "bùng nổ", nhịp điệu có thể càng nhanh, nhiều dấu chấm than hơn.
Nếu từ khóa là "ẩm thực", liên tưởng về mùi vị, hình ảnh món ăn có thể xuất hiện rõ nét hơn.
Quan Trọng: Sự điều chỉnh này phải tinh tế, không làm mất đi bản chất năng lượng cao, hỗn loạn và lạc quan cốt lõi của nhân vật. Nó giống như thêm một chút "gia vị" khác nhau mỗi ngày.
Tích Hợp Từ Khóa: Từ khóa {daily_seed_word} phải xuất hiện trong đoạn văn. Nó có thể là điểm bắt đầu cho sự ảnh hưởng tinh tế nói trên, hoặc đơn giản là một yếu tố xen ngang bất ngờ.
Khoảnh khắc "Eureka!" Ngớ Ngẩn: Vẫn kết thúc bằng MỘT câu "chân lý" hoặc lời khuyên độc đáo, nghe sâu sắc nhưng thực chất lại vô tri hoặc hài hước (gần cuối đoạn, 1-2 câu).
Thách Thức Sáng Tạo:

Quên Hẳn Hôm Qua: Tuyệt đối tránh lặp lại nội dung ({previous_ramble}) và phong cách của ngày hôm trước. Mỗi ngày là một bản phối mới dựa trên cùng một nền nhạc.
Bối Cảnh Gợi Ý (Không bắt buộc): Vẫn có thể đặt nhân vật trong một bối cảnh đời thường để làm nổi bật sự tương phản với dòng suy nghĩ "bùng nổ" bên trong.


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