from pathlib import Path
import subprocess as sp
import shutil as sh
import psycopg

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

def test_deploy_copies_nginx_config():
    config_source = project_root / "nginx" / "site.conf"
    config_dest = Path("/etc/nginx/sites-available/devops-site")
    
    sp.run(["bash", str(project_root / "scripts" / "deploy.sh")], check=True)
    assert config_dest.is_file()
    assert config_source.read_text() == config_dest.read_text()

def test_deploy_logs_to_postgres():
    # Step 1: connect to ops_db
    conn = psycopg.connect("dbname=ops_db user=postgres password=password host=localhost")
    cur = conn.cursor()
    
    # Step 2: count before deploy
    cur.execute("SELECT COUNT(*) FROM operations")
    count_before = cur.fetchone()[0]
    
    # Step 3: run deploy
    sp.run(["bash", str(project_root / "scripts" / "deploy.sh")], check=True)

    # Step 4: assert count increased by 1
    cur.execute("SELECT COUNT(*) FROM operations")
    count_after = cur.fetchone()[0]
    assert count_after == count_before + 1

    # Step 5: fetch latest row and assert
    cur.execute("SELECT action_type, status FROM operations ORDER BY id DESC LIMIT 1")
    action_type, status = cur.fetchone()
    assert action_type == "deploy"
    assert status == "success"

    # Cleanup: delete the row created by this test
    cur.execute("DELETE FROM operations WHERE id = (SELECT MAX(id) FROM operations)")
    conn.commit()
    cur.close()
    conn.close()