from PIL import Image
import os
import sys

def extract_sort_key(filename):
    """
    Извлекает числовую часть из имени файла. Если имя состоит только из числа,
    используется это число. Если числа нет, возвращается 0.
    """
    try:
        name, _ = os.path.splitext(filename)
        if name.isdigit():
            return int(name)
        key = int(name.split('_')[-1])
        return key
    except ValueError:
        return 0

def create_sprite_list(output_file="sprite.png"):
    # Определяем путь к директории исполняемого файла
    script_dir = os.path.dirname(sys.argv[0])

    # Получаем список PNG-файлов из этой директории
    files = [f for f in os.listdir(script_dir) if f.endswith(".png")]

    if not files:
        print("В директории нет PNG-файлов.")
        return

    # Сортируем файлы по числовому ключу
    files.sort(key=extract_sort_key)

    images = []
    sprite_width = 0
    sprite_height = 0

    for file in files:
        try:
            img_path = os.path.join(script_dir, file)
            img = Image.open(img_path)
            img.verify()
            img = Image.open(img_path)
            img.load()

            if not images:
                sprite_width, sprite_height = img.size
                images.append(img)
            else:
                if img.size == (sprite_width, sprite_height):
                    images.append(img)
                else:
                    print(f"Пропущено: {file} (размер {img.size}, ожидается {sprite_width}x{sprite_height})")
        except Exception as e:
            print(f"Ошибка обработки файла {file}: {e}")

    if not images:
        print("Не удалось найти изображения с одинаковыми размерами.")
        return

    total_width = sprite_width * len(images)
    result_image = Image.new("RGBA", (total_width, sprite_height))

    x_offset = 0
    for img in images:
        result_image.paste(img, (x_offset, 0))
        x_offset += sprite_width

    output_path = os.path.join(script_dir, output_file)
    result_image.save(output_path)
    print(f"Спрайтлист сохранён как {output_path}")

if __name__ == "__main__":
    create_sprite_list()
