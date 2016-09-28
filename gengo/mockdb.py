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
A huge map of every Gengo API endpoint to a function definition in gengo-
python.

Parameters that need to be embedded in the URL are treated with mustaches,
e.g:

{{bert}}, etc

When creating new endpoint definitions, keep in mind that the name of the
mustache will be replaced with the keyword that gets passed in to the
function at call time.

i.e, in this case, if I pass bert = 47 to any function, {{bert}} will be
replaced with 47, instead of defaulting to 1 (said defaulting takes place
at conversion time).
"""

# Gengo API urls. {version} gets replaced with v1/etc at run time.
api_urls = {
    'sandbox': 'http://api.sandbox.gengo.com/{version}',
    'base': 'https://api.gengo.com/{version}',
}

# The API endpoint 'table', 'database', 'hash', 'dictionary', whatever
# you'd like to call it. To keep things uber nice and organized, we secure
# away all the endpoints here with easily replaceable scenarios. Win!
apihash = {
    # All Account-information based methods...
    'getAccountStats': {
        'url': '/account/stats',
        'method': 'GET',
    },
    'getAccountBalance': {
        'url': '/account/balance',
        'method': 'GET',
    },
    # retrieve authenticate user details
    'getAccountMe': {
        'url': '/account/me',
        'method': 'GET',
    },

    'postTranslationJobs': {
        'url': '/translate/jobs',
        'method': 'POST',
    },

    # Updating an existing translation request.
    'updateTranslationJob': {
        'url': '/translate/job/{{id}}',
        'method': 'PUT',
    },

    # Updating an existing translation requests.
    'updateTranslationJobs': {
        'url': '/translate/jobs',
        'method': 'PUT',
    },

    # Viewing existing translation requests.
    'getTranslationJob': {
        'url': '/translate/job/{{id}}',
        'method': 'GET',
    },
    'getTranslationJobs': {
        'url': '/translate/jobs',
        'method': 'GET',
    },
    'getTranslationJobBatch': {
        'url': '/translate/jobs/{{id}}',
        'method': 'GET',
    },

    # Get a quote for how much a given job will cost.
    'determineTranslationCost': {
        'url': '/translate/service/quote',
        'method': 'POST',
        'upload': True,  # with this being set the payload will be checked
        # for file_path args and - if found - modified in a way so that
        # opened file descriptors are passed to requests to do a multi part
        # file upload. for now this is tied to jobs data only.
    },

    # Deal with comments and other metadata about a TranslationJob in
    # progress.
    'postTranslationJobComment': {
        'url': '/translate/job/{{id}}/comment',
        'method': 'POST',
    },
    'getTranslationJobComments': {
        'url': '/translate/job/{{id}}/comments',
        'method': 'GET',
    },
    'getTranslationJobFeedback': {
        'url': '/translate/job/{{id}}/feedback',
        'method': 'GET',
    },
    'getTranslationJobRevisions': {
        'url': '/translate/job/{{id}}/revisions',
        'method': 'GET',
    },
    'getTranslationJobRevision': {
        'url': '/translate/job/{{id}}/revision/{{revision_id}}',
        'method': 'GET',
    },

    # Delete a job...
    'deleteTranslationJob': {
        'url': '/translate/job/{{id}}',
        'method': 'DELETE',
    },

    # Translation Service language information. Holds information
    # about which languages can be converted to which, etc.
    'getServiceLanguagePairs': {
        'url': '/translate/service/language_pairs',
        'method': 'GET',
    },
    'getServiceLanguages': {
        'url': '/translate/service/languages',
        'method': 'GET',
    },
    'getServiceLanguageMatrix': {
        'url': '/translate/service/language_matrix',
        'method': 'GET',
    },

    # glossary stuff
    'getGlossaryList': {
        'url': '/translate/glossary',
        'method': 'GET',
    },

    'getGlossary': {
        'url': '/translate/glossary/{{id}}',
        'method': 'GET',
    },

    # order information
    'getTranslationOrderJobs': {
        'url': '/translate/order/{{id}}',
        'method': 'GET',
    },

    # Delete Translation order
    'deleteTranslationOrder': {
        'url': '/translate/order/{{id}}',
        'method': 'DELETE',
    },

    # Deal with comments and other metadata about an Order in
    # progress.
    'postOrderComment': {
        'url': '/translate/order/{{id}}/comment',
        'method': 'POST',
    },
    'getOrderComments': {
        'url': '/translate/order/{{id}}/comments',
        'method': 'GET',
    },

    # get list of preferred translators
    'getPreferredTranslators': {
        'url': '/account/preferred_translators',
        'method': 'GET',
    }
}
