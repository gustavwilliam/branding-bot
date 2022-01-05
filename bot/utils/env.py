def env_list(
    data: str | None,
    type_: type = str,
    delimiter: str = ",",
) -> list | None:
    """
    Splits the given `data` and returns a list of values, with the given `output_type`.

    Returns `None` if `data` is `None`
    """
    if data is not None:
        return [type_(item) for item in data.split(delimiter)]
