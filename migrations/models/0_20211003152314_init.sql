-- upgrade --
CREATE TABLE IF NOT EXISTS "users" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "name" VARCHAR(129) NOT NULL,
    "telegram_id" BIGINT NOT NULL UNIQUE,
    "api_key" VARCHAR(171) NOT NULL
);
CREATE TABLE IF NOT EXISTS "quotes" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "text" VARCHAR(280) NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "user_id" UUID NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(20) NOT NULL,
    "content" JSONB NOT NULL
);
