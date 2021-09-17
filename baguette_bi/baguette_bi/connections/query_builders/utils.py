import math
from typing import Tuple


def determine_bin_size(
    extent,
    anchor=None,
    base=10,
    divide=[5, 2],
    maxbins=10,
    minstep=0,
    nice=True,
    step=None,
    steps=None,
) -> Tuple:  # start, stop, step
    """Reference:
    https://github.com/vega/vega/blob/master/packages/vega-statistics/src/bin.js
    https://github.com/vega/vega/blob/master/packages/vega-transforms/src/Bin.js
    The function was kinda-mindlessly ported from the links. I don't really understand
    everything it does.
    """
    mi, ma = extent
    logb = math.log(base)
    span = ma - mi
    if step is None:  # if step size is explicitly given, use that
        if steps is not None:
            # if provided, limit choice to acceptable step sizes
            step = next(s for s in steps if s < span / maxbins)  # get first value
        else:
            # else use span to determine step size
            level = math.ceil(math.log(maxbins) / logb)
            step = max(
                minstep,
                math.pow(base, round(math.log(span) / logb) - level),
            )
            # increase step size if too many bins
            while math.ceil(span / step) > maxbins:
                step *= base
            # decrease step size if allowed
            for d in divide:
                v = step / d
                if v >= minstep and span / v <= maxbins:
                    step = v
    # update precision, min and max (what?)
    v = math.log(step)
    precision = 0 if v >= 0 else int(-v / logb)  # int here is equivalent to js ~~
    eps = pow(base, -precision - 1)
    if nice:
        v = math.floor(mi / step + eps) * step
        mi = v - step if mi < v else v
        ma = math.ceil(ma / step) * step
    start = mi
    stop = mi + step if ma == mi else ma

    # now the statistics function is done, but there's also anchor implemented in the
    # transform itself
    if anchor is not None:
        d = anchor - (start + step * math.floor((anchor - start) / step))
        start += d
        stop += d

    return start, stop, step
