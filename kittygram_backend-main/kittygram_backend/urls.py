from rest_framework import routers

from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from pathlib import Path

from cats.views import AchievementViewSet, CatViewSet


router = routers.DefaultRouter()
router.register(r'cats', CatViewSet)
router.register(r'achievements', AchievementViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/', include('djoser.urls')),  # Работа с пользователями
    path('api/', include('djoser.urls.authtoken')),  # Работа с токенами
]

# Обслуживание React приложения
REACT_BUILD_DIR = Path(settings.BASE_DIR) / 'frontend' / 'build'

if REACT_BUILD_DIR.exists():
    # В production обслуживаем статические файлы React
    # Настраиваем шаблоны для обслуживания index.html
    if REACT_BUILD_DIR not in settings.TEMPLATES[0]['DIRS']:
        settings.TEMPLATES[0]['DIRS'].append(REACT_BUILD_DIR)
    
    # Обслуживание статических файлов из build/static
    # Важно: этот маршрут должен быть ДО catch-all маршрута
    static_root = REACT_BUILD_DIR / 'static'
    urlpatterns += [
        re_path(r'^static/(?P<path>.*)$', serve, {
            'document_root': static_root,
            'show_indexes': False,
        }),
    ]
    
    # Обслуживание других файлов из build (favicon, manifest и т.д.)
    urlpatterns += [
        re_path(r'^(favicon\.ico|manifest\.json|robots\.txt)$', serve, {
            'document_root': REACT_BUILD_DIR,
            'show_indexes': False,
        }),
    ]
    
    # Catch-all маршрут для React Router (должен быть последним)
    # Все не-API запросы будут возвращать index.html для client-side routing
    urlpatterns += [
        re_path(r'^(?!api|admin|static|media|favicon|manifest|robots).*$', TemplateView.as_view(template_name='index.html')),
    ]
else:
    # Если build не существует, показываем информационное сообщение
    def frontend_info(request):
        from django.http import HttpResponse
        message = """
        <html>
        <head><title>Frontend не собран</title></head>
        <body style="font-family: Arial; padding: 40px; text-align: center;">
            <h1>React приложение не собрано</h1>
            <p>Для запуска приложения выполните одно из следующих действий:</p>
            <h2>Вариант 1: Режим разработки (рекомендуется)</h2>
            <p>Запустите React dev server в отдельном терминале:</p>
            <pre style="background: #f5f5f5; padding: 15px; border-radius: 5px; display: inline-block;">
cd frontend
npm install
npm start
            </pre>
            <p>Затем откройте <a href="http://localhost:3000">http://localhost:3000</a></p>
            <h2>Вариант 2: Production режим</h2>
            <p>Соберите React приложение:</p>
            <pre style="background: #f5f5f5; padding: 15px; border-radius: 5px; display: inline-block;">
cd frontend
npm install
npm run build
            </pre>
            <p>Затем обновите эту страницу.</p>
            <hr>
            <p><strong>API доступен по адресу:</strong> <a href="/api/">/api/</a></p>
            <p><strong>Админ панель:</strong> <a href="/admin/">/admin/</a></p>
        </body>
        </html>
        """
        return HttpResponse(message)
    
    urlpatterns += [
        re_path(r'^(?!api|admin|static|media).*$', frontend_info),
    ]

# Обслуживание медиа файлов (изображения котиков)
# Важно: это должно быть после всех других маршрутов
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)