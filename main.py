import json
from datetime import datetime
from collections import defaultdict

def validate_date(date_string):
    """Проверяет, что строка соответствует формату YYYY-MM-DD."""
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def load_books():
    """Загружает список книг из JSON‑файла."""
    try:
        with open('books.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except (PermissionError, json.JSONDecodeError) as e:
        print(f"Ошибка при работе с файлом: {e}")
        return []

def save_books(books):
    """Сохраняет список книг в JSON‑файл."""
    try:
        with open('books.json', 'w', encoding='utf-8') as f:
            json.dump(books, f, ensure_ascii=False, indent=2)
    except PermissionError as e:
        print(f"Не удалось сохранить файл: {e}")

def add_book(books):
    """Добавляет новую книгу с проверкой на дубликаты и валидацией данных."""
    author = input("Автор: ").strip()
    title = input("Название: ").strip()

    # Проверка на дубликаты (книга с таким автором и названием уже есть)
    for book in books:
        if book['author'].lower() == author.lower() and book['title'].lower() == title.lower():
            print("Ошибка: эта книга уже есть в списке!")
            return

    # Валидация оценки (целое число от 1 до 5)
    while True:
        try:
            rating = int(input("Оценка (1–5): "))
            if 1 <= rating <= 5:
                break
            else:
                print("Ошибка: оценка должна быть от 1 до 5.")
        except ValueError:
            print("Ошибка: введите целое число от 1 до 5.")

    # Ввод даты (если не введена — используется текущая дата)
    date_input = input("Дата прочтения (YYYY-MM-DD, по умолчанию — сегодня): ").strip()
    if date_input:
        if validate_date(date_input):
            date = date_input
        else:
            print("Ошибка: неверный формат даты. Используется текущая дата.")
            date = datetime.now().strftime("%Y-%m-%d")
    else:
        date = datetime.now().strftime("%Y-%m-%d")

    # Добавление книги в список
    books.append({
        'author': author,
        'title': title,
        'rating': rating,
        'date': date
    })
    save_books(books)
    print(f"Книга '{title}' успешно добавлена!")

def list_books(books):
    """Выводит список всех книг с нумерацией."""
    if not books:
        print("Список книг пуст.")
        return
    print("\nСписок прочитанных книг:")
    for i, book in enumerate(books, 1):
        print(f"{i}. '{book['title']}' — {book['author']} ({book['rating']}/5, {book['date']})")

def show_average_rating(books):
    """Рассчитывает и выводит среднюю оценку всех книг."""
    if not books:
        print("Нет книг для расчёта средней оценки.")
        return
    total = sum(book['rating'] for book in books)
    average = total / len(books)
    print(f"Средняя оценка всех книг: {average:.2f}")


def show_author_stats(books):
    """Выводит статистику по авторам (сколько книг каждого автора прочитано)."""
    if not books:
        print("Нет данных для статистики.")
        return
    stats = defaultdict(int)
    for book in books:
        stats[book['author']] += 1
    # Сортировка по убыванию количества книг
    sorted_stats = sorted(stats.items(), key=lambda x: x[1], reverse=True)
    print("\nСтатистика по авторам (отсортировано по убыванию):")
    for author, count in sorted_stats:
        print(f"{author}: {count} книг")

def delete_book(books):
    """Удаляет книгу по номеру из списка с подтверждением."""
    list_books(books)
    if not books:
        return
    try:
        index = int(input("Введите номер книги для удаления: ")) - 1
        if 0 <= index < len(books):
            removed = books[index]
            confirm = input(f"Удалить книгу '{removed['title']}'? (да/нет): ").strip().lower()
            if confirm in ('да', 'y', 'yes'):
                books.pop(index)
                save_books(books)
                print(f"Книга '{removed['title']}' успешно удалена.")
            else:
                print("Удаление отменено.")
        else:
            print("Ошибка: неверный номер книги.")
    except ValueError:
        print("Ошибка: введите корректный номер книги.")

def main():
    """Главный цикл приложения — отображает меню и обрабатывает выбор пользователя."""
    books = load_books()
    while True:
        print("\n" + "="*40)
        print("ТРЕКЕР ПРОЧИТАННЫХ КНИГ")
        print("="*40)
        print(f"Всего книг в коллекции: {len(books)}")
        print("1. Добавить книгу")
        print("2. Показать все книги")
        print("3. Показать среднюю оценку")
        print("4. Статистика по авторам")
        print("5. Удалить книгу")
        print("6. Выход")
        choice = input("\nВыберите действие (1–6): ").strip()

        if choice == '1':
            add_book(books)
        elif choice == '2':
            list_books(books)
        elif choice == '3':
            show_average_rating(books)
        elif choice == '4':
            show_author_stats(books)
        elif choice == '5':
            delete_book(books)
        elif choice == '6':
            print("До свидания!")
            break
        else:
            print("Ошибка: выберите действие от 1 до 6.")


if __name__ == "__main__":
    main()
