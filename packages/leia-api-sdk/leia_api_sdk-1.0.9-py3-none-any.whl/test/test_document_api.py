# coding: utf-8

"""
    LEIA RESTful API for AI

    Leia API  # noqa: E501

    OpenAPI spec version: 1.0.0
    Contact: 
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import unittest

import leiaapi.generated
from leiaapi.generated.api.document_api import DocumentApi  # noqa: E501
from leiaapi.generated.rest import ApiException


class TestDocumentApi(unittest.TestCase):
    """DocumentApi unit test stubs"""

    def setUp(self):
        self.api = DocumentApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_create_document(self):
        """Test case for create_document

        Uploads a document to the Leia API  # noqa: E501
        """
        pass

    def test_delete_document(self):
        """Test case for delete_document

        Deletes a document from Leia API  # noqa: E501
        """
        pass

    def test_edit_document(self):
        """Test case for edit_document

        Updates a document in Leia API  # noqa: E501
        """
        pass

    def test_get_document(self):
        """Test case for get_document

        Retrieves a document from Leia API  # noqa: E501
        """
        pass

    def test_get_document_contents(self):
        """Test case for get_document_contents

        Retrieves a document from Leia API  # noqa: E501
        """
        pass

    def test_get_documents(self):
        """Test case for get_documents

        Retrieves documents from Leia API (paginated)  # noqa: E501
        """
        pass

    def test_get_documents_tags(self):
        """Test case for get_documents_tags

        Retrieves documents' tags from Leia API  # noqa: E501
        """
        pass

    def test_get_documents_zip(self):
        """Test case for get_documents_zip

        Retrieves documents from Leia API (paginated)  # noqa: E501
        """
        pass

    def test_tag_document(self):
        """Test case for tag_document

        Tags a document  # noqa: E501
        """
        pass

    def test_transform_document_async(self):
        """Test case for transform_document_async

        Asynchronously converts a document within Leia API  # noqa: E501
        """
        pass

    def test_untag_document(self):
        """Test case for untag_document

        Untags an document  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
