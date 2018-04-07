#!/usr/bin/env python3

import sys, unittest
sys.path.append('python-lib')

import hrunits



class TestHrSmallSizes(unittest.TestCase):
    """
    Test encoding of small sizes up to and around the 1000-1024 range
    """

    def test0(self):
        result = hrunits.getSizeStringBytesBinary(0)
        self.assertEqual(result, "0 B")
        result = hrunits.getSizeStringBytesDecimal(0)
        self.assertEqual(result, "0 B")
        result = hrunits.getSizeStringBitsBinary(0)
        self.assertEqual(result, "0 bit")
        result = hrunits.getSizeStringBitsDecimal(0)
        self.assertEqual(result, "0 bit")

    def test1000(self):
        result = hrunits.getSizeStringBytesBinary(1000)
        self.assertEqual(result, "1000 B")
        result = hrunits.getSizeStringBytesDecimal(1000)
        self.assertEqual(result, "1.00 kB")
        result = hrunits.getSizeStringBitsBinary(1000)
        self.assertEqual(result, "1000 bit")
        result = hrunits.getSizeStringBitsDecimal(1000)
        self.assertEqual(result, "1.00 kbit")

    def test1024(self):
        result = hrunits.getSizeStringBytesBinary(1024)
        self.assertEqual(result, "1.00 KiB")
        result = hrunits.getSizeStringBytesDecimal(1024)
        self.assertEqual(result, "1.02 kB")
        result = hrunits.getSizeStringBitsBinary(1024)
        self.assertEqual(result, "1.00 Kibit")
        result = hrunits.getSizeStringBitsDecimal(1024)
        self.assertEqual(result, "1.02 kbit")

    def test1026(self):
        result = hrunits.getSizeStringBytesBinary(1026)
        self.assertEqual(result, "1.00 KiB")
        result = hrunits.getSizeStringBytesDecimal(1026)
        self.assertEqual(result, "1.03 kB")
        result = hrunits.getSizeStringBitsBinary(1026)
        self.assertEqual(result, "1.00 Kibit")
        result = hrunits.getSizeStringBitsDecimal(1026)
        self.assertEqual(result, "1.03 kbit")



