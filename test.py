if __name__ == '__main__':
    from amatino.tests.test_sequence import SEQUENCE
    for test in SEQUENCE:
        instance = test()
        instance.execute()
        print(instance.report())