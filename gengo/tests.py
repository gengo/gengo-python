#!/usr/bin/python
# -*- coding: utf-8 -*-
# All code provided from the http://gengo.com site, such as API example code
# and libraries, is provided under the New BSD license unless otherwise
# noted. Details are below.
#
# New BSD License
# Copyright (c) 2009-2012, Gengo, Inc.
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
import os
import random
import time

from gengo import Gengo, GengoError, GengoAuthError

API_PUBKEY = os.getenv('GENGO_PUBKEY')
API_PRIVKEY = os.getenv('GENGO_PRIVKEY')


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
        self.assertRaises(AttributeError, getattr, Gengo, 'bert')

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

    def test_getAccountStats(self):
        stats = self.gengo.getAccountStats()
        self.assertEqual(stats['opstat'], 'ok')

    def test_getAccountBalance(self):
        balance = self.gengo.getAccountBalance()
        self.assertEqual(balance['opstat'], 'ok')


class TestLanguageServiceMethods(unittest.TestCase):

    """
    Tests the methods that deal with getting information about language-
    translation service support from Gengo.
    """
    def setUp(self):
        self.gengo = Gengo(public_key=API_PUBKEY,
                           private_key=API_PRIVKEY,
                           sandbox=True)

    def test_getServiceLanguagePairs(self):
        resp = self.gengo.getServiceLanguagePairs()
        self.assertEqual(resp['opstat'], 'ok')

    def test_getServiceLanguages(self):
        resp = self.gengo.getServiceLanguages()
        self.assertEqual(resp['opstat'], 'ok')


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
        self.created_job_ids = []

        multiple_jobs_quote = {
            'job_1': {
                'type': 'file',
                'file_path': './examples/testfiles/test_file1.txt',
                'lc_src': 'en',
                'lc_tgt': 'ja',
                'tier': 'standard',
            },
            'job_2': {
                'type': 'file',
                'file_path': './examples/testfiles/test_file2.txt',
                'lc_src': 'ja',
                'lc_tgt': 'en',
                'tier': 'standard',
            },
        }

        # Now that we've got the jobs, let's go ahead and see how much it'll
        # cost.
        cost_assessment = self.gengo.determineTranslationCost(
            jobs=multiple_jobs_quote)
        self.assertEqual(cost_assessment['opstat'], 'ok')

        self.multiple_jobs = {}
        for k, j in cost_assessment['response']['jobs'].iteritems():
            self.multiple_jobs[k] = {
                'type': 'file',
                'identifier': j['identifier'],
                'comment': 'Test comment for %s' % (k,),
                'glossary_id': None,
                'use_preferred': 1,
                'force': 1,
            }

        jobs = self.gengo.postTranslationJobs(
            jobs={'jobs': self.multiple_jobs, 'as_group': 0})
        self.assertEqual(jobs['opstat'], 'ok')
        self.assertTrue('order_id' in jobs['response'])
        self.assertTrue('credits_used' in jobs['response'])
        self.assertEqual(jobs['response']['job_count'], 2)

        # get some order information - in v2 the jobs need to have gone
        # through a queueing system so we wait a little bit
        time.sleep(20)
        resp = self.gengo.getTranslationOrderJobs(
            id=jobs['response']['order_id'])
        self.assertEqual(resp['response']['order']['as_group'], 0)
        self.assertEqual(len(resp['response']['order']['jobs_available']), 2)
        self.created_job_ids.\
            extend(resp['response']['order']['jobs_available'])

    def test_postJobComment(self):
        """
        Tests posting a comment to a job.
        """
        posted_comment = self.gengo.postTranslationJobComment(
            id=self.created_job_ids[0],
            comment={'body': 'I love lamp oh mai gawd'})
        self.assertEqual(posted_comment['opstat'], 'ok')
        job_comments = self.gengo.getTranslationJobComments(
            id=self.created_job_ids[0])
        self.assertEqual(posted_comment['opstat'], 'ok')
        self.assertEqual(job_comments['opstat'], 'ok')
        self.assertEqual(job_comments['response']['thread'][0]['body'],
                         'Test comment for job_2')
        self.assertEqual(job_comments['response']['thread'][1]['body'],
                         'I love lamp oh mai gawd')

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
        job = self.gengo.getTranslationJob(id=self.created_job_ids[0])
        self.assertEqual(job['opstat'], 'ok')

        # Pull down the 10 most recently submitted jobs.
        jobs = self.gengo.getTranslationJobs()
        self.assertEqual(jobs['opstat'], 'ok')

        # Test getting the batch that a job is in.
        job_batch = self.gengo.getTranslationJobBatch(
            id=self.created_job_ids[1])
        self.assertEqual(job_batch['opstat'], 'ok')

        # Pull down feedback. This should work fine, but there'll be no
        # feedback.
        feedback = self.gengo.getTranslationJobFeedback(
            id=self.created_job_ids[0])
        self.assertEqual(feedback['opstat'], 'ok')

        # Lastly, pull down any revisions that definitely didn't occur due
        # to this being a simulated test.
        revisions = self.gengo.getTranslationJobRevisions(
            id=self.created_job_ids[0])
        self.assertEqual(revisions['opstat'], 'ok')

        # So it's worth noting here that we can't really test
        # getTranslationJobRevision(), because no real revisions
        # exist at this point, and a revision ID is required to pull that
        # method off successfully. Bai now.

    def tearDown(self):
        """
        Delete every job we've created.
        """
        for id in self.created_job_ids:
            deleted_job = self.gengo.deleteTranslationJob(id=id)
            self.assertEqual(deleted_job['opstat'], 'ok')


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

        multiple_jobs_quote = {
            'job_3': {
                'type': 'text',
                'body_src': 'This is a group job test job 1.',
                'lc_src': 'en',
                'lc_tgt': 'zh',
                'tier': 'standard',
            },
            'job_4': {
                'type': 'text',
                'body_src': 'This is a group job test job 2.',
                'lc_src': 'en',
                'lc_tgt': 'zh',
                'tier': 'standard',
            },
        }

        # Now that we've got the jobs, let's go ahead and see how much it'll
        # cost.
        self.jobs = jobs = self.gengo.postTranslationJobs(
            jobs={'jobs': multiple_jobs_quote, 'as_group': 1})

        self.assertEqual(jobs['opstat'], 'ok')
        self.assertTrue('order_id' in jobs['response'])
        self.assertTrue('credits_used' in jobs['response'])
        self.assertEqual(jobs['response']['job_count'], 2)

        time.sleep(20)
        resp = self.gengo.getTranslationOrderJobs(
            id=self.jobs['response']['order_id'])

        self.created_job_ids.\
            extend(resp['response']['order']['jobs_available'])

    def test_postTranslationJobs_as_group(self):
        """
        Make sure that the as_group setting gets interpreted by the API
        correctly.
        """
        resp = self.gengo.getTranslationOrderJobs(
            id=self.jobs['response']['order_id'])

        self.assertEqual(resp['response']['order']['as_group'], 1)
        self.assertEqual(len(resp['response']['order']['jobs_available']), 2)

    def tearDown(self):
        """
        Delete every job we've created.
        """
        for id in self.created_job_ids:
            deleted_job = self.gengo.deleteTranslationJob(id=id)
            self.assertEqual(deleted_job['opstat'], 'ok')


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
        self.created_job_ids = []

        multiple_jobs_quote = {
            'job_1': {
                'type': 'file',
                'file_path': './examples/testfiles/test_file1.txt',
                'lc_src': 'en',
                'lc_tgt': 'ja',
                'tier': 'standard',
            },
            'job_2': {
                'type': 'text',
                'body_src': '''Liverpool Football Club is an English
                Premier League football club based in Liverpool,
                Merseyside. Liverpool is awesome and is the best club
                around. Liverpool was founded in 1892 and admitted into the
                Football League the following year. The club has played at
                its home ground, Anfield, since its founding, and the team
                has played in an all-red home strip since 1964.
                Domestically, Liverpool has won eighteen league titles -
                the second most in English football - as well as seven FA
                Cups, a record eight League Cups and fifteen FA Community
                Shields. Liverpool has also won more European titles than
                any other English club, with five European Cups, three UEFA
                Cups and three UEFA Super Cups. The most successful period
                in Liverpool''',
                'lc_src': 'en',
                'lc_tgt': 'ja',
                'tier': 'standard',
            },
        }

        # Now that we've got the job, let's go ahead and see how much it'll
        # cost.
        cost_assessment = self.gengo.determineTranslationCost(
            jobs=multiple_jobs_quote)
        self.assertEqual(cost_assessment['opstat'], 'ok')

        multiple_jobs = {}
        for k, j in cost_assessment['response']['jobs'].iteritems():
            if j['type'] == 'file':
                multiple_jobs[k] = {
                    'type': 'file',
                    'file_path': './examples/testfiles/test_file1.txt',
                    'identifier': j['identifier'],
                    'comment': 'Test comment for filejob %s' % (k,),
                    'glossary_id': None,
                    'use_preferred': 0,
                    'force': 1
                }
            else:
                multiple_jobs[k] = multiple_jobs_quote[k]
                multiple_jobs[k]['comment'] = \
                    'Test comment for textjob %s' % (k,)
                multiple_jobs[k]['glossary_id'] = None
                multiple_jobs[k]['use_preferred'] = 0
                multiple_jobs[k]['force'] = 1

        jobs = self.gengo.postTranslationJobs(
            jobs=multiple_jobs)
        self.assertEqual(jobs['opstat'], 'ok')
        self.assertTrue('order_id' in jobs['response'])
        self.assertTrue('credits_used' in jobs['response'])
        self.assertEqual(jobs['response']['job_count'], 2)

        cleared_queue = False
        ping_count = 0

        # Get some order information - in v2 the jobs need to have gone
        # through a queueing system so we'll try up to 10 times, with 10 second
        # breaks
        while False == cleared_queue and ping_count < 10:
            time.sleep(10)
            resp = self.gengo.getTranslationOrderJobs(
                id=jobs['response']['order_id'])

            if len(resp['response']['order']['jobs_available']) != 2:
                print "\nJobs still queued; pausing 10s and checking again..."
                ping_count += 1
                continue

            cleared_queue = True

        if ping_count == 10:
            self.assertTrue(False, "API Queue not processing jobs!")

        # We'll use the job ids in another test
        self.created_job_ids.\
            extend(resp['response']['order']['jobs_available'])

    def test_postJobComment(self):
        """
        Tests posting a comment to a job.
        """
        posted_comment = self.gengo.postTranslationJobComment(
            id=self.created_job_ids[0],
            comment={'body': 'I love lamp oh mai gawd'})
        self.assertEqual(posted_comment['opstat'], 'ok')
        job_comments = self.gengo.getTranslationJobComments(
            id=self.created_job_ids[0])
        self.assertEqual(posted_comment['opstat'], 'ok')
        self.assertEqual(job_comments['opstat'], 'ok')
        self.assertEqual(job_comments['response']['thread'][0]['body'],
                         'Test comment for textjob job_2')
        self.assertEqual(job_comments['response']['thread'][1]['body'],
                         'I love lamp oh mai gawd')

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
        job = self.gengo.getTranslationJob(id=self.created_job_ids[0])
        self.assertEqual(job['opstat'], 'ok')

        # Pull down the 10 most recently submitted jobs.
        jobs = self.gengo.getTranslationJobs()
        self.assertEqual(jobs['opstat'], 'ok')

        # Test getting the batch that a job is in...
        job_batch = self.gengo.getTranslationJobBatch(
            id=self.created_job_ids[1])
        self.assertEqual(job_batch['opstat'], 'ok')

        # Pull down feedback. This should work fine, but there'll be no
        # feedback.
        feedback = self.gengo.getTranslationJobFeedback(
            id=self.created_job_ids[0])
        self.assertEqual(feedback['opstat'], 'ok')

        # Lastly, pull down any revisions that definitely didn't occur due
        # to this being a simulated test.
        revisions = self.gengo.getTranslationJobRevisions(
            id=self.created_job_ids[0])
        self.assertEqual(revisions['opstat'], 'ok')

        # So it's worth noting here that we can't really test
        # getTranslationJobRevision(), because no real revisions
        # exist at this point, and a revision ID is required to pull that
        # method off successfully. Bai now.

    def tearDown(self):
        """
        Delete every job we've created for this somewhat ridiculously
        thorough testing scenario.
        """
        for id in self.created_job_ids:
            deleted_job = self.gengo.deleteTranslationJob(id=id)
            self.assertEqual(deleted_job['opstat'], 'ok')


class TestGlossaryFunctions(unittest.TestCase):

    """
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

    def test_getGlossaryList(self):
        resp = self.gengo.getGlossaryList()
        self.assertEqual(resp['opstat'], 'ok')


if __name__ == '__main__':
    unittest.main()
