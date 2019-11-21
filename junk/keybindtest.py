import msvcrt

class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        self.impl = self.readChar()

    def __call__(self): return self.impl()

    def readChar(echo=True):
        "Get a single character on Windows."
        while msvcrt.kbhit():
            msvcrt.getch()
        ch = msvcrt.getch()
        while ch in b'\x00\xe0':
            msvcrt.getch()
            ch = msvcrt.getch()
        if echo:
            msvcrt.putch(ch)
            print('char: {0}'.format(ch))
        return ch.decode()


getch = _Getch()
