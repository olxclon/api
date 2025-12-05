-- Migration: Seed categories table with initial data
INSERT INTO public.categories (name)
VALUES
    ('Електроніка'),
    ('Нерухомість'),
    ('Транспорт'),
    ('Дім і сад'),
    ('Робота'),
    ('Послуги')
ON CONFLICT (name) DO NOTHING;
