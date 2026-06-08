# RAG Evaluation Results

## Framework sử dụng

Framework: **Offline heuristic evaluator**. Script đo cùng 4 trục yêu cầu của RAG eval (faithfulness, answer relevance, context recall, context precision) bằng lexical overlap và kiểm tra source metadata. Cách này chạy được local, không cần judge LLM/API ngoài.

## Overall Scores

| Metric | Config A (hybrid + rerank + legal boost) | Config B (hybrid no rerank) | Δ |
|--------|-------------------------------------------|------------------------------|---|
| Faithfulness | 94.3% | 98.4% | -0.041 |
| Answer Relevance | 72.5% | 63.3% | +0.092 |
| Context Recall | 91.3% | 93.0% | -0.017 |
| Context Precision | 90.7% | 94.7% | -0.040 |
| **Average** | 87.2% | 87.3% | -0.002 |

## A/B Comparison Analysis

**Config A:** Config A - hybrid + rerank + legal boost. Dùng pipeline Task 9 đầy đủ, reranking Task 7 và ưu tiên tài liệu pháp luật khi nguồn cùng mức liên quan.

**Config B:** Config B - hybrid no rerank. Tắt reranking để quan sát chất lượng retrieval thô.

**Kết luận:** Config B - hybrid no rerank có average score cao hơn trong bộ golden dataset này. Với câu hỏi pháp lý, legal boost giúp nguồn luật xuất hiện ổn định hơn trong top context.

## Worst Performers (Bottom 3, Config A)

| # | Question | Faithfulness | Relevance | Recall | Precision | Likely Cause |
|---|----------|--------------|-----------|--------|-----------|--------------|
| 1 | Nếu câu hỏi vừa hỏi về nghệ sĩ vừa hỏi về chế tài ma túy, pipeline cần lấy loại tài liệu nào? | 100.0% | 56.1% | 0.0% | 100.0% | Expected context not exact in top sources |
| 2 | Bài VietnamNet trong dữ liệu tổng hợp chủ đề gì? | 96.9% | 74.6% | 100.0% | 40.0% | Answer wording differs from expected answer |
| 3 | Nghị định nào quy định danh mục chất ma túy và tiền chất? | 50.0% | 93.9% | 70.0% | 100.0% | Expected context not exact in top sources |

## Recommendations

### Cải tiến 1
**Action:** Tách chunk theo điều/khoản đối với tài liệu luật thay vì chỉ fixed-size character chunks.  
**Expected impact:** Tăng context precision và citation rõ hơn cho câu hỏi pháp lý.

### Cải tiến 2
**Action:** Bổ sung metadata `law_name`, `article`, `year`, `news_source`, `published_date` trong standardized Markdown.  
**Expected impact:** Giúp frontend hiển thị citation đẹp hơn và evaluator kiểm tra source chính xác hơn.

### Cải tiến 3
**Action:** Dùng reranker multilingual thực tế (Jina/Qwen) cho top 20 candidates khi có API/GPU.  
**Expected impact:** Giảm source nhiễu, đặc biệt với câu hỏi mixed giữa tin tức và chế tài pháp luật.

## Per-case Details (Config A)

