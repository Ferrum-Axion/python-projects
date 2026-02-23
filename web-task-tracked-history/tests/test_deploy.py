import subprocess
import shutil
from pathlib import Path
import pytest
from log_operations import execute_query

project_root = Path(__file__).resolve().parents[1] 
dest_site_dir = Path("/var/www/devops-site")
config_source = Path("/etc/nginx/sites-available")

@pytest.fixture
def run_deploy():
    temp_site_dir = Path("/tmp/site_backup")
    temp_config_dir = Path("/tmp/config_backup")
    shutil.copytree(dest_site_dir, temp_site_dir, dirs_exist_ok=True )
    shutil.copytree(config_source, temp_config_dir, dirs_exist_ok=True )
    yield
    shutil.copytree(temp_site_dir,dest_site_dir, dirs_exist_ok=True )
    shutil.copytree(temp_config_dir, config_source, dirs_exist_ok=True )


def test_index_moved_succesfuly(run_deploy):
    site_dir = project_root / "site"
    marker = "\n --- TEST MARKER ---"
    index_content_dev = ( site_dir / "index.html").read_text()
    (site_dir / "index.html").write_text(index_content_dev + marker)
    subprocess.run([project_root / "scripts" / "deploy.sh"])

    assert  marker in (dest_site_dir / "index.html").read_text()

    (site_dir / "index.html").write_text(index_content_dev)


def test_configuration_available(run_deploy):
    dev_config = (project_root / "nginx" / "site.conf").read_text()
    subprocess.run([project_root / "scripts" / "deploy.sh"])
    config_content = (config_source / "devops-site").read_text() 
    assert config_content == dev_config


def test_logoperation(run_deploy):
    
    current_count = execute_query("SELECT COUNT(*) from operations", True)[0][0]
    subprocess.run([project_root / "scripts" / "deploy.sh"])
    after_test_count = execute_query("SELECT COUNT(*) from operations", True)[0][0]
    print(after_test_count)
    print(current_count)

    assert after_test_count == current_count + 1















