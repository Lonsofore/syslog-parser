from datetime import datetime

from pytest import fixture
from pyparsing import ParseException

from parser import Parser


@fixture
def parse():
    parser = Parser()
    return parser.parse
    fields = parser.parse(line)
    return fields


def test_correct(parse):
    line = 'Jun 11 00:01:11 test-hostname anacron[1111]: Normal exit (1 job run)'
    fields = parse(line)
    assert fields['timestamp'].isoformat() == datetime(datetime.now().year, 6, 11, 0, 1, 11).isoformat()
    assert fields['hostname'] == 'test-hostname'
    assert fields['app'] == 'anacron'
    assert fields['pid'] == '1111'
    assert fields['message'] == 'Normal exit (1 job run)'


def test_incorrect(parse):
    line = '11 00:01:11 test-hostname anacron[1111]: Normal exit (1 job run)'
    try:
        fields = parse(line)
        assert False
    except ParseException:
        assert True
