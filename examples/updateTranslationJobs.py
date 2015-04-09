#!/usr/bin/env python
# -*- coding: utf-8 -*-

# All code provided from the http://gengo.com site, such as API example code
# and libraries, is provided under the New BSD license unless otherwise
# noted. Details are below.
#
# New BSD License
# Copyright (c) 2009-2012, myGengo, Inc.
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
# Neither the name of myGengo, Inc. nor the names of its contributors may
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

from gengo import Gengo

# Get an instance of Gengo to work with...
gengo = Gengo(
    public_key='foo',
    private_key='bar',
    sandbox=False,
    debug=True,
    api_url='http://api.gengo.dev/v2'
)

# Archive all jobs
gengo.updateTranslationJobs(action={
    'job_ids': [4020, 1082],
    'action': 'archive'
})

# Revise a group of jobs
gengo.updateTranslationJobs(action={
    'action': 'revise',
    'reason': 'This job is total bananas',
    'job_ids': [{'job_id': 556, 'comment': 'Please change banana to gorilla'},
                {'job_id': 553, 'comment': 'Please change banana to monkey'}],
})

# Reject a group of jobs
gengo.updateTranslationJobs(action={
    'action': 'reject',
    'job_ids': [{'job_id': 630,
                 'reason': 'quality',
                 'comment': 'This sentence should be in the past tense',
                 'captcha': 'AAAA'},
                {'job_id': 631,
                 'reason': 'quality',
                 'comment': 'This should have be capitalized',
                 'captcha': 'BBBB'}
                ],
})

# Approve a group of jobs
gengo.updateTranslationJobs(action={
  'action': 'approve',
  'job_ids': [{'job_id': 1077, 'comment': 'Keep up the good work'},
              {'job_id': 629, 'comment': 'Great job!'}],
})