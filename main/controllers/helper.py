def get_ownership(item, identity):
    result = dict()
    for key, value in item.__dict__.items():
        if key == "creator_id":
            result["is_creator"] = identity == value
        else:
            result[key] = value
    return result


def get_ownership_list(items, identity):
    result = []
    for item in items:
        result.append(get_ownership(item, identity))
    return result
