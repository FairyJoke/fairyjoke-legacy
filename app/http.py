from flask import request

def get_params() -> dict:
    result = request.get_json() or request.form or request.args or {}
    return dict(result)
