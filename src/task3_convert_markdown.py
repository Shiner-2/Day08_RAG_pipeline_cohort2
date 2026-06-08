"""
Task 3 — Convert toàn bộ file trong data/landing/ thành Markdown.

Sử dụng MarkItDown của Microsoft:
    https://github.com/microsoft/markitdown

Cài đặt:
    pip install markitdown

Hướng dẫn:
    1. Scan toàn bộ file trong data/landing/ (PDF, DOCX, JSON)
    2. Convert sang Markdown
    3. Lưu vào data/standardized/ giữ nguyên cấu trúc thư mục
"""

import json
from pathlib import Path

try:
    from markitdown import MarkItDown
except ImportError:
    MarkItDown = None

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None

LANDING_DIR = Path(__file__).parent.parent / "data" / "landing"
OUTPUT_DIR = Path(__file__).parent.parent / "data" / "standardized"


def _markdown_from_pdf(filepath: Path) -> str:
    """Extract PDF text with pypdf when MarkItDown is not installed."""
    if PdfReader is None:
        raise ImportError("Cần cài markitdown hoặc pypdf để convert PDF")

    reader = PdfReader(str(filepath))
    parts = [f"# {filepath.stem}\n"]
    for page_num, page in enumerate(reader.pages, 1):
        text = page.extract_text() or ""
        text = text.strip()
        if text:
            parts.append(f"\n\n## Page {page_num}\n\n{text}")
    content = "\n".join(parts).strip() + "\n"
    if len(content) > 200:
        return content

    return _fallback_pdf_markdown(filepath, len(reader.pages))


def _fallback_pdf_markdown(filepath: Path, page_count: int) -> str:
    """Create useful metadata when a signed/scanned PDF has no extractable text."""
    known_titles = {
        "nghi-dinh-105-2021": (
            "Nghị định 105/2021/NĐ-CP",
            "Quy định chi tiết và hướng dẫn thi hành một số điều của Luật Phòng, chống ma túy.",
        ),
        "nghi-dinh-57-2022": (
            "Nghị định 57/2022/NĐ-CP",
            "Quy định các danh mục chất ma túy và tiền chất.",
        ),
    }
    title, description = known_titles.get(
        filepath.stem,
        (filepath.stem, "Văn bản pháp luật trong bộ dữ liệu landing/legal."),
    )

    return (
        f"# {title}\n\n"
        f"**File gốc:** `{filepath.name}`\n\n"
        f"**Số trang PDF:** {page_count}\n\n"
        f"**Mô tả:** {description}\n\n"
        "## Ghi chú chuyển đổi\n\n"
        "File PDF này là bản ký số hoặc bản quét nên thư viện `pypdf` không trích "
        "được nội dung chữ đầy đủ trong môi trường hiện tại. Bản Markdown này giữ "
        "metadata quan trọng để pipeline vẫn nhận diện được tài liệu, còn nếu cần "
        "full text thì nên cài `markitdown` kèm engine OCR hoặc dùng bản DOC/text "
        "từ nguồn văn bản pháp luật chính thức.\n"
    )


def _convert_document_to_markdown(filepath: Path) -> str:
    if MarkItDown is not None:
        result = MarkItDown().convert(str(filepath))
        return result.text_content

    if filepath.suffix.lower() == ".pdf":
        return _markdown_from_pdf(filepath)

    raise ImportError(f"Không thể convert {filepath.suffix}; hãy cài markitdown")


def convert_legal_docs():
    """Convert PDF/DOCX files trong data/landing/legal/ sang markdown."""
    legal_dir = LANDING_DIR / "legal"
    output_dir = OUTPUT_DIR / "legal"
    output_dir.mkdir(parents=True, exist_ok=True)

    for filepath in legal_dir.iterdir():
        if filepath.suffix.lower() in (".pdf", ".docx", ".doc"):
            print(f"Converting: {filepath.name}")
            content = _convert_document_to_markdown(filepath)
            output_path = output_dir / f"{filepath.stem}.md"
            output_path.write_text(content, encoding="utf-8")
            print(f"  ✓ Saved: {output_path}")


def convert_news_articles():
    """Convert JSON crawled articles trong data/landing/news/ sang markdown."""
    news_dir = LANDING_DIR / "news"
    output_dir = OUTPUT_DIR / "news"
    output_dir.mkdir(parents=True, exist_ok=True)

    for filepath in news_dir.iterdir():
        if filepath.suffix.lower() == ".json":
            print(f"Converting: {filepath.name}")
            data = json.loads(filepath.read_text(encoding="utf-8"))
            output_path = output_dir / f"{filepath.stem}.md"

            header = f"# {data.get('title', 'Unknown')}\n\n"
            header += f"**Source:** {data.get('source', 'N/A')}\n\n"
            header += f"**URL:** {data.get('url', 'N/A')}\n\n"
            header += f"**Published:** {data.get('published_time', 'N/A')}\n\n"
            header += f"**Crawled:** {data.get('date_crawled', 'N/A')}\n\n---\n\n"

            body = data.get("content_markdown") or data.get("content_text") or ""
            output_path.write_text(header + body.strip() + "\n", encoding="utf-8")
            print(f"  ✓ Saved: {output_path}")


def convert_all():
    """Convert toàn bộ files."""
    print("=" * 50)
    print("Task 3: Convert to Markdown (MarkItDown)")
    print("=" * 50)

    print("\n--- Legal Documents ---")
    convert_legal_docs()

    print("\n--- News Articles ---")
    convert_news_articles()

    print("\n✓ Done! Output tại:", OUTPUT_DIR)


if __name__ == "__main__":
    convert_all()
