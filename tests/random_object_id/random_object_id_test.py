import re
import sys

from contextlib import contextmanager
from StringIO import StringIO

import mock

from random_object_id.random_object_id import \
    gen_random_object_id, parse_args, main


@contextmanager
def captured_output():
    new_out = StringIO()
    old_out = sys.stdout
    try:
        sys.stdout = new_out
        yield sys.stdout
    finally:
        sys.stdout = old_out


def test_gen_random_object_id_time():
    with mock.patch('time.time') as mock_time:
        mock_time.return_value = 1429506585.786924
        object_id = gen_random_object_id()

    assert re.match('55348a19', object_id)


def test_gen_random_object_id_length():
    assert len(gen_random_object_id()) == 24


def test_parse_args():
    assert parse_args(['-l']).long_form


def test_main():
    with mock.patch('sys.argv', ['random_object_id']):
        with captured_output() as output:
            main()

    assert re.match('[0-9a-f]{24}\n', output.getvalue())


def test_main_l():
    with mock.patch('sys.argv', ['random_object_id', '-l']):
        with captured_output() as output:
            main()

    assert re.match('ObjectId\("[0-9a-f]{24}"\)\n', output.getvalue())
