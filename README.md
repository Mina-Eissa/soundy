# soundy

soundy will be like any audio app.
[this chat describe what i need to do](https://chatgpt.com/c/68a5f871-5af4-832c-acb0-2a71b2f33264).

## `2025-8-21`

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
   1. [ ] Like(user, track)
   2. [ ] Follow(fan → artist)
   3. [ ] Comment(track, user, text)

2. APIs:
   . [ ] `POST /tracks/{id}/like/`
   . [ ] `POST /users/{id}/follow/`
   . [ ] `POST /tracks/{id}/comment/`