def social_details(backend, details, response, *args, **kwargs):
    return {'details': dict(backend.get_user_details(response), **details)}
