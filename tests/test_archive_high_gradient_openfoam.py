import json
import tarfile

from tools.archive_high_gradient_openfoam import archive_completed


def test_archiver_keeps_only_complete_cases(tmp_path):
    work = tmp_path / "work"
    evidence = tmp_path / "evidence"
    work.mkdir()
    protocol = {
        "end_time": 0.05,
        "spatial_matrix": {"cell_counts": [16], "delta_t": 0.001},
        "temporal_matrix": {"cell_count": 32, "delta_t": [0.001]},
        "problem_reproduction_rule": {"required_fine_grid_counts": [16, 32]},
    }
    protocol_path = tmp_path / "protocol.json"
    protocol_path.write_text(json.dumps(protocol))
    (work / "run-environment.json").write_text(json.dumps({"source_commit": "fixture"}))

    complete = work / "n16-dt0.001"
    (complete / "0.05").mkdir(parents=True)
    for name in ("U", "p", "C", "phi"):
        (complete / "0.05" / name).write_text(name)
    (complete / "exit.json").write_text('{"exit_code":0}')
    (complete / "parameters.json").write_text("{}")
    (complete / "log.foamRun").write_text(
        "".join(f"Time = {i / 1000:g}s\nPIMPLE: Converged in 2 iterations\n" for i in range(1, 51))
        + "End\n"
    )
    diagnostics = {
        "parameters": {"n": 16, "dt": 0.001, "end": 0.05},
        "standard_acceptance": {"status": "PASS"},
        "local_quality": {"status": "FAIL"},
    }
    (complete / "diagnostics.json").write_text(json.dumps(diagnostics))

    partial = work / "n32-dt0.001"
    partial.mkdir()
    (partial / "log.foamRun").write_text("Time = 0.001s\n")

    manifest = archive_completed(work, evidence, protocol_path)

    assert manifest["matrix_status"] == "INCOMPLETE"
    assert manifest["problem_reproduction"]["status"] == "UNCERTAIN"
    assert [row["case"] for row in manifest["completed_cases"]] == ["n16-dt0.001"]
    assert [row["case"] for row in manifest["incomplete_cases"]] == ["n32-dt0.001"]
    with tarfile.open(evidence / "n16-dt0.001.tar.gz", "r:gz") as archive:
        assert "n16-dt0.001/0.05/U" in archive.getnames()
    assert not (evidence / "n32-dt0.001.tar.gz").exists()

    archive_hash = manifest["completed_cases"][0]["archive_sha256"]
    repeated = archive_completed(work, evidence, protocol_path)
    assert repeated["completed_cases"][0]["archive_sha256"] == archive_hash
