from pytest_cases import get_case_id


def IDGen(case_fun):
    return "#%s#" % get_case_id(case_fun)
