import subprocess
import sys
from datetime import datetime
from pathlib import Path


def _venv_python() -> str:
    """Always use the venv Python so all installed plugins are available."""
    venv_python = Path(__file__).resolve().parent / ".venv" / "Scripts" / "python.exe"
    if venv_python.exists():
        return str(venv_python)
    return sys.executable


def main() -> int:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from utils.config_reader import ConfigReader

    env = _get_env_arg()
    config = ConfigReader(env=env)

    report_dir = Path(__file__).resolve().parent / config.get("report_path", "reports")
    report_dir.mkdir(parents=True, exist_ok=True)
    allure_dir = Path(__file__).resolve().parent / "allure-results"
    allure_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = report_dir / f"playwright_report_{timestamp}.html"

    command = [
        _venv_python(), "-m", "pytest",
        "-n", str(config.get("workers", "auto")),
        "--reruns", str(config.get("retry", 1)),
        "--html", str(report_file),
        "--self-contained-html",
        f"--alluredir={allure_dir}",
    ]

    if env:
        command += ["--env", env]

    result = subprocess.run(command)
    print(f"\nEnvironment  : {env or 'default'}")
    print(f"HTML Report  : {report_file}")
    print(f"Allure Data  : {allure_dir}")
    print(f"Exit Code    : {result.returncode}")
    return result.returncode


def _get_env_arg() -> str | None:
    for i, arg in enumerate(sys.argv[1:], 1):
        if arg == "--env" and i < len(sys.argv):
            return sys.argv[i + 1]
        if arg.startswith("--env="):
            return arg.split("=", 1)[1]
    return None


if __name__ == "__main__":
    raise SystemExit(main())
