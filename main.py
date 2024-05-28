import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
import requests
import os


def fetch_content():
    url = url_entry.get()
    directory = directory_entry.get()
    if not url:
        messagebox.showerror("Ошибка", "Введите URL.")
        return
    if not directory:
        messagebox.showerror("Ошибка", "Укажите директорию для сохранения.")
        return

    try:
        response = requests.get(url)
        response.raise_for_status()
        content_text.delete(1.0, tk.END)
        content_text.insert(tk.INSERT, response.text)
        save_content(response.text, directory)
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Ошибка", f"Не удалось получить данные: {e}")


def save_content(content, directory):
    if not os.path.isdir(directory):
        messagebox.showerror("Ошибка", "Указанная директория не существует.")
        return

    filename = os.path.join(directory, "web_content.html")
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(content)
        messagebox.showinfo("Успех", f"Контент сохранен в: {filename}")
    except IOError as e:
        messagebox.showerror("Ошибка", f"Не удалось сохранить файл: {e}")


def browse_directory():
    directory = filedialog.askdirectory()
    if directory:
        directory_entry.delete(0, tk.END)
        directory_entry.insert(0, directory)


def paste_url():
    url_entry.delete(0, tk.END)
    url_entry.insert(tk.END, root.clipboard_get())


# Создание основного окна
root = tk.Tk()
root.title("Web Scraper")

# URL ввод
url_label = tk.Label(root, text="Введите URL:")
url_label.pack(pady=5)
url_frame = tk.Frame(root)
url_frame.pack(pady=5)
url_entry = tk.Entry(url_frame, width=50)
url_entry.pack(side=tk.LEFT, padx=(0, 5))
paste_button = tk.Button(url_frame, text="Вставить", command=paste_url)
paste_button.pack(side=tk.LEFT)

# Директория для сохранения
directory_label = tk.Label(root, text="Укажите директорию для сохранения:")
directory_label.pack(pady=5)
directory_frame = tk.Frame(root)
directory_frame.pack(pady=5)
directory_entry = tk.Entry(directory_frame, width=40)
directory_entry.pack(side=tk.LEFT, padx=(0, 5))
browse_button = tk.Button(directory_frame, text="Обзор", command=browse_directory)
browse_button.pack(side=tk.LEFT)

# Кнопка для запуска скрапинга
fetch_button = tk.Button(root, text="Получить контент", command=fetch_content)
fetch_button.pack(pady=5)

# Поле для отображения полученного контента
content_text = scrolledtext.ScrolledText(root, wrap=tk.NONE, width=80, height=20)
content_text.pack(pady=10)

# Запуск основного цикла
root.mainloop()


