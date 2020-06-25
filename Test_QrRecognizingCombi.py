import unittest
from QrRecognizingCombi import notneeded, defaultSettings

class MyTestCase(unittest.TestCase):
    def test_unittest(self):
        self.assertEqual(notneeded(0), None)
    def test_defaultSettings(self):
        self.assertEqual(defaultSettings(), (640, 480, 'cascade70N20S.xml', 0, 'QR', (0, 128, 0)))

if __name__ == '__main__':
    unittest.main()
