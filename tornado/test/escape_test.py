#!/usr/bin/env python



import tornado.escape
import unittest

from tornado.escape import utf8, xhtml_escape, xhtml_unescape, url_escape, url_unescape, to_unicode, json_decode, json_encode
from tornado.util import b

linkify_tests = [
    # (input, linkify_kwargs, expected_output)

    ("hello http://world.com/!", {},
     'hello <a href="http://world.com/">http://world.com/</a>!'),

    ("hello http://world.com/with?param=true&stuff=yes", {},
     'hello <a href="http://world.com/with?param=true&amp;stuff=yes">http://world.com/with?param=true&amp;stuff=yes</a>'),

    # an opened paren followed by many chars killed Gruber's regex
    ("http://url.com/w(aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", {},
     '<a href="http://url.com/w">http://url.com/w</a>(aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'),

    # as did too many dots at the end
    ("http://url.com/withmany.......................................", {},
     '<a href="http://url.com/withmany">http://url.com/withmany</a>.......................................'),

    ("http://url.com/withmany((((((((((((((((((((((((((((((((((a)", {},
     '<a href="http://url.com/withmany">http://url.com/withmany</a>((((((((((((((((((((((((((((((((((a)'),

    # some examples from http://daringfireball.net/2009/11/liberal_regex_for_matching_urls
    # plus a fex extras (such as multiple parentheses).
    ("http://foo.com/blah_blah", {},
     '<a href="http://foo.com/blah_blah">http://foo.com/blah_blah</a>'),

    ("http://foo.com/blah_blah/", {},
     '<a href="http://foo.com/blah_blah/">http://foo.com/blah_blah/</a>'),

    ("(Something like http://foo.com/blah_blah)", {},
     '(Something like <a href="http://foo.com/blah_blah">http://foo.com/blah_blah</a>)'),

    ("http://foo.com/blah_blah_(wikipedia)", {},
     '<a href="http://foo.com/blah_blah_(wikipedia)">http://foo.com/blah_blah_(wikipedia)</a>'),

    ("http://foo.com/blah_(blah)_(wikipedia)_blah", {},
     '<a href="http://foo.com/blah_(blah)_(wikipedia)_blah">http://foo.com/blah_(blah)_(wikipedia)_blah</a>'),

    ("(Something like http://foo.com/blah_blah_(wikipedia))", {},
     '(Something like <a href="http://foo.com/blah_blah_(wikipedia)">http://foo.com/blah_blah_(wikipedia)</a>)'),

    ("http://foo.com/blah_blah.", {},
     '<a href="http://foo.com/blah_blah">http://foo.com/blah_blah</a>.'),

    ("http://foo.com/blah_blah/.", {},
     '<a href="http://foo.com/blah_blah/">http://foo.com/blah_blah/</a>.'),

    ("<http://foo.com/blah_blah>", {},
     '&lt;<a href="http://foo.com/blah_blah">http://foo.com/blah_blah</a>&gt;'),

    ("<http://foo.com/blah_blah/>", {},
     '&lt;<a href="http://foo.com/blah_blah/">http://foo.com/blah_blah/</a>&gt;'),

    ("http://foo.com/blah_blah,", {},
     '<a href="http://foo.com/blah_blah">http://foo.com/blah_blah</a>,'),

    ("http://www.example.com/wpstyle/?p=364.", {},
     '<a href="http://www.example.com/wpstyle/?p=364">http://www.example.com/wpstyle/?p=364</a>.'),

    ("rdar://1234",
     {"permitted_protocols": ["http", "rdar"]},
     '<a href="rdar://1234">rdar://1234</a>'),

    ("rdar:/1234",
     {"permitted_protocols": ["rdar"]},
     '<a href="rdar:/1234">rdar:/1234</a>'),

    ("http://userid:password@example.com:8080", {},
     '<a href="http://userid:password@example.com:8080">http://userid:password@example.com:8080</a>'),

    ("http://userid@example.com", {},
     '<a href="http://userid@example.com">http://userid@example.com</a>'),

    ("http://userid@example.com:8080", {},
     '<a href="http://userid@example.com:8080">http://userid@example.com:8080</a>'),

    ("http://userid:password@example.com", {},
     '<a href="http://userid:password@example.com">http://userid:password@example.com</a>'),

    ("message://%3c330e7f8409726r6a4ba78dkf1fd71420c1bf6ff@mail.gmail.com%3e",
     {"permitted_protocols": ["http", "message"]},
     '<a href="message://%3c330e7f8409726r6a4ba78dkf1fd71420c1bf6ff@mail.gmail.com%3e">message://%3c330e7f8409726r6a4ba78dkf1fd71420c1bf6ff@mail.gmail.com%3e</a>'),

    ("http://\u27a1.ws/\u4a39", {},
     '<a href="http://\u27a1.ws/\u4a39">http://\u27a1.ws/\u4a39</a>'),

    ("<tag>http://example.com</tag>", {},
     '&lt;tag&gt;<a href="http://example.com">http://example.com</a>&lt;/tag&gt;'),

    ("Just a www.example.com link.", {},
     'Just a <a href="http://www.example.com">www.example.com</a> link.'),

    ("Just a www.example.com link.",
     {"require_protocol": True},
     'Just a www.example.com link.'),

    ("A http://reallylong.com/link/that/exceedsthelenglimit.html",
     {"require_protocol": True, "shorten": True},
     'A <a href="http://reallylong.com/link/that/exceedsthelenglimit.html" title="http://reallylong.com/link/that/exceedsthelenglimit.html">http://reallylong.com/link...</a>'),

    ("A http://reallylongdomainnamethatwillbetoolong.com/hi!",
     {"shorten": True},
     'A <a href="http://reallylongdomainnamethatwillbetoolong.com/hi" title="http://reallylongdomainnamethatwillbetoolong.com/hi">http://reallylongdomainnametha...</a>!'),

    ("A file:///passwords.txt and http://web.com link", {},
     'A file:///passwords.txt and <a href="http://web.com">http://web.com</a> link'),

    ("A file:///passwords.txt and http://web.com link",
     {"permitted_protocols": ["file"]},
     'A <a href="file:///passwords.txt">file:///passwords.txt</a> and http://web.com link'),

    ("www.external-link.com",
     {"extra_params": 'rel="nofollow" class="external"'},
     '<a href="http://www.external-link.com" rel="nofollow" class="external">www.external-link.com</a>'),

    ("www.external-link.com and www.internal-link.com/blogs extra",
     {"extra_params": lambda href:'class="internal"' if href.startswith("http://www.internal-link.com") else 'rel="nofollow" class="external"'},
     '<a href="http://www.external-link.com" rel="nofollow" class="external">www.external-link.com</a> and <a href="http://www.internal-link.com/blogs" class="internal">www.internal-link.com/blogs</a> extra'),

    ("www.external-link.com",
     {"extra_params": lambda href:'    rel="nofollow" class="external"  '},
     '<a href="http://www.external-link.com" rel="nofollow" class="external">www.external-link.com</a>'),
]


