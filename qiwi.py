import requests

def check_payment(user_id, deal, curs, db):
    buffer = []
    s = requests.Session()
    s.headers['authorization'] = 'Bearer ' + '910e6098ac91ec688ce01ff235ca27a0'
    parameters = {'rows': 10}
    h = s.get('https://edge.qiwi.com/payment-history/v2/persons/' + '+79585675126' + '/payments', params = parameters).json()['data']
    for comments in h:
        if comments["comment"] == f"{user_id}.{deal}" and comments["sum"]["currency"] == 643:
            buffer.append(comments["comment"])
            return comments['sum']['amount']
    if len(buffer) == 0:
        return False
