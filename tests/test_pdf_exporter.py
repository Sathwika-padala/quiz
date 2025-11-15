"""Test for PDF exporter."""

import pytest
import tempfile
from pathlib import Path
from src.utils.pdf_exporter import PDFExporter


def test_pdf_exporter_init():
    with tempfile.TemporaryDirectory() as tmpdir:
        exporter = PDFExporter(Path(tmpdir))
        assert exporter.output_dir.exists()


def test_export_quiz_as_pdf():
    with tempfile.TemporaryDirectory() as tmpdir:
        exporter = PDFExporter(Path(tmpdir))
        questions = [{"text": "Q1", "answer": "A"}]
        path = exporter.export_quiz_as_pdf("Test Quiz", questions)
        assert Path(path).exists()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
