# ShadowTrace

ShadowTrace — a legal, privacy-first real-time phone location intelligence & recovery platform.
This repo contains:
- backend: FastAPI + PostgreSQL + PostGIS
- mobile: React Native (Android-first)
- dashboard: Next.js visualization

Focus: Spatial database features (PostGIS) — trajectories, geofences, spatial queries, and forensic evidence packaging.

See docs/ for ERD, demo instructions, and lecturer notes.
          #test command 
curl -X POST "http://localhost:8000/api/v1/devices/<device_id>/locations" \
 -H "Authorization: Bearer <token>" \
 -H "Content-Type: application/json" \
 -d '[
  {"lat": -1.2921, "lon": 36.8219, "recorded_at":"2025-11-21T10:00:00Z", "accuracy":5.0},
  {"lat": -1.2922, "lon": 36.8220, "recorded_at":"2025-11-21T10:02:00Z", "accuracy":5.0}
 ]'


       #fetch trajectory 

curl "http://localhost:8000/api/v1/devices/<device_id>/trajectory?start=2025-11-21T00:00:00Z&
end=2025-11-21T23:59:59Z" -H "Authorization: Bearer <token>"






Track lost or stolen phones with real-time location updates

Store and query location history using a spatial database (PostGIS)

Create geofences (alerts when a device enters/exits an area)

Capture evidence (images, videos) remotely

Perform remote actions on the device (ring, lock, limited “lost mode”)

Provide a web dashboard for map visualization and analytics

Provide a mobile app for the user device (React Native)

Focus on a spatial database with PostGIS to show advanced queries 
