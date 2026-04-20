# PDF Page Deleter

A simple command-line Python tool to remove one or more pages from a PDF using **1-based page numbers**.

It is built for quick, practical use from the terminal and writes the result to a new PDF without modifying the original file.

## Features

- Delete one or many pages in a single command
- Uses **1-based page numbering** so it matches how humans count pages
- Keeps the original PDF untouched
- Automatically creates a sensible output filename when one is not provided
- Preserves PDF metadata when possible
- Validates bad inputs such as non-PDF files, page numbers out of range, or deleting every page
- Single-pass copy of kept pages with fast page lookup using a set

## File

- `delete_page.py`

## Requirements

- Python 3.9+
- One of the following libraries:
  - `pypdf`
  - `PyPDF2`

`pypdf` is recommended.

## Installation

Clone your repository or place the script in a folder of your choice, then install a PDF library:

```bash
pip install pypdf
```

Fallback option:

```bash
pip install PyPDF2
```

## Usage

Basic usage:

```bash
python delete_page.py <pdflocation> 10 20
```

This deletes **pages 10 and 20** from the input PDF.

### Example

```bash
python delete_page.py ./documents/report.pdf 10 20
```

If no output path is given, the script creates a new file with this naming pattern:

```text
<input_name>_pages_deleted.pdf
```

So the example above will create:

```text
report_pages_deleted.pdf
```

## Custom Output File

You can choose your own output file using `-o` or `--output`:

```bash
python delete_page.py ./documents/report.pdf 10 20 -o ./documents/report_cleaned.pdf
```

## More Examples

Delete a single page:

```bash
python delete_page.py thesis.pdf 5
```

Delete multiple pages:

```bash
python delete_page.py handbook.pdf 2 4 7 11 19
```

Use an absolute path:

```bash
python delete_page.py /Users/you/Desktop/file.pdf 3 8
```

Write output to a different folder:

```bash
python delete_page.py input.pdf 6 9 -o output/cleaned.pdf
```

## How It Works

The script:

1. Opens the source PDF
2. Converts the pages to delete into a set for fast membership checks
3. Iterates through the PDF once
4. Copies only the pages that should be kept into a new PDF
5. Tries to preserve metadata
6. Writes the result to a new file

This approach is straightforward and efficient for normal command-line PDF cleanup tasks.

## Page Numbering

This tool uses **1-based page numbering**.

That means:

- `1` = first page
- `2` = second page
- `10` = tenth page

So this command:

```bash
python delete_page.py file.pdf 10 20
```

means **delete page 10 and page 20**.

## Validation and Safety Checks

The script will stop with an error if:

- the input file does not exist
- the input file is not a `.pdf`
- a page number is `0` or negative
- a requested page is larger than the total number of pages in the PDF
- the command would delete all pages from the document
- the PDF cannot be read or the output cannot be written

## Example Output

Successful run:

```text
Done: deleted 2 page(s); kept 118 page(s).
Output: /full/path/to/report_pages_deleted.pdf
```

Example failure:

```text
Error: page(s) out of range for a 12-page PDF: 20
```

## Notes on Performance

This script is designed to be lean and practical:

- page numbers to delete are stored in a set for `O(1)` membership checks
- the PDF is processed in a single pass when building the output
- duplicate page numbers on the command line are automatically ignored because the script stores them in a set

For most everyday PDF editing tasks, this is a clean and efficient approach.

## Limitations

- This tool only deletes pages; it does not reorder, rotate, merge, split, or compress PDFs
- Some PDFs with unusual internal structures or protections may fail to read depending on the backend library
- Metadata preservation is best-effort

## Exit Behavior

- Returns exit code `0` on success
- Returns a non-zero exit code on failure

## Quick Copy-Paste Commands

Install dependency:

```bash
pip install pypdf
```

Run with default output:

```bash
python delete_page.py myfile.pdf 10 20
```

Run with custom output:

```bash
python delete_page.py myfile.pdf 10 20 -o cleaned.pdf
```

## License

Add the license that matches your repository.

## Suggested Repository Structure

```text
.
├── delete_page.py
└── README.md
```

## Minimal README Snippet

If you want a shorter version for the top of your repo, use this:

```md
# PDF Page Deleter

Delete one or more pages from a PDF using 1-based page numbers.

## Usage

```bash
python delete_page.py <pdflocation> 10 20
```

Optional custom output:

```bash
python delete_page.py <pdflocation> 10 20 -o cleaned.pdf
```
```
