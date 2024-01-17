

def get_exception_group():
    exception_group = ExceptionGroup(
        "LerkaGroup", [
            ValueError("Lerka is not value..."),
            ModuleNotFoundError("Hi bro is not found..."),
            ModuleNotFoundError("Vlad is not memorized..."),
        ]
    )
    raise exception_group


# 1
try:
    get_exception_group()
except ExceptionGroup as exp:
    print(exp.exceptions)


# 2
try:
    get_exception_group()
except* ValueError as e:
    print(f"{e=}")
except* ModuleNotFoundError as e:
    for error in e.exceptions:
        print(str(error))
