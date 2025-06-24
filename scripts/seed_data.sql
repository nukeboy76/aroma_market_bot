BEGIN;

-- Wine
INSERT INTO product (name, category, country, grape, description, price, image_url, post_url, thread_id) VALUES
('Cabernet Sauvignon', 'Wine', 'France', 'Cabernet Sauvignon', 'Классическое бордоское красное вино с насыщенным вкусом черной смородины', 1500, NULL, NULL, NULL),
('Chardonnay',         'Wine', 'France', 'Chardonnay',         'Белое вино Бургундии с нотами яблока и ванили',                  1400, NULL, NULL, NULL),
('Pinot Noir',         'Wine', 'France', 'Pinot Noir',         'Деликатное красное вино с ягодными и земляными оттенками',      1600, NULL, NULL, NULL),
('Sauvignon Blanc',    'Wine', 'France', 'Sauvignon Blanc',    'Освежающее белое вино с цитрусовыми и травяными нотами',         1300, NULL, NULL, NULL);

-- Cognac
INSERT INTO product (name, category, country, grape, description, price, image_url, post_url, thread_id) VALUES
('Hennessy VSOP',      'Cognac','France', NULL, 'Классический VSOP коньяк с оттенками ванили и специй',           4500, NULL, NULL, NULL),
('Rémy Martin VSOP',   'Cognac','France', NULL, 'Баланcированный VSOP с фруктово-цветочным букетом',              4400, NULL, NULL, NULL),
('Courvoisier VSOP',   'Cognac','France', NULL, 'Сложный VSOP коньяк с древесными и карамельными нотами',         4300, NULL, NULL, NULL),
('D\'Usse VSOP',       'Cognac','France', NULL, 'Дерзкий VSOP с интенсивным вкусом фруктов и шоколада',           4200, NULL, NULL, NULL);

-- Whiskey
INSERT INTO product (name, category, country, grape, description, price, image_url, post_url, thread_id) VALUES
('Johnnie Walker Blue Label',      'Whiskey','Scotland', NULL, 'Премиум шотландский бленд с глубоким вкусом дыма и специй', 8000, NULL, NULL, NULL),
('Jameson Irish Whiskey',          'Whiskey','Ireland',  NULL, 'Классический ирландский виски с мягким и слегка сладковатым послевкусием', 3000, NULL, NULL, NULL),
('Buchanan\'s Deluxe 12 Year',     'Whiskey','Scotland', NULL, '12-летний шотландский бленд с нотами меда и орехов',      5500, NULL, NULL, NULL),
('Crown Royal Canadian Whisky',    'Whiskey','Canada',   NULL, 'Канадский виски с бархатистой текстурой и фруктовыми акцентами', 3500, NULL, NULL, NULL);

-- Vodka
INSERT INTO product (name, category, country, grape, description, price, image_url, post_url, thread_id) VALUES
('Ketel One Vodka',    'Vodka','Netherlands', NULL, 'Чистая зерновая водка с мягким и чистым вкусом',     2500, NULL, NULL, NULL),
('Grey Goose Vodka',   'Vodka','France',      NULL, 'Премиальная французская водка с шелковистым послевкусием', 3000, NULL, NULL, NULL),
('Tito\'s Handmade Vodka','Vodka','USA',     NULL, 'Американская кукурузная водка с нейтральным вкусом и мягкостью', 2200, NULL, NULL, NULL),
('Belvedere Vodka',    'Vodka','Poland',      NULL, 'Польская рождественская водка с легкими ванильными и кремовыми оттенками', 2800, NULL, NULL, NULL);

COMMIT;
