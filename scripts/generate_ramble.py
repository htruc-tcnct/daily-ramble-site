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
Nhiệm vụ: Viết một đoạn độc thoại ngắn từ góc nhìn của một nhân vật đang trải qua một ngày bình thường, nhưng mọi thứ trong đầu họ như một cơn bão. Họ đang bước qua những suy nghĩ lộn xộn, những mảnh ký ức không liên quan, và những hình ảnh thoáng qua. Mỗi suy nghĩ như một mảnh ghép ngẫu nhiên, thỉnh thoảng lại có những khoảnh khắc tĩnh lặng ngắn ngủi, nhưng ngay lập tức những suy nghĩ khác lại ùa vào. Đoạn độc thoại này phải thể hiện sự ảnh hưởng tinh tế từ từ khóa của ngày hôm nay {daily_seed_word}, và tuyệt đối tránh lặp lại từ khóa của hôm trước {previous_ramble}.

Yêu cầu về "Chất liệu" bên trong:

Nhịp điệu tự nhiên: Suy nghĩ của nhân vật có thể rất dồn dập, nhưng vẫn cần duy trì sự nhẹ nhàng và không quá căng thẳng. Những ý tưởng như thể tự do lang thang trong đầu, không bị ép buộc hay theo một trật tự cụ thể.

Lạc Quan nhẹ nhàng: Dù suy nghĩ có thể hỗn loạn, nhưng vẫn phải mang một chút tươi mới và tích cực. Nhân vật không cần phải "phóng đại" mọi thứ, mà chỉ đơn giản tìm thấy niềm vui trong sự bình thường của cuộc sống.

Ngôn ngữ nhẹ nhàng, đời thường: Sử dụng ngôn ngữ tự nhiên, gần gũi như thể nhân vật đang trò chuyện với chính mình. Tránh sử dụng từ ngữ phô trương hay quá khoa trương, mà chỉ phản ánh sự sống động và năng lượng trong một bối cảnh giản dị.

Từ khóa nhẹ nhàng, tinh tế: Từ khóa của ngày hôm nay {daily_seed_word} sẽ được tích hợp một cách tự nhiên vào suy nghĩ của nhân vật. Đảm bảo rằng từ khóa này có sự ảnh hưởng nhẹ nhàng, không quá nổi bật hay phô trương. Đồng thời, tuyệt đối tránh lặp lại từ khóa của hôm trước {previous_ramble}.

Khoảnh khắc hài hước nhẹ: Kết thúc đoạn độc thoại bằng một khoảnh khắc hài hước nhẹ nhàng, nơi nhân vật nhận ra một sự thật giản đơn nhưng lại khiến họ mỉm cười vì sự ngớ ngẩn của chính mình.

Mục tiêu là tạo ra một dòng suy nghĩ thoải mái, dễ chịu, vui vẻ và sáng tạo, trong khi vẫn giữ cho câu chuyện chân thật và gần gũi. Cố gắng tránh sự lặp lại từ khóa của ngày hôm trước và mang lại một sự mới mẻ cho mỗi ngày.
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