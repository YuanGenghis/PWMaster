class Hash(object):
    """ Common class for all hash methods.
    
    It copies the one of the hashlib module (https://docs.python.org/3.5/library/hashlib.html).
    """
    
    def __init__(self, *args, **kwargs):
        """ Create the Hash object."""
        self.name = self.__class__.__name__  # https://docs.python.org/3.5/library/hashlib.html#hashlib.hash.name
        self.byteorder   = 'little'
        self.digest_size = 0                # https://docs.python.org/3.5/library/hashlib.html#hashlib.hash.digest_size
        self.block_size  = 0                # https://docs.python.org/3.5/library/hashlib.html#hashlib.hash.block_size

    def __str__(self):
        return self.name
        
    def update(self, arg):
        """ Update the hash object with the object arg, which must be interpretable as a buffer of bytes."""
        pass

    def digest(self):
        """ Return the digest of the data passed to the update() method so far. This is a bytes object of size digest_size which may contain bytes in the whole range from 0 to 255."""
        return b""

    def hexdigest(self):
        """ Like digest() except the digest is returned as a string object of double length, containing only hexadecimal digits. This may be used to exchange the value safely in email or other non-binary environments."""
        digest = self.digest()
        raw = digest.to_bytes(self.digest_size, byteorder=self.byteorder)
        format_str = '{:0' + str(2 * self.digest_size) + 'x}'
        return format_str.format(int.from_bytes(raw, byteorder='big'))