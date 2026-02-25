from pathlib import Path
import subprocess as sp
import shutil as sh

project_root = Path(__file__).resolve().parent.parent 
tmp_dir = project_root / ".tmp"
tmp_dir.mkdir(exist_ok=True)  

def test_sanity():
    file = tmp_dir / "test.txt"
    file.write_text("Aviv is testing!")
    assert file.read_text() == "Aviv is testing!"

def test_deploy_copies_site():
    site_source = project_root / "site"
    site_dest = Path("/var/www/devops-site")
    source_html = site_source / "index.html"
    
    # Backup deployed site
    backup = tmp_dir / "site_backup"
    if backup.exists():
        sh.rmtree(backup)
    sh.copytree(site_dest, backup)
    
    # Save original content and add marker
    original_content = source_html.read_text()
    marker = "<!-- TEST-MARKER -->"
    try:
        source_html.write_text(original_content + "\n" + marker)
        sp.run(["bash", str(project_root / "scripts" / "deploy.sh")], check=True)
        assert marker in (site_dest / "index.html").read_text()
    finally:
        source_html.write_text(original_content)
        sh.rmtree(site_dest)
        sh.copytree(backup, site_dest)
