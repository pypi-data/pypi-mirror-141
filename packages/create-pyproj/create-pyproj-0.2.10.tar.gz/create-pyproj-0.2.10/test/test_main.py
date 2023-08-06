import shutil
from pathlib import Path

# import pytest
from src.create_pyproj.createfile import copyTemplates, createFiles

DIR = Path(__file__).parent.absolute()

projectname = 'z-test-proj'
cli = False
python_version = '3.8'

TEST_DIR = DIR.parent / projectname
PROJ_DIR = TEST_DIR / 'src' / projectname.replace('-', '_')


def test_copy_templates():
    if TEST_DIR.exists():
        shutil.rmtree(TEST_DIR)
    assert not TEST_DIR.exists(), f"{TEST_DIR} should not exist"
    copyTemplates(projectname, cli)
    assert (PROJ_DIR / '_config' / 'logging.yaml').exists(), 'logging.yaml not copied to '


def test_create_files():
    createFiles(projectname, cli, python_version)
    assert (TEST_DIR / '.gitlab-ci.yml').exists(), f'gitlab-ci.yml not copied to {PROJ_DIR}'
