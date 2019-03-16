EXECUTION_MESSAGE = """Beginning Amatino Python test sequence"""

if __name__ == '__main__':
    from amatino.tests.test_sequence import SEQUENCE
    print(EXECUTION_MESSAGE)
    for test in SEQUENCE:
        instance = test()
        instance.execute()
        print(instance.report())
