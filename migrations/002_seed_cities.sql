-- Migration: Seed cities table with initial data
INSERT INTO public.cities (name)
VALUES
    ('Київ'),
    ('Львів'),
    ('Одеса'),
    ('Харків'),
    ('Дніпро'),
    ('Запоріжжя')
ON CONFLICT (name) DO NOTHING;
