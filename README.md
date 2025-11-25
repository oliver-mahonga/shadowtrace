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








queries 
#phones in 1 km      
SELECT name
FROM lost_items
WHERE ST_DWithin(
    last_seen,
    ST_GeogFromText('POINT(36.8210 -1.2920)'),
    1000
);



#nearest phone 
SELECT name, ST_Distance(
    last_seen,
    ST_GeogFromText('POINT(36.8210 -1.2920)')
) AS distance_meters
FROM lost_items
ORDER BY distance_meters
LIMIT 1;



#customer polygon 
SELECT name
FROM lost_items
WHERE ST_Within(
    last_seen,
    ST_GeogFromText('POLYGON((36.819 -1.295, 36.829 -1.295, 36.829 -1.290, 36.819 -1.290, 36.819 -1.295))')
);




#distance btn 2 phones
SELECT a.name AS phone1, b.name AS phone2, ST_Distance(a.last_seen, b.last_seen) AS distance_meters
FROM lost_items a, lost_items b
WHERE a.id <> b.id
ORDER BY distance_meters
LIMIT 5;




#introduction
A spatial database is a database optimized to store, query, and manage geographical or location-based data.
Unlike regular databases, it can handle points, lines, polygons, and complex geometries, and allows queries like "find all points within a radius" or "find nearest objects".

#where it can be used 


GPS navigation apps (Google Maps, Waze)

Delivery or ride-hailing apps (Uber, Bolt)

Real estate apps (find nearby houses, plots, or stores)

Environmental monitoring (tracking rivers, forests, deforestation areas)

Public safety (fire stations, hospitals, or lost item tracking)