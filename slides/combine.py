
from pathlib import Path
import sys
import argparse
from typing import Iterable
from pathlib import Path
import sys
import argparse
from typing import Iterable


lecture_list = [
    r"C:\Users\songjoon\OneDrive\7 2025가을학기\오토마타\CS322_fall2025\slides\Lec01_FiniteAutomata.pdf",
    r"C:\Users\songjoon\OneDrive\7 2025가을학기\오토마타\CS322_fall2025\slides\Lec02_NFA.pdf",
    r"C:\Users\songjoon\OneDrive\7 2025가을학기\오토마타\CS322_fall2025\slides\Lec03_NFA=DFA,operations.pdf",
    r"C:\Users\songjoon\OneDrive\7 2025가을학기\오토마타\CS322_fall2025\slides\Lec04_RegularExpressions.pdf",
    r"C:\Users\songjoon\OneDrive\7 2025가을학기\오토마타\CS322_fall2025\slides\Lec05_PumpingLemma.pdf",
    r"C:\Users\songjoon\OneDrive\7 2025가을학기\오토마타\CS322_fall2025\slides\Lec06_Myhill-Nerode+MSO_my.pdf",
    r"C:\Users\songjoon\OneDrive\7 2025가을학기\오토마타\CS322_fall2025\slides\Lec06_Myhill-Nerode+MSO.pdf",
    r"C:\Users\songjoon\OneDrive\7 2025가을학기\오토마타\CS322_fall2025\slides\Lec07_Properties_Regular.pdf",
    r"C:\Users\songjoon\OneDrive\7 2025가을학기\오토마타\CS322_fall2025\slides\Lec08_MoreOnRL+ContextFreeGrammar.pdf",
    r"C:\Users\songjoon\OneDrive\7 2025가을학기\오토마타\CS322_fall2025\slides\Lec09_derivation+parsetree.pdf",
    r"C:\Users\songjoon\OneDrive\7 2025가을학기\오토마타\CS322_fall2025\slides\Lec10_Ambiguity+PushdownAutomata.pdf",
    r"C:\Users\songjoon\OneDrive\7 2025가을학기\오토마타\CS322_fall2025\slides\Lec11_PDAandCFG.pdf",
]


def combine_pdfs(paths: Iterable[str], output: str | Path, skip_missing: bool = False) -> Path:
    """Combine a sequence of PDF file paths into a single PDF using PyPDF2.

    The import of PyPDF2 is done lazily so that calling this module with
    --list will not require PyPDF2 to be installed.
    """
    try:
        from PyPDF2 import PdfReader, PdfWriter
    except Exception as exc:
        raise RuntimeError("PyPDF2 is required. Install with: python -m pip install PyPDF2") from exc

    writer = PdfWriter()
    total_pages = 0
    appended = 0

    for p in paths:
        pth = Path(p)
        if not pth.exists():
            msg = f"Missing file: {pth}"
            if skip_missing:
                print("Warning:", msg)
                continue
            raise FileNotFoundError(msg)

        try:
            reader = PdfReader(str(pth))
            num = len(reader.pages)
            for page in reader.pages:
                writer.add_page(page)
            total_pages += num
            appended += 1
            print(f"Appended: {pth.name} ({num} pages)")
        except Exception as e:
            raise RuntimeError(f"Failed to append {pth}: {e}") from e

    if appended == 0:
        raise RuntimeError("No files were appended. Nothing to write.")

    out_path = Path(output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("wb") as f:
        writer.write(f)

    print(f"Wrote {out_path} — {total_pages} pages from {appended} files")
    return out_path


def _build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Merge PDFs listed in this file into one PDF")
    default_out = Path(__file__).parent / "Combined_Lectures.pdf"
    p.add_argument("--output", "-o", default=str(default_out), help="Destination PDF path")
    p.add_argument("--skip-missing", action="store_true", help="Skip missing input files instead of failing")
    p.add_argument("--list", action="store_true", help="Print the list of PDFs that would be merged and exit")
    return p


def main(argv: list[str] | None = None) -> int:
    argv = list(argv) if argv is not None else None
    parser = _build_arg_parser()
    args = parser.parse_args(argv)

    if args.list:
        for p in lecture_list:
            print(p)
        return 0

    try:
        combine_pdfs(lecture_list, args.output, skip_missing=args.skip_missing)
        return 0
    except FileNotFoundError as e:
        print("Error:", e, file=sys.stderr)
        return 2
    except Exception as e:
        print("Error:", e, file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
