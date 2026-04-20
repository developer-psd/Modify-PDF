#!/usr/bin/env python3
"""Delete one or more 1-based page numbers from a PDF.

Usage:
    python delete_page.py <pdf_path> 10 20
    python delete_page.py <pdf_path> 10 20 -o output.pdf

This deletes pages 10 and 20 from the input PDF and writes a new PDF.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    from pypdf import PdfReader, PdfWriter
except Exception:
    try:
        from PyPDF2 import PdfReader, PdfWriter  # type: ignore
    except Exception as exc:  # pragma: no cover
        raise SystemExit(
            "Missing dependency. Install one of: pip install pypdf  or  pip install PyPDF2"
        ) from exc


def build_output_path(input_path: Path) -> Path:
    return input_path.with_name(f"{input_path.stem}_pages_deleted{input_path.suffix}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Delete one or more pages from a PDF using 1-based page numbers."
    )
    parser.add_argument("pdf_path", help="Path to the input PDF")
    parser.add_argument(
        "pages",
        nargs="+",
        type=int,
        help="1-based page numbers to delete, e.g. 10 20 35",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Optional output PDF path. Defaults to <input>_pages_deleted.pdf",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_path = Path(args.pdf_path).expanduser().resolve()

    if not input_path.is_file():
        print(f"Error: file not found: {input_path}", file=sys.stderr)
        return 1

    if input_path.suffix.lower() != ".pdf":
        print("Error: input must be a .pdf file", file=sys.stderr)
        return 1

    output_path = Path(args.output).expanduser().resolve() if args.output else build_output_path(input_path)

    delete_pages = set(args.pages)
    if not delete_pages:
        print("Error: no pages provided", file=sys.stderr)
        return 1

    if any(page <= 0 for page in delete_pages):
        print("Error: page numbers must be positive and 1-based", file=sys.stderr)
        return 1

    try:
        reader = PdfReader(str(input_path))
    except Exception as exc:
        print(f"Error: failed to read PDF: {exc}", file=sys.stderr)
        return 1

    total_pages = len(reader.pages)
    invalid = sorted(page for page in delete_pages if page > total_pages)
    if invalid:
        print(
            f"Error: page(s) out of range for a {total_pages}-page PDF: {', '.join(map(str, invalid))}",
            file=sys.stderr,
        )
        return 1

    if len(delete_pages) >= total_pages:
        print("Error: cannot delete all pages from the PDF", file=sys.stderr)
        return 1

    writer = PdfWriter()

    # Copy only pages we keep. Membership checks are O(1).
    for zero_based_index, page in enumerate(reader.pages):
        if (zero_based_index + 1) not in delete_pages:
            writer.add_page(page)

    # Preserve metadata when available.
    try:
        if reader.metadata:
            writer.add_metadata(dict(reader.metadata))
    except Exception:
        pass

    try:
        with output_path.open("wb") as out_file:
            writer.write(out_file)
    except Exception as exc:
        print(f"Error: failed to write output PDF: {exc}", file=sys.stderr)
        return 1

    kept = total_pages - len(delete_pages)
    print(f"Done: deleted {len(delete_pages)} page(s); kept {kept} page(s).")
    print(f"Output: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