class EscapeTestCase(unittest.TestCase):
    def test_linkify(self):
        for text, kwargs, html in linkify_tests:
            linked = tornado.escape.linkify(text, **kwargs)
            self.assertEqual(linked, html)

    def test_xhtml_escape(self):
        tests = [
            ("<foo>", "&lt;foo&gt;"),
            ("<foo>", "&lt;foo&gt;"),
            (b("<foo>"), b("&lt;foo&gt;")),

            ("<>&\"", "&lt;&gt;&amp;&quot;"),
            ("&amp;", "&amp;amp;"),
            ]
        for unescaped, escaped in tests:
            self.assertEqual(utf8(xhtml_escape(unescaped)), utf8(escaped))
            self.assertEqual(utf8(unescaped), utf8(xhtml_unescape(escaped)))

    def test_url_escape(self):
        tests = [
            # byte strings are passed through as-is
            ('\u00e9'.encode('utf8'), '%C3%A9'),
            ('\u00e9'.encode('latin1'), '%E9'),

            # unicode strings become utf8
            ('\u00e9', '%C3%A9'),
            ]
        for unescaped, escaped in tests:
            self.assertEqual(url_escape(unescaped), escaped)

    def test_url_unescape(self):
        tests = [
            ('%C3%A9', '\u00e9', 'utf8'),
            ('%C3%A9', '\u00c3\u00a9', 'latin1'),
            ('%C3%A9', utf8('\u00e9'), None),
            ]
        for escaped, unescaped, encoding in tests:
            # input strings to url_unescape should only contain ascii
            # characters, but make sure the function accepts both byte
            # and unicode strings.
            self.assertEqual(url_unescape(to_unicode(escaped), encoding), unescaped)
            self.assertEqual(url_unescape(utf8(escaped), encoding), unescaped)

    def test_escape_return_types(self):
        # On python2 the escape methods should generally return the same
        # type as their argument
        self.assertEqual(type(xhtml_escape("foo")), str)
        self.assertEqual(type(xhtml_escape("foo")), str)

    def test_json_decode(self):
        # json_decode accepts both bytes and unicode, but strings it returns
        # are always unicode.
        self.assertEqual(json_decode(b('"foo"')), "foo")
        self.assertEqual(json_decode('"foo"'), "foo")

        # Non-ascii bytes are interpreted as utf8
        self.assertEqual(json_decode(utf8('"\u00e9"')), "\u00e9")

    def test_json_encode(self):
        # json deals with strings, not bytes, but our encoding function should
        # accept bytes as well as long as they are utf8.
        self.assertEqual(json_decode(json_encode("\u00e9")), "\u00e9")
        self.assertEqual(json_decode(json_encode(utf8("\u00e9"))), "\u00e9")
        self.assertRaises(UnicodeDecodeError, json_encode, b("\xe9"))