import re
from emoji import is_emoji

CODE_REGEX = re.compile(r"[a-f1-9][a-f0-9]{3,5}$")


def alias_to_name(alias: str) -> str:
    """
    Transform a unicode alias to an emoji name.

    Example usages:
    >>> alias_to_name(":falling_leaf:")
    "Falling leaf"
    >>> alias_to_name(":family_man_girl_boy:")
    "Family man girl boy"
    """
    name = alias[1:-1].replace("_", " ")
    return name.capitalize()


def get_codepoint(emoji: str) -> str:
    """
    Returns the codepoint, in a trimmed format, of a single emoji.

    `emoji` should be an emoji character, such as "🐍" and "🥰", and
    not a codepoint like "1f1f8". When working with combined emojis,
    such as "🇸🇪" and "👨‍👩‍👦", send the component emojis through the method
    one at a time.
    """
    return hex(ord(emoji))[2:]


def trim_code(codepoint: str | None) -> str | None:
    """
    Returns the meaningful information from the given `codepoint`.

    If no codepoint is found, `None` is returned.

    Example usages:
    >>> trim_code("U+1f1f8")
    "1f1f8"
    >>> trim_code("\u0001f1f8")
    "1f1f8"
    >>> trim_code("1f466")
    "1f466"
    """
    if not codepoint:
        return None
    if code := CODE_REGEX.search(codepoint):
        return code.group()


def get_emoji(codepoint: str) -> str:
    """
    Returns the emoji corresponding to a given `codepoint`, or `""` if no emoji was found.

    The return value is an emoji character, such as "🍂". The `codepoint`
    argument can be of any format, since it will be trimmed automatically.
    """
    if code := trim_code(codepoint):
        return chr(int(code, 16))
    return ""


def codepoint_from_input(raw_emoji: str) -> str:
    """
    Returns the codepoint corresponding to the passed tuple, separated by "-".

    The return format matches the format used in URLs for emoji source files.

    Example usages:
    >>> codepoint_from_input(("🐍",))
    "1f40d"
    >>> codepoint_from_input(("1f1f8", "1f1ea"))
    "1f1f8-1f1ea"
    >>> codepoint_from_input(("👨‍👧‍👦",))
    "1f468-200d-1f467-200d-1f466"
    """
    emoji_list: list[str] = [emoji.lower() for emoji in raw_emoji.split()]
    if is_emoji(emoji_list[0]):
        emojis = (get_codepoint(emoji) for emoji in emoji_list[0])
        return "-".join(emojis)

    emoji = "".join(get_emoji(trim_code(code)) for code in emoji_list)  # type: ignore
    if is_emoji(emoji):
        return "-".join(get_codepoint(e) for e in emoji)

    raise ValueError("No codepoint could be obtained from the given input")
