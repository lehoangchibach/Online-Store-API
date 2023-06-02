def get_ownership(item, identity):
    item = item.__dict__
    item["is_creator"] = identity == item["creator_id"]
    return item


def get_ownership_list(items, identity):
    result = []
    for item in items:
        item = item.__dict__
        item["is_creator"] = identity == item["creator_id"]
        result.append(item)
    return result
