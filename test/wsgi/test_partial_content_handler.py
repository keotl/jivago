import os
import unittest

import test_data
from jivago.wsgi.request.partial_content_handler import PartialContentHandler
from test_utils.request_builder import RequestBuilder

TEST_FILE = os.path.join(os.path.dirname(test_data.__file__), "binary_file")
TEST_FILE_TOTAL_SIZE = os.path.getsize(TEST_FILE)


class PartialContentHandlerTest(unittest.TestCase):

    def setUp(self):
        self.partialContentHandler = PartialContentHandler()

    def test_givenHttpPartialRange_whenHandlingContentRequest_thenResponseHas206HttpStatus(self):
        partial_request = RequestBuilder().headers({"Range": "bytes=0-"}).build()

        response = self.partialContentHandler.handle_partial_content_request(partial_request, TEST_FILE)

        self.assertEqual(206, response.status)

    def test_givenStartingByteRange_whenHandlingContentRequest_thenReturnBytesStartingAtOffset(self):
        a_starting_offset = 6
        partial_request = RequestBuilder().headers({"Range": f"bytes={a_starting_offset}-"}).build()

        response = self.partialContentHandler.handle_partial_content_request(partial_request, TEST_FILE, max_block_size=1000000000)

        self.assertEqual(TEST_FILE_TOTAL_SIZE - a_starting_offset, len(response.body))
        with open(TEST_FILE, 'rb') as f:
            f.seek(6)
            self.assertEqual(f.read(), response.body)

    def test_givenMissingHttpRange_whenHandlingContentRequest_thenReturn200OkStatus(self):
        request = RequestBuilder().build()

        response = self.partialContentHandler.handle_partial_content_request(request, TEST_FILE)

        self.assertEqual(200, response.status)

    def test_givenMissingHttpRange_whenHandlingContentRequest_thenReturnTheWholeFile(self):
        request = RequestBuilder().build()

        response = self.partialContentHandler.handle_partial_content_request(request, TEST_FILE)

        with open(TEST_FILE, 'rb') as f:
            self.assertEqual(f.read(), response.body)

# TODO actual test with defined end offset
