'''
Tests for cleaner.py
'''
from unittest import TestCase
from unittest.mock import patch

from libs.kafka.logging import LogMessage
from libs.markdown.cleaner import remove_tabs_and_spaces_front, clear_yara_start_and_end


class CleanerTests(TestCase):
    '''
    Tests for the cleaner.
    '''

    def test_remove_tabs_and_spaces_front_throws_exception_when_given_None_as_parameter(self):
        '''
        Test to check if the function throws an exception,
        when None has been given as a parameter.
        '''
        with patch.object(LogMessage, "log", return_value="ERROR"):
            self.assertRaises(Exception, remove_tabs_and_spaces_front(None))

    def test_remove_tabs_and_spaces_front_returns_empty_list_when_given_empty_list_as_parameter(self):
        '''
        Test to check if the function returns an empty dict
        when an empty list has been given as a parameter.
        '''
        test_list = []

        output = remove_tabs_and_spaces_front(test_list)

        self.assertIsNotNone(output)
        self.assertIsInstance(output, list)
        self.assertTrue(len(output) == 0)

    def test_remove_tabs_and_spaces_front_throws_exception_when_given_None_as_list_element(self):
        '''
        Test to check if the function throws an exception,
        when None has been given as a list element.
        '''
        test_list = [None]

        with patch.object(LogMessage, "log", return_value="ERROR"):
            self.assertRaises(Exception, remove_tabs_and_spaces_front(test_list))

    def test_remove_tabs_and_spaces_front_returns_empty_string_when_given_empty_string_as_parameter(self):
        '''
        Test to check if the function returns an empty string
        when given an empty string as the parameter.
        '''
        test_list = [""]

        output = remove_tabs_and_spaces_front(test_list)

        self.assertIsNotNone(output)
        self.assertIsInstance(output, list)
        self.assertTrue(len(output) == 1)
        self.assertIsInstance(output[0], str)
        self.assertEqual(output[0], "")

    def test_remove_tabs_and_spaces_front_returns_empty_string_when_given_space_as_parameter(self):
        '''
        Test to check if the function returns an empty string
        when given a space as the parameter.
        '''
        test_list = [" "]

        output = remove_tabs_and_spaces_front(test_list)

        self.assertIsNotNone(output)
        self.assertIsInstance(output, list)
        self.assertTrue(len(output) == 1)
        self.assertIsInstance(output[0], str)
        self.assertEqual(output[0], "")

    def test_remove_tabs_and_spaces_front_returns_empty_string_when_given_tab_as_parameter(self):
        '''
        Test to check if the function returns an empty string
        when given a tab as the parameter.
        '''
        test_list = ["  "]

        output = remove_tabs_and_spaces_front(test_list)

        self.assertIsNotNone(output)
        self.assertIsInstance(output, list)
        self.assertTrue(len(output) == 1)
        self.assertIsInstance(output[0], str)
        self.assertEqual(output[0], "")

    def test_remove_tabs_and_spaces_front_returns_cleaned_string_when_given_uncleaned_input(self):
        '''
        Test to check if the function returns a string
        without tabs or spaces at the front and at the
        end, when given an uncleaned string as the parameter.
        '''
        test_list = ["  TEST     "]

        output = remove_tabs_and_spaces_front(test_list)

        self.assertIsNotNone(output)
        self.assertIsInstance(output, list)
        self.assertTrue(len(output) == 1)
        self.assertIsInstance(output[0], str)
        self.assertEqual(output[0], "TEST")

    def test_remove_tabs_and_spaces_front_returns_cleaned_string_with_space_in_the_middle_when_given_uncleaned_input(self):
        '''
        Test to check if the function returns a string
        without tabs or spaces at the front and at the
        end, but at the middle when given an uncleaned
        string as the parameter.
        '''
        test_list = ["  TE ST     "]

        output = remove_tabs_and_spaces_front(test_list)

        self.assertIsNotNone(output)
        self.assertIsInstance(output, list)
        self.assertTrue(len(output) == 1)
        self.assertIsInstance(output[0], str)
        self.assertEqual(output[0], "TE ST")

    def test_clear_yara_start_and_end_throws_exception_when_given_None_as_parameter(self):
        '''
        Test to check if the function throws an exception,
        when None has been given as a parameter.
        '''
        with patch.object(LogMessage, "log", return_value="ERROR"):
            self.assertRaises(Exception, clear_yara_start_and_end(None))

    def test_clear_yara_start_and_end_returns_empty_list_when_given_empty_list_as_parameter(self):
        '''
        Test to check if the function returns an empty dict
        when an empty list has been given as a parameter.
        '''
        test_list = []

        output = clear_yara_start_and_end(test_list)

        self.assertIsNotNone(output)
        self.assertIsInstance(output, list)
        self.assertTrue(len(output) == 0)

    def test_clear_yara_start_and_end_throws_exception_when_given_None_as_list_element(self):
        '''
        Test to check if the function throws an exception,
        when None has been given as a list element.
        '''
        test_list = [None]

        with patch.object(LogMessage, "log", return_value="ERROR"):
            self.assertRaises(Exception, clear_yara_start_and_end(test_list))

    def test_clear_yara_start_and_end_returns_empty_string_when_given_empty_string_as_parameter(self):
        '''
        Test to check if the function returns an empty string
        when given an empty string as the parameter.
        '''
        test_list = [""]

        output = clear_yara_start_and_end(test_list)

        self.assertIsNotNone(output)
        self.assertIsInstance(output, list)
        self.assertTrue(len(output) == 1)
        self.assertIsInstance(output[0], str)
        self.assertEqual(output[0], "")

    def test_clear_yara_start_and_end_returns_space_when_given_space_as_parameter(self):
        '''
        Test to check if the function returns a space
        when given a space as the parameter.
        '''
        test_list = [" "]

        output = clear_yara_start_and_end(test_list)

        self.assertIsNotNone(output)
        self.assertIsInstance(output, list)
        self.assertTrue(len(output) == 1)
        self.assertIsInstance(output[0], str)
        self.assertEqual(output[0], " ")

    def test_clear_yara_start_and_end_returns_empty_string_when_given_accent_aigu_as_parameter(self):
        '''
        Test to check if the function returns an empty string
        when given an accent aigu as the parameter.
        '''
        test_list = ["`"]

        output = clear_yara_start_and_end(test_list)

        self.assertIsNotNone(output)
        self.assertIsInstance(output, list)
        self.assertTrue(len(output) == 1)
        self.assertIsInstance(output[0], str)
        self.assertEqual(output[0], "")

    def test_clear_yara_start_and_end_returns_empty_string_when_given_php_as_parameter(self):
        '''
        Test to check if the function returns an empty string
        when given php as the parameter.
        '''
        test_list = ["php"]

        output = clear_yara_start_and_end(test_list)

        self.assertIsNotNone(output)
        self.assertIsInstance(output, list)
        self.assertTrue(len(output) == 1)
        self.assertIsInstance(output[0], str)
        self.assertEqual(output[0], "")