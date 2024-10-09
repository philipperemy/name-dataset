import json
import logging
import sys
from typing import Union, Optional, Any, List, Dict

from flask import Flask, request
from paste.translogger import TransLogger
from waitress import serve

from names_dataset import NameDataset, NameWrapper
from names_dataset.emails import extract_names_from_email, try_to_split_with_two_last_names

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(threadName)s - %(message)s',
    stream=sys.stdout
)

app = Flask(__name__)
nd = NameDataset()


def _generate_output(d: Union[str, dict]) -> str:
    status = 'error' not in d
    return json.dumps({'status': status, 'message': d}, ensure_ascii=False, default=str)


def _validate_input(
        req, names: Union[str, List[str]],
        required: bool = True,
        default: Optional[Any] = None,
        var_type: Any = str
):
    if isinstance(names, str):
        names = [names]
    var = None
    for name in names:
        var = req.args.get(name)
        if var is not None:
            break
    if var is None and required:
        raise ValueError(f'Provide a parameter for [{names[0]}].')
    elif var is None:
        var = default
    return var_type(var) if var is not None else None


@app.errorhandler(404)
def _invalid_route(e):
    return _generate_output('invalid endpoint')


def _str2bool(s: Union[bool, str]) -> bool:
    if isinstance(s, bool):
        return s
    # noinspection PyBroadException
    try:
        return bool(eval(s))
    except Exception:
        if s.lower() in {'1', 'true', 'y', 't', 'yes', 'on'}:
            return True
        elif s.lower() in {'0', 'false', 'n', 'no', 'off'}:
            return False
    raise ValueError(f'Cannot convert to boolean: [{s}].')


def _process_inputs(req):
    name = _validate_input(req, 'name', required=True)
    n = _validate_input(req, 'n', required=False, default=5, var_type=int)
    use_first_names = _validate_input(req, 'use_first_names', required=True, var_type=_str2bool)
    gender = _validate_input(req, 'gender', required=False)
    country_alpha2 = _validate_input(req, 'country_alpha2', required=False)
    return name, n, use_first_names, gender, country_alpha2


@app.route('/')
def _main():
    endpoints = [a for a, b in globals().items() if not str(a).startswith('_') and 'function' in str(b)]
    return _generate_output(f'Welcome to the Name Search API! List of endpoints: [{", ".join(sorted(endpoints))}].')


def package_name(name: str, identifier: str) -> Optional[Dict]:
    if name is not None:
        result = nd.search(name)[identifier]
        if result is not None:
            result['name'] = name.title()
        return result
    else:
        return None


@app.route('/split', methods=['GET'])
def split():
    try:
        req = request
        q = req.args.get('q')
        if q is None:
            return _generate_output(
                'provide a parameter q, for example '
                'q=philipperemy@gmail.com or philipperemy'
            )
        else:
            first_name, last_name = extract_names_from_email(nd, q)
            last_name2 = None
            if first_name is None or last_name is None:
                first_name, last_name, last_name2 = try_to_split_with_two_last_names(nd, q)
            result_first_name = package_name(first_name, 'first_name')
            result_last_name = package_name(last_name, 'last_name')
            result_last_name2 = package_name(last_name2, 'last_name')
            result = {
                'first_name': result_first_name,
                'last_name': result_last_name,
                'last_name2': result_last_name2
            }
            return _generate_output({'result': result})
    except Exception as e:
        return _generate_output({'error': str(e)})


@app.route('/country_codes', methods=['GET'])
def country_codes():
    try:
        req = request
        alpha_2 = _str2bool(req.args.get('alpha_2', False))
        result = nd.get_country_codes(alpha_2=alpha_2, cache=True)
        return _generate_output({'result': result})
    except Exception as e:
        return _generate_output({'error': str(e)})


@app.route('/top', methods=['GET'])
def top():
    try:
        req = request
        n = int(req.args.get('n', 100))
        use_first_names = _str2bool(req.args.get('use_first_names', True))
        country_alpha2 = req.args.get('country_alpha2', None)
        gender = req.args.get('gender', None)
        result = nd.get_top_names(n, use_first_names, country_alpha2, gender)
        return _generate_output({'result': result})
    except Exception as e:
        return _generate_output({'error': str(e)})


@app.route('/search', methods=['GET'])
def search():  # legacy.
    try:
        name = request.args.get('q')
        if name is None:
            return _generate_output('provide a parameter q, for example q=Mike')
        else:
            result = nd.search(name)
            result['describe'] = NameWrapper(result).describe
            return _generate_output({'result': result})
    except Exception as e:
        return _generate_output({'error': str(e)})


@app.route('/fuzzy_search', methods=['GET'])
def fuzzy_search():
    try:
        name, n, use_first_names, gender, country_alpha2 = _process_inputs(request)
        result = nd.fuzzy_search(
            name=name, n=n, use_first_names=use_first_names, country_alpha2=country_alpha2, gender=gender
        )
        return _generate_output({'result': result})
    except Exception as e:
        return _generate_output({'error': str(e)})


@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    try:
        name, n, use_first_names, gender, country_alpha2 = _process_inputs(request)
        result = nd.auto_complete(
            name=name, n=n, use_first_names=use_first_names, country_alpha2=country_alpha2, gender=gender
        )
        return _generate_output({'result': result})
    except Exception as e:
        return _generate_output({'error': str(e)})


if __name__ == '__main__':
    serve(TransLogger(app, setup_console_handler=False), port=9999, threads=4)
