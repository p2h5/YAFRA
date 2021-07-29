'''
Tests for commit.py
'''
from unittest import TestCase
from unittest.mock import patch, Mock, MagicMock

from gitlab import Gitlab
from gitlab.v4.objects import ProjectCommitManager

from libs.gitlabl.commit import get_latest_commit_hash_by_branch
from libs.kafka.logging import LogMessage


class CommitTests(TestCase):
    '''
    Tests for commit.
    '''

    # TODO add tests for get_filename_since_last_timestamp after refactoring.

    def test_get_latest_commit_hash_by_branch_throws_exception_when_gitlab_server_is_None(self):
        '''
        Test to check if the function throws an exception,
        when None has been given as the gitlab server parameter.
        '''

        with patch.object(LogMessage, "log", return_value="ERROR"):
            self.assertRaises(Exception, get_latest_commit_hash_by_branch(None, "TEST_TOKEN", "TEST_REPOSITORY", "TEST_BRANCH", "TEST_SERVICENAME"))

    def test_get_latest_commit_hash_by_branch_throws_exception_when_gitlab_token_is_None(self):
        '''
        Test to check if the function throws an exception,
        when None has been given as the gitlab token parameter.
        '''

        with patch.object(LogMessage, "log", return_value="ERROR"):
            self.assertRaises(Exception, get_latest_commit_hash_by_branch("TEST_SERVER", None, "TEST_REPOSITORY", "TEST_BRANCH", "TEST_SERVICENAME"))

    def test_get_latest_commit_hash_by_branch_throws_exception_when_gitlab_repository_is_None(self):
        '''
        Test to check if the function throws an exception,
        when None has been given as the gitlab repository parameter.
        '''
        with patch.object(LogMessage, "log", return_value="ERROR"):
            self.assertRaises(Exception, get_latest_commit_hash_by_branch("TEST_SERVER", "TEST_TOKEN", None, "TEST_BRANCH", "TEST_SERVICENAME"))

    def test_get_latest_commit_hash_by_branch_throws_exception_when_gitlab_branch_is_None(self):
        '''
        Test to check if the function throws an exception,
        when None has been given as the gitlab branch parameter.
        '''
        with patch.object(LogMessage, "log", return_value="ERROR"):
            self.assertRaises(Exception, get_latest_commit_hash_by_branch("TEST_SERVER", "TEST_TOKEN", "TEST_REPOSITORY", None, "TEST_SERVICENAME"))

    def test_get_latest_commit_hash_by_branch_throws_exception_when_project_id_is_None(self):
        '''
        Test to check if the function throws an exception,
        when None has been returned as the project id.
        '''
        with patch.object(LogMessage, "log", return_value="ERROR"), patch('libs.gitlabl.commit.get_projectid_by_name') as mock_get_projectid_by_name:
            mock_get_projectid_by_name.return_value = None
            self.assertRaises(Exception, get_latest_commit_hash_by_branch("TEST_SERVER", "TEST_TOKEN", "TEST_REPOSITORY", "TEST_BRANCH", "TEST_SERVICENAME"))

    def test_get_latest_commit_hash_by_branch_throws_exception_when_gitlab_projects_is_None(self):
        '''
        Test to check if the function throws an exception,
        when None has been returned as the gitlab projects.
        '''
        with patch.object(LogMessage, "log", return_value="ERROR"), patch('libs.gitlabl.commit.get_projectid_by_name') as mock_get_projectid_by_name, patch.object(Gitlab, "http_get") as mock_gitlab_projects:
            mock_get_projectid_by_name.return_value = 1
            mock_gitlab_projects.return_value = None
            self.assertRaises(Exception, get_latest_commit_hash_by_branch("TEST_SERVER", "TEST_TOKEN", "TEST_REPOSITORY", "TEST_BRANCH", "TEST_SERVICENAME"))

    def test_get_latest_commit_hash_by_branch_throws_exception_when_gitlab_commits_is_None(self):
        '''
        Test to check if the function throws an exception,
        when None has been returned as the gitlab commits.
        '''
        with patch.object(LogMessage, "log", return_value="ERROR"), patch('libs.gitlabl.commit.get_projectid_by_name') as mock_get_projectid_by_name, patch.object(Gitlab, "http_get") as mock_gitlab_projects, patch.object(ProjectCommitManager, "list") as mock_gitlab_commits:
            mock_get_projectid_by_name.return_value = 1
            gitlab_projects_mock = MagicMock()
            mock_gitlab_projects.return_value = gitlab_projects_mock
            mock_gitlab_commits.return_value = None
            self.assertRaises(Exception, get_latest_commit_hash_by_branch("TEST_SERVER", "TEST_TOKEN", "TEST_REPOSITORY", "TEST_BRANCH", "TEST_SERVICENAME"))

    def test_get_latest_commit_hash_by_branch_throws_exception_when_gitlab_commits_is_empty(self):
        '''
        Test to check if the function throws an exception,
        when the returned gitlab commits list is empty.
        '''
        with patch.object(LogMessage, "log", return_value="ERROR"), patch('libs.gitlabl.commit.get_projectid_by_name') as mock_get_projectid_by_name, patch.object(Gitlab, "http_get") as mock_gitlab_projects, patch.object(ProjectCommitManager, "list") as mock_gitlab_commits:
            mock_get_projectid_by_name.return_value = 1
            gitlab_projects_mock = MagicMock()
            mock_gitlab_projects.return_value = gitlab_projects_mock
            mock_gitlab_commits.return_value = []
            self.assertRaises(Exception, get_latest_commit_hash_by_branch("TEST_SERVER", "TEST_TOKEN", "TEST_REPOSITORY", "TEST_BRANCH", "TEST_SERVICENAME"))

    def test_get_latest_commit_hash_by_branch_returns_valid_commit_hash_when_given_valid_parameters(self):
        '''
        Test to check if the function returns a valid
        hash from the commit, when given valid parameters.
        '''
        with patch('libs.gitlabl.commit.get_projectid_by_name') as mock_get_projectid_by_name, patch.object(Gitlab, "http_get") as mock_gitlab_projects, patch.object(ProjectCommitManager, "list") as mock_gitlab_commits:
            mock_get_projectid_by_name.return_value = 1
            gitlab_projects_mock = MagicMock()
            mock_gitlab_projects.return_value = gitlab_projects_mock
            gitlab_commit_mock = Mock()
            gitlab_commit_mock_id = str(gitlab_commit_mock.id)
            mock_gitlab_commits.return_value = [gitlab_commit_mock]
            output = get_latest_commit_hash_by_branch("TEST_SERVER", "TEST_TOKEN", "TEST_REPOSITORY", "TEST_BRANCH", "TEST_SERVICENAME")

            self.assertIsNotNone(output)
            self.assertIsInstance(output, str)
            self.assertEqual(output, gitlab_commit_mock_id)