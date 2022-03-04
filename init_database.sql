CREATE TABLE users
(
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) NOT NULL,
    password VARCHAR(64) NOT NULL
);

CREATE TABLE contacts
(
    id SERIAL PRIMARY KEY,
    user_id integer ,
    name text NOT NULL,
    phone integer NOT NULL,
    CONSTRAINT contacts_name_key UNIQUE (name),
    CONSTRAINT contacts_user_id_fkey FOREIGN KEY (user_id)
        REFERENCES public.users (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);
