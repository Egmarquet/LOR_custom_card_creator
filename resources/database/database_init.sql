CREATE TABLE sessions(
  session_id INTEGER PRIMARY KEY AUTOINCREMENT,
  last_updated_date TEXT
);

CREATE TABLE card(
  session_id INTEGER NOT NULL,
  card_id PRIMARY KEY INTEGER AUTOINCREMENT,
  type TEXT,
  name TEXT,
  hp TEXT,
  mana TEXT,
  pwr TEXT,
  card_text TEXT,
  lvl_up_text TEXT,
  tribe TEXT,
  region TEXT,
  image_path TEXT,
  FOREIGN KEY (session_id) references sessions(session_id)
);

CREATE TABLE card_keywords(
  card_id INTEGER NOT NULL,
  keyword_id INTEGER NOT NULL
);

CREATE TABLE keywords(
  keyword_id INTEGER PRIMARY KEY AUTOINCREMENT,
  keyword TEXT
);

INSERT INTO keywords (keyword) VALUES
  ('stun'),
  ('overwhelm'),
  ('last breath'),
  ('double attack'),
  ('regeneration'),
  ('tough'),
  ('frostbite'),
  ('elusive'),
  ('lifesteal'),
  ('quick attack'),
  ('barrier'),
  ('ephemeral'),
  ('challenger'),
  ('fleeting'),
  ('fearsome'),
  ("can't block"),
  ('burst'),
  ('fast'),
  ('slow'),
  ('skill')
