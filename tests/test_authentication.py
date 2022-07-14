import time
from apis import authentication
import unittest
import helpers
helpers.modify_system_path()


class TestAuthentication(unittest.TestCase):

    def test_token(self):
        self.assertEqual(authentication.API_TUTOR_TOKEN,
                         'API.fda8c628-f8f0-448d-aad8-42c2fcd067ec')

    def test_get_key(self):
        yelp_key = authentication.get_token(
            'https://www.apitutor.org/yelp/key')
        self.assertEqual(len(yelp_key), 128)
        time.sleep(1.0)
        spotify_key = authentication.get_token(
            'https://www.apitutor.org/spotify/key')
        self.assertEqual(len(spotify_key), 144)
        time.sleep(1.0)


if __name__ == '__main__':
    unittest.main()
