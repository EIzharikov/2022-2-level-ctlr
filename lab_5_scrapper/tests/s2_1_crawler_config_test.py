"""
Crawler configuration validation
"""

import json
import shutil
import unittest

import pytest

from config.test_params import TEST_CRAWLER_CONFIG_PATH, TEST_PATH
from core_utils.constants import (CRAWLER_CONFIG_PATH, TIMEOUT_LOWER_LIMIT,
                                  TIMEOUT_UPPER_LIMIT)
from lab_5_scrapper import scrapper
from lab_5_scrapper.scrapper import (IncorrectEncodingError,
                                     IncorrectHeadersError,
                                     IncorrectNumberOfArticlesError,
                                     IncorrectSeedURLError,
                                     IncorrectTimeoutError,
                                     IncorrectVerifyError,
                                     NumberOfArticlesOutOfRangeError)
from lab_5_scrapper.tests.config_generator import generate_config

print("Stage 1A: Validating Crawler Config")
print("Starting tests with received config")


class ExceptionIsNotRaised(Exception):
    """
    No exception was raised
    """


class ExtendedTestCase(unittest.TestCase):
    """
    Enable messaging when assertRaises is triggered
    """

    # pylint: disable=invalid-name
    def assertRaisesWithMessage(self, msg, exception, func, *args, **kwargs):
        """
        assertRaises method counterpart with enabled messaging
        """
        try:
            func(*args, **kwargs)
            print(msg)
            raise ExceptionIsNotRaised
        except ExceptionIsNotRaised:
            raise AssertionError(msg) from ExceptionIsNotRaised
        except Exception as inst:  # pylint: disable=broad-except
            self.assertEqual(type(inst), exception, msg)


