import re

lowercase_words = {
    "a",  # articles
    "an",
    "the",
    "for",
    "and",  # coordinate conjunctions
    "nor",
    "but",
    "or",
    "yet",
    "so",
    "at",  # prepositions
    "around",
    "by",
    "after",
    "along",
    "for",
    "from",
    "of",
    "on",
    "to",
    "with",
    "without",
    "ca",
    "circa",
    "per",
    "over",
}


split = re.compile(r"([A-Z](?![a-z]))+|[A-Z][a-z]*|\d+")


def class_to_name(class_name):
    result = []
    for match in split.finditer(class_name):
        group = match.group()
        lower = group.lower()
        if lower in lowercase_words:
            result.append(lower)
            continue
        result.append(group)
    return " ".join(result)
