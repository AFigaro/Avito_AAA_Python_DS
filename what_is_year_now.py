import urllib.request
import json
import unittest
import unittest.mock


API_URL = 'http://worldclockapi.com/api/json/utc/now'

YMD_SEP = '-'
YMD_SEP_INDEX = 4
YMD_YEAR_SLICE = slice(None, YMD_SEP_INDEX)

DMY_SEP = '.'
DMY_SEP_INDEX = 5
DMY_YEAR_SLICE = slice(DMY_SEP_INDEX + 1, DMY_SEP_INDEX + 5)


def what_is_year_now() -> int:

    """
    Получает текущее время из API-worldclock и извлекает из поля
    'currentDateTime' год
    Предположим, что currentDateTime может быть в двух форматах:
      * YYYY-MM-DD - 2019-03-01
      * DD.MM.YYYY - 01.03.2019
    """

    with urllib.request.urlopen(API_URL) as resp:
        resp_json = json.load(resp)

    datetime_str = resp_json['currentDateTime']
    if datetime_str[YMD_SEP_INDEX] == YMD_SEP:
        year_str = datetime_str[YMD_YEAR_SLICE]
    elif datetime_str[DMY_SEP_INDEX] == DMY_SEP:
        year_str = datetime_str[DMY_YEAR_SLICE]
    else:
        raise ValueError('Invalid format')

    return int(year_str)


class TestWhatIsYearNow(unittest.TestCase):

    @unittest.mock.patch('urllib.request.urlopen')
    def test_ymd_date(self, mock_urlopen):
        mocked_data = unittest.mock.MagicMock()
        mocked_data.read.return_value = '{"currentDateTime": "2022-11-12"}'
        mocked_data.__enter__.return_value = mocked_data
        mock_urlopen.return_value = mocked_data
        self.assertEqual(what_is_year_now(), 2022)

    @unittest.mock.patch('urllib.request.urlopen')
    def test_dmy_date(self, mock_urlopen):
        mocked_data = unittest.mock.MagicMock()
        mocked_data.read.return_value = '{"currentDateTime": "12.11.2022"}'
        mocked_data.__enter__.return_value = mocked_data
        mock_urlopen.return_value = mocked_data
        self.assertEqual(what_is_year_now(), 2022)

    @unittest.mock.patch('urllib.request.urlopen')
    def test_invalid_date(self, mock_urlopen):
        mocked_data = unittest.mock.MagicMock()
        mocked_data.read.return_value = '{"currentDateTime": "12/11/2022"}'
        mocked_data.__enter__.return_value = mocked_data
        mock_urlopen.return_value = mocked_data
        with self.assertRaises(ValueError):
            self.assertEqual(what_is_year_now(), 2022)
