"""
Main CLI entry point for Gmail CLI application.
"""

import sys
import click
from rich.console import Console
from rich.panel import Panel
from .gmail_client import GmailClient
from .table_formatter import EmailTableFormatter


@click.command()
@click.option(
    "--max-results",
    "-m",
    default=50,
    help="Maximum number of emails to retrieve (default: 50)",
)
@click.option(
    "--credentials",
    "-c",
    default="credentials.json",
    help="Path to OAuth credentials file (default: credentials.json)",
)
@click.option(
    "--token",
    "-t",
    default="token.json",
    help="Path to OAuth token file (default: token.json)",
)
@click.version_option(version="0.1.0", prog_name="gmail-cli")
def main(max_results: int, credentials: str, token: str):
    """
    Gmail CLI - List unread emails from your Gmail account.

    This tool requires Gmail API credentials.
    Follow the setup instructions in the README to
    configure OAuth 2.0 credentials.
    """
    console = Console()
    formatter = EmailTableFormatter()

    # Show welcome message
    console.print(
        Panel(
            "[bold cyan]Gmail CLI[/bold cyan]\n"
            "Access your unread Gmail messages from the command line",
            style="blue",
            border_style="blue",
        )
    )

    try:
        gmail_client = GmailClient(credentials, token)
        if not gmail_client.authenticate():
            formatter.show_error(
                "Authentication failed! Please check your credentials file."
            )
            sys.exit(1)

        formatter.show_success("Successfully authenticated with Gmail!")

        emails = gmail_client.get_unread_emails(max_results)
        formatter.display_emails(emails, max_results)
    except Exception as e:
        formatter.show_error(f"An unexpected error occurred: {str(e)}")
        console.print(f"\n[dim]Error details: {type(e).__name__}: {e}[/dim]")
        sys.exit(1)


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    main()
