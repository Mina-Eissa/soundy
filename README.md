# Soundy Backend 🎵

Backend API for the Soundy project. All endpoints are documented and can be viewed or imported for testing.

## 1. Project Overview

This is the backend API for Soundy, a music streaming platform 
It allows:

- User authentication
- Retrieving tracks and playlists
- Interact with track ( React and Comment)
- Managing playlists

## 2. API docs

- [View API YAML](soundy/docs/APIDocs.yaml)
you can see it by import this file into **Postman/Insomnia/Swagger**

## 3. Launch this app

**1. clone the repository**.

``` bash
git clone https://github.com/Mina-Eissa/soundy.git
cd soundy/soundy
```

**2. create virtual environment**.

``` bash
python3 -m venv sound-env
source sound-env/bin/activate
```

**3. install dependencies**.

``` bash
pip install -r requirements.txt
```

**4. create `.env` file**.

``` bash
touch .env
```

**5. setup environment variables**.

``` env
DB_NAME=soundy
DB_USER=<your-database-user>
DB_USER_PASS=<your-database-user-password>
DB_HOST=localhost
DB_PORT=<database-port>
SECRET_KEY=<email-me-to-send>
DEBUG=True
```

**6. apply migrations**.

``` bash
python manage.py migrate
```

**7. run the server**.

```bash
python manage.py migrate
```

## ⚠️ Notes

> - Make sure Python 3.10+ is installed
> - Ensure your database is running (PostgreSQL if used)
> - Update .env with correct database credentials

`2026-03-22`
<!-- [this chat describe what i need to do](https://chatgpt.com/c/68a5f871-5af4-832c-acb0-2a71b2f33264). -->

<!-- ## `2025-8-21`

- [x] Install Django, DRF, PostgreSQL.
- [x] Create a new project `soundy/`.
- [x] Create a custom User model (extend `AbstractUser`).
- [x] Add JWT authentication (`djangorestframework-simplejwt`).
- [x] Test with Postman: register → login → access protected route.

## `2025-8-23`

1. [ ] Models:

   1. [ ] Artist (profile for a user)
   2. [X] Track (title, file, cover, duration, artist)
   3. [ ] Album
   4. [X] Playlist

2. [X] APIs:

   1. [X] Create/List/Detail for tracks, playlists, albums.
   2. [X] Add/remove tracks from playlists.

3. [X] File handling:

   1. [X] Local uploads (MEDIA_URL) for now.
   2. [X] Support audio files + cover images.

## `2025-10-03`

1. Models:
   1. [X] Like(user, track)
   2. [X] Follow(fan → artist)
   3. [X] Comment(track, user, text)

2. APIs:
   - [ ] `POST /React/`
   - [ ] `GET  /React/`
   - [ ] `POST /users/{id}/follow/`
   - [ ] `POST /tracks/{id}/comment/` -->
