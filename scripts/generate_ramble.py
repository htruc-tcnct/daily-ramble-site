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
    Nhiệm vụ: Viết một đoạn độc thoại ngắn từ góc nhìn của một nhân vật đang trải qua một ngày bình thường, nhưng mọi thứ trong đầu họ như một cơn bão. Họ đang bước qua những suy nghĩ lộn xộn, những mảnh ký ức không liên quan, và những hình ảnh thoáng qua. Mỗi suy nghĩ như một mảnh ghép ngẫu nhiên, thỉnh thoảng lại gặp phải những giây phút "ngừng lại" ngắn ngủi để thở, nhưng ngay lập tức bị cuốn đi bởi những suy nghĩ khác. Đoạn độc thoại này phải có ảnh hưởng tinh tế từ từ khóa của ngày hôm nay {daily_seed_word}, và tuyệt đối tránh lặp lại từ khóa của hôm trước {previous_ramble}.

Yêu cầu về "Chất liệu" bên trong:

Nhịp điệu tự nhiên: Mặc dù suy nghĩ khá dồn dập, nhưng phải giữ được cảm giác nhẹ nhàng, không quá căng thẳng hay vội vàng. Hãy để cho các ý tưởng tự do "lang thang" trong đầu, như thể chúng xuất hiện rồi biến mất mà không bị ép buộc.

Lạc Quan nhẹ nhàng: Giữ sự tươi mới và tích cực, nhưng không phải quá lố, chỉ đơn giản là tìm thấy một chút niềm vui trong sự bình thường của cuộc sống. Không cần phải "phóng đại" mọi thứ, nhưng hãy để mọi suy nghĩ mang một chút ánh sáng vui vẻ.

Ngôn ngữ nhẹ nhàng, đời thường: Sử dụng những từ ngữ tự nhiên và gần gũi, như thể nhân vật đang trò chuyện với chính mình. Chú ý đừng sử dụng các từ ngữ quá phô trương hay khoa trương, chỉ cần phản ánh một tâm trạng sống động, đầy năng lượng trong một bối cảnh bình thường.

Từ khóa nhẹ nhàng, tinh tế: Chọn một từ khóa cho ngày hôm nay {daily_seed_word} và để từ khóa này xuất hiện một cách tự nhiên trong suy nghĩ của nhân vật. Từ khóa sẽ ảnh hưởng đến cách nhân vật nhìn nhận sự việc, nhưng đừng làm nó quá rõ rệt hoặc phô trương. Đảm bảo không lặp lại từ khóa của hôm trước {previous_ramble}.

Khoảnh khắc hài hước nhẹ: Cuối đoạn, tạo một khoảnh khắc nhỏ mà nhân vật nhận ra một sự thật giản đơn nhưng lại khiến họ mỉm cười vì sự ngớ ngẩn của chính mình.

Mục tiêu là tạo ra một dòng suy nghĩ thoải mái, dễ chịu, với một chút vui vẻ và sáng tạo, trong khi vẫn giữ cho câu chuyện chân thật và gần gũi, đồng thời tránh sự lặp lại từ khóa của ngày hôm trước.
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