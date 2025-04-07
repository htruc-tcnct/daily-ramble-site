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