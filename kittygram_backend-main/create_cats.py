"""
Скрипт для создания тестовых котиков
Запуск: python create_cats.py
"""
import os
import sys
import django
from pathlib import Path

# Настройка Django
BASE_DIR = Path(__file__).parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kittygram_backend.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.core.files import File
from cats.models import Cat, Achievement, AchievementCat

User = get_user_model()

def create_sample_cats():
    # Создаем или получаем тестового пользователя
    username = 'demo_user'
    user, created = User.objects.get_or_create(
        username=username,
        defaults={'password': 'pbkdf2_sha256$260000$demo$demo'}
    )
    if created:
        user.set_password('demo123')
        user.save()
        print(f'✓ Создан пользователь: {username} (пароль: demo123)')
    else:
        print(f'✓ Пользователь {username} уже существует')

    # Создаем достижения
    achievements_data = [
        'Лучший охотник',
        'Мурлыка года',
        'Самый пушистый',
        'Король дивана',
        'Мастер сна',
        'Эксперт по играм',
    ]
    
    achievements = {}
    for ach_name in achievements_data:
        achievement, _ = Achievement.objects.get_or_create(name=ach_name)
        achievements[ach_name] = achievement
        print(f'✓ Достижение: {ach_name}')

    # Данные для котиков
    cats_data = [
        {'name': 'Мурзик', 'color': '#FFA500', 'birth_year': 2020, 'achievements': ['Лучший охотник', 'Мурлыка года']},
        {'name': 'Барсик', 'color': '#000000', 'birth_year': 2019, 'achievements': ['Самый пушистый', 'Король дивана']},
        {'name': 'Рыжик', 'color': '#FF8C00', 'birth_year': 2021, 'achievements': ['Мастер сна']},
        {'name': 'Снежок', 'color': '#FFFFFF', 'birth_year': 2022, 'achievements': ['Эксперт по играм', 'Мурлыка года']},
        {'name': 'Тигра', 'color': '#D2691E', 'birth_year': 2018, 'achievements': ['Лучший охотник', 'Король дивана', 'Самый пушистый']},
        {'name': 'Серый', 'color': '#808080', 'birth_year': 2020, 'achievements': ['Мастер сна', 'Эксперт по играм']},
        {'name': 'Васька', 'color': '#DEB887', 'birth_year': 2017, 'achievements': ['Лучший охотник', 'Мастер сна', 'Король дивана']},
        {'name': 'Пушок', 'color': '#F5F5F5', 'birth_year': 2023, 'achievements': ['Самый пушистый', 'Эксперт по играм']},
        {'name': 'Рысь', 'color': '#8B4513', 'birth_year': 2019, 'achievements': ['Лучший охотник', 'Мурлыка года']},
        {'name': 'Маркиз', 'color': '#A9A9A9', 'birth_year': 2016, 'achievements': ['Король дивана', 'Мастер сна', 'Самый пушистый']},
        {'name': 'Белка', 'color': '#FFE4C4', 'birth_year': 2021, 'achievements': ['Эксперт по играм', 'Мурлыка года']},
        {'name': 'Том', 'color': '#DCDCDC', 'birth_year': 2020, 'achievements': ['Лучший охотник', 'Эксперт по играм']},
        {'name': 'Гарфилд', 'color': '#FF8C00', 'birth_year': 2015, 'achievements': ['Король дивана', 'Мастер сна', 'Мурлыка года']},
        {'name': 'Луна', 'color': '#FFFFFF', 'birth_year': 2022, 'achievements': ['Самый пушистый', 'Эксперт по играм']},
        {'name': 'Тень', 'color': '#000000', 'birth_year': 2018, 'achievements': ['Лучший охотник', 'Мастер сна']},
    ]

    # Получаем путь к изображению
    frontend_images_dir = BASE_DIR / 'frontend' / 'src' / 'images'
    default_image_path = frontend_images_dir / 'default-kitty.jpg'

    created_count = 0
    for cat_data in cats_data:
        # Проверяем, существует ли уже такой котик
        if Cat.objects.filter(name=cat_data['name'], owner=user).exists():
            print(f'⚠ Котик {cat_data["name"]} уже существует, пропускаем')
            continue

        # Создаем котика
        cat = Cat.objects.create(
            name=cat_data['name'],
            color=cat_data['color'],
            birth_year=cat_data['birth_year'],
            owner=user
        )

        # Добавляем изображение, если оно существует
        if default_image_path.exists():
            try:
                with open(default_image_path, 'rb') as f:
                    cat.image.save(
                        f'{cat_data["name"]}.jpg',
                        File(f),
                        save=True
                    )
            except Exception as e:
                print(f'⚠ Не удалось добавить изображение для {cat_data["name"]}: {e}')

        # Добавляем достижения
        for ach_name in cat_data['achievements']:
            if ach_name in achievements:
                AchievementCat.objects.get_or_create(
                    cat=cat,
                    achievement=achievements[ach_name]
                )

        created_count += 1
        print(f'✓ Создан котик: {cat_data["name"]} ({cat_data["birth_year"]} г.р.)')

    print(f'\n{"="*50}')
    print(f'✓ Всего создано котиков: {created_count}')
    print(f'✓ Пользователь для входа: {username} / demo123')
    print(f'{"="*50}')

if __name__ == '__main__':
    create_sample_cats()

