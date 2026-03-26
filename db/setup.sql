CREATE TABLE IF NOT EXISTS server(
    guild_id INTEGER PRIMARY KEY,
    welcome_channel INTEGER,
    counting_channel INTEGER,
    log_channel INTEGER
);
CREATE TABLE IF NOT EXISTS count_state(
    guild_id INTEGER PRIMARY KEY,
    current_count INTEGER,
    best_count INTEGER,
    last_user_id INTEGER
);
CREATE TABLE IF NOT EXISTS user(
    user_id INTEGER,
    guild_id INTEGER,
    exp INTEGER DEFAULT 0,
    last_time_collected INTEGER,
    currency INTEGER DEFAULT 100,
    PRIMARY KEY (user_id, guild_id)
);
CREATE TABLE IF NOT EXISTS user_inventory(
  user_id INTEGER,
  guild_id INTEGER,
  item_id TEXT,
  item_name TEXT,
  quantity INTEGER DEFAULT 1,
  PRIMARY KEY (user_id, guild_id, item_id)
);
CREATE TABLE IF NOT EXISTS shop(
  guild_id INTEGER,
  item_id TEXT,
  item_name TEXT,
  price INTEGER,
  PRIMARY KEY (guild_id, item_id)
);
