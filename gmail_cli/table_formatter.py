"""
Table formatter for displaying Gmail emails in CLI.
"""

from typing import List, Dict
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from .gmail_client import GmailClient


class EmailTableFormatter:
    """Formatter for displaying emails in a rich CLI table."""

    def __init__(self):
        """Initialize the formatter with a console."""
        self.console = Console()

    def display_emails(
        self, emails: List[Dict], max_results: int = 50
    ) -> None:
        """
        Display emails in a formatted table.

        Args:
            emails: List of email dictionaries
            max_results: Maximum number of emails to display
        """
        if not emails:
            self.console.print(
                Panel(
                    "No unread emails found! 📭",
                    style="blue",
                    border_style="blue",
                )
            )
            return

        # Create the table
        table = Table(
            title="📧 Unread Gmail Messages",
            show_header=True,
            header_style="bold magenta",
            border_style="blue",
            title_style="bold cyan",
        )

        # Add columns
        table.add_column("From", style="cyan", width=30, no_wrap=True)
        table.add_column("Subject", style="white", width=50, no_wrap=False)
        table.add_column("Date", style="green", width=20, no_wrap=True)

        # Add rows
        gmail_client = GmailClient()

        for email in emails:
            from_text = self._format_sender(email.get("from", ""))
            subject_text = self._format_subject(email.get("subject", ""))
            date_text = gmail_client.format_date(email.get("date", ""))

            table.add_row(from_text, subject_text, date_text)
            # Don't add empty row after the last email
            if email != emails[-1]:
                table.add_row("", "", "")

        # Display the table
        self.console.print(table)

        # Show summary
        count = len(emails)
        if count < max_results:
            self.console.print(
                f"\n[bold green]Found {count} unread email(s)[/bold green]"
            )
        else:
            self.console.print(
                f"\n[bold green]Showing {count} unread email(s)[/bold green]"
            )

    def _format_sender(self, sender: str) -> str:
        """
        Format sender email for display.

        Args:
            sender: Raw sender string

        Returns:
            Formatted sender string
        """
        if not sender:
            return "Unknown"

        # Extract name from "Name <email@domain.com>" format
        if "<" in sender and ">" in sender:
            name = sender.split("<")[0].strip()
            email = sender.split("<")[1].split(">")[0].strip()
            if name:
                return f"{name}\n[dim]{email}[/dim]"
            return email

        return sender

    def _format_subject(self, subject: str) -> str:
        """
        Format subject line for display.

        Args:
            subject: Raw subject string

        Returns:
            Formatted subject string
        """
        if not subject:
            return "[dim](No subject)[/dim]"

        # Truncate long subjects
        if len(subject) > 85:
            return subject[:82] + "..."

        return subject

    def show_error(self, message: str) -> None:
        """
        Display an error message.

        Args:
            message: Error message to display
        """
        self.console.print(
            Panel(f"❌ {message}", style="red", border_style="red")
        )

    def show_success(self, message: str) -> None:
        """
        Display a success message.

        Args:
            message: Success message to display
        """
        self.console.print(
            Panel(f"✅ {message}", style="green", border_style="green")
        )

    def show_info(self, message: str) -> None:
        """
        Display an info message.

        Args:
            message: Info message to display
        """
        self.console.print(
            Panel(f"ℹ️  {message}", style="blue", border_style="blue")
        )
