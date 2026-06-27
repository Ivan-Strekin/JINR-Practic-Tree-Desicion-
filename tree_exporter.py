import numpy as np


class BinaryTreeArrayExporter:

    #Преобразует обученное дерево в массив бинарного дерева.

    def __init__(self, model, feature_names, class_map):
        self.model = model
        self.feature_names = feature_names
        self.class_map = class_map
        self.items = {}

    def export(self, X, y):
        self.items = {}
        self._walk(
            node=self.model.root,
            X=X.values,
            y=y.values,
            index=0,
            depth=0,
            branch="Корень"
        )

        if not self.items:
            return []

        max_index = max(self.items.keys())
        result = [None] * (max_index + 1)
        for index, item in self.items.items():
            result[index] = item
        return result

    def _class_counts(self, y):
        counts = np.bincount(y, minlength=len(self.class_map))
        return [
            {
                "class_id": int(class_id),
                "name": self.class_map[class_id],
                "count": int(counts[class_id])
            }
            for class_id in range(len(self.class_map))
        ]

    def _walk(self, node, X, y, index, depth, branch):
        entropy = float(self.model._entropy(y))
        counts = self._class_counts(y)
        object_count = int(len(y))

        item = {
            "index": index,
            "depth": depth,
            "branch": branch,
            "entropy": round(entropy, 4),
            "object_count": object_count,
            "objects": counts,
            "is_leaf": node.value is not None,
            "prediction": self.class_map[int(node.value)] if node.value is not None else None,
            "question": None,
            "feature": None,
            "threshold": None,
            "left_index": None,
            "right_index": None,
        }

        if node.value is None:
            feature_name = self.feature_names[node.feature]
            threshold = float(node.threshold)
            left_mask = X[:, node.feature] <= threshold

            item.update({
                "question": f"{feature_name} <= {threshold:.4f}",
                "feature": feature_name,
                "threshold": round(threshold, 4),
                "left_index": 2 * index + 1,
                "right_index": 2 * index + 2,
            })

            self.items[index] = item

            self._walk(
                node=node.left,
                X=X[left_mask],
                y=y[left_mask],
                index=2 * index + 1,
                depth=depth + 1,
                branch="Да"
            )
            self._walk(
                node=node.right,
                X=X[~left_mask],
                y=y[~left_mask],
                index=2 * index + 2,
                depth=depth + 1,
                branch="Нет"
            )
        else:
            self.items[index] = item
