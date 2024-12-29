import argparse
from logger import Logger


def main():
    # TODO Get email
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', dest='mail', type=str, required=True)
    mail = parser.parse_args().mail

    logger = Logger()
    logger.write_log('Program Started')
    # TODO Run program in background
    # TODO Create icon in taskbar
    # TODO Create script in %AppData%/Microsoft/Windows/Start Menu/Programs/Startup


if __name__ == "__main__":
    main()
