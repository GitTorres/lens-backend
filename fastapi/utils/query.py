from functools import reduce
from typing import List, Tuple, TypedDict, Union


def build_filter_query(params: List[Tuple]):
    """
    Build a filter query from a given set of parameters.

    Input:
    - params: List[(name: str, val: Union[str, float], op: str)]

    Output: Dict
    """

    def _to_SON(name: str, val: Union[str, float], op: str):
        # return valid SON for a given operator
        assert op in ["$eq", "$gt", "$gte", "$lt", "$lte", "$regex"]

        if op == "$eq":
            return {name: val}
        elif op in ["$gt", "$gte", "$lt", "$lte"]:
            return {name: {op: val}}
        else:  # op == '$regex'
            return {name: {"$regex": val}}

    return reduce(
        lambda query, filter_item: {**query, **_to_SON(*filter_item)}, params, {}
    )
