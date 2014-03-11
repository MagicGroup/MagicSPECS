import gpgme
from StringIO import StringIO

ctx = gpgme.Context()
ctx.armor = True

key = ctx.get_key('B10A449E4CFB9A60A2DB996701AF93D991CFA34D')

plain = StringIO('Hello World\n')
cipher = StringIO()

ctx.encrypt([key], 0, plain, cipher)

print cipher.getvalue()
