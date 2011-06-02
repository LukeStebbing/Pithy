from __future__ import unicode_literals
import codecs
import os
import os.path as pth

from six import text_type as str

from pithy import F


class PathFactory(object):

    def __call__(self, *parts):
        return Path(pth.normpath(pth.expanduser(pth.join(*parts))))

    @property
    def cwd(self):
        return P(os.getcwd())


P = PathFactory()


class Path(str):

    def __format__(self, spec=''):
        return self.replace(P('~'), '~') if spec == '~' else self

    @property
    def absolute(self):
        return P(pth.abspath(self))

    @property
    def exists(self):
        return pth.exists(self)

    @property
    def is_file(self):
        return pth.isfile(self)

    def remove(self):
        os.remove(self)

    def open(self, mode='r'):
        return codecs.open(self, mode, encoding='utf-8')

    @property
    def lines(self):
        with self.open() as stream:
            return [line.rstrip('\n') for line in stream]

    @lines.setter
    def lines(self, lines):
        with self.open('w') as stream:
            stream.writelines(str(line) + '\n' for line in lines)
