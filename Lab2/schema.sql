CREATE TABLE users(
  email text NOT NULL,
  firstname text NOT NULL,
  familyname text NOT NULL,
  gender text NOT NULL,
  city text NOT NULL,
  country text NOT NULL,
  password text NOT NULL,
  primary key(email)
);
