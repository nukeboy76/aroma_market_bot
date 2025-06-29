BEGIN;

-- Wine
INSERT INTO product (name, category, country, grape, description, price, image_url, post_url, thread_id) VALUES
  ('Château du Soleil 2018',   'Wine',   'France', 'Merlot',      'Плотное красное вино с нотами спелой вишни и тёмного шоколада.',                    239900,
    'https://t.me/aroma_market_group/7/photo',
    'https://t.me/aroma_market_group/7',
    7),
  ('Barolo La Terra 2017',      'Wine',   'Italy',  'Nebbiolo',    'Элегантное сухое вино с выразительными тонами розы и пряных специй.',                289900,
    'https://t.me/aroma_market_group/10/photo',
    'https://t.me/aroma_market_group/10',
    10),
  ('Marques de Sol Crianza 20', 'Wine',   'Spain',  'Tempranillo', 'Фруктовое красное вино с 6-месячной выдержкой в американском дубе, с нотами ягод и специй.', 119900,
    'https://t.me/aroma_market_group/13/photo',
    'https://t.me/aroma_market_group/13',
    13);

-- Whiskey
INSERT INTO product (name, category, country, grape, description, price, image_url, post_url, thread_id) VALUES
  ('Glen Highland 12 y.o.',          'Whiskey', 'Scotland', NULL, 'Выдержанный в бочках из-под бурбона, с карамельными и древесными нотами.', 459900,
    'https://t.me/aroma_market_group/8/photo',
    'https://t.me/aroma_market_group/8',
    8),
  ('Kentucky Straight Bourbon',      'Whiskey', 'USA',      NULL, 'Аромат дуба, ванили и карамели в каждой капле настоящего американского бурбона.', 179900,
    'https://t.me/aroma_market_group/12/photo',
    'https://t.me/aroma_market_group/12',
    12);

-- Brandy
INSERT INTO product (name, category, country, grape, description, price, image_url, post_url, thread_id) VALUES
  ('Gran Reserva Brandy XO', 'Brandy', 'Spain', NULL, 'Мягкий бренди с ванильно-карамельным послевкусием и тонким пряным ароматом.', 319900,
    'https://t.me/aroma_market_group/9/photo',
    'https://t.me/aroma_market_group/9',
    9);

-- Liqueur
INSERT INTO product (name, category, country, grape, description, price, image_url, post_url, thread_id) VALUES
  ('Irish Meadow Cream', 'Liqueur', 'Ireland', NULL, 'Нежный ликёр на основе виски, с мягким сливочным и ванильным профилем.', 139900,
    'https://t.me/aroma_market_group/11/photo',
    'https://t.me/aroma_market_group/11',
    11);

COMMIT;