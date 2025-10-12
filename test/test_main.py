"""Tests for app.main module."""

from unittest import mock

import pytest

from app.__main__ import main, setup_parser


def test_main_pull():
    """Test main function."""
    with mock.patch("app.__main__.setup_parser") as m_parser, mock.patch("app.__main__.pull_all_workouts") as m_pull:
        m_parser.return_value = mock.Mock(command="pull", page_size=10)
        main()
        m_pull.assert_called_once_with(10)


def test_main_serve():
    """Test main function."""
    with mock.patch("app.__main__.setup_parser") as m_parser, mock.patch("app.__main__.uvicorn.run") as m_serve:
        m_parser.return_value = mock.Mock(command="serve", host="localhost", port=8000)
        main()
        m_serve.assert_called_once_with(mock.ANY, host="localhost", port=8000)


def test_main_unknown():
    """Test main function with unknown command."""
    with mock.patch("app.__main__.setup_parser") as m_parser, pytest.raises(SystemExit):
        m_parser.return_value = mock.Mock(command="unknown")
        main()


def test_setup_parser():
    """Test setup_parser function."""
    # push into the environment the args we want to test
    test_args = ["prog", "pull", "--page_size", "20"]
    with mock.patch("sys.argv", test_args):
        args = setup_parser()
        assert args.command == "pull"
        assert args.page_size == 20