class TestHrEvenBinarySizes(unittest.TestCase):
    """
    Test powers of 1024
    """

    def test_binary_power_1(self):
        result = hrunits.getSizeStringBytesBinary(1024)
        self.assertEqual(result, "1.00 KiB")
        result = hrunits.getSizeStringBytesDecimal(1024)
        self.assertEqual(result, "1.02 kB")
        result = hrunits.getSizeStringBitsBinary(1024)
        self.assertEqual(result, "1.00 Kibit")
        result = hrunits.getSizeStringBitsDecimal(1024)
        self.assertEqual(result, "1.02 kbit")

    def test_binary_power_2(self):
        result = hrunits.getSizeStringBytesBinary(1024**2)
        self.assertEqual(result, "1.00 MiB")
        result = hrunits.getSizeStringBytesDecimal(1024**2)
        self.assertEqual(result, "1.05 MB")
        result = hrunits.getSizeStringBitsBinary(1024**2)
        self.assertEqual(result, "1.00 Mibit")
        result = hrunits.getSizeStringBitsDecimal(1024**2)
        self.assertEqual(result, "1.05 Mbit")

    def test_binary_power_3(self):
        result = hrunits.getSizeStringBytesBinary(1024**3)
        self.assertEqual(result, "1.00 GiB")
        result = hrunits.getSizeStringBytesDecimal(1024**3)
        self.assertEqual(result, "1.07 GB")
        result = hrunits.getSizeStringBitsBinary(1024**3)
        self.assertEqual(result, "1.00 Gibit")
        result = hrunits.getSizeStringBitsDecimal(1024**3)
        self.assertEqual(result, "1.07 Gbit")

    def test_binary_power_4(self):
        result = hrunits.getSizeStringBytesBinary(1024**4)
        self.assertEqual(result, "1.00 TiB")
        result = hrunits.getSizeStringBytesDecimal(1024**4)
        self.assertEqual(result, "1.10 TB")
        result = hrunits.getSizeStringBitsBinary(1024**4)
        self.assertEqual(result, "1.00 Tibit")
        result = hrunits.getSizeStringBitsDecimal(1024**4)
        self.assertEqual(result, "1.10 Tbit")

    def test_binary_power_5(self):
        result = hrunits.getSizeStringBytesBinary(1024**5)
        self.assertEqual(result, "1.00 PiB")
        result = hrunits.getSizeStringBytesDecimal(1024**5)
        self.assertEqual(result, "1.13 PB")
        result = hrunits.getSizeStringBitsBinary(1024**5)
        self.assertEqual(result, "1.00 Pibit")
        result = hrunits.getSizeStringBitsDecimal(1024**5)
        self.assertEqual(result, "1.13 Pbit")

    def test_binary_power_6(self):
        result = hrunits.getSizeStringBytesBinary(1024**6)
        self.assertEqual(result, "1.00 EiB")
        result = hrunits.getSizeStringBytesDecimal(1024**6)
        self.assertEqual(result, "1.15 EB")
        result = hrunits.getSizeStringBitsBinary(1024**6)
        self.assertEqual(result, "1.00 Eibit")
        result = hrunits.getSizeStringBitsDecimal(1024**6)
        self.assertEqual(result, "1.15 Ebit")

    def test_binary_power_7(self):
        result = hrunits.getSizeStringBytesBinary(1024**7)
        self.assertEqual(result, "1.00 ZiB")
        result = hrunits.getSizeStringBytesDecimal(1024**7)
        self.assertEqual(result, "1.18 ZB")
        result = hrunits.getSizeStringBitsBinary(1024**7)
        self.assertEqual(result, "1.00 Zibit")
        result = hrunits.getSizeStringBitsDecimal(1024**7)
        self.assertEqual(result, "1.18 Zbit")

    def test_binary_power_8(self):
        result = hrunits.getSizeStringBytesBinary(1024**8)
        self.assertEqual(result, "1.00 YiB")
        result = hrunits.getSizeStringBytesDecimal(1024**8)
        self.assertEqual(result, "1.21 YB")
        result = hrunits.getSizeStringBitsBinary(1024**8)
        self.assertEqual(result, "1.00 Yibit")
        result = hrunits.getSizeStringBitsDecimal(1024**8)
        self.assertEqual(result, "1.21 Ybit")

    def test_binary_power_9(self):
        result = hrunits.getSizeStringBytesBinary(1024**9)
        self.assertEqual(result, "1024 YiB")
        result = hrunits.getSizeStringBytesDecimal(1024**9)
        self.assertEqual(result, "1238 YB")
        result = hrunits.getSizeStringBitsBinary(1024**9)
        self.assertEqual(result, "1024 Yibit")
        result = hrunits.getSizeStringBitsDecimal(1024**9)
        self.assertEqual(result, "1238 Ybit")



