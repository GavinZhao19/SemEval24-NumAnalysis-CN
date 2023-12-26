import unittest

from src.translator import translate_value


class TestTranslator(unittest.TestCase):

    def test(self):
        """ From the googletrans.constants.py we may choose the appropriate translation.
                'zh-cn': 'chinese (simplified)'
                'zh-tw': 'chinese (traditional)'
        """
        text = translate_value("從四個選項中選出正確的選項，選項內容都為數字，填在問題的___中", dest="en", src="zh-cn")
        print("Translation:", text)


if __name__ == '__main__':
    unittest.main()
