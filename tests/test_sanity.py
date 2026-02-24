from pathlib import Path

project_root = Path(__file__).resolve().parent.parent  # Go up to project root
tmp_dir = project_root / ".tmp"
tmp_dir.mkdir(exist_ok=True)  

def test_sanity():
    file = tmp_dir / "test.txt"
    file.write_text("Aviv is the testing!")
    assert file.read_text() == "Aviv is the testing!"