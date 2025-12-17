"""Main CLI application.

Command-line interface for ununseptium library.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from ununseptium import __version__

console = Console()


@click.group()
@click.version_option(version=__version__, prog_name="ununseptium")
@click.option("--debug/--no-debug", default=False, help="Enable debug mode")
@click.pass_context
def cli(ctx: click.Context, debug: bool) -> None:
    """Ununseptium - RegTech & Cybersecurity Library.

    A comprehensive framework for KYC/AML automation, data security,
    and AI-powered risk assessment.
    """
    ctx.ensure_object(dict)
    ctx.obj["DEBUG"] = debug

    if debug:
        console.print("[yellow]Debug mode enabled[/yellow]")


@cli.command()
def info() -> None:
    """Display library information."""
    from ununseptium import __author__, __version__

    panel = Panel.fit(
        f"[bold blue]Ununseptium[/bold blue] v{__version__}\n"
        f"Author: {__author__}\n"
        f"Python: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        title="Library Info",
        border_style="blue",
    )
    console.print(panel)


@cli.group()
def verify() -> None:
    """Verification commands."""
    pass


@verify.command("identity")
@click.argument("data", type=click.Path(exists=True))
@click.option("--output", "-o", type=click.Path(), help="Output file for results")
def verify_identity(data: str, output: str | None) -> None:
    """Verify an identity from JSON file.

    DATA: Path to JSON file containing identity data.
    """
    from ununseptium.kyc import IdentityVerifier

    try:
        with Path(data).open() as f:
            identity_data = json.load(f)

        verifier = IdentityVerifier()
        result = verifier.verify(identity_data)

        table = Table(title="Verification Result")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="green")

        table.add_row("Status", result.status.value)
        table.add_row("Risk Level", result.risk_level.value)
        table.add_row("Score", f"{result.score:.2f}")
        table.add_row("Passed", str(result.passed))

        console.print(table)

        if output:
            with Path(output).open("w") as f:
                json.dump(result.model_dump(mode="json"), f, indent=2)
            console.print(f"[green]Results saved to {output}[/green]")

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise click.Abort from e


@cli.group()
def audit() -> None:
    """Audit log commands."""
    pass


@audit.command("verify")
@click.argument("logfile", type=click.Path(exists=True))
def audit_verify(logfile: str) -> None:
    """Verify audit log integrity.

    LOGFILE: Path to audit log file (JSON).
    """
    from ununseptium.security import AuditLog

    try:
        log = AuditLog.load(logfile)
        is_valid = log.verify()

        if is_valid:
            console.print(
                Panel(
                    f"[green]Audit log verified successfully[/green]\n"
                    f"Entries: {len(log)}",
                    title="Integrity Check",
                    border_style="green",
                )
            )
        else:
            console.print(
                Panel(
                    "[red]Audit log integrity check FAILED[/red]\n"
                    "Possible tampering detected!",
                    title="Integrity Check",
                    border_style="red",
                )
            )

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise click.Abort from e


@audit.command("show")
@click.argument("logfile", type=click.Path(exists=True))
@click.option("--limit", "-n", default=10, help="Number of entries to show")
def audit_show(logfile: str, limit: int) -> None:
    """Show audit log entries.

    LOGFILE: Path to audit log file.
    """
    from ununseptium.security import AuditLog

    try:
        log = AuditLog.load(logfile)
        entries = log.get_entries()[-limit:]

        table = Table(title=f"Audit Log ({len(entries)} of {len(log)} entries)")
        table.add_column("Timestamp", style="dim")
        table.add_column("Action", style="cyan")
        table.add_column("Actor", style="green")
        table.add_column("Resource", style="yellow")

        for entry in entries:
            table.add_row(
                entry.timestamp.isoformat(),
                entry.action,
                entry.actor or "-",
                entry.resource or "-",
            )

        console.print(table)

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise click.Abort from e


@cli.group()
def screen() -> None:
    """Screening commands."""
    pass


@screen.command("name")
@click.argument("name")
@click.option("--threshold", "-t", default=0.8, help="Match threshold")
def screen_name(name: str, threshold: float) -> None:
    """Screen a name against watchlists.

    NAME: Name to screen.
    """
    from ununseptium.kyc import ScreeningEngine

    try:
        engine = ScreeningEngine()
        result = engine.screen(name)

        if result.matches:
            table = Table(title=f"Screening Results for '{name}'")
            table.add_column("Matched Name", style="red")
            table.add_column("Score", style="yellow")
            table.add_column("List Type", style="cyan")

            for match in result.matches:
                if match.score >= threshold:
                    table.add_row(
                        match.matched_name,
                        f"{match.score:.2%}",
                        match.watchlist_type.value,
                    )

            console.print(table)
        else:
            console.print(f"[green]No matches found for '{name}'[/green]")

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise click.Abort from e


@cli.group()
def model() -> None:
    """Model management commands."""
    pass


@model.command("list")
def model_list() -> None:
    """List registered models."""
    from ununseptium.ai import ModelRegistry

    registry = ModelRegistry()

    # Note: In real usage, would load from persistent storage
    console.print("[yellow]No models registered (registry is empty)[/yellow]")
    console.print("Use 'ununseptium model register' to add models.")


@model.command("validate")
@click.argument("model_card", type=click.Path(exists=True))
def model_validate(model_card: str) -> None:
    """Validate a model card.

    MODEL_CARD: Path to model card JSON.
    """
    from ununseptium.ai import ModelCard, ModelValidator

    try:
        with Path(model_card).open() as f:
            card_data = json.load(f)

        card = ModelCard.model_validate(card_data)
        validator = ModelValidator()
        result = validator.validate(card)

        if result.status.value == "passed":
            console.print(Panel(
                f"[green]Model validation passed[/green]\n{result.message}",
                title="Validation Result",
                border_style="green",
            ))
        else:
            console.print(Panel(
                f"[red]Model validation failed[/red]\n{result.message}",
                title="Validation Result",
                border_style="red",
            ))

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise click.Abort from e


@cli.command()
def doctor() -> None:
    """Run diagnostics to check library health."""
    console.print(Panel("[bold]Running Ununseptium Diagnostics[/bold]", border_style="blue"))

    checks: list[tuple[str, bool, str]] = []

    # Check imports
    try:
        import ununseptium

        checks.append(("Library import", True, f"v{ununseptium.__version__}"))
    except ImportError as e:
        checks.append(("Library import", False, str(e)))

    # Check core module
    try:
        from ununseptium.core import Settings  # noqa: F401

        checks.append(("Core module", True, "OK"))
    except ImportError as e:
        checks.append(("Core module", False, str(e)))

    # Check KYC module
    try:
        from ununseptium.kyc import IdentityVerifier  # noqa: F401

        checks.append(("KYC module", True, "OK"))
    except ImportError as e:
        checks.append(("KYC module", False, str(e)))

    # Check AML module
    try:
        from ununseptium.aml import TransactionParser  # noqa: F401

        checks.append(("AML module", True, "OK"))
    except ImportError as e:
        checks.append(("AML module", False, str(e)))

    # Check Security module
    try:
        from ununseptium.security import PIIDetector  # noqa: F401

        checks.append(("Security module", True, "OK"))
    except ImportError as e:
        checks.append(("Security module", False, str(e)))

    # Check AI module
    try:
        from ununseptium.ai import RiskScorer  # noqa: F401

        checks.append(("AI module", True, "OK"))
    except ImportError as e:
        checks.append(("AI module", False, str(e)))

    # Check dependencies
    try:
        import pydantic

        checks.append(("Pydantic", True, f"v{pydantic.__version__}"))
    except ImportError:
        checks.append(("Pydantic", False, "Not installed"))

    try:
        import numpy

        checks.append(("NumPy", True, f"v{numpy.__version__}"))
    except ImportError:
        checks.append(("NumPy", False, "Not installed"))

    # Display results
    table = Table(title="Diagnostic Results")
    table.add_column("Check", style="cyan")
    table.add_column("Status", style="bold")
    table.add_column("Details", style="dim")

    all_passed = True
    for check_name, passed, details in checks:
        status = "[green]PASS[/green]" if passed else "[red]FAIL[/red]"
        if not passed:
            all_passed = False
        table.add_row(check_name, status, details)

    console.print(table)

    if all_passed:
        console.print("\n[green]All checks passed! Library is healthy.[/green]")
    else:
        console.print("\n[red]Some checks failed. Please review the issues above.[/red]")


# Alias for entry point
app = cli


def main() -> None:
    """Main entry point."""
    cli()


if __name__ == "__main__":
    main()
