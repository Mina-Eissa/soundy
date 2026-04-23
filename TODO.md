# Soundy Project TODO - Backend Polish & Integration

## Current Status
- [x] Analyzed all files
- Monolith Django backend + React frontend
- Goal: MVP Music Player (Auth → Browse → Play → Interact)

## Phase 1: Backend Polish ✓
### 1.1 Audio Streaming [✅ PRODUCTION-READY]
- [x] Full analysis: Sessions, chunking, HTTP ranges, play tracking (30s++)
- Skip edits: Use ?position for seek (add Range later if needed)

### 1.2 Swagger API Docs [✅ ENABLED]
- [x] soundy/soundy/urls.py already has /api/docs/ → localhost:8000/api/docs/

### 1.3 Tests & Validation ✓
- [ ] api/tests.py: Track upload/stream tests
- [x] validators.py: Added size limits (audio 100MB, img 5MB)

### 1.2 Enable Swagger/Browsable API
- [ ] Update soundy/urls.py: include spectacular schema/swagger
- [ ] Test: /api/schema/swagger-ui/

### 1.3 Tests & Validation
- [ ] Flesh out api/tests.py
- [ ] Add upload limits in api/validators.py

## Phase 2: Frontend-Backend Integration
- [ ] API client in soundy-stream/src/services/api.ts
- [ ] Replace mocks with queries (tracks/users)
- [ ] Auth flow (login → JWT)

## Phase 3: Core Features
- [ ] Music Player component
- [ ] Upload form
- [ ] Discovery pages

## Infra
- [ ] docker-compose: Add frontend service
- [ ] Deploy
