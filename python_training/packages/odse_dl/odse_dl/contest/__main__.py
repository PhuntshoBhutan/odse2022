from sys import argv

from . import (
    submit,
    register,
    scoreboard,
    rebuild_credentials,
)

if __name__ == '__main__':
    command, *args = argv[1:]
    submition_file = argv[1]

    if command == 'submit':
        submition_file = args[0]
        submit(submition_file)

    elif command == 'register':
        name = args[0]
        register(name)

    elif command == 'rebuild_credentials':
        token = args[0]
        rebuild_credentials(token)

    elif command == 'scoreboard':
        scoreboard()

    else:
        print('Command has to be one of: submit, register, rebuild_credentials, scoreboard')
