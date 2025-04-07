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
H### Nhiệm vụ: Sáng tạo Độc thoại Nội tâm Hỗn loạn Đầy Năng lượng

**Mục tiêu:** Viết một đoạn độc thoại nội tâm ngắn (khoảng 150-250 từ) thể hiện góc nhìn của một nhân vật có các đặc điểm sau:

1.  **Năng lượng Cực Cao & Bất ổn:** Nhân vật luôn trong trạng thái "tăng động", hào hứng quá mức, nhưng đồng thời cũng có vẻ hơi mất kiểm soát, suy nghĩ bay nhảy lung tung. Giống như uống 10 cốc cà phê và cố gắng ngồi thiền vậy.
2.  **Lạc quan Phi lý Trí (Toxic Positivity Kiểu Hài Hước):** Bất chấp sự hỗn loạn trong suy nghĩ hoặc tình huống thực tế (có thể là rất bình thường hoặc hơi tiêu cực), nhân vật luôn tìm ra cách để nhìn nhận mọi thứ một cách tích cực đến mức vô lý, thậm chí là ngớ ngẩn. Sự lạc quan này không dựa trên logic vững chắc mà là một dạng cơ chế đối phó "tự chế".
3.  **Tư duy Hỗn loạn & Nhảy cóc (Stream of Consciousness):** Dòng suy nghĩ không đi theo một đường thẳng. Các ý tưởng, chủ đề, quan sát nối tiếp nhau một cách đột ngột, ít hoặc không có sự liên kết logic rõ ràng. Có thể đang nghĩ về chuyện A, đột nhiên nhảy sang chuyện Z mà không cần cầu nối.
4.  **Ngôn ngữ "Vietglish" Sáng tạo:**
    * Sử dụng kết hợp tiếng Việt và tiếng Anh một cách tự nhiên *hoặc* cố tình gượng ép để tạo hiệu ứng hài hước.
    * Ưu tiên các từ/cụm tiếng Anh thông dụng, dễ hiểu trong giao tiếp hàng ngày hoặc trên mạng xã hội (VD: *OMG, wow, cool, amazing, seriously, basically, literally, vibe, mood, chill, crazy, epic, fantastic, awesome, totally, maybe, like, you know, for real?*,...).
    * Có thể dùng cả những thuật ngữ "buzzword" (VD: *mindset, challenge, opportunity, level up, skill, energy, flow, deadline, feedback,...*) nhưng áp dụng vào ngữ cảnh đời thường hoặc sai lệch một cách hài hước.
5.  **Thông điệp "Tích cực" Ngớ ngẩn:** Lồng ghép một lời khuyên, một triết lý sống, hoặc một kết luận có vẻ lạc quan, nhưng nền tảng của nó phải dựa trên suy luận "trời ơi đất hỡi", so sánh khập khiễng, hoặc áp dụng vào một tình huống hoàn toàn không liên quan. Mục đích là tạo ra sự hài hước từ sự phi lý đó.
6.  **Giọng điệu & Phong cách:**
    * Tràn đầy sự phấn khích: Sử dụng nhiều dấu chấm than (!!!), có thể viết hoa một vài từ để nhấn mạnh (kiểu như SHOUTING nhưng không quá lố).
    * Dùng các từ cảm thán, từ đệm thể hiện sự hào hứng hoặc ngạc nhiên (VD: *Trời ơi!, Wowza!, Úi chà!, Yay!, Woohoo!, Tuyệt vời!, Đỉnh!, Chất!, Không thể tin được!, Thiệt luôn á?!*,...).
    * Nhịp điệu nhanh, gấp gáp.
7.  **Yếu tố THEN CHỐT - Từ khóa Ngẫu nhiên:** Hôm nay, hãy để từ khóa **'{daily_seed_word}'** xuất hiện một cách bất ngờ và phi lý nhất trong dòng suy nghĩ của nhân vật. Nó không cần phải là chủ đề chính, chỉ cần len lỏi vào, có thể làm gián đoạn hoặc chuyển hướng suy nghĩ một cách kỳ cục. Sự xuất hiện của từ này phải củng cố thêm tính hỗn loạn và ngẫu hứng của nhân vật.

**LƯU Ý QUAN TRỌNG:**
* **KHÔNG** cần bắt đầu bằng một từ cụ thể nào trong các từ cảm thán đã liệt kê, có thể hãy suy nghĩ 1 cụm từ khác và **KHÔNG** cần kết thúc bằng "Go go go" hay bất kỳ cụm từ định sẵn nào. Hãy để độc thoại bắt đầu và kết thúc một cách tự nhiên theo dòng suy nghĩ hỗn loạn của nhân vật.

* Ví dụ về giọng điệu trong prompt gốc chỉ mang tính tham khảo về *cảm giác chung*, không phải là khuôn mẫu cứng nhắc. Hãy sáng tạo!

**Hãy bắt đầu dòng suy nghĩ hỗn loạn nhưng đầy lạc quan này!**
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