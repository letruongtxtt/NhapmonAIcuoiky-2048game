# 2048 AI Solver - Báo cáo & Hướng dẫn Sử dụng

Dự án này là một chương trình giải quyết trò chơi **2048** tự động sử dụng các thuật toán Trí tuệ nhân tạo (AI) nâng cao bao gồm **Expectimax**, **Minimax**, và **Greedy Heuristic**. Giao diện ứng dụng được phát triển trực quan dựa trên thư viện đồ họa **Tkinter** của Python, đi kèm bảng điều khiển thời gian thực (Dashboard) hỗ trợ thay đổi thuật toán động và tự động chơi/lập lại.

---

## 1. Kiến trúc Hệ thống (Project Architecture)

Mã nguồn được tổ chức phân lớp rõ ràng theo mô hình hướng đối tượng, bao gồm các cấu phần chính sau:

*   **[main.py](file:///c:/Users/OS/Downloads/duancuoiky/main.py)**: Điểm khởi chạy ứng dụng (Entry Point). Kích hoạt vòng lặp chính của giao diện đồ họa.
*   **[gui.py](file:///c:/Users/OS/Downloads/duancuoiky/gui.py)**: Thành phần Giao diện người dùng (GUI) xây dựng bằng `Tkinter`. Quản lý các trạng thái hiển thị (Đang chơi, Thắng, Thua, Bị kẹt), bảng điểm số (Score/Best Score), bộ điều khiển lựa chọn thuật toán và luồng chạy thời gian thực (`mainloop`).
*   **[ai_agent.py](file:///c:/Users/OS/Downloads/duancuoiky/ai_agent.py)**: Lớp xử lý AI cốt lõi. Chứa các hàm tìm kiếm quyết định như Expectimax, Minimax và hàm lượng giá trạng thái Heuristic.
*   **[game_logic.py](file:///c:/Users/OS/Downloads/duancuoiky/game_logic.py)**: Định nghĩa luật chơi 2048, các phép biến đổi ma trận khi dịch chuyển (Trượt, Gộp ô) và tạo ngẫu nhiên ô số mới (2 hoặc 4).
*   **[config.py](file:///c:/Users/OS/Downloads/duancuoiky/config.py)**: Tệp cấu hình chứa các tham số hệ thống như kích thước lưới ($4 \times 4$), bảng màu giao diện, độ sâu tìm kiếm tìm kiếm ($d = 3$), và ma trận trọng số Heuristic.

---

## 2. Cơ sở Lý thuyết & Thuật toán AI

Trò chơi 2048 có đặc thù là **Trò chơi ngẫu nhiên (Stochastic Game)** và có thông tin hoàn hảo. Do tính chất xuất hiện ngẫu nhiên của các ô mới (2 hoặc 4), trạng thái tiếp theo của bảng cờ không hoàn toàn được quyết định bởi hành động của người chơi. Dự án hiện thực hóa 3 giải thuật tìm kiếm để giải quyết bài toán này:

### A. Thuật toán Expectimax Search
Expectimax là sự mở rộng của thuật toán Minimax đối với các trò chơi có yếu tố ngẫu nhiên (chứa nút cơ hội - **Chance Nodes**). Trong 2048, các nút cơ hội đại diện cho việc máy tính sinh ngẫu nhiên ô số mới tại các vị trí trống.
*   **Nút Max (Lượt của AI)**: Chọn hướng di chuyển ($Up, Down, Left, Right$) nhằm tối đa hóa điểm lượng giá trả về từ các nút con.
    $$\text{Value}(s) = \max_{a \in \text{Actions}} \text{Expectimax}(\text{Result}(s, a), \text{depth} - 1)$$
*   **Nút Chance (Lượt của môi trường)**: Tính toán giá trị kỳ vọng (Expected Value) dựa trên xác suất xuất hiện ô số mới ($90\%$ cho ô giá trị 2, $10\%$ cho ô giá trị 4). Để tối ưu hiệu năng tính toán, thuật toán giới hạn duyệt qua 4 ô trống đầu tiên:
    $$\text{Value}(s) = \sum_{c \in \text{Empty Cells}} P(c) \times \left( 0.9 \times \text{Expectimax}(s_{c \leftarrow 2}, \text{depth}-1) + 0.1 \times \text{Expectimax}(s_{c \leftarrow 4}, \text{depth}-1) \right)$$

### B. Thuật toán Minimax Search (Adversarial Search)
Khác với Expectimax giả định phân phối xác suất trung lập, Minimax mô hình hóa môi trường giống như một **đối thủ cạnh tranh** có ý đồ xấu (Adversarial).
*   **Nút Min (Lượt của môi trường)**: Giả định môi trường sẽ thả ô số 2 hoặc 4 vào các vị trí trống sao cho **tối thiểu hóa** điểm số của người chơi. Mô hình này mang tính phòng thủ cực đoan (Worst-case Scenario).
    $$\text{Value}(s) = \min_{c \in \text{Empty Cells}, v \in \{2, 4\}} \text{Minimax}(s_{c \leftarrow v}, \text{depth} - 1)$$
*   Minimax giúp AI chơi an toàn hơn ở các giai đoạn cờ chật hẹp, tránh các tình huống xấu nhất nhưng đôi khi quá thận trọng so với Expectimax.

### C. Thuật toán Greedy Heuristic
Thuật toán tham lam cục bộ chỉ tìm kiếm với độ sâu $d = 1$. Tại mỗi bước đi, AI thực hiện thử nghiệm cả 4 hướng di chuyển khả thi và ngay lập tức chọn hướng đem lại điểm lượng giá Heuristic cao nhất tại thời điểm hiện tại mà không dự đoán trước các phản ứng tiếp theo từ môi trường.

---

## 3. Hàm Lượng giá Heuristic (Evaluation Function)

Chìa khóa thành công của tác tử AI nằm ở hàm lượng giá trạng thái $f(s)$ tại các nút lá của cây quyết định. Hàm này được thiết kế đa tiêu chí để đánh giá độ "tốt" của một thế cờ:

$$f(s) = S_{\text{weight}} + S_{\text{empty}} + S_{\text{smoothness}}$$

Trong đó:
1.  **Điểm trọng số vị trí ($S_{\text{weight}}$)**: Sử dụng kỹ thuật ma trận trọng số hình rắn (**Snake Pattern Weight Matrix**). Chiến thuật này ép các ô có giá trị lớn dồn về một góc cố định (ở đây là góc trên-trái) để duy trì cấu trúc bàn cờ ngăn nắp:
    $$W = \begin{pmatrix} 10000 & 4000 & 1000 & 500 \\ 200 & 400 & 600 & 800 \\ 150 & 100 & 50 & 20 \\ 0 & 2 & 5 & 10 \end{pmatrix}$$
    $$S_{\text{weight}} = \sum_{i=1}^{4}\sum_{j=1}^{4} M_{i,j} \times W_{i,j}$$
2.  **Độ thoáng bảng cờ ($S_{\text{empty}}$)**: Ưu tiên các trạng thái có nhiều ô trống hơn để duy trì không gian xoay sở và giảm tỷ lệ bị thua cuộc:
    $$S_{\text{empty}} = N_{\text{empty}} \times 1000$$
3.  **Độ mịn liền kề ($S_{\text{smoothness}}$)**: Đo lường sự chênh lệch giá trị giữa các ô cạnh nhau (sử dụng thang đo logarit $\log_2$). Hàm Heuristic sẽ phạt nặng các thế cờ có sự chênh lệch lớn giữa các ô liền kề nhằm giữ cho các ô dễ dàng gộp vào nhau:
    $$S_{\text{smoothness}} = 200 \times \left( -\sum_{i,j} \left| \log_2(M_{i,j}) - \log_2(M_{\text{neighbor}}) \right| \right)$$

---

## 4. Hướng dẫn Cài đặt & Sử dụng

### Yêu cầu hệ thống
*   Python từ 3.8 trở lên.
*   Hệ điều hành: Windows, macOS hoặc Linux.

### Các bước cài đặt
1.  Tải hoặc sao chép thư mục mã nguồn về máy tính cá nhân.
2.  Mở chương trình dòng lệnh (Command Prompt / PowerShell / Terminal) và điều hướng đến thư mục dự án.
3.  Cài đặt thư viện phụ thuộc bằng lệnh:
    ```bash
    pip install -r requirements.txt
    ```

### Hướng dẫn chạy chương trình
Khởi chạy tệp tin `main.py` để khởi động giao diện đồ họa:
```bash
python main.py
```

### Sử dụng Bảng Điều khiển (Dashboard)
1.  **Lựa chọn thuật toán**: Sử dụng thanh thả xuống (Combobox) ở góc dưới bên trái để chọn một trong ba giải thuật:
    *   `Expectimax` (Khuyên dùng - Hiệu năng cao nhất)
    *   `Minimax`
    *   `Greedy Heuristic`
2.  **Kích hoạt AI**: Nhấn nút **KÍCH HOẠT** để AI bắt đầu tự động giải quyết trò chơi. Nút này sẽ đổi màu đỏ thành **TẠM DỪNG** cho phép bạn tạm ngưng trò chơi bất cứ lúc nào.
3.  **Hệ thống tự động Reset**: Khi trò chơi kết thúc với các trạng thái:
    *   **Thắng cuộc** (Đạt ô 2048) $\rightarrow$ Nút chuyển thành `WIN! CHƠI LẠI` (màu xanh lá).
    *   **Thua cuộc** (Hết nước đi) $\rightarrow$ Nút chuyển thành `THUA! CHƠI LẠI` (màu xám tối).
    *   **Bị kẹt** (Không tìm thấy hướng đi hợp lệ) $\rightarrow$ Nút chuyển thành `KẸT! CHƠI LẠI` (màu cam).
    *   Bạn chỉ cần nhấn vào nút chơi lại tương ứng để thiết lập lại bàn cờ mới ngay lập tức.
