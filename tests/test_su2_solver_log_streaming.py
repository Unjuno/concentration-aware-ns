import sys
import threading
import time

from tools.run_su2_full_horizon_cfl_pair import run_logged_command


def test_solver_output_is_visible_while_running_and_saved_byte_for_byte(tmp_path, capsys):
    log_path = tmp_path / "solver.log"
    command = [
        sys.executable,
        "-c",
        "import sys,time; print('iteration 1', flush=True); time.sleep(.6); "
        "print('late stderr', file=sys.stderr, flush=True); sys.exit(7)",
    ]
    result = []
    worker = threading.Thread(
        target=lambda: result.append(run_logged_command(command, log_path))
    )

    worker.start()
    visible_before_exit = False
    deadline = time.monotonic() + 0.5
    captured = ""
    while time.monotonic() < deadline and worker.is_alive():
        captured += capsys.readouterr().out
        if "iteration 1" in captured:
            visible_before_exit = True
            break
        time.sleep(0.01)
    worker.join(timeout=2)
    captured += capsys.readouterr().out

    assert not worker.is_alive()
    assert visible_before_exit
    assert len(result) == 1
    assert result[0].returncode == 7
    assert captured == "iteration 1\nlate stderr\n"
    assert log_path.read_bytes() == b"iteration 1\nlate stderr\n"
