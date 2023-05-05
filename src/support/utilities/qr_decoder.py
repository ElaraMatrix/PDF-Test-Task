import zxing

reader = zxing.BarCodeReader()


def decode(filepath):
    data = reader.decode(filepath)
    return data
