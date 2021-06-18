import os
from typing import Tuple

from jivago.wsgi.request.request import Request
from jivago.wsgi.request.response import Response


class PartialContentHandler(object):

    def handle_partial_content_request(self, request: Request, filepath: str, *, max_block_size: int = 2000000,
                                       content_type = "application/octet-stream") -> Response:
        if request.headers['Range']:
            total_filesize = os.path.getsize(filepath)
            start, end = self._parse_range_string(request.headers['Range'], max_block_size, total_filesize)
            return Response(206, {"Content-Type": content_type, "Accept-Ranges": "bytes",
                                  "Content-Range": f"bytes {start}-{end-1}/{total_filesize}"}, self._read_partial_file(filepath, start, end))

        return Response(200, {"Content-Type": content_type}, self._read_whole_file(filepath))

    def _parse_range_string(self, range_string: str, default_block_size: int, file_end_offset: int) -> Tuple[int, int]:
        start = int(range_string.split("=")[1].split("-")[0])
        end_string = range_string.split("-")[1]
        end = int(end_string) if end_string != '' else start + default_block_size

        if end > file_end_offset:
            end = file_end_offset

        return start, end

    def _read_partial_file(self, filepath: str, start: int, end: int) -> bytes:
        with open(filepath, 'rb') as f:
            f.seek(start)
            return f.read(end - start + 1)

    def _read_whole_file(self, filepath: str) -> bytes:
        with open(filepath, 'rb') as f:
            return f.read()
