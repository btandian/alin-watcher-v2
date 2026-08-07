from src.watcher import run_watcher


def main():
    try:
        run_watcher()

    except Exception as error:
        print(
            f"Erreur : {error}"
        )


if __name__ == "__main__":
    main()