-- Enable pgcrypto for UUID generation
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Users table (with current_data_provider_id)
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT UNIQUE NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    login_type TEXT NOT NULL
        CHECK (login_type IN ('manual', 'google', 'facebook')),
    external_id TEXT,
    password_hash TEXT,
    is_admin BOOLEAN DEFAULT FALSE,
    is_verified BOOLEAN DEFAULT FALSE,
    current_data_provider_id UUID
        REFERENCES data_providers(id) ON DELETE SET NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT chk_login_fields CHECK (
        (login_type = 'manual' AND password_hash IS NOT NULL AND external_id IS NULL)
        OR
        (login_type != 'manual' AND password_hash IS NULL AND external_id IS NOT NULL)
    ),
    UNIQUE (login_type, external_id)
);

-- Trigger function to auto-update `updated_at`
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_update_users_updated_at
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- Data providers
CREATE TABLE data_providers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Lookup table for Data Source Types (e.g. raw, processed, …)
CREATE TABLE data_source_types (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Lookup table for Aggregation Types (e.g. hour, day, year, …)
CREATE TABLE aggregation_types (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Data sources, now referencing a type
CREATE TABLE data_sources (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    data_provider_id UUID NOT NULL
        REFERENCES data_providers(id) ON DELETE CASCADE,
    data_source_type_id UUID NOT NULL
        REFERENCES data_source_types(id) ON DELETE RESTRICT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Many-to-many: which aggregations apply to each data source
CREATE TABLE data_source_aggregations (
    data_source_id UUID NOT NULL
        REFERENCES data_sources(id) ON DELETE CASCADE,
    aggregation_type_id UUID NOT NULL
        REFERENCES aggregation_types(id) ON DELETE RESTRICT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (data_source_id, aggregation_type_id)
);

-- Mapping users to providers (unchanged)
CREATE TABLE data_provider_users (
    user_id UUID NOT NULL
        REFERENCES users(id) ON DELETE CASCADE,
    data_provider_id UUID NOT NULL
        REFERENCES data_providers(id) ON DELETE CASCADE,
    role TEXT NOT NULL
        CHECK (role IN ('owner', 'editor', 'viewer')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (user_id, data_provider_id)
);

-- Seed Data Source Types
INSERT INTO data_source_types (name, description)
VALUES
  ('raw',       'Unmodified/raw sensor values'),
  ('processed', 'Values after enrichment or cleaning')
ON CONFLICT (name) DO NOTHING;

-- Seed Aggregation Types
INSERT INTO aggregation_types (name, description)
VALUES
  ('hour', 'Aggregate values by hour'),
  ('day',  'Aggregate values by day'),
  ('year', 'Aggregate values by year')
ON CONFLICT (name) DO NOTHING;
