CREATE TABLE IF NOT EXISTS server (
  guild_id INTEGER PRIMARY KEY, 
  welcome_channel INTEGER,
  counting_channel INTEGER,
  log_channel INTEGER
);

CREATE TABLE IF NOT EXISTS count_state (
  guild_id INTEGER PRIMARY KEY,
  current_count INTEGER,
  best_count INTEGER,
  last_user_id INTEGER
);
