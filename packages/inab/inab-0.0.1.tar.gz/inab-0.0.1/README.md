When reading a file containing bytes using Python, you are often looking to read it like this b"\xd8\xa7\xd9\x84\xd8\xa8\xd9\x84\xd9\x8a\xd8\xba, 
for example
o = open("bytes.txt", "rb")
y = x.read()
In fact, the exit is like this b"\\\xd8\\\xa7\\\xd9\\\x84\\\xd8\\\xa8\\\xd9\\\x84\\\xd9\\\x8a\\\xd8\\\xba, and when you try to decode it, you will get this back \xd8\xa7\xd9\x84\xd8\xa8\xd9\x84\xd9\x8a\xd8\xba, but it is a literal type, and whenever you code it, it will give you two slashback, and when you decode it, it takes you back to \xd8\xa7\xd9\x84\xd8\xa8\xd9\x84\xd9\x8a\xd8\xba.
This problem I encountered when I was scraping a website and recving the data in bytes in a string type that included HTML. and it will face you in the future or you may have encountered before,
I recently built a library to solve this problem where it is enough to pass it a byte with two slashback and it will decode it to the original text.

# decode arabic utf-8 
from inab import arabic_de
str_bytes = "\\\xd8\\\xa7\\\xd9\\\x84\\\xd8\\\xa8\\\xd9\\\x84\\\xd9\\\x8a\\\xd8\\\xba"
x = bytes(str_bytes, "utf-8")
print(x)
text = arabic_de(x)
print(text)

# decode english utf-16
from inab import eng_de
str_bytes = "\\\xff\\\xfei\\\x00n\\\x00a\\\x00b\\\x00 \\\x00l\\\x00i\\\x00b\\\x00"
text = eng_de(str_bytes)
print(text)