| ID | Category | Avg | Expected Context | Retrieved Sources |
|----|----------|-----|------------------|-------------------|
| legal_001 | legal | 87.6% | luat-phong-chong-ma-tuy-2021.md | luat-phong-chong-ma-tuy-2021.md, luat-phong-chong-ma-tuy-2021.md, luat-phong-chong-ma-tuy-2021.md, luat-phong-chong-ma-tuy-2021.md, luat-phong-chong-ma-tuy-2021.md |
| legal_002 | legal | 83.7% | bo-luat-hinh-su-2015-phan-1.md | bo-luat-hinh-su-2015-phan-1.md, luat-phong-chong-ma-tuy-2021.md, luat-phong-chong-ma-tuy-2021.md, 05-sao-viet-ten-tin-dinh-ma-tuy-vietnamnet.md, 02-truy-to-chi-dan-an-tay-dan-tri.md |
| legal_003 | legal | 99.6% | nghi-dinh-105-2021.md | nghi-dinh-105-2021.md, luat-phong-chong-ma-tuy-2021.md, luat-phong-chong-ma-tuy-2021.md, vbhn-danh-muc-chat-ma-tuy-tien-chat-2020.md, luat-phong-chong-ma-tuy-2021.md |
| legal_004 | legal | 78.5% | nghi-dinh-57-2022.md | vbhn-danh-muc-chat-ma-tuy-tien-chat-2020.md, vbhn-danh-muc-chat-ma-tuy-tien-chat-2020.md, vbhn-danh-muc-chat-ma-tuy-tien-chat-2020.md, vbhn-danh-muc-chat-ma-tuy-tien-chat-2020.md, vbhn-danh-muc-chat-ma-tuy-tien-chat-2020.md |
| legal_005 | legal | 90.9% | luat-phong-chong-ma-tuy-2021.md | luat-phong-chong-ma-tuy-2021.md, nghi-dinh-105-2021.md, luat-phong-chong-ma-tuy-2021.md, luat-phong-chong-ma-tuy-2021.md, luat-phong-chong-ma-tuy-2021.md |
| legal_006 | legal | 84.2% | bo-luat-hinh-su-2015-phan-1.md | luat-phong-chong-ma-tuy-2021.md, 02-truy-to-chi-dan-an-tay-dan-tri.md, bo-luat-hinh-su-2015-phan-1.md, luat-phong-chong-ma-tuy-2021.md, luat-phong-chong-ma-tuy-2021.md |
| legal_007 | legal | 93.0% | vbhn-danh-muc-chat-ma-tuy-tien-chat-2020.md | vbhn-danh-muc-chat-ma-tuy-tien-chat-2020.md, vbhn-danh-muc-chat-ma-tuy-tien-chat-2020.md, nghi-dinh-57-2022.md, luat-phong-chong-ma-tuy-2021.md, 05-sao-viet-ten-tin-dinh-ma-tuy-vietnamnet.md |
| legal_008 | legal | 94.1% | luat-phong-chong-ma-tuy-2021.md | luat-phong-chong-ma-tuy-2021.md, nghi-dinh-105-2021.md, luat-phong-chong-ma-tuy-2021.md, luat-phong-chong-ma-tuy-2021.md, nghi-dinh-57-2022.md |
| news_001 | news | 92.7% | 01-chi-dan-an-tay-truc-phuong-thanh-nien.md | 01-chi-dan-an-tay-truc-phuong-thanh-nien.md, 01-chi-dan-an-tay-truc-phuong-thanh-nien.md, 01-chi-dan-an-tay-truc-phuong-thanh-nien.md, 02-truy-to-chi-dan-an-tay-dan-tri.md, 01-chi-dan-an-tay-truc-phuong-thanh-nien.md |
| news_002 | news | 90.9% | 02-truy-to-chi-dan-an-tay-dan-tri.md | 02-truy-to-chi-dan-an-tay-dan-tri.md, 02-truy-to-chi-dan-an-tay-dan-tri.md, 02-truy-to-chi-dan-an-tay-dan-tri.md, 05-sao-viet-ten-tin-dinh-ma-tuy-vietnamnet.md, 02-truy-to-chi-dan-an-tay-dan-tri.md |
| news_003 | news | 89.0% | 03-huu-tin-bi-tam-giu-vnexpress.md | 05-sao-viet-ten-tin-dinh-ma-tuy-vietnamnet.md, 03-huu-tin-bi-tam-giu-vnexpress.md, 05-sao-viet-ten-tin-dinh-ma-tuy-vietnamnet.md, 03-huu-tin-bi-tam-giu-vnexpress.md, 05-sao-viet-ten-tin-dinh-ma-tuy-vietnamnet.md |
| news_004 | news | 93.5% | 04-chau-viet-cuong-vnexpress.md | 04-chau-viet-cuong-vnexpress.md, 05-sao-viet-ten-tin-dinh-ma-tuy-vietnamnet.md, 04-chau-viet-cuong-vnexpress.md, 04-chau-viet-cuong-vnexpress.md, 04-chau-viet-cuong-vnexpress.md |
| news_005 | news | 77.9% | 05-sao-viet-ten-tin-dinh-ma-tuy-vietnamnet.md | luat-phong-chong-ma-tuy-2021.md, luat-phong-chong-ma-tuy-2021.md, 05-sao-viet-ten-tin-dinh-ma-tuy-vietnamnet.md, bo-luat-hinh-su-2015-phan-1.md, 05-sao-viet-ten-tin-dinh-ma-tuy-vietnamnet.md |
| mixed_001 | mixed | 88.4% | luat-phong-chong-ma-tuy-2021.md | nghi-dinh-57-2022.md, 02-truy-to-chi-dan-an-tay-dan-tri.md, luat-phong-chong-ma-tuy-2021.md, 05-sao-viet-ten-tin-dinh-ma-tuy-vietnamnet.md, 01-chi-dan-an-tay-truc-phuong-thanh-nien.md |
| mixed_002 | mixed | 64.0% | bo-luat-hinh-su-2015-phan-1.md | nghi-dinh-105-2021.md, nghi-dinh-57-2022.md, 02-truy-to-chi-dan-an-tay-dan-tri.md, 02-truy-to-chi-dan-an-tay-dan-tri.md, 04-chau-viet-cuong-vnexpress.md |
