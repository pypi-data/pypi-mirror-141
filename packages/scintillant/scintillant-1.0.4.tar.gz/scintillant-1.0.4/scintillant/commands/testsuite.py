"""
Commands for activating the test environment


"""
import sys
import os
import json
import time
from http import HTTPStatus
from zipfile import ZipFile
import multiprocessing
from livereload import Server
import click
import requests

from scintillant import addons_versions
from scintillant.apimodels import User, Client, SkillResponse, SkillRequest, Message
from scintillant.commands.utils import get_config


def create_snlt():
    with open(os.getcwd() + '/.snlt', 'w+') as snlt:
        if sys.platform == 'win32':
            std_path = 'C:\\snlt\\testsuite\\'
        else:
            std_path = '/ust/testsuite/'
        path = input("Specify the path where Python can create "
                     f"the test environment files ({std_path}): ")
        path = std_path if not path else path
        click.echo(path)
        json.dump({
            "skill_name": "bottle-skill-template",
            "skill_working_url": "http://localhost:8080",
            "testsuite": {
                "version": addons_versions['__testsuite__'],
                "path": path,
                "theme": "dark",
                "api_host": "localhost",
                "api_port": "8080"
            }
        }, snlt, sort_keys=True, indent=4)


def update_snlt():
    js = json.load(open(os.getcwd() + '/.snlt'))
    if sys.platform == 'win32':
        std_path = 'C:\\snlt\\testsuite\\'
    else:
        std_path = './testsuite/'
    path = input("Specify the path where Python can create "
                 f"the test environment files ({std_path}): ")
    path = std_path if not path else path
    with open(os.getcwd() + '/.snlt', 'w+') as snlt:
        if 'testsuite' in js and 'path' not in js['testsuite']:
            js['testsuite']['path'] = path
        elif 'testsuite' not in js:
            js['testsuite'] = {'theme': 'dark'}
            js['testsuite']['path'] = path
        json.dump(js, snlt, sort_keys=True, indent=4)


def install_suite(path):
    suite_release = ("https://github.com/PaperDevil/snlt_testsuite/releases/download/"
                     f"{addons_versions['__testsuite__']}"
                     "/dist.zip")
    r = requests.get(suite_release)
    os.makedirs(os.path.dirname(path + 'temp.zip'), exist_ok=True)
    with open(path + 'temp.zip', 'wb') as f:
        f.write(r.content)
    with ZipFile(path + 'temp.zip', 'r') as repo_zip:
        repo_zip.extractall(path)
    os.remove(path + 'temp.zip')


def get_current_app(app_path: str = None):
    try:
        click.echo("Tryng get application instance...")
        sys.path.append(app_path or os.getcwd())
        from manage import run_app
        return run_app
    except ImportError as exc:
        raise ImportError(
            "The specified path does not contain a valid manage.py file. "
            "Make sure you've installed all the dependencies from the "
            "requirements.txt file and created the run_app function correctly "
            "inside the manage.py file!"
        )


def start_bot_server(host: str = 'localhost', port: str = '8080'):
    app = get_current_app()
    click.echo("Starting application server...")
    try:
        app(host=host, port=port)
    except Exception as exc:
        click.echo(exc)


def initial_test_shell(skill_url: str) -> None:
    client: Client = Client(name='testshell')
    user: User = User(idx=0, username='Scintillant', client=client)
    text: str = "!start"
    context: dict = {}
    while True:
        if text in ['!quit', '!exit', '!stop']:
            break
        data = SkillRequest(
            message=Message(user=user, text=text),
            context=context
        ).dict()
        request = requests.post(skill_url + '/skill', json=data).json()
        response = SkillResponse(**request)
        context = response.context
        if response.status == HTTPStatus.RESET_CONTENT:
            click.echo("End of operating...")
            break
        if response.status != HTTPStatus.OK:
            click.echo("End of operating with exception!")
            break

        click.echo(f"{response.status}: {response.text}")
        text = str(click.prompt('', type=str))


def start_test_shell():
    js = get_config()

    if not js:
        create_snlt()
        start_test_shell()
    if 'testsuite' not in js:
        update_snlt()
        start_test_shell()
    # Serving current backend application
    click.echo("Creating server process...")
    _process = multiprocessing.Process(target=start_bot_server, args=(
        js['testsuite'].get('api_host', 'localhost'), js['testsuite'].get('api_port', '8080')
    ))
    _process.start()
    # Starting Shell for testing bot
    click.echo("Starting testshell inputs...")
    time.sleep(3)
    initial_test_shell(js['skill_working_url'])
    _process.terminate()
    _process.join()


def start_test_suite():
    js = get_config()
    if not js:
        create_snlt()
        return start_test_suite()
    if 'testsuite' not in js or 'path' not in js['testsuite']:
        update_snlt()
        return start_test_suite()
    else:
        test_suite_path = js['testsuite']['path']
        install_suite(test_suite_path)

    if not os.path.exists(test_suite_path):
        install_suite(test_suite_path)
        return start_test_suite()

    # Serving current backend application
    click.echo("Creates processes...")
    _process = multiprocessing.Process(target=start_bot_server, args=(
        js['testsuite'].get('api_host', 'localhost'), js['testsuite'].get('api_port', '8080')
    ))
    _process.start()
    # Serving testsuite frontend application
    click.echo("starting testsuite...")
    server = Server()
    server.serve(root=test_suite_path, default_filename='index.html')
