from envparse import env

BOT_API_KEY = env.str("BOT_API_KEY")
DATABASE_URL = env.str("DATABASE_URL")
TELEGRAM_API_KEY = env.str("TELEGRAM_API_KEY")

TORTOISE_ORM = {
  "connections": {
    "default": DATABASE_URL
  },
  "apps": {
    "models": {
      "models": ["app.models", "aerich.models"],
      "default_connection": "default"
    }
  }
}
