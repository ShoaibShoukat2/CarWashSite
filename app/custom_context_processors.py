

def session_value(request):
    return {
        'session': request.session.get('user_email'),
        'user_id': request.session.get('user_id'),
        'user_name': request.session.get('user_name')
        }



