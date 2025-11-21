-- backend/sql/schema.sql
-- enable extensions
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- users table
CREATE TABLE IF NOT EXISTS users (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  email TEXT UNIQUE NOT NULL,
  hashed_password TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- devices table
CREATE TABLE IF NOT EXISTS devices (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id uuid REFERENCES users(id) ON DELETE CASCADE,
  device_uuid TEXT UNIQUE NOT NULL, -- device-generated id
  display_name TEXT,
  public_key TEXT, -- device asymmetric key for mutual auth
  status TEXT DEFAULT 'active',
  last_active TIMESTAMP WITH TIME ZONE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- locations: store GPS points (SRID 4326)
CREATE TABLE IF NOT EXISTS locations (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  device_id uuid REFERENCES devices(id) ON DELETE CASCADE,
  recorded_at TIMESTAMP WITH TIME ZONE NOT NULL,
  geom geometry(Point,4326) NOT NULL,
  accuracy_m float,
  provider TEXT,
  speed float,
  altitude float,
  metadata JSONB DEFAULT '{}'::jsonb
);

CREATE INDEX IF NOT EXISTS idx_locations_geom ON locations USING GIST (geom);
CREATE INDEX IF NOT EXISTS idx_locations_device_time ON locations (device_id, recorded_at DESC);

-- trajectories cached table (optional) - precomputed linestrings for quick playback
CREATE TABLE IF NOT EXISTS trajectories (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  device_id uuid REFERENCES devices(id) ON DELETE CASCADE,
  period_start TIMESTAMP WITH TIME ZONE,
  period_end TIMESTAMP WITH TIME ZONE,
  geom geometry(LineString,4326),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_trajectories_geom ON trajectories USING GIST (geom);

-- geofences
CREATE TABLE IF NOT EXISTS geofences (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  owner_id uuid REFERENCES users(id) ON DELETE CASCADE,
  name TEXT,
  geom geometry(Polygon,4326) NOT NULL,
  action_on_enter JSONB DEFAULT '{}'::jsonb,
  action_on_exit JSONB DEFAULT '{}'::jsonb,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_geofences_geom ON geofences USING GIST (geom);

-- evidence (media metadata)
CREATE TABLE IF NOT EXISTS evidence (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  device_id uuid REFERENCES devices(id) ON DELETE CASCADE,
  recorded_at TIMESTAMP WITH TIME ZONE NOT NULL,
  geom geometry(Point,4326),
  s3_path TEXT,
  media_type TEXT,
  hash_sha256 TEXT,
  signed_by_server BOOLEAN DEFAULT false,
  metadata JSONB DEFAULT '{}'::jsonb,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- events (SIM change, geo fence triggers, remote actions logs)
CREATE TABLE IF NOT EXISTS events (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  device_id uuid REFERENCES devices(id) ON DELETE CASCADE,
  type TEXT NOT NULL,
  payload JSONB DEFAULT '{}'::jsonb,
  occurred_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);
