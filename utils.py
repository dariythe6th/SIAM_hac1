import ast

def safe_parse_intervals(s):
    """
    Преобразует строковое представление списка в настоящий список с помощью ast.literal_eval.
    Это безопаснее, чем использование eval.
    """
    return ast.literal_eval(s)
