from tools.replay_sanitizer import portable_command, sanitize_output


def test_portable_command_hides_environment_specific_python_path():
    assert portable_command(["/tmp/venv/bin/python", "-m", "tools.check"]) == [
        "python3", "-m", "tools.check",
    ]


def test_sanitize_output_replaces_only_ephemeral_temp_roots():
    output = (
        "/private/var/folders/ab/tmp123/result.tar.zst: 12 bytes\n"
        "/tmp/replay-xyz/log.json\n"
        "evidence/of13/case.tar.gz\n"
        "trailing-space  \n"
    )
    assert sanitize_output(output) == (
        "<TEMP_PATH>: 12 bytes\n<TEMP_PATH>\n"
        "evidence/of13/case.tar.gz\ntrailing-space\n"
    )
