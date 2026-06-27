import numpy as np


class Node:
    def __init__(self, feature=None, threshold=None, left=None, right=None, value=None):
        self.feature = feature     # Индекс колонки, по которой делим
        self.threshold = threshold # Число-порог для разделения
        self.left = left           # Ссылка на левый узел, ветка "ДА"
        self.right = right         # Ссылка на правый узел, ветка "НЕТ"
        self.value = value         # Если это конечный узел, тут хранится ответ


class MyDecisionTree:
    def __init__(self, max_depth=5, verbose=False):
        # verbose - активатор консольного вывода структуры дерева решений для тестов, для стандартной работы он не требуется.
        self.max_depth = max_depth
        self.verbose = verbose
        self.root = None

    def _entropy(self, y):
        if len(y) == 0:
            return 0
        proportions = np.bincount(y) / len(y)
        return -np.sum([p * np.log2(p + 1e-9) for p in proportions if p > 0])

    def _information_gain(self, y, y_left, y_right):
        parent_entropy = self._entropy(y)
        n = len(y)
        n_l, n_r = len(y_left), len(y_right)
        child_entropy = (n_l / n) * self._entropy(y_left) + (n_r / n) * self._entropy(y_right)
        return parent_entropy - child_entropy

    def _best_split(self, X, y):
        best_gain = -1
        split_idx, split_thr = None, None
        for idx in range(X.shape[1]):
            thresholds = np.unique(X[:, idx])
            for thr in thresholds:
                left_mask = X[:, idx] <= thr
                if not np.any(left_mask) or not np.any(~left_mask):
                    continue
                gain = self._information_gain(y, y[left_mask], y[~left_mask])
                if gain > best_gain:
                    best_gain, split_idx, split_thr = gain, idx, thr
        return split_idx, split_thr

    def _build_tree(self, X, y, depth=0):
        num_samples = len(y)
        current_entropy = self._entropy(y)
        counts = np.bincount(y, minlength=3)

        indent = "  " * depth
        if self.verbose:
            stats = (
                f"Алкоголь 1-го типа: {counts[0]}, "
                f"Алкоголь 2-го типа: {counts[1]}, "
                f"Алкоголь 3-го типа: {counts[2]}"
            )
            print(f"{indent}УЗЕЛ (глубина {depth}): {num_samples} об. [{stats}], Энтропия: {current_entropy:.4f}")

        if len(np.unique(y)) == 1 or depth >= self.max_depth or num_samples < 2:
            leaf_val = np.argmax(counts)
            class_names = {
                0: "Алкоголь 1-го типа",
                1: "Алкоголь 2-го типа",
                2: "Алкоголь 3-го типа"
            }
            if self.verbose:
                print(f"{indent}  --> УЗЕЛ: классифицирован как [{class_names[leaf_val]}]")
            return Node(value=leaf_val)

        idx, thr = self._best_split(X, y)
        if idx is None:
            return Node(value=np.argmax(counts))

        if self.verbose:
            print(f"{indent}  [?] Вопрос: признак #{idx} <= {thr:.4f}?")

        left_idx = X[:, idx] <= thr
        left = self._build_tree(X[left_idx], y[left_idx], depth + 1)
        right = self._build_tree(X[~left_idx], y[~left_idx], depth + 1)
        return Node(feature=idx, threshold=thr, left=left, right=right)

    def fit(self, X, y):
        self.root = self._build_tree(X.values, y.values)

    def _predict_one(self, x, node):
        if node.value is not None:
            return node.value
        if x[node.feature] <= node.threshold:
            return self._predict_one(x, node.left)
        return self._predict_one(x, node.right)

    def predict(self, X):
        return np.array([self._predict_one(x, self.root) for x in X.values])
