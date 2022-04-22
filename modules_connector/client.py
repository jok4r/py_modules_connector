import rsa
import oe_common
import struct
from ov_aes_cipher import AESCipher


class Client:
    def __init__(self, filename):
        self.filename = filename
        # self.aes = AESCipher(key=str(random.randint(100, 100 ** 5)))
        self.rsa_public = None
        self.struct_type = '<Q'
        self.struct_size = struct.calcsize(self.struct_type)
        self.init_file()

    def init_file(self):
        with open(self.filename, 'rb') as f:
            size = struct.unpack(self.struct_type, f.read(self.struct_size))[0]
            self.rsa_public = rsa.PublicKey.load_pkcs1(f.read(size))

    def write(self, data):
        aes = AESCipher(key=oe_common.get_rnd_string(100))
        with open(self.filename, 'rb+') as f:
            key_size = struct.unpack(self.struct_type, f.read(self.struct_size))[0]
            pub_key = rsa.PublicKey.load_pkcs1(f.read(key_size))
            if not isinstance(data, bytes):
                data = data.encode()
            data_aes = aes.encrypt(data)
            aes_key_rsa = rsa.encrypt(aes.key, pub_key)
            aes_key_rsa_len = struct.pack(self.struct_type, len(aes_key_rsa))
            f.write(aes_key_rsa_len)
            # print('public_key:', pub_key)
            # print('aes_key_rsa:', aes_key_rsa)
            f.write(aes_key_rsa)
            # f.write(rsa.encrypt(aes.key, self.rsa_public))
            data_len = struct.pack(self.struct_type, len(data_aes))
            f.write(data_len)
            f.write(data_aes)
        # print('sent data aes: %s' % data_aes)
        # print('sent data is: %s' % data)
