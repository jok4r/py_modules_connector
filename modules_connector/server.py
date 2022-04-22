import rsa
import os
import struct
from ov_aes_cipher import AESCipher


class Server:
    def __init__(self, filename, callback):
        self.filename = filename
        self.callback = callback
        # self.aes = AESCipher(key=str(random.randint(100, 100 ** 5)))
        self.rsa_public, self.rsa_private = rsa.newkeys(2048)
        self.struct_type = '<Q'
        self.struct_size = struct.calcsize(self.struct_type)
        self.init_file()

    def init_file(self):
        if os.path.isdir(self.filename):
            raise OSError('%s is directory, can not create it' % self.filename)
        spk = rsa.PublicKey.save_pkcs1(self.rsa_public)

        with open(self.filename, 'wb') as f:
            f.write(struct.pack(self.struct_type, len(spk)))
            f.write(spk)

    def read(self):
        file_size = os.stat(self.filename).st_size
        with open(self.filename, 'rb') as f:
            key_size = struct.unpack(self.struct_type, f.read(self.struct_size))[0]
            # f.seek(int(size))
            f.read(key_size)
            if f.tell() + self.struct_size >= file_size:
                return
            aes_key_size = struct.unpack(self.struct_type, f.read(self.struct_size))[0]
            # print('public_key:', self.rsa_public)
            # print('private key:', self.rsa_private)
            aes_key_rsa = f.read(aes_key_size)
            # print('aes_key_rsa:', aes_key_rsa)
            aes_key = rsa.decrypt(aes_key_rsa, self.rsa_private)
            aes = AESCipher(hash_key=aes_key)
            size = struct.unpack(self.struct_type, f.read(self.struct_size))[0]
            data_aes = f.read(size)
            data = aes.decrypt(data_aes)
        # print('received data_aes: %s' % data_aes)
        # print('received data is: %s' % data)
        self.callback(data.decode())
