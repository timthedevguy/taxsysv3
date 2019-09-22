def social_details(backend, details, response, *args, **kwargs):
    return {'details': dict(backend.get_user_details(response), **details)}


def social_uid(backend, details, response, *args, **kwargs):
    return {'uid': backend.get_user_id(details, response)}
