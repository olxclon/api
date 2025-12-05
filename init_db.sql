-- Database initialization for the API listings service
-- Run this against your Supabase/PostgreSQL database to provision
-- the tables expected by the application.

-- Enable pgcrypto for UUID generation (available in Supabase by default)
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Listings table
CREATE TABLE IF NOT EXISTS public.listings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT NOT NULL,
    description TEXT,
    price NUMERIC(12, 2),
    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc', now()),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc', now())
);

-- Maintain updated_at timestamps
CREATE OR REPLACE FUNCTION public.set_current_timestamp_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = timezone('utc', now());
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_listings_updated_at ON public.listings;
CREATE TRIGGER trg_listings_updated_at
BEFORE UPDATE ON public.listings
FOR EACH ROW EXECUTE FUNCTION public.set_current_timestamp_updated_at();

-- Seed demo data
INSERT INTO public.listings (title, description, price)
VALUES
    ('Sample listing A', 'A demo listing you can replace or remove.', 19.99),
    ('Sample listing B', 'Another example listing.', 42.00)
ON CONFLICT DO NOTHING;
