import os
import shutil

from tools.check_clean_export import child_environment


def test_clean_export_children_resolve_python_from_the_fresh_venv_first(tmp_path):
    env_dir = tmp_path / "venv"
    scripts_dir = "Scripts" if os.name == "nt" else "bin"
    venv_python = env_dir / scripts_dir / ("python.exe" if os.name == "nt" else "python")
    venv_python.parent.mkdir(parents=True)
    venv_python.write_text("venv interpreter")
    if os.name != "nt":
        venv_python.chmod(0o755)

    system_dir = tmp_path / "system-bin"
    system_dir.mkdir()
    system_python = system_dir / ("python.exe" if os.name == "nt" else "python")
    system_python.write_text("system interpreter")
    if os.name != "nt":
        system_python.chmod(0o755)

    child_env = child_environment(env_dir, {"PATH": str(system_dir)})

    assert shutil.which("python", path=child_env["PATH"]) == str(venv_python)
