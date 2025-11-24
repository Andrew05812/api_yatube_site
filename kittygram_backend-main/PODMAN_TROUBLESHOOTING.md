# Решение проблем с Podman

## Проблема: "Cannot connect to Podman"

Эта ошибка означает, что Podman machine не инициализирована или не запущена.

### Решение 1: Через Podman Desktop (Рекомендуется)

1. **Откройте Podman Desktop**
2. **Проверьте статус машины:**
   - В левом нижнем углу должно быть "Podman machine is running" (зеленый)
   - Если написано "Stopped" или "Not running" - нажмите кнопку "Start" или "Play"

3. **Если машины нет:**
   - В Podman Desktop нажмите "Settings" (шестеренка)
   - Перейдите в "Resources" → "Machines"
   - Нажмите "Create Machine" или "Add Machine"
   - Выберите имя (можно оставить "podman-machine-default")
   - Нажмите "Create"
   - Дождитесь создания и запуска

### Решение 2: Через командную строку

Если Podman Desktop не помогает, инициализируйте машину вручную:

```bash
# Инициализация машины (если еще не создана)
podman machine init

# Запуск машины
podman machine start

# Проверка статуса
podman machine list
```

### Решение 3: Проверка подключения

Проверьте доступные подключения:

```bash
podman system connection list
```

Должно быть что-то вроде:
```
Name                         Identity                                    Default
podman-machine-default       C:\Users\Andre\.ssh\podman-machine-default  true
```

Если подключений нет, создайте:

```bash
podman machine init
podman machine start
```

### Решение 4: Перезапуск Podman Desktop

1. Закройте Podman Desktop полностью
2. Откройте диспетчер задач (Ctrl+Shift+Esc)
3. Убедитесь, что все процессы Podman закрыты
4. Запустите Podman Desktop снова
5. Дождитесь полной загрузки (зеленый индикатор)

### Решение 5: Пересоздание машины

Если ничего не помогает, пересоздайте машину:

```bash
# Остановите и удалите старую машину
podman machine stop
podman machine rm

# Создайте новую
podman machine init
podman machine start

# Проверьте
podman ps
```

## Проблема: "No such file or directory"

### Решение:

Убедитесь, что вы находитесь в правильной директории:

```bash
# Проверьте текущую директорию
pwd

# Найдите правильный путь
ls -la

# Перейдите в нужную директорию
cd ~/OneDrive/Рабочий\ стол/VUZ/бэкенд/15/my/kittygram/kittygram_backend-main

# Или если вы уже в kittygram:
cd kittygram_backend-main
```

## Полная последовательность запуска

```bash
# 1. Убедитесь, что Podman Desktop запущен и машина работает

# 2. Проверьте подключение
podman ps

# 3. Перейдите в директорию проекта
cd ~/OneDrive/Рабочий\ стол/VUZ/бэкенд/15/my/kittygram/kittygram_backend-main

# 4. Проверьте, что файл .env существует
ls -la .env

# 5. Если нет - создайте
bash create_env.sh

# 6. Запустите проект
podman-compose up -d
```

## Проверка работоспособности

После решения проблем проверьте:

```bash
# 1. Podman работает
podman --version
podman ps

# 2. podman-compose установлен
podman-compose --version

# 3. Вы в правильной директории
pwd
ls docker-compose.yml

# 4. Файл .env существует
ls .env
```

## Если все еще не работает

Попробуйте использовать Podman через WSL2:

1. Установите WSL2 (если еще не установлен):
```powershell
wsl --install
```

2. В WSL2 установите Podman:
```bash
# В WSL2 терминале
sudo apt update
sudo apt install -y podman podman-compose
```

3. Используйте проект из WSL2:
```bash
cd /mnt/c/Users/Andre/OneDrive/Рабочий\ стол/VUZ/бэкенд/15/my/kittygram/kittygram_backend-main
podman-compose up -d
```

