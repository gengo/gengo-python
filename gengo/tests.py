# -*- coding: utf-8 -*-
# All code provided from the http://gengo.com site, such as API example code
# and libraries, is provided under the New BSD license unless otherwise
# noted. Details are below.
#
# New BSD License
# Copyright (c) 2009-2015, Gengo, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
# Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
# Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
# Neither the name of Gengo, Inc. nor the names of its contributors may
# be used to endorse or promote products derived from this software
# without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
# IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
A set of tests for the Gengo API. They all require an internet connection.
"""

import unittest
try:
    import mock
except ImportError:
    import unittest.mock as mock

import mockdb
from gengo import Gengo, GengoError, GengoAuthError

API_PUBKEY = 'dummypublickey'
API_PRIVKEY = 'dummyprivatekey'


class TestGengoCore(unittest.TestCase):

    """
    Handles testing the core parts of Gengo (i.e, authentication
    signing, etc).
    """
    def test_MethodDoesNotExist(self):
        gengo = Gengo(public_key=API_PUBKEY,
                      private_key=API_PRIVKEY,
                      sandbox=True)
        # With how we do functions, AttributeError is a bit tricky to
        # catch...
        self.assertRaises(AttributeError, getattr, gengo, 'bert')

    def test_GengoAuthNoCredentials(self):
        gengo = Gengo(public_key='',
                      private_key='')
        self.assertRaises(GengoError, gengo.getAccountStats)

    def test_GengoAuthBadCredentials(self):
        gengo = Gengo(public_key='bert',
                      private_key='beeeerrrttttt')
        self.assertRaises(GengoAuthError, gengo.getAccountStats)


class TestAccountMethods(unittest.TestCase):

    """
    Tests the methods that deal with retrieving basic information about
    the account you're authenticating as. Checks for one property on
    each method.
    """
    def setUp(self):
        self.gengo = Gengo(public_key=API_PUBKEY,
                           private_key=API_PRIVKEY,
                           sandbox=True)

        from gengo import requests
        self.json_mock = mock.Mock()
        self.json_mock.json.return_value = {'opstat': 'ok'}
        self.getMock = RequestsMock(return_value=self.json_mock)
        self.requestsPatch = mock.patch.object(requests, 'get', self.getMock)
        self.requestsPatch.start()

    def tearDown(self):
        self.requestsPatch.stop()

    def test_getAccountStats(self):
        stats = self.gengo.getAccountStats()
        self.assertEqual(stats['opstat'], 'ok')
        self.getMock.assert_path_contains(
            mockdb.apihash['getAccountStats']['url'])

    def test_getAccountBalance(self):
        balance = self.gengo.getAccountBalance()
        self.assertEqual(balance['opstat'], 'ok')
        self.getMock.assert_path_contains(
            mockdb.apihash['getAccountBalance']['url'])


class TestLanguageServiceMethods(unittest.TestCase):

    """
    Tests the methods that deal with getting information about language-
    translation service support from Gengo.
    """
    def setUp(self):
        self.gengo = Gengo(public_key=API_PUBKEY,
                           private_key=API_PRIVKEY,
                           sandbox=True)

        from gengo import requests
        self.json_mock = mock.Mock()
        self.json_mock.json.return_value = {'opstat': 'ok'}
        self.getMock = RequestsMock(return_value=self.json_mock)
        self.requestsPatch = mock.patch.object(requests, 'get', self.getMock)
        self.requestsPatch.start()

    def tearDown(self):
        self.requestsPatch.stop()

    def test_getServiceLanguagePairs(self):
        resp = self.gengo.getServiceLanguagePairs()
        self.assertEqual(resp['opstat'], 'ok')
        self.getMock.assert_path_contains(
            mockdb.apihash['getServiceLanguagePairs']['url'])

    def test_getServiceLanguages(self):
        resp = self.gengo.getServiceLanguages()
        self.assertEqual(resp['opstat'], 'ok')
        self.getMock.assert_path_contains(
            mockdb.apihash['getServiceLanguages']['url'])

    def test_getServiceLanguageMatrix(self):
        resp = self.gengo.getServiceLanguageMatrix()
        self.assertEqual(resp['opstat'], 'ok')
        self.getMock.assert_path_contains(
            mockdb.apihash['getServiceLanguageMatrix']['url'])


class TestPostTranslationJobComment(unittest.TestCase):

    """
    Tests the flow of creating a job, updating one of them, getting the
    details, and then deleting the jobs.
    """
    def setUp(self):
        """
        Creates the initial batch of jobs for the other test functions here
        to operate on.
        """
        self.gengo = Gengo(public_key=API_PUBKEY,
                           private_key=API_PRIVKEY,
                           sandbox=True)

        from gengo import requests
        self.json_mock = mock.Mock()
        self.json_mock.json.return_value = {'opstat': 'ok'}
        self.getMock = RequestsMock(return_value=self.json_mock)
        self.requestsPatch = mock.patch.object(requests, 'post', self.getMock)
        self.requestsPatch.start()

    def tearDown(self):
        self.requestsPatch.stop()

    def test_postJobComment(self):
        """
        Tests posting a comment to a job.
        """
        posted_comment = self.gengo.postTranslationJobComment(
            id=123,
            comment={'body': 'I love lamp oh mai gawd'})
        self.assertEqual(posted_comment['opstat'], 'ok')
        self.getMock.assert_path_contains(
            mockdb.apihash['postTranslationJobComment']['url']
            .replace('{{id}}', '123'))


class TestPostTranslationJobCommentWithAttachments(unittest.TestCase):

    """
    Tests the flow of creating a job, updating one of them, getting the
    details, and then deleting the jobs.
    """
    def setUp(self):
        """
        Creates the initial batch of jobs for the other test functions here
        to operate on.
        """
        self.gengo = Gengo(public_key=API_PUBKEY,
                           private_key=API_PRIVKEY,
                           sandbox=True)

        from gengo import requests
        self.json_mock = mock.Mock()
        self.json_mock.json.return_value = {'opstat': 'ok'}
        self.getMock = RequestsMock(return_value=self.json_mock)
        self.requestsPatch = mock.patch.object(requests, 'post', self.getMock)
        self.requestsPatch.start()

    def tearDown(self):
        self.requestsPatch.stop()

    def test_postJobCommentWithAttachments(self):
        """
        Tests posting a comment with attachments to a job.
        """
        posted_comment = self.gengo.postTranslationJobComment(
            id=123,
            comment={
                'body': 'I love lamp oh mai gawd'
            },
            file_attachments=[
                './examples/testfiles/test_file1.txt',
                './examples/testfiles/test_file2.txt'
            ]
        )
        self.assertEqual(posted_comment['opstat'], 'ok')
        self.getMock.assert_path_contains(
            mockdb.apihash['postTranslationJobComment']['url']
            .replace('{{id}}', '123'))


class TestTranslationJobFlowFileUpload(unittest.TestCase):

    """
    Tests the flow of creating a job, updating one of them, getting the
    details, and then deleting the jobs.
    """
    def setUp(self):
        """
        Creates the initial batch of jobs for the other test functions here
        to operate on.
        """
        self.gengo = Gengo(public_key=API_PUBKEY,
                           private_key=API_PRIVKEY,
                           sandbox=True)

        from gengo import requests
        self.json_mock = mock.Mock()
        self.json_mock.json.return_value = {'opstat': 'ok'}
        self.getMock = RequestsMock(return_value=self.json_mock)
        self.requestsPatch = mock.patch.object(requests, 'get', self.getMock)
        self.requestsPatch.start()

    def tearDown(self):
        self.requestsPatch.stop()

    def test_getJobDataMethods(self):
        """
        Test a ton of methods that GET data from the Gengo API, based on
        the jobs we've created and such.

        These are separate from the other GET request methods because this
        might be a huge nuisance to their API,
        and I figure it's worth separating out the pain-point test cases so
        they could be disabled easily in a
        distribution or something.
        """
        # Pull down data about one specific job.
        job = self.gengo.getTranslationJob(id=123)
        self.assertEqual(job['opstat'], 'ok')
        self.getMock.assert_path_contains(
            mockdb.apihash['getTranslationJob']['url']
            .replace('{{id}}', '123'))

        # Pull down the 10 most recently submitted jobs.
        jobs = self.gengo.getTranslationJobs()
        self.assertEqual(jobs['opstat'], 'ok')
        self.getMock.assert_path_contains(
            mockdb.apihash['getTranslationJobs']['url'])

        # Test getting the batch that a job is in.
        job_batch = self.gengo.getTranslationJobBatch(id=123)
        self.assertEqual(job_batch['opstat'], 'ok')
        self.getMock.assert_path_contains(
            mockdb.apihash['getTranslationJobBatch']['url']
            .replace('{{id}}', '123'))

        # Pull down feedback. This should work fine, but there'll be no
        # feedback.
        feedback = self.gengo.getTranslationJobFeedback(id=123)
        self.assertEqual(feedback['opstat'], 'ok')
        self.getMock.assert_path_contains(
            mockdb.apihash['getTranslationJobFeedback']['url']
            .replace('{{id}}', '123'))

        # Lastly, pull down any revisions that definitely didn't occur due
        # to this being a simulated test.
        revisions = self.gengo.getTranslationJobRevisions(id=123)
        self.assertEqual(revisions['opstat'], 'ok')
        self.getMock.assert_path_contains(
            mockdb.apihash['getTranslationJobRevisions']['url']
            .replace('{{id}}', '123'))


class TestTranslationJobFlowGroupJob(unittest.TestCase):

    """
    Tests the flow of creating a job, updating one of them, getting the
    details, and then deleting the jobs.
    """
    def setUp(self):
        """
        Creates the initial batch of jobs for the other test functions here
        to operate on.
        """
        """
        Creates the initial batch of jobs for the other test functions here
        to operate on.
        """
        self.gengo = Gengo(public_key=API_PUBKEY,
                           private_key=API_PRIVKEY,
                           sandbox=True)
        self.created_job_ids = []

        from gengo import requests
        self.json_mock = mock.Mock()
        self.json_mock.json.return_value = {'opstat': 'ok'}
        self.getMock = RequestsMock(return_value=self.json_mock)
        self.requestsPatch = mock.patch.object(requests, 'get', self.getMock)
        self.requestsPatch.start()

    def tearDown(self):
        self.requestsPatch.stop()

    def test_postTranslationJobs_as_group(self):
        """
        Make sure that the as_group setting gets interpreted by the API
        correctly.
        """
        resp = self.gengo.getTranslationOrderJobs(id=321)
        self.assertEqual(resp['opstat'], 'ok')
        self.getMock.assert_path_contains(
            mockdb.apihash['getTranslationOrderJobs']['url']
            .replace('{{id}}', '321'))


class TestTranslationJobFlowMixedOrder(unittest.TestCase):

    """
    Tests the flow of creating a file job and a text job, updating one of them,
    getting the details, and then deleting the job.
    """
    def setUp(self):
        """
        Creates the initial batch of jobs for the other test functions here
        to operate on.
        """
        # First we'll create three jobs - one regular, and two at the same
        # time...
        self.gengo = Gengo(public_key=API_PUBKEY,
                           private_key=API_PRIVKEY,
                           sandbox=True)

        from gengo import requests
        self.json_mock = mock.Mock()
        self.json_mock.json.return_value = {'opstat': 'ok'}
        self.getMock = RequestsMock(return_value=self.json_mock)
        self.requestsPatch = mock.patch.object(requests, 'get', self.getMock)
        self.requestsPatch.start()

    def tearDown(self):
        self.requestsPatch.stop()

    def test_postJobComment(self):
        """
        Tests posting a comment to a job.
        """
        job_comments = self.gengo.getTranslationJobComments(id=1)
        self.assertEqual(job_comments['opstat'], 'ok')
        self.getMock.assert_path_contains(
            mockdb.apihash['getTranslationJobComments']['url']
            .replace('{{id}}', '1'))

    def test_getJobDataMethods(self):
        """
        Test a ton of methods that GET data from the Gengo API, based on
        the jobs we've created and such.

        These are separate from the other GET request methods because this
        might be a huge nuisance to their API,
        and I figure it's worth separating out the pain-point test cases so
        they could be disabled easily in a
        distribution or something.
        """
        # Pull down data about one specific job...
        job = self.gengo.getTranslationJob(id=1)
        self.assertEqual(job['opstat'], 'ok')
        self.getMock.assert_path_contains(
            mockdb.apihash['getTranslationJob']['url']
            .replace('{{id}}', '1'))

        # Pull down the 10 most recently submitted jobs.
        jobs = self.gengo.getTranslationJobs()
        self.assertEqual(jobs['opstat'], 'ok')
        self.getMock.assert_path_contains(
            mockdb.apihash['getTranslationJobs']['url'])

        # Test getting the batch that a job is in...
        job_batch = self.gengo.getTranslationJobBatch(id=1)
        self.assertEqual(job_batch['opstat'], 'ok')
        self.getMock.assert_path_contains(
            mockdb.apihash['getTranslationJobBatch']['url']
            .replace('{{id}}', '1'))

        # Pull down feedback. This should work fine, but there'll be no
        # feedback.
        feedback = self.gengo.getTranslationJobFeedback(id=1)
        self.assertEqual(feedback['opstat'], 'ok')
        self.getMock.assert_path_contains(
            mockdb.apihash['getTranslationJobFeedback']['url']
            .replace('{{id}}', '1'))

        # Lastly, pull down any revisions that definitely didn't occur due
        # to this being a simulated test.
        revisions = self.gengo.getTranslationJobRevisions(id=1)
        self.assertEqual(revisions['opstat'], 'ok')
        self.getMock.assert_path_contains(
            mockdb.apihash['getTranslationJobRevisions']['url']
            .replace('{{id}}', '1'))


class TestGlossaryFunctions(unittest.TestCase):

    """
    """
    def setUp(self):
        """
        Creates the initial batch of jobs for the other test functions here
        to operate on.
        """
        self.gengo = Gengo(public_key=API_PUBKEY,
                           private_key=API_PRIVKEY,
                           sandbox=True)

        from gengo import requests
        self.json_mock = mock.Mock()
        self.json_mock.json.return_value = {'opstat': 'ok'}
        self.getMock = RequestsMock(return_value=self.json_mock)
        self.requestsPatch = mock.patch.object(requests, 'get', self.getMock)
        self.requestsPatch.start()

    def tearDown(self):
        self.requestsPatch.stop()

    def test_getGlossaryList(self):
        resp = self.gengo.getGlossaryList()
        self.assertEqual(resp['opstat'], 'ok')
        self.getMock.assert_path_contains(
            mockdb.apihash['getGlossaryList']['url'])


class RequestsMock(mock.Mock):

    def assert_path_contains(self, url_part):
        if not self.call_args or not self.call_args[0]:
            raise AssertionError("Invalid arguments for function call")
        if url_part not in self.call_args[0][0]:
            raise AssertionError(
                "{} is not being called in call to Gengo API".format(url_part))
        return True


class TestPreferredTranslatorsFunction(unittest.TestCase):

    """
    """
    def setUp(self):
        """
        Creates the initial batch of jobs for the other test functions here
        to operate on.
        """
        self.gengo = Gengo(public_key=API_PUBKEY,
                           private_key=API_PRIVKEY,
                           sandbox=True,
                           )

        from gengo import requests
        self.json_mock = mock.Mock()
        self.json_mock.json.return_value = {'opstat': 'ok'}
        self.getMock = RequestsMock(return_value=self.json_mock)
        self.requestsPatch = mock.patch.object(requests, 'get', self.getMock)
        self.requestsPatch.start()

    def tearDown(self):
        self.requestsPatch.stop()

    def test_getPreferredTranslators(self):
        resp = self.gengo.getPreferredTranslators()
        self.assertEqual(resp['opstat'], 'ok')
        # self.getMock.assert_any_call()
        self.getMock.assert_path_contains(
            mockdb.apihash['getPreferredTranslators']['url'])


if __name__ == '__main__':
    unittest.main()
