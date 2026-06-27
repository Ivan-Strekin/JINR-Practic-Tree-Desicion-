# Запуск веб-версии практики в Windows 10/11

## 1. Перейти в папку проекта

```bash
cd wine_decision_tree_practice
```

## 2. Создать виртуальное окружение

```bash
python3 -m venv venv
source venv/bin/activate
```

Если `venv` не создаётся:

```bash
sudo apt install python3-venv
```

## 3. Установить зависимости

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Запустить сайт

```bash
python app.py
```

## 5. Открыть в браузере

```text
http://127.0.0.1:5000/
```

