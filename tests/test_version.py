from setuptools_sky import ScmVersion, get_version
import unittest
import six

if six.PY2:
    from mock import patch
else:
    from unittest.mock import patch

CURRENT_TAG = '1.0.2rc0-2-g249a213'


def mock_git_parse(root, dirty=False, preformatted=False, *args, **kwargs):
    tag, number, node = CURRENT_TAG.rsplit('-', 2)

    return ScmVersion(tag, int(number), node, dirty, preformatted, **kwargs)


class TestVersion(unittest.TestCase):
    def setUp(self):
        self.configs = {
            'root': '.',
            'version_scheme': 'guess-next-dev',
            'local_scheme': 'node-and-date',
            'write_to': None,
            'write_to_template': None,
            'relative_to': None,
            'parse': None,
        }

        self.expected = '1.0.3beta2'

    @patch('setuptools_sky.git.parse', side_effect=mock_git_parse)
    def test_get_version(self, *args, **kwargs):
        self.assertEqual(get_version(**self.configs), self.expected)


if __name__ == '__main__':
    unittest.main()
