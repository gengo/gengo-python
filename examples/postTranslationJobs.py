#!/usr/bin/env python
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

from gengo import Gengo

# Get an instance of Gengo to work with...
gengo = Gengo(
    public_key='your_public_key',
    private_key='your_private_key',
    sandbox=True,
    debug=True
)

# This is an exhaustive view of this object; chances are your code will never
# have to be this verbose because you'd want to build it up programmatically.
data = {
    'jobs': {
        'job_1': {
            'type': 'text',  # REQUIRED. Type to translate, you'll probably always put 'text' here. ;P
            'slug': 'Single :: English to Japanese',  # REQUIRED. Slug for internally storing, can be generic.
            'body_src': 'Testing Gengo API library calls.',  # REQUIRED. The text you're translating. ;P
            'lc_src': 'en',  # REQUIRED. source_language_code (see getServiceLanguages() for a list of codes)
            'lc_tgt': 'ja',  # REQUIRED. target_language_code (see getServiceLanguages() for a list of codes)
            'tier': 'standard',  # REQUIRED. tier type ("machine", "standard", "pro", or "ultra")

            'auto_approve': 0,  # OPTIONAL. Hopefully self explanatory (1 = yes, 0 = no),
            'comment': 'HEY THERE TRANSLATOR',  # OPTIONAL. Comment to leave for translator.
            'url_attachments': [  # OPTIONAL. Comment URL attachments.
                {
                    'url': 'https://gengo.github.io/style-guide/assets/images/logos/gengo_logo_circle_512.png',
                    'filename': 'gengo_logo_circle_512.png',
                    'mime_type': 'image/png',
                },
            ],
            'callback_url': 'http://...',  # OPTIONAL. Callback URL that updates are sent to.
            'custom_data': 'your optional custom data, limited to 1kb.'  # OPTIONAL
        },
        'job_2': {
            'type': 'text',  # REQUIRED. Type to translate, you'll probably always put 'text' here. ;P
            'slug': 'Single :: English to Japanese',  # REQUIRED. Slug for internally storing, can be generic.
            'body_src': 'Testing Gengo API library calls.',  # REQUIRED. The text you're translating. ;P
            'lc_src': 'en',  # REQUIRED. source_language_code (see getServiceLanguages() for a list of codes)
            'lc_tgt': 'ja',  # REQUIRED. target_language_code (see getServiceLanguages() for a list of codes)
            'tier': 'standard',  # REQUIRED. tier type ("machine", "standard", "pro", or "ultra")

            'auto_approve': 0,  # OPTIONAL. Hopefully self explanatory (1 = yes, 0 = no),
            'comment': 'HEY THERE TRANSLATOR',  # OPTIONAL. Comment to leave for translator.
            'callback_url': 'http://...',  # OPTIONAL. Callback URL that updates are sent to.
            'custom_data': 'your optional custom data, limited to 1kb.'  # OPTIONAL
        },
    },
    'comment': 'Please make sure each translation sounds formal.',
    'process': 1,  # OPTIONAL. 1 (true, default) / 0 (false). Whether to pay for the job(s) and make them available for translation.
    'as_group': 1,  # OPTIONAL. 1 (true) / 0 (false, default). Whether all jobs in this group should be done by one translator.
}

# And now we post them over...
print(gengo.postTranslationJobs(jobs=data))