class TestHrEvenDecimalSizes(unittest.TestCase):
    """
    Test powers of 1000
    """

    def test_decimal_power_1(self):
        result = hrunits.getSizeStringBytesBinary(1000)
        self.assertEqual(result, "1000 B")
        result = hrunits.getSizeStringBytesDecimal(1000)
        self.assertEqual(result, "1.00 kB")
        result = hrunits.getSizeStringBitsBinary(1000)
        self.assertEqual(result, "1000 bit")
        result = hrunits.getSizeStringBitsDecimal(1000)
        self.assertEqual(result, "1.00 kbit")

    def test_decimal_power_2(self):
        result = hrunits.getSizeStringBytesBinary(1000**2)
        self.assertEqual(result, "977 KiB")
        result = hrunits.getSizeStringBytesDecimal(1000**2)
        self.assertEqual(result, "1.00 MB")
        result = hrunits.getSizeStringBitsBinary(1000**2)
        self.assertEqual(result, "977 Kibit")
        result = hrunits.getSizeStringBitsDecimal(1000**2)
        self.assertEqual(result, "1.00 Mbit")

    def test_decimal_power_3(self):
        result = hrunits.getSizeStringBytesBinary(1000**3)
        self.assertEqual(result, "954 MiB")
        result = hrunits.getSizeStringBytesDecimal(1000**3)
        self.assertEqual(result, "1.00 GB")
        result = hrunits.getSizeStringBitsBinary(1000**3)
        self.assertEqual(result, "954 Mibit")
        result = hrunits.getSizeStringBitsDecimal(1000**3)
        self.assertEqual(result, "1.00 Gbit")

    def test_decimal_power_4(self):
        result = hrunits.getSizeStringBytesBinary(1000**4)
        self.assertEqual(result, "931 GiB")
        result = hrunits.getSizeStringBytesDecimal(1000**4)
        self.assertEqual(result, "1.00 TB")
        result = hrunits.getSizeStringBitsBinary(1000**4)
        self.assertEqual(result, "931 Gibit")
        result = hrunits.getSizeStringBitsDecimal(1000**4)
        self.assertEqual(result, "1.00 Tbit")

    def test_decimal_power_5(self):
        result = hrunits.getSizeStringBytesBinary(1000**5)
        self.assertEqual(result, "909 TiB")
        result = hrunits.getSizeStringBytesDecimal(1000**5)
        self.assertEqual(result, "1.00 PB")
        result = hrunits.getSizeStringBitsBinary(1000**5)
        self.assertEqual(result, "909 Tibit")
        result = hrunits.getSizeStringBitsDecimal(1000**5)
        self.assertEqual(result, "1.00 Pbit")

    def test_decimal_power_6(self):
        result = hrunits.getSizeStringBytesBinary(1000**6)
        self.assertEqual(result, "888 PiB")
        result = hrunits.getSizeStringBytesDecimal(1000**6)
        self.assertEqual(result, "1.00 EB")
        result = hrunits.getSizeStringBitsBinary(1000**6)
        self.assertEqual(result, "888 Pibit")
        result = hrunits.getSizeStringBitsDecimal(1000**6)
        self.assertEqual(result, "1.00 Ebit")

    def test_decimal_power_7(self):
        result = hrunits.getSizeStringBytesBinary(1000**7)
        self.assertEqual(result, "867 EiB")
        result = hrunits.getSizeStringBytesDecimal(1000**7)
        self.assertEqual(result, "1.00 ZB")
        result = hrunits.getSizeStringBitsBinary(1000**7)
        self.assertEqual(result, "867 Eibit")
        result = hrunits.getSizeStringBitsDecimal(1000**7)
        self.assertEqual(result, "1.00 Zbit")

    def test_decimal_power_8(self):
        result = hrunits.getSizeStringBytesBinary(1000**8)
        self.assertEqual(result, "847 ZiB")
        result = hrunits.getSizeStringBytesDecimal(1000**8)
        self.assertEqual(result, "1.00 YB")
        result = hrunits.getSizeStringBitsBinary(1000**8)
        self.assertEqual(result, "847 Zibit")
        result = hrunits.getSizeStringBitsDecimal(1000**8)
        self.assertEqual(result, "1.00 Ybit")

    def test_decimal_power_9(self):
        result = hrunits.getSizeStringBytesBinary(1000**9)
        self.assertEqual(result, "827 YiB")
        result = hrunits.getSizeStringBytesDecimal(1000**9)
        self.assertEqual(result, "1000 YB")
        result = hrunits.getSizeStringBitsBinary(1000**9)
        self.assertEqual(result, "827 Yibit")
        result = hrunits.getSizeStringBitsDecimal(1000**9)
        self.assertEqual(result, "1000 Ybit")



class TestHrHugeSizes(unittest.TestCase):
    """
    Test very large sizes
    """

    #TODO: add a few very large size tests to make sure that we never fall off the top end of the units



class TestHrEdgeCases(unittest.TestCase):
    """
    Test exceptional cases
    """

    #TODO: define / implement appropriate behavior for invalid input - string not containing a pure number
    #TODO: define / implement appropriate behavior for string - containing text of a number
    #TODO: define / implement appropriate behavior for decimal input



if __name__ == '__main__':
    unittest.main()
