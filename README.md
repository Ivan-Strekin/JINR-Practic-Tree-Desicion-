
# Введение

<p>Дерево решений реализовано с помощью python, а визуализация сделана через сайт. В общем виде проект состоит из frontend и backend частей, где backend - python часть.</p>
<p> Frontend-часть реализована с помощью HTML, CSS и JavaScript. После нажатия на кнопку начала обучения на сайте JavaScript отправляет запрос на backend, получает от него данные в формате JSON и выводит их на страницу.</p>
<p>Backend-часть реализована на Python с использованием Flask. Flask создаёт локальный веб-сервер и принимает запросы от сайта.</p>
<p> Инструкция по установке нужных компонентов и запуску сервера можно увидеть ниже </p>






# Запуск веб-версии практики на Linux Ubuntu

```
## 1. Создать виртуальное окружение

```bash
python3 -m venv venv
source venv/bin/activate
```

Если `venv` не создаётся:

```bash
sudo apt install python3-venv
```

## 2. Установить зависимости

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## 3. Запустить сайт

```bash
python app.py
```

## 4. Открыть в браузере

```text
http://127.0.0.1:5000/
```

# Запуск веб-версии практики в Windows 10/11

## 1. Создать виртуальное окружение

```powershell
python -m venv venv
```

Если команда `python` не работает, попробуйте:

```powershell
py -m venv venv
```

## 2. Активировать виртуальное окружение

### PowerShell

```powershell
.\venv\Scripts\Activate.ps1
```

Если PowerShell выдаёт ошибку политики выполнения, выполните команду:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

После этого снова активируйте окружение:

```powershell
.\venv\Scripts\Activate.ps1
```

## 3. Установить зависимости

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Запустить сайт

```powershell
python app.py
```

## 5. Открыть сайт в браузере

```text
http://127.0.0.1:5000/
```
