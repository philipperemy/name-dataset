import json
import logging
import sys
from typing import Union

from flask import Flask, request
from paste.translogger import TransLogger
from waitress import serve

from names_dataset import NameDataset, NameWrapper
from names_dataset.emails import extract_names_from_email

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(threadName)s - %(message)s',
    stream=sys.stdout
)

app = Flask(__name__)
nd = NameDataset()


def generate_output(d: Union[str, dict], status: bool) -> str:
    return json.dumps({'status': status, 'message': d}, ensure_ascii=False, default=str)


@app.errorhandler(404)
def invalid_route(e):
    return generate_output('invalid endpoint', status=False)


@app.route('/')
def main():
    return generate_output('Welcome user! Name dataset api. query /search to perform a search.', status=True)


def str2bool(s: Union[bool, str]) -> bool:
    if isinstance(s, bool):
        return s
    # noinspection PyBroadException
    try:
        return bool(eval(s))
    except Exception:
        if s.lower() in ['1', '0', 'true', 'y']:
            return True
        return False


@app.route('/split', methods=['GET'])
def split():
    try:
        req = request
        q = req.args.get('q')
        if q is None:
            return generate_output(
                'provide a parameter q, for example '
                'q=philipperemy@gmail.com or philipperemy', status=False
            )
        else:
            first_name, last_name = extract_names_from_email(nd, q)
            if first_name is not None:
                result_first_name = nd.search(first_name)['first_name']
            else:
                result_first_name = None
            if last_name is not None:
                result_last_name = nd.search(last_name)['last_name']
            else:
                result_last_name = None
            result_first_name['name'] = first_name
            result_last_name['name'] = last_name
            result = {
                'first_name': result_first_name,
                'last_name': result_last_name
            }
            return generate_output({'result': result}, status=True)
    except Exception as e:
        return generate_output({'error': str(e)}, status=True)


@app.route('/country_codes', methods=['GET'])
def country_codes():
    try:
        req = request
        alpha_2 = str2bool(req.args.get('alpha_2', False))
        result = nd.get_country_codes(alpha_2=alpha_2)
        return generate_output({'result': result}, status=True)
    except Exception as e:
        return generate_output({'error': str(e)}, status=True)


@app.route('/top', methods=['GET'])
def top():
    try:
        req = request
        n = int(req.args.get('n', 100))
        use_first_names = str2bool(req.args.get('use_first_names', True))
        country_alpha2 = req.args.get('country_alpha2', None)
        gender = req.args.get('gender', None)
        result = nd.get_top_names(n, use_first_names, country_alpha2, gender)
        return generate_output({'result': result}, status=True)
    except Exception as e:
        return generate_output({'error': str(e)}, status=True)


@app.route('/search', methods=['GET'])
def search():
    try:
        req = request
        q = req.args.get('q')
        if q is None:
            return generate_output('provide a parameter q, for example q=Mike', status=False)
        else:
            result = nd.search(q)
            result['describe'] = NameWrapper(result).describe
            return generate_output({'result': result}, status=True)
    except Exception as e:
        return generate_output({'error': str(e)}, status=True)


if __name__ == '__main__':
    serve(TransLogger(app, setup_console_handler=False), port=8888, threads=4)
