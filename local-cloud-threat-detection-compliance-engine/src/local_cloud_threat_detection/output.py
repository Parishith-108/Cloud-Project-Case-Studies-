import json
from pathlib import Path
from rich.console import Console
from rich.table import Table


console = Console()


def emit_findings(findings: list[dict], report_path: Path) -> None:
    table = Table(title="Local Cloud Threat Detection Findings")
    table.add_column("Resource Type", style="cyan")
    table.add_column("Resource ID", style="magenta")
    table.add_column("Issue", style="red")
    table.add_column("Suggested Fix", style="green")

    for finding in findings:
        table.add_row(
            finding.get("resource_type", "unknown"),
            finding.get("resource_id", "n/a"),
            finding.get("issue", "n/a"),
            finding.get("suggested_fix", "n/a"),
        )

    console.print(table)
    console.print(f"Saved compliance findings to: [bold]{report_path}[/bold]")

    report = {"findings": findings}
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
