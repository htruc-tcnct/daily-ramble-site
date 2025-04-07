import google.generativeai as genai
import os
import json
import random
from datetime import datetime
import sys # Thêm thư viện sys

# Danh sách từ khóa gợi ý ngẫu nhiên
# Danh sách từ khóa gợi ý ngẫu nhiên (Mở rộng)
seed_words = [
    "mây", "cà phê", "tắc đường", "giấc mơ", "con mèo", "wifi", "cái ghế",
    "âm nhạc", "màu xanh", "vì sao", "cuốn sách", "ổ bánh mì", "cơn mưa",
    "đôi dép", "bóng đèn", "cái cây", "điện thoại", "cửa sổ", "kẹo mút",

    # Đồ vật hàng ngày
    "cái kéo", "bát mì", "remote TV", "khẩu trang", "chìa khóa", "cục sạc",
    "đôi tất", "ly nước", "cái gương", "quyển vở", "cái thìa", "xe máy",

    # Thiên nhiên & Thời tiết
    "mặt trời", "mặt trăng", "ngọn gió", "bãi biển", "ngọn núi", "dòng sông",
    "hoa lá", "hạt giống", "bầu trời đêm", "sấm sét", "cầu vồng", "lá vàng",

    # Khái niệm & Cảm xúc
    "thời gian", "không gian", "tình yêu", "nỗi buồn", "hy vọng", "sự im lặng",
    "tiếng cười", "ký ức", "tương lai", "cơ hội", "thách thức", "bất ngờ",

    # Địa điểm & Hoạt động
    "công viên", "siêu thị", "chuyến xe buýt", "cuộc họp online", "lướt mạng",
    "giấc ngủ trưa", "đi bộ", "nấu ăn", "xem phim", "trò chuyện", "ngôi nhà",

    # Linh tinh & Ngẫu nhiên
    "bong bóng", "robot", "khủng long", "ngoài hành tinh", "ninja", "kho báu",
    "mật mã", "phép thuật", "lỗ đen", "hạt bụi", "tiếng chuông", "bí mật"
]

try:
    # Lấy API key từ GitHub Secrets (được truyền vào qua biến môi trường)
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("API key not found in environment variables.")

    genai.configure(api_key=api_key)

    # Chọn model (Flash thường nhanh và tiết kiệm)
    model = genai.GenerativeModel('gemini-1.5-flash')

    # Chọn từ khóa ngẫu nhiên cho ngày hôm nay
    daily_seed_word = random.choice(seed_words)

    # Xây dựng prompt hoàn chỉnh
    prompt = f"""
Hãy viết một đoạn độc thoại ngắn (khoảng 100-150 từ) với giọng điệu của một người có **năng lượng cực kỳ cao, bất ổn, hỗn loạn nhưng lại lạc quan một cách phi lý**.
Yêu cầu:
- Sử dụng ngôn ngữ **xen lẫn tiếng Việt và tiếng Anh (Vietglish)** một cách tự nhiên hoặc hài hước (dùng các từ/cụm từ tiếng Anh thông dụng như OMG, wow, cool, amazing, seriously, level up, challenge, opportunity, mindset, vibes, etc.).
- Thể hiện **suy nghĩ nhảy cóc**, chuyển chủ đề đột ngột, logic "xàm xàm".
- Lồng ghép một thông điệp có vẻ **tích cực** hoặc một **lời khuyên răn** nhưng phải dựa trên **lý lẽ ngớ ngẩn** hoặc áp dụng vào tình huống vô lý.
- Dùng nhiều **dấu chấm than!!!** và từ ngữ thể hiện sự hào hứng quá mức (Yaaa, Woohoo, Tuyệt vời, Không thể tin được!, ...).
- **Quan trọng (Yếu tố thay đổi):** Hôm nay hãy lấy cảm hứng từ từ khóa ngẫu nhiên sau: '{daily_seed_word}'. Hãy để từ khóa này len lỏi vào dòng suy nghĩ một cách bất ngờ và phi lý nhất có thể!

Ví dụ giọng điệu (chỉ tham khảo): OMG! Năng lượng hôm nay amazing! Phải làm gì đó thật epic! Hay là mình thử dạy con mèo nhà mình cách trả lời email công việc nhỉ? Level up skill cho boss liền! Đó là mindset phải có! Cứ tin là làm được! Go go go!!!
"""

    # Gọi Gemini API
    print(f"Generating content with seed word: {daily_seed_word}") # Log để debug
    response = model.generate_content(prompt)

    # Lấy text và làm sạch sơ bộ
    ramble_text = response.text.strip()
    print(f"Generated text: {ramble_text[:100]}...") # Log để debug

    # Chuẩn bị dữ liệu để lưu
    today_date = datetime.now().strftime("%Y-%m-%d")
    data = {"date": today_date, "seed_word": daily_seed_word, "ramble": ramble_text}

    # Xác định đường dẫn file (quan trọng!)
    # Giả sử script chạy từ thư mục gốc repo, lưu vào thư mục _data
    # Nếu dùng cấu trúc khác, cần chỉnh sửa đường dẫn này
    file_path = "data/daily_ramble.json" 
    
    # Tạo thư mục nếu chưa có (quan trọng khi chạy lần đầu trên Actions)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Ghi file JSON
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Successfully updated {file_path}")

except Exception as e:
    print(f"An error occurred: {e}", file=sys.stderr) # In lỗi ra stderr
    sys.exit(1) # Thoát với mã lỗi để Actions biết là thất bại