import random
from collections import defaultdict

def create_balanced_subset(captures, x):
    """
    Create a balanced subset of capture_ids with at most x captures contributed per class.

    Args:
        captures (dict): Dict of capture_id to capture dict with 'Entities' list.
        x (int): Maximum number of captures contributed by each class.

    Returns:
        list: List of capture_ids for the subset.
    """
    # Collect all entities with their capture_id
    entities = []
    for cap_id, cap in captures.items():
        for entity in cap['Entities']:
            entities.append((cap_id, entity['FineClassName']))

    # Group by class and build capture-class membership
    class_groups = defaultdict(list)
    capture_class_sets = defaultdict(set)
    for cap_id, cls in entities:
        class_groups[cls].append(cap_id)
        capture_class_sets[cap_id].add(cls)

    # Convert per-class capture lists to unique ordered lists
    unique_class_caps = {
        cls: list(dict.fromkeys(cap_ids))
        for cls, cap_ids in class_groups.items()
    }
    sorted_classes = sorted(unique_class_caps.keys(), key=lambda c: len(unique_class_caps[c]), reverse=True)

    selected_captures = set()
    for cls in sorted_classes:
        cap_ids = unique_class_caps[cls]
        # Count how many selected captures already contain this class
        selected_captures_for_cls = len(selected_captures.intersection(cap_ids))
        captures_to_add_for_cls = max(0, x - selected_captures_for_cls)
        if captures_to_add_for_cls == 0:
            continue

        # Select new captures for this class without exceeding x contributions
        remaining_caps = [cap_id for cap_id in cap_ids if cap_id not in selected_captures]
        remaining_caps.sort(key=lambda cap_id: len(capture_class_sets[cap_id] - {cls}))
        selected_captures.update(remaining_caps[:captures_to_add_for_cls])

    return list(selected_captures)