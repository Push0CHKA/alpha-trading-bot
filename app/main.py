from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


if __name__ == "__main__":
    from app.bot.bot import run

    run()
