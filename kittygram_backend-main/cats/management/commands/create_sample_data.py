"""
Команда для создания тестовых данных (котиков с фотографиями)
Использование: python manage.py create_sample_data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.core.files import File
from pathlib import Path
import os

from cats.models import Cat, Achievement, AchievementCat

User = get_user_model()


class Command(BaseCommand):
    help = 'Создает тестовых котиков с фотографиями для демонстрации'

    def handle(self, *args, **options):
        # Создаем или получаем тестового пользователя
        username = 'demo_user'
        user, created = User.objects.get_or_create(
            username=username,
            defaults={'password': 'pbkdf2_sha256$260000$demo$demo'}  # Демо пароль
        )
        if created:
            user.set_password('demo123')
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Создан пользователь: {username} (пароль: demo123)'))
        else:
            self.stdout.write(self.style.WARNING(f'Пользователь {username} уже существует'))

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

        # Данные для котиков - разнообразная коллекция
        cats_data = [
            {
                'name': 'Мурзик',
                'color': '#FFA500',  # orange
                'birth_year': 2020,
                'achievements': ['Лучший охотник', 'Мурлыка года'],
                'image_name': 'default-kitty.jpg'
            },
            {
                'name': 'Барсик',
                'color': '#000000',  # black
                'birth_year': 2019,
                'achievements': ['Самый пушистый', 'Король дивана'],
                'image_name': 'default-kitty.jpg'
            },
            {
                'name': 'Рыжик',
                'color': '#FF8C00',  # darkorange
                'birth_year': 2021,
                'achievements': ['Мастер сна'],
                'image_name': 'default-kitty.jpg'
            },
            {
                'name': 'Снежок',
                'color': '#FFFFFF',  # white
                'birth_year': 2022,
                'achievements': ['Эксперт по играм', 'Мурлыка года'],
                'image_name': 'default-kitty.jpg'
            },
            {
                'name': 'Тигра',
                'color': '#D2691E',  # chocolate
                'birth_year': 2018,
                'achievements': ['Лучший охотник', 'Король дивана', 'Самый пушистый'],
                'image_name': 'default-kitty.jpg'
            },
            {
                'name': 'Серый',
                'color': '#808080',  # gray
                'birth_year': 2020,
                'achievements': ['Мастер сна', 'Эксперт по играм'],
                'image_name': 'default-kitty.jpg'
            },
            {
                'name': 'Васька',
                'color': '#DEB887',  # burlywood
                'birth_year': 2017,
                'achievements': ['Лучший охотник', 'Мастер сна', 'Король дивана'],
                'image_name': 'default-kitty.jpg'
            },
            {
                'name': 'Пушок',
                'color': '#F5F5F5',  # whitesmoke
                'birth_year': 2023,
                'achievements': ['Самый пушистый', 'Эксперт по играм'],
                'image_name': 'default-kitty.jpg'
            },
            {
                'name': 'Рысь',
                'color': '#8B4513',  # saddlebrown
                'birth_year': 2019,
                'achievements': ['Лучший охотник', 'Мурлыка года'],
                'image_name': 'default-kitty.jpg'
            },
            {
                'name': 'Маркиз',
                'color': '#A9A9A9',  # darkgrey
                'birth_year': 2016,
                'achievements': ['Король дивана', 'Мастер сна', 'Самый пушистый'],
                'image_name': 'default-kitty.jpg'
            },
            {
                'name': 'Белка',
                'color': '#FFE4C4',  # bisque
                'birth_year': 2021,
                'achievements': ['Эксперт по играм', 'Мурлыка года'],
                'image_name': 'default-kitty.jpg'
            },
            {
                'name': 'Том',
                'color': '#DCDCDC',  # gainsboro
                'birth_year': 2020,
                'achievements': ['Лучший охотник', 'Эксперт по играм'],
                'image_name': 'default-kitty.jpg'
            },
            {
                'name': 'Гарфилд',
                'color': '#FF8C00',  # darkorange
                'birth_year': 2015,
                'achievements': ['Король дивана', 'Мастер сна', 'Мурлыка года'],
                'image_name': 'default-kitty.jpg'
            },
            {
                'name': 'Луна',
                'color': '#FFFFFF',  # white
                'birth_year': 2022,
                'achievements': ['Самый пушистый', 'Эксперт по играм'],
                'image_name': 'default-kitty.jpg'
            },
            {
                'name': 'Тень',
                'color': '#000000',  # black
                'birth_year': 2018,
                'achievements': ['Лучший охотник', 'Мастер сна'],
                'image_name': 'default-kitty.jpg'
            },
        ]

        # Получаем путь к изображению по умолчанию
        frontend_images_dir = Path(__file__).parent.parent.parent.parent / 'frontend' / 'src' / 'images'
        default_image_path = frontend_images_dir / 'default-kitty.jpg'

        created_count = 0
        for cat_data in cats_data:
            # Проверяем, существует ли уже такой котик
            if Cat.objects.filter(name=cat_data['name'], owner=user).exists():
                self.stdout.write(self.style.WARNING(f'Котик {cat_data["name"]} уже существует, пропускаем'))
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
                    self.stdout.write(self.style.WARNING(f'Не удалось добавить изображение для {cat_data["name"]}: {e}'))

            # Добавляем достижения
            for ach_name in cat_data['achievements']:
                if ach_name in achievements:
                    AchievementCat.objects.get_or_create(
                        cat=cat,
                        achievement=achievements[ach_name]
                    )

            created_count += 1
            self.stdout.write(self.style.SUCCESS(f'Создан котик: {cat_data["name"]}'))

        self.stdout.write(self.style.SUCCESS(f'\nВсего создано котиков: {created_count}'))
        self.stdout.write(self.style.SUCCESS(f'Пользователь для входа: {username} / demo123'))

