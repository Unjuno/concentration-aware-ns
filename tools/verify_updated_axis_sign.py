"""Check extension compatibility in the separately prepared updated source volume."""
from tools.verify_axis_sign import verify


if __name__ == '__main__':
    raise SystemExit(0 if verify(
        runner_path='runtime/lean-verification/check_updated_axis_sign.sh',
        output_stem='evidence/upstream-refresh/updated-axis-force-sign',
        replay='python3 -m tools.verify_updated_axis_sign',
    ) else 1)
