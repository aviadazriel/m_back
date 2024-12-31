# neon
users_tbl = """CREATE TABLE users (
    id SERIAL PRIMARY KEY,                 -- Unique identifier for each user
    username VARCHAR(50) NOT NULL UNIQUE, -- Username, must be unique
    email VARCHAR(100) NOT NULL UNIQUE,   -- Email, must be unique
    phone VARCHAR(10) NOT NULL UNIQUE,   -- phone, must be unique
    password_hash VARCHAR(255) NOT NULL,  -- Hashed password for security
    first_name VARCHAR(50),               -- Optional first name
    last_name VARCHAR(50),                -- Optional last name
    profile_image_url TEXT,               -- URL to the user's profile image
    is_active BOOLEAN DEFAULT TRUE,       -- Indicates if the account is active
    is_admin BOOLEAN DEFAULT FALSE,       -- Indicates if the user is an admin
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Timestamp for creation
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Timestamp for last update
);"""

insert_users_query = """INSERT INTO users (username, email,phone, password_hash, first_name, last_name, profile_image_url, is_active, is_admin)
VALUES
    ('johndoe', 'john.doe@example.com','0522257283', 'hashed_password_1', 'John', 'Doe', 'https://example.com/johndoe.jpg', TRUE, FALSE),
    ('janedoe', 'jane.doe@example.com','0522257284', 'hashed_password_2', 'Jane', 'Doe', 'https://example.com/janedoe.jpg', TRUE, TRUE);
"""
articles = """
CREATE TABLE articles (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    image_url TEXT NOT NULL,
    published_date DATE NOT NULL,
    related_articles INT[],
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

insert_articles = """
INSERT INTO articles (title, description, image_url, published_date, related_articles)
VALUES
('סוגי ריביות, יתרונות וחסרונות',
 'במאמר זה נעמיק ביתרונות והחסרונות של כל סוג ריבית...',
 'https://www.sarit-lari.co.il/wp-content/uploads/2024/04/A-mortgage-for-any-purpose.png',
 '2024-01-08',
 ARRAY[2, 5, 6]),
('עמלת פירעון מוקדם',
 'מתכננים לסגור את המשכנתא מוקדם? לפני שאתם מתחילים...',
 'https://www.taxfinance.co.il/wp-content/uploads/2021/11/%D7%94%D7%97%D7%96%D7%A8-%D7%9E%D7%A1-%D7%9E%D7%A9%D7%9B%D7%A0%D7%AA%D7%90.jpg',
 '2024-01-11',
 ARRAY[1, 2, 3]),
('רכישת דירה ראשונה',
 'רכישת דירה ראשונה היא צעד מרגש, אך כרוך באתגרים כלכליים...',
 'https://www.hon.co.il/wp-content/uploads/2011/11/%D7%9E%D7%93%D7%A8%D7%99%D7%9B%D7%99-%D7%9E%D7%A9%D7%9B%D7%A0%D7%AA%D7%90%D7%95%D7%AA-55x55-1.jpg',
 '2024-01-15',
 ARRAY[1, 2, 3]);
-- Add remaining articles similarly

"""



news = """
CREATE TABLE news (
    id SERIAL PRIMARY KEY,                  -- Unique identifier for each news item
    title VARCHAR(255) NOT NULL,            -- Title of the news article
    link TEXT NOT NULL,                     -- Link to the news article
    description TEXT NOT NULL,              -- Brief description of the news
    image_url TEXT,                         -- URL of the news image
    source VARCHAR(100),                    -- Source of the news (e.g., Calcalist, Globes)
    publish_date DATE NOT NULL,             -- Publish date of the news
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Creation timestamp
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Update timestamp
);

"""

insert_news = """INSERT INTO news (title, link, description, image_url, source, publish_date)
VALUES
('הדירות החדשות בת"א מגיעות במחירים מפתיעים',
 'https://www.calcalist.co.il/real-estate/article/r1ens4yzke',
 'כתבה מרתקת על מחירי הנדל"ן בתל אביב ושינויים בשוק.',
 'https://pic1.calcalist.co.il/picserver3/crop_images/2024/11/06/HJ39gGFb1x/HJ39gGFb1x_0_0_2500_1667_0_x-large.jpg',
 'Calcalist',
 '2024-11-07'),
('שוק הנדל"ן בתנודתיות: מה צופן העתיד?',
 'https://www.calcalist.co.il/investing/article/rjegyri70',
 'לקוחות משלמים 70 אלף שקל בשנה לבנק למשכנתא, ולמרות זאת חייבים אותו הסכום.',
 'https://pic1.calcalist.co.il/picserver3/crop_images/2023/02/27/rkKfzJ5Rj/rkKfzJ5Rj_1_0_1000_668_0_x-large.jpg',
 'Calcalist',
 '2024-05-19'),
('תחזיות כלכליות לשוק הדיור בישראל',
 'https://www.calcalist.co.il/investing/article/hyb8hnokje',
 'שוק הדיור בוער: זינוק של 32% במשכנתאות בספטמבר לעומת הממוצע.',
 'https://pic1.calcalist.co.il/picserver3/crop_images/2024/09/05/HkhdvbPnR/HkhdvbPnR_0_0_2000_1333_0_x-large.jpg',
 'Calcalist',
 '2024-10-15');
"""