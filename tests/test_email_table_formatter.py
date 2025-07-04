# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring
from gmail_cli.email_table_formatter import EmailTableFormatter


class TestEmailTableFormatter:
    def test_format_sender(self):
        formatter = EmailTableFormatter()
        # pylint: disable=protected-access
        assert (
            formatter._format_sender("Test Sender <test@example.com>")
            == "Test Sender\n[dim]test@example.com[/dim]"
        )
        assert (
            formatter._format_sender("test@example.com") == "test@example.com"
        )
        assert formatter._format_sender("") == "Unknown"

    def test_format_subject(self):
        formatter = EmailTableFormatter()
        # pylint: disable=protected-access
        assert formatter._format_subject("Test Subject") == "Test Subject"
        assert formatter._format_subject("A" * 100) == "A" * 82 + "..."
        assert formatter._format_subject("") == "[dim](No subject)[/dim]"

    def test_format_date(self):
        formatter = EmailTableFormatter()
        assert (
            # pylint: disable=protected-access
            formatter._format_date("Mon, 1 Jan 2024 12:00:00 +0000")
            == "2024-01-01 12:00"
        )

    def test_format_date_invalid(self):
        formatter = EmailTableFormatter()
        assert (
            # pylint: disable=protected-access
            formatter._format_date("2025-01-01 12:00:05")
            == "2025-01-01 12:00:05"
        )

    def test_format_date_empty_string(self):
        formatter = EmailTableFormatter()
        # pylint: disable=protected-access
        assert formatter._format_date("") == ""
