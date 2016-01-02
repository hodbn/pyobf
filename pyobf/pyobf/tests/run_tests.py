import sys
import pytest
import multiprocessing


def main():
    if len(sys.argv) > 1 and sys.argv[1] == '-p':
        pytest.main(['-v', '-s', '-n', '%d' % (multiprocessing.cpu_count(), )])
    else:
        pytest.main(['-v'])


if __name__ == '__main__':
    sys.exit(main())
