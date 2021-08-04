'''
Tests for files.py
'''
import base64
import json
from unittest import TestCase
from unittest.mock import patch, Mock, MagicMock

from gitlab import Gitlab
from gitlab.v4.objects import ProjectCommitManager, ProjectFile

from libs.core.get_path import get_path
from libs.gitlabl.files import read_file_from_gitlab
from libs.kafka.logging import LogMessage


class FilesTests(TestCase):
    '''
    Tests for files.
    '''

    def test_read_file_from_gitlab_throws_exception_when_gitlab_server_is_None(self):
        '''
        Test to check if the function throws an exception,
        when None has been given as the gitlab server parameter.
        '''

        with patch.object(LogMessage, "log", return_value="ERROR"):
            self.assertRaises(Exception, read_file_from_gitlab(None, "TEST_TOKEN", "TEST_FILE", "TEST_SERVICENAME", "TEST_BRANCHNAME"))

    def test_read_file_from_gitlab_throws_exception_when_gitlab_token_is_None(self):
        '''
        Test to check if the function throws an exception,
        when None has been given as the gitlab token parameter.
        '''

        with patch.object(LogMessage, "log", return_value="ERROR"):
            self.assertRaises(Exception, read_file_from_gitlab("TEST_SERVER", None, "TEST_FILE", "TEST_SERVICENAME", "TEST_BRANCHNAME"))

    def test_read_file_from_gitlab_throws_exception_when_gitlab_repository_is_None(self):
        '''
        Test to check if the function throws an exception,
        when None has been given as the gitlab repository parameter.
        '''
        with patch.object(LogMessage, "log", return_value="ERROR"):
            self.assertRaises(Exception, read_file_from_gitlab("TEST_SERVER", "TEST_TOKEN", None, "TEST_FILE", "TEST_SERVICENAME", "TEST_BRANCHNAME"))

    def test_read_file_from_gitlab_throws_exception_when_file_is_None(self):
        '''
        Test to check if the function throws an exception,
        when None has been given as the file parameter.
        '''
        with patch.object(LogMessage, "log", return_value="ERROR"):
            self.assertRaises(Exception, read_file_from_gitlab("TEST_SERVER", "TEST_TOKEN", "TEST_REPOSITORY", None, "TEST_SERVICENAME", "TEST_BRANCHNAME"))

    def test_read_file_from_gitlab_throws_exception_when_branchname_is_None(self):
        '''
        Test to check, if the function throws an exception,
        when None has been given as the file parameter.
        '''
        with patch.object(LogMessage, "log", return_value="ERROR"):
            self.assertRaises(Exception, read_file_from_gitlab("TEST_SERVER", "TEST_TOKEN", "TEST_REPOSITORY", "TEST_FILE", "TEST_SERVICENAME", None))

    def test_read_file_from_gitlab_gets_branchname_when_no_branchname_given_as_a_parameter(self):
        '''
        Test to check, if the function gets a
        brnachname, when no branchname is given
        as a parameter.
        '''
        with patch.object(LogMessage, "log", return_value="ERROR"), patch('libs.gitlabl.files.get_branch_name') as mock_branchname:
            mock_branchname.return_value = "TEST_BRANCHNAME"
            read_file_from_gitlab("TEST_SERVER", "TEST_TOKEN", "TEST_REPOSITORY", "TEST_FILE", "TEST_SERVICENAME", "")
            mock_branchname.assert_called_once()

    def test_read_file_from_gitlab_gets_branchname_when_no_branchname_given_as_a_parameter_(self):
        '''
        Test to check, if the function gets a
        brnachname, when no branchname is given
        as a parameter.
        '''
        with patch('libs.gitlabl.files.get_project_handle') as service_mock:
            # service_mock.return_value.files.return_value.get.return_value.decode.return_value.decode.return_value = "FOO"
            service_mock.files.get.decode.return_value = "FOO"
            output = read_file_from_gitlab("TEST_SERVER", "TEST_TOKEN", "TEST_REPOSITORY", "test.json", "TEST_SERVICENAME","TEST_BRANCHNAME")
            print(output)
            print(type(output))

        # path = get_path(__file__, 'resources/test.json')
        #
        # with open(str(path)) as test_json_file:
        #     test_text = json.load(test_json_file)
        #     test_text = json.dumps(test_text)
        #     with patch('libs.gitlabl.files.get_project_handle') as mock_gitlab_projects, patch.object(ProjectFile, "decode") as mock_gitlab_decode:
        #         gitlab_projects_mock = Mock(return_value="FOO")
        #         mock_gitlab_projects.return_value = gitlab_projects_mock
        #         mock_gitlab_projects.decode = Mock(return_value="BAR")
        #         gitlab_commit_mock = Mock()
        #         mock_gitlab_decode.return_value = "gitlab_commit_mock"
        #         # gitlab_projects_mock = MagicMock()
        #         # gitlab_projects_mock.files.get = Mock(return_value=ProjectFile("manager", "attrs"))
        #         # mock_gitlab_projects.return_value = gitlab_projects_mock
        #         read_file_from_gitlab("TEST_SERVER", "TEST_TOKEN", "TEST_REPOSITORY", "test.json", "TEST_SERVICENAME", "TEST_BRANCHNAME")


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