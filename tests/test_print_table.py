from biocutils import format_table


def test_format_table():
    contents = [
        ["asdasd", "1", "2", "3", "4"],
        [""] + ["|"] * 4,
        ["asyudgausydga", "A", "B", "C", "D"],
    ]
    print(format_table(contents))
    print(format_table(contents, floating_names=["", "aarg", "boo", "ffoo", "stuff"]))
    print(format_table(contents, window=10))
    print(
        format_table(
            contents, window=10, floating_names=["", "AAAR", "BBBB", "XXX", "STUFF"]
        )
    )
