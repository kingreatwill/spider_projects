


import base64
from Cryptodome.Cipher import AES


def decrypt(_str):
    iv = "amlheW91LHFpYW53".encode(encoding='utf-8')
    key = 'anN2bXA2NjYsamlh'.encode(encoding='utf-8')
    cryptor = AES.new(key=key, mode=AES.MODE_CFB, IV=iv, segment_size=128)
    decode = base64.b64decode(_str)
    plain_text = cryptor.decrypt(decode)
    # json_object = json.loads(plain_text)
    # json_formatted_str = json.dumps(json_object, indent=2)
    # print(json_formatted_str)
    _plain_text = str(plain_text, encoding='utf-8')
    print(_plain_text)
    return _plain_text

if __name__ == '__main__':
    # data1 = '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'
    # decrypt(data1)
    data2 = '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'
    decrypt(data2)


