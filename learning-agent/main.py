#!/usr/bin/env python3
import os
import sys
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

sys.path.insert(0, str(Path(__file__).parent / "src"))

from learning_agent import run_learning_agent


def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <path_to_docx_file>")
        sys.exit(1)
    
    docx_path = sys.argv[1]
    if not Path(docx_path).exists():
        print(f"Error: File not found: {docx_path}")
        sys.exit(1)
    
    print(f"Processing document: {docx_path}")
    result = run_learning_agent(docx_path)
    
    print("\n" + "=" * 50)
    print("✓ Processing complete!")
    print(f"✓ Obsidian note saved to: {result['note_path']}")
    print(f"✓ Log saved to: {result['log_path']}")
    print("=" * 50)


if __name__ == "__main__":
    main()
