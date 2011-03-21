import math

def get_tag_sizes(cls, collection):
    tag_sizes = {}

    if cls == 'group':
        total = sum(len(group.nodes) for group in collection)

        for item in collection:
            weight = math.log(len(item.nodes) or 1 * 4) + 12
            tag_sizes[item.name] = int(weight)

    return tag_sizes

