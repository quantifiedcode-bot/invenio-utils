# -*- coding: utf-8 -*-
##
## $Id$
##
## This file is part of CDS Invenio.
## Copyright (C) 2002, 2003, 2004, 2005, 2006 CERN.
##
## CDS Invenio is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## CDS Invenio is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.  
##
## You should have received a copy of the GNU General Public License
## along with CDS Invenio; if not, write to the Free Software Foundation, Inc.,
## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

"""TestUtils Regression Test Suite."""

__revision__ = "$Id$"

import unittest

from invenio.config import weburl
from invenio.testutils import make_test_suite, warn_user_about_tests_and_run, \
                              test_web_page_content

class TestFunctionTestWebPageContent(unittest.TestCase):
    """Check browser test_web_page_content() function."""

    def test_function_test_web_page_content_login(self):
        """testutils - test_web_page_content() and username arguments""" 
        # should login as admin without password:
        self.assertEqual([],
                         test_web_page_content(weburl,
                                               username="admin",
                                               expected_text="</html>"))        
        # should not login as admin with password:
        errmsgs = test_web_page_content(weburl,
                                        username="admin",
                                        password="foo",
                                        expected_text="</html>")
        if errmsgs[0].find("ERROR: Cannot login as admin, test skipped.") > -1:
            pass
        else:
            self.fail("Should not be able to login as admin with foo password.")
        return
    
    def test_function_test_web_page_content_via_expected_text_argument(self):
        """testutils - test_web_page_content() and expected_text argument""" 
        # should find HTML in an HTML page:
        self.assertEqual([],
                         test_web_page_content(weburl + "/search?p=ellis",
                                               expected_text="</html>"))
        # should not find HTML tag in an XML page:
        errmsgs = test_web_page_content(weburl + "/search?p=ellis&of=xm")
        if errmsgs[0].find(" does not contain </html>") > -1:
            pass
        else:
            self.fail("Should not find </html> in an XML page.")
        return

    def test_function_test_web_page_content_via_expected_link_arguments(self):
        """testutils - test_web_page_content() and expected_link arguments""" 
        # should find link to ALEPH:
        self.assertEqual([],
                         test_web_page_content(weburl,
                                               expected_link_target=weburl+"/collection/ALEPH"))
        # should find link entitled ISOLDE:
        self.assertEqual([],
                         test_web_page_content(weburl,
                                               expected_link_label="ISOLDE"))
        # should find link to ISOLDE entitled ISOLDE:
        self.assertEqual([],
                         test_web_page_content("http://localhost/",
                                               expected_link_target=weburl+"/collection/ISOLDE",
                                               expected_link_label="ISOLDE"))
        # should not find link to ALEPH entitled ISOLDE:
        errmsgs = test_web_page_content(weburl,
                                        expected_link_target=weburl+"/collection/ALEPH",
                                        expected_link_label="ISOLDE")
        if errmsgs[0].find(" does not contain link to ") > -1:
            pass
        else:
            self.fail("Should not find link to ALEPH entitled ISOLDE.")
        return
    
test_suite = make_test_suite(TestFunctionTestWebPageContent)

if __name__ == "__main__":
    warn_user_about_tests_and_run(test_suite)