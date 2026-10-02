"""Normalize local Python and temporary paths in published replay records."""
import re


def portable_command(command):
    """Replace the environment-specific Python executable with python3."""
    return ["python3", *command[1:]]


def sanitize_output(output):
    """Hide ephemeral macOS/Linux temporary paths from published logs."""
    output = re.sub(r"/private/var/folders/[^\s:]+", "<TEMP_PATH>", output)
    output = re.sub(r"(?<![\w])(?:/private)?/tmp/[^\s:]+", "<TEMP_PATH>", output)
    lines = output.splitlines()
    return "\n".join(line.rstrip() for line in lines) + ("\n" if output.endswith("\n") else "")
