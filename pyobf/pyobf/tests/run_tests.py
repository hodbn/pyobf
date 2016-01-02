import sys
import pytest
import multiprocessing


def main():
    pytest.main(['-v', '-s', '-n', '%d' % (multiprocessing.cpu_count(), )])


if __name__ == '__main__':
    sys.exit(main())
