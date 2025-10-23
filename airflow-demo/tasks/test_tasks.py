from airflow.decorators import task


@task
def do_something(some_str: str) -> list[str]:
    return list(some_str)


if __name__ == "__main__":
    some_list = do_something("Hello")  # -> ["H", "e", ...]
    for i in some_list:
        print(i)