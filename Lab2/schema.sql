CREATE TABLE IF NOT EXISTS users(
  token text,
  email text NOT NULL CHECK(email <> '') PRIMARY KEY,
  firstname text CHECK(firstname <> ''),
  familyname text NOT NULL CHECK(familyname <> ''),
  gender text NOT NULL CHECK(gender <> ''),
  city text NOT NULL CHECK(city <> ''),
  country text NOT NULL CHECK(country <> ''),
  password text NOT NULL CHECK(password <> ''),
  CONSTRAINT name_unique UNIQUE (token)
);

CREATE TABLE IF NOT EXISTS messages(
  message_id integer NOT NULL CHECK(message_id <> '') PRIMARY KEY autoincrement,
  sender text NOT NULL CHECK(sender <> ''),
  receiver text NOT NULL CHECK(receiver <> ''),
  content text
);
