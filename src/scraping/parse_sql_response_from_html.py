import re
import typing


def parse_sql_response_from_html(text: str, names: list, prefix: str, suffix: str) -> typing.List[
    typing.Tuple[str, str]]:
    names_group = f'({"|".join([name for name in names])})'
    prefix_escaped = re.escape(prefix)
    suffix_escaped = re.escape(suffix)
    pattern = f'{prefix_escaped}{names_group}:(.+?){suffix_escaped}'
    return re.findall(pattern, text, re.I)
