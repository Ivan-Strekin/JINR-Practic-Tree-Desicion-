from flask import Flask, jsonify, render_template

from data_loader import FEATURE_COLUMNS, load_wine_dataset
from decision_tree import MyDecisionTree
from tree_exporter import BinaryTreeArrayExporter


app = Flask(__name__)

TREE_DEPTH = 3

CLASS_MAP = {
    0: "Алкоголь 1-го типа",
    1: "Алкоголь 2-го типа",
    2: "Алкоголь 3-го типа",
}

FEATURE_DESCRIPTIONS = [
    {
        "name": "alcohol",
        "title": "Содержание спирта",
        "description": "Доля алкоголя в образце вина."
    },
    {
        "name": "malic_acid",
        "title": "Яблочная кислота",
        "description": "Количество яблочной кислоты, влияющей на кислотность вкуса."
    },
    {
        "name": "ash",
        "title": "Зола",
        "description": "Минеральный остаток после сжигания органической части вина."
    },
    {
        "name": "alcalinity_of_ash",
        "title": "Щёлочность золы",
        "description": "Показатель щёлочности минерального остатка."
    },
    {
        "name": "magnesium",
        "title": "Магний",
        "description": "Концентрация магния в химическом составе вина."
    },
    {
        "name": "total_phenols",
        "title": "Общие фенолы",
        "description": "Общее содержание фенольных соединений."
    },
    {
        "name": "flavanoids",
        "title": "Флаваноиды",
        "description": "Группа фенольных веществ, связанных с цветом и вкусом вина."
    },
    {
        "name": "nonflavanoid_phenols",
        "title": "Нефлаваноидные фенолы",
        "description": "Фенольные соединения, не относящиеся к флаваноидам."
    },
    {
        "name": "proanthocyanins",
        "title": "Проантоцианины",
        "description": "Полифенольные соединения, влияющие на терпкость."
    },
    {
        "name": "color_intensity",
        "title": "Интенсивность цвета",
        "description": "Насыщенность окраски образца вина."
    },
    {
        "name": "hue",
        "title": "Оттенок",
        "description": "Цветовой оттенок образца вина."
    },
    {
    "name": "phenolic_index",
    "title": "Индекс фенольных соединений",
    "description": "Оптический показатель, который помогает отличать вина по составу фенольных веществ."
    },
    {
        "name": "proline",
        "title": "Пролин",
        "description": "Аминокислота, используемая как химический признак вина."
    },
    {
        "name": "REAL_CLASS",
        "title": "Истинный тип алкоголя",
        "description": "Класс образца: алкоголь 1-го, 2-го или 3-го типа."
    },
]


def build_preview(X_test, y_test, limit=5):
    preview_df = X_test.head(limit).copy()
    preview_df["REAL_CLASS"] = [CLASS_MAP[int(value)] for value in y_test.head(limit)]
    return preview_df.round(4).to_dict(orient="records")


def build_test_rows(model, X_test, y_test):
    predictions = model.predict(X_test)
    rows = []
    correct_count = 0

    for index, prediction in enumerate(predictions):
        real_value = int(y_test.iloc[index])
        predicted_value = int(prediction)
        is_correct = predicted_value == real_value

        if is_correct:
            correct_count += 1

        rows.append({
            "number": index + 1,
            "prediction": CLASS_MAP[predicted_value],
            "real": CLASS_MAP[real_value],
            "result": "Верно" if is_correct else "Ошибка",
            "correct": bool(is_correct),
        })

    accuracy = correct_count / len(y_test) if len(y_test) else 0
    return rows, correct_count, accuracy


@app.route("/")
def index():
    return render_template(
        "index.html",
        features=FEATURE_DESCRIPTIONS,
        tree_depth=TREE_DEPTH
    )


@app.post("/api/train")
def train():
    try:
        X_train, X_test, y_train, y_test, full_df = load_wine_dataset()

        model = MyDecisionTree(max_depth=TREE_DEPTH)
        model.fit(X_train, y_train)

        test_rows, correct_count, test_accuracy = build_test_rows(model, X_test, y_test)

        exporter = BinaryTreeArrayExporter(
            model=model,
            feature_names=FEATURE_COLUMNS,
            class_map=CLASS_MAP
        )
        tree_nodes = exporter.export(X_train, y_train)

        return jsonify({
            "success": True,
            "depth": TREE_DEPTH,
            "dataset_rows": int(len(full_df)),
            "train_rows": int(len(X_train)),
            "test_rows_count": int(len(X_test)),
            "features_count": int(len(FEATURE_COLUMNS)),
            "accuracy": test_accuracy,
            "accuracy_text": f"{test_accuracy:.4f}",
            "accuracy_percent": f"{test_accuracy:.1%}",
            "correct_count": correct_count,
            "test_count": int(len(y_test)),
            "preview": build_preview(X_test, y_test),
            "test_rows": test_rows,
            "tree_nodes": tree_nodes,
        })

    except Exception as error:
        return jsonify({
            "success": False,
            "error": "Не удалось выполнить обучение.",
            "details": str(error),
        }), 500


if __name__ == "__main__":
    app.run(debug=True)
