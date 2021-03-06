# -*- coding: utf-8 -*-

"""
Copyright (C) 2013 Dariusz Suchojad <dsuch at zato.io>

Licensed under LGPLv3, see LICENSE.txt for terms and conditions.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

# stdlib
from unittest import TestCase
from uuid import uuid4

# lxml
from lxml import etree

# Zato
from zato.common import ParsingException, soap_body_xpath, zato_path
from zato.common import util

class ZatoPathTestCase(TestCase):
    def test_zato_path(self):
        xml = etree.fromstring("""<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
         xmlns="https://zato.io/ns/20130518">
      <soap:Body>
            <zato_channel_amqp_edit_response xmlns="https://zato.io/ns/20130518">
               <zato_env>
                  <cid>K08984532360785332835581231451</cid>
                  <result>ZATO_OK</result>
               </zato_env>
               <item>
                  <id>1</id>
                  <name>crm.account</name>
               </item>
            </zato_channel_amqp_edit_response>
      </soap:Body>
   </soap:Envelope>""")

        request = soap_body_xpath(xml)[0].getchildren()[0]
        zato_path('item', True).get_from(request)
        
        path = uuid4().hex
        try:
            zato_path(path, True).get_from(request)
        except ParsingException:
            pass
        else:
            raise AssertionError('Expected an ParsingException with path:[{}]'.format(path))


class UtilsTestCase(TestCase):
    def test_uncamelify(self):
        original = 'ILikeToReadWSDLDocsNotReallyNOPENotMeQ'
        expected1 = 'i-like-to-read-wsdl-docs-not-really-nope-not-me-q'
        expected2 = 'I_LIKE_TO_READ_WSDL_DOCS_NOT_REALLY_NOPE_NOT_ME_Q'
        
        self.assertEquals(util.uncamelify(original), expected1)
        self.assertEquals(util.uncamelify(original, '_', unicode.upper), expected2)
