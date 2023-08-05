import clarus.services

def volume(output=None, **params):
    return clarus.services.api_request('SBSDR', 'Volume', output=output, **params)