# pylint: disable=too-many-instance-attributes
class CrawlerConfigCheck(ExtendedTestCase):
    """
    A class for Crawler configuration validation
    """

    def setUp(self) -> None:
        with CRAWLER_CONFIG_PATH.open() as file:
            self.reference = json.load(file)

        self.seed_urls_correct = ['https://sample.com/']
        self.num_articles_correct = 10
        self.headers_correct = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/97.0.4692.99 Safari/537.36 OPR/83.0.4254.70",
        }
        self.timeout_correct = 5
        self.encoding_correct = 'utf-8'
        self.should_verify_certificate = False
        self.headless_mode = False

        self.seed_urls_incorrect = ['https://sample.com/', True, 1, ['does_not_match_pattern']]
        self.num_articles_incorrect = [-5, False, {1: 2}]
        self.headers_incorrect = [True, 1, 'headers']
        self.timeout_incorrect = [
            'five secs',
            {False: 5},
            TIMEOUT_LOWER_LIMIT - 5,
            TIMEOUT_UPPER_LIMIT + 5
        ]
        self.encoding_incorrect = [5, False, [1, 2, 3]]
        self.verify_incorrect = ['verify', {1: 2}, (1, 2)]
        self.headless_incorrect = ['false', {1: 4}, (1, 2, 3)]

    @pytest.mark.mark4
    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_2_1_crawler_config_check
    @pytest.mark.lab_5_scrapper
    def test_incorrect_base_urls_config_param(self):
        """
        Checks that Config class returns error message and exit code 1 with incorrect config params
        """

        for incorrect_seed_urls in self.seed_urls_incorrect:
            generate_config(seed_urls=incorrect_seed_urls,
                            num_articles=self.num_articles_correct,
                            timeout=self.timeout_correct,
                            headers=self.headers_correct,
                            encoding=self.encoding_correct,
                            should_verify_certificate=self.should_verify_certificate,
                            headless_mode=self.headless_mode)

            error_message = """Checking that scrapper can handle incorrect seed_urls inputs.
    Seed URLs must be a list of strings, not a single string"""
            self.assertRaisesWithMessage(error_message,
                                         IncorrectSeedURLError,
                                         scrapper.Config,
                                         TEST_CRAWLER_CONFIG_PATH)

    @pytest.mark.mark4
    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_2_1_crawler_config_check
    @pytest.mark.lab_5_scrapper
    def test_incorrect_num_urls_config_param(self):
        """
        Checks that Config class returns error message and exit code 1 with incorrect config params
        """

        for incorrect_num_urls in self.num_articles_incorrect:
            generate_config(seed_urls=self.seed_urls_correct,
                            num_articles=incorrect_num_urls,
                            timeout=self.timeout_correct,
                            headers=self.headers_correct,
                            encoding=self.encoding_correct,
                            should_verify_certificate=self.should_verify_certificate,
                            headless_mode=self.headless_mode)

            error_message = """Checking that scrapper can handle incorrect num articles inputs.
    Num articles must be a positive integer."""
            self.assertRaisesWithMessage(error_message,
                                         IncorrectNumberOfArticlesError,
                                         scrapper.Config,
                                         TEST_CRAWLER_CONFIG_PATH)

    @pytest.mark.mark4
    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_2_1_crawler_config_check
    @pytest.mark.lab_5_scrapper
    def test_incorrect_num_urls_too_large_config_param(self):
        """
        Checks that Config class returns error message and exit code 1 with incorrect config params
        """

        generate_config(seed_urls=self.seed_urls_correct,
                        num_articles=1000000,
                        timeout=self.timeout_correct,
                        headers=self.headers_correct,
                        encoding=self.encoding_correct,
                        should_verify_certificate=self.should_verify_certificate,
                        headless_mode=self.headless_mode)

        error_message = """Checking that scrapper can handle incorrect num articles inputs.
Num articles must not be too large"""
        self.assertRaisesWithMessage(error_message,
                                     NumberOfArticlesOutOfRangeError,
                                     scrapper.Config,
                                     TEST_CRAWLER_CONFIG_PATH)

    @pytest.mark.mark4
    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_2_1_crawler_config_check
    @pytest.mark.lab_5_scrapper
    def test_incorrect_timeout_too_large_config_param(self):
        """
        Checks that Config class returns error message and exit code 1 with incorrect config params
        """

        for incorrect_timeout in self.timeout_incorrect:
            generate_config(seed_urls=self.seed_urls_correct,
                            num_articles=self.num_articles_correct,
                            timeout=incorrect_timeout,
                            headers=self.headers_correct,
                            encoding=self.encoding_correct,
                            should_verify_certificate=self.should_verify_certificate,
                            headless_mode=self.headless_mode)

            error_message = """Checking that scrapper can handle incorrect timeout inputs.
        Num articles must be an integer between 0 and 60. 0 is a valid value"""
            self.assertRaisesWithMessage(error_message,
                                         IncorrectTimeoutError,
                                         scrapper.Config,
                                         TEST_CRAWLER_CONFIG_PATH)

    @pytest.mark.mark4
    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_2_1_crawler_config_check
    @pytest.mark.lab_5_scrapper
    def test_incorrect_headers_config_param(self):
        """
        Checks that Config class returns error message and exit code 1 with incorrect config params
        """

        for incorrect_headers in self.headers_incorrect:
            generate_config(seed_urls=self.seed_urls_correct,
                            num_articles=self.num_articles_correct,
                            timeout=self.timeout_correct,
                            headers=incorrect_headers,
                            encoding=self.encoding_correct,
                            should_verify_certificate=self.should_verify_certificate,
                            headless_mode=self.headless_mode)

        error_message = """Checking that scrapper can handle incorrect headers.
Headers must be a dictionary with string keys and string values"""
        self.assertRaisesWithMessage(error_message,
                                     IncorrectHeadersError,
                                     scrapper.Config,
                                     TEST_CRAWLER_CONFIG_PATH)

    @pytest.mark.mark4
    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_2_1_crawler_config_check
    @pytest.mark.lab_5_scrapper
    def test_incorrect_encoding_config_param(self):
        """
        Checks that Config class returns error message and exit code 1 with incorrect config params
        """

        for incorrect_encoding in self.encoding_incorrect:
            generate_config(seed_urls=self.seed_urls_correct,
                            num_articles=self.num_articles_correct,
                            timeout=self.timeout_correct,
                            headers=self.headers_correct,
                            encoding=incorrect_encoding,
                            should_verify_certificate=self.should_verify_certificate,
                            headless_mode=self.headless_mode)

        error_message = """Checking that scrapper can handle incorrect encoding.
    Encoding must be a string"""
        self.assertRaisesWithMessage(error_message,
                                     IncorrectEncodingError,
                                     scrapper.Config,
                                     TEST_CRAWLER_CONFIG_PATH)

    @pytest.mark.mark4
    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_2_1_crawler_config_check
    @pytest.mark.lab_5_scrapper
    def test_incorrect_verify_cert_config_param(self):
        """
        Checks that Config class returns error message and exit code 1 with incorrect config params
        """

        for incorrect_verify in self.verify_incorrect:
            generate_config(seed_urls=self.seed_urls_correct,
                            num_articles=self.num_articles_correct,
                            timeout=self.timeout_correct,
                            headers=self.headers_correct,
                            encoding=self.encoding_correct,
                            should_verify_certificate=incorrect_verify,
                            headless_mode=self.headless_mode)

        error_message = """Checking that scrapper can handle incorrect verify certificate argument.
    Verify certificate must be either True or False"""
        self.assertRaisesWithMessage(error_message,
                                     IncorrectVerifyError,
                                     scrapper.Config,
                                     TEST_CRAWLER_CONFIG_PATH)

    @pytest.mark.mark4
    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_2_1_crawler_config_check
    @pytest.mark.lab_5_scrapper
    def test_incorrect_headless_config_param(self):
        """
        Checks that Config class returns error message and exit code 1 with incorrect config params
        """

        for incorrect_headless in self.headless_incorrect:
            generate_config(seed_urls=self.seed_urls_correct,
                            num_articles=self.num_articles_correct,
                            timeout=self.timeout_correct,
                            headers=self.headers_correct,
                            encoding=self.encoding_correct,
                            should_verify_certificate=self.should_verify_certificate,
                            headless_mode=incorrect_headless)

        error_message = """Checking that scrapper can handle headless mode argument.
    Headless mode must be either True or False"""
        self.assertRaisesWithMessage(error_message,
                                     IncorrectVerifyError,
                                     scrapper.Config,
                                     TEST_CRAWLER_CONFIG_PATH)

    @pytest.mark.mark4
    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_2_1_crawler_config_check
    @pytest.mark.lab_5_scrapper
    def test_config_initialization(self):
        """
        Checks that Config class returns error message and exit code 1 with incorrect config params
        """
        generate_config(
            seed_urls=self.seed_urls_correct,
            num_articles=self.num_articles_correct,
            timeout=self.timeout_correct,
            headers=self.headers_correct,
            encoding=self.encoding_correct,
            should_verify_certificate=self.should_verify_certificate,
            headless_mode=self.headless_mode
        )
        attr_names = ['path_to_config', '_seed_urls', '_num_articles', '_headers',
                      '_encoding', '_timeout', '_should_verify_certificate']
        config = scrapper.Config(TEST_CRAWLER_CONFIG_PATH)
        all_attrs = [hasattr(config, attr_name) for attr_name in attr_names]
        error_message = """Checking that scrapper saves relevant data to attributes."""
        self.assertTrue(all(all_attrs), msg=error_message)

    @pytest.mark.mark4
    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_2_1_crawler_config_check
    @pytest.mark.lab_5_scrapper
    def test_config_getters(self):
        """
        Checks that Config class returns error message and exit code 1 with incorrect config params
        """
        generate_config(
            seed_urls=self.seed_urls_correct,
            num_articles=self.num_articles_correct,
            timeout=self.timeout_correct,
            headers=self.headers_correct,
            encoding=self.encoding_correct,
            should_verify_certificate=self.should_verify_certificate,
            headless_mode=self.headless_mode
        )
        config = scrapper.Config(TEST_CRAWLER_CONFIG_PATH)
        getters = [config.get_seed_urls, config.get_num_articles,
                   config.get_headers, config.get_encoding,
                   config.get_timeout, config.get_verify_certificate,
                   config.get_headless_mode]
        values = [self.seed_urls_correct, self.num_articles_correct,
                  self.headers_correct, self.encoding_correct,
                  self.timeout_correct, self.should_verify_certificate,
                  self.headless_mode]
        self.assertTrue(all(method() == value for method, value in zip(getters, values)))

    def tearDown(self) -> None:
        if TEST_PATH.exists():
            shutil.rmtree(TEST_PATH)
