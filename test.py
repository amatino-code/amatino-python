import sys

EXECUTION_MESSAGE = """Beginning Amatino Python test sequence"""

ONE_ONLY = False
if '--single' in sys.argv[1:] or '-s' in sys.argv[1:]:
    ONE_ONLY = True

START_INDEX = 0
i = 0
for argument in sys.argv[1:]:
    if argument == '--index' or argument == '-i':
        START_INDEX = int(sys.argv[1:][i + 1]) - 1
        break
    i += 1

if __name__ == '__main__':
    from amatino.tests.test_sequence import SEQUENCE
    print(EXECUTION_MESSAGE)
    i = -1
    for test in SEQUENCE:
        i += 1
        if i < START_INDEX:
            continue
        instance = test()
        instance.execute()
        print(instance.report(i + 1))
        if ONE_ONLY:
            break
        continue
