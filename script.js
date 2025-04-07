document.addEventListener('DOMContentLoaded', () => {
    // QUAN TRỌNG: Đường dẫn này PHẢI ĐÚNG với vị trí file JSON
    // sau khi GitHub Pages build (nếu có) hoặc vị trí tương đối
    // từ file index.html trong repo.
    // Nếu file JSON nằm ở `_data/daily_ramble.json` và bạn không dùng
    // Jekyll/Eleventy build gì đặc biệt, bạn cần tìm cách để file này
    // được copy ra thư mục gốc hoặc một thư mục public khi deploy.
    // Cách đơn giản nhất có thể là lưu file JSON vào thư mục gốc repo,
    // ví dụ: `data/daily_ramble.json` và đường dẫn fetch sẽ là `/data/daily_ramble.json`
    // Dưới đây dùng đường dẫn giả định là nằm ở thư mục gốc cho dễ test.
    const dataUrl = '/data/daily_ramble.json'; // <<< *** CHỈNH SỬA ĐƯỜNG DẪN NÀY ***
  
    // Thêm tham số ngẫu nhiên để tránh cache trình duyệt
    fetch(dataUrl + '?cb=' + new Date().getTime()) 
      .then(response => {
        if (!response.ok) {
          // Nếu lỗi 404, có thể file chưa được tạo hoặc đường dẫn sai
          if(response.status === 404) {
               throw new Error(`File not found at ${dataUrl}. Check path or wait for first generation.`);
          }
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        const outputDiv = document.getElementById('ramble-output');
        const dateSpan = document.getElementById('update-date');
        const seedSpan = document.getElementById('seed-word');
  
        if (outputDiv && data.ramble) {
          // Thay thế ký tự xuống dòng bằng thẻ <br> để hiển thị trên HTML
          outputDiv.innerHTML = `<p>${data.ramble.replace(/\n/g, '<br>')}</p>`;
        } else {
           outputDiv.innerHTML = '<p>Hôm nay năng lượng bị lag nặng, xin lỗi nha!</p>';
        }
        if (dateSpan && data.date) {
            dateSpan.textContent = data.date;
        }
        if (seedSpan && data.seed_word) {
            seedSpan.textContent = data.seed_word;
        }
      })
      .catch(error => {
        console.error('Error fetching daily ramble:', error);
        const outputDiv = document.getElementById('ramble-output');
        if (outputDiv) {
          outputDiv.innerHTML = `<p>Oops! Lỗi kết nối năng lượng vũ trụ rồi! (${error.message}). Thử F5 lại trang xem sao!</p>`;
        }
      });
  });

  // ---- Tilt Effect on Mouse Move ----

const container = document.querySelector('.container');
const siteWrapper = document.querySelector('.site-wrapper'); // Vùng lắng nghe sự kiện

// Kiểm tra nếu .container tồn tại
if (container && siteWrapper) {
  const maxTilt = 10; // Độ nghiêng tối đa (độ)

  siteWrapper.addEventListener('mousemove', (e) => {
    // Lấy kích thước và vị trí của container
    const rect = container.getBoundingClientRect();
    // Lấy vị trí chuột trong viewport
    const mouseX = e.clientX;
    const mouseY = e.clientY;

    // Tính tâm của container
    const centerX = rect.left + rect.width / 2;
    const centerY = rect.top + rect.height / 2;

    // Tính khoảng cách từ chuột đến tâm container
    const deltaX = mouseX - centerX;
    const deltaY = mouseY - centerY;

    // Tính % khoảng cách so với nửa chiều rộng/cao
    // Giới hạn giá trị từ -1 đến 1
    const percentX = Math.max(-1, Math.min(1, deltaX / (rect.width / 2)));
    const percentY = Math.max(-1, Math.min(1, deltaY / (rect.height / 2)));

    // Tính độ nghiêng (rotateY dựa vào deltaX, rotateX dựa vào deltaY)
    // * (-1) để đảo chiều nghiêng cho tự nhiên
    const rotateY = percentX * maxTilt * (-1);
    const rotateX = percentY * maxTilt;

    // Áp dụng transform (thêm perspective ở parent để có hiệu ứng 3D)
    // Thêm scale nhẹ để đẹp hơn
    container.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale(1.03)`;
  });

  // Reset transform khi chuột rời khỏi vùng wrapper
  siteWrapper.addEventListener('mouseleave', () => {
    container.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) scale(1)';
  });
} else {
    console.warn("Element '.container' or '.site-wrapper' not found for tilt effect.");
}

// ---- Existing JavaScript code ----
document.addEventListener('DOMContentLoaded', () => {
    // ... (code fetch data của bạn giữ nguyên ở đây) ...
    const dataUrl = './data/daily_ramble.json'; // <<< *** NHỚ KIỂM TRA ĐƯỜNG DẪN NÀY ***

    fetch(dataUrl + '?cb=' + new Date().getTime())
        .then(response => {
            // ... (code xử lý response giữ nguyên) ...
            if (!response.ok) {
                if(response.status === 404) {
                     throw new Error(`File not found at ${dataUrl}. Check path or wait for first generation.`);
                }
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            // ... (code hiển thị data giữ nguyên) ...
            const outputDiv = document.getElementById('ramble-output');
            const dateSpan = document.getElementById('update-date');
            const seedSpan = document.getElementById('seed-word');

             if (outputDiv && data.ramble) {
                outputDiv.innerHTML = `<p>${data.ramble.replace(/\n/g, '<br>')}</p>`;
             } else {
                 outputDiv.innerHTML = '<p>Hôm nay năng lượng bị lag nặng, xin lỗi nha!</p>';
             }
             if (dateSpan && data.date) {
                 dateSpan.textContent = data.date;
             }
            if (seedSpan && data.seed_word) {
                seedSpan.textContent = data.seed_word;
             }
        })
        .catch(error => {
            // ... (code xử lý lỗi giữ nguyên) ...
            console.error('Error fetching daily ramble:', error);
             const outputDiv = document.getElementById('ramble-output');
             if (outputDiv) {
                 outputDiv.innerHTML = `<p>Oops! Lỗi kết nối năng lượng vũ trụ rồi! (${error.message}). Thử F5 lại trang xem sao!</p>`;
             }
        });
}); // Kết thúc DOMContentLoaded