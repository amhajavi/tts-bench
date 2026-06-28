import re


def strip_commas_in_numbers(s: str) -> str:
    """Remove commas that appear between digits (e.g. 1,234 -> 1234)."""
    return re.sub(r'(?<=\d),(?=\d)', '', s)


def _has_dollar_mention(s: str) -> bool:
    """Return True if string contains a dollar sign or the word 'dollar(s)'."""
    return bool(re.search(r"\$|\bdollars?\b", s, flags=re.IGNORECASE))


def _dollar_sign_variant(s: str) -> str:
    """Normalize dollar mentions to the '$<number>' form.

    Examples:
        '$33'        -> '$33'
        '$ 33'       -> '$33'
        '33 dollars' -> '$33'
        '$1,234'     -> '$1234'   (commas in numbers are also stripped)
    """
    # Normalize '$ 33' or '$33' -> '$<digits>'
    out = re.sub(r'\$\s*(\d[\d,]*(?:\.\d+)?)', lambda m: '$' + m.group(1).replace(',', ''), s)
    # Normalize '33 dollars' -> '$33'  (must run after the $ form is already normalized)
    out = re.sub(r'(?i)\b(\d[\d,]*(?:\.\d+)?)\s+dollars?\b',
                 lambda m: '$' + m.group(1).replace(',', ''), out)
    return out


def _dollars_word_variant(s: str) -> str:
    """Normalize dollar mentions to the '<number> dollars' form.

    Examples:
        '$33'        -> '33 dollars'
        '$ 33'       -> '33 dollars'
        '33 dollars' -> '33 dollars'  (unchanged)
        '$1,234'     -> '1234 dollars'
    """
    # Normalize '$33' or '$ 33' -> '<digits> dollars'
    out = re.sub(r'\$\s*(\d[\d,]*(?:\.\d+)?)',
                 lambda m: m.group(1).replace(',', '') + ' dollars', s)
    # Normalize '33 dollars' -> '<digits> dollars'  (strips commas in the number)
    out = re.sub(r'(?i)\b(\d[\d,]*(?:\.\d+)?)\s+dollars?\b',
                 lambda m: m.group(1).replace(',', '') + ' dollars', out)
    return out


def compute_best_dollar_aware_error(ref: str, trans: str, metric_func) -> float:
    """Compute a WER/CER-style metric between *ref* and *trans*.

    If either string contains dollar mentions (``$`` or the word *dollar(s)*),
    the metric is evaluated over four normalization combos:

    * ``$<number>``        vs ``$<number>``
    * ``<number> dollars`` vs ``<number> dollars``

    The baseline (no normalization) is always included.  The **lowest** score
    across all evaluated combos is returned so that the metric rewards the TTS
    model regardless of which monetary form the ASR transcription picks.
    """
    scores = [metric_func(ref, trans)]

    if _has_dollar_mention(ref) or _has_dollar_mention(trans):
        ref_sign = _dollar_sign_variant(ref)
        ref_word = _dollars_word_variant(ref)
        trans_sign = _dollar_sign_variant(trans)
        trans_word = _dollars_word_variant(trans)

        for r, t in (
            (ref_sign, trans_sign),
            (ref_word, trans_word),
        ):
            try:
                scores.append(metric_func(r, t))
            except Exception:
                pass

    return min(scores)
