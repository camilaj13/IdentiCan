# Roadmap - IdentiCan

## Phase 1 - MVP (Complete)

- [x] Complete backend API (FastAPI)
- [x] JWT authentication
- [x] Dog CRUD operations
- [x] Vaccine records
- [x] QR code generation (PNG + PDF)
- [x] 3 verifications/day limit
- [x] Functional mobile app (React Native + Expo)
- [x] CI/CD configured
- [x] Multilanguage support (English, Spanish, Portuguese)
- [x] Integrate Pet-ReID-IMAG model with the backend
- [x] Real-time embedding extraction (2048-dim vectors via ResNeSt-101)
- [x] Real canine nose matching (cosine similarity with configurable threshold)
- [x] Sample nose test images and end-to-end verification tests
- [x] Admin web dashboard with statistics and user management

## Phase 1.5 - Web App & Premium (Complete)

- [x] Full web application at `/app` mirroring the mobile app
- [x] All screens replicated: login, register, home, add dog, profile, vaccines, QR, scan nose, scan QR, result
- [x] Same role-based permissions on web and mobile
- [x] Shared backend and database between mobile and web
- [x] Users can login from either platform with the same account
- [x] Unlimited verifications for Admin and Premium users
- [x] 3-language support on web app (ES / EN / PT)
- [x] Comprehensive README with architecture diagram and setup guides

## Phase 2 - Production & Payments

- [ ] Nose capture in the mobile app (expo-camera)
- [ ] Nose capture in the web app (WebRTC / getUserMedia)
- [ ] Model accuracy improvements (threshold tuning, ensemble methods)
- [ ] Mercado Pago payment integration for premium subscriptions
- [ ] Production deployment (Railway + EAS)
- [ ] Real Cloudflare R2 storage (currently mock)
- [ ] Refresh tokens and token rotation
- [ ] Push notifications for vaccine reminders

## Phase 3 - Advanced Features

- [ ] Shelter integration (bulk dog registration)
- [ ] Public dog lookup by QR (no login required)
- [ ] Lost & found report system
- [ ] Veterinary clinic portal
- [ ] Export health booklet as PDF
- [ ] Analytics dashboard for verification trends
