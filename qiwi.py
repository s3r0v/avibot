import requests

def check_payment(user_id, deal, curs, db):
    buffer = []
    s = requests.Session()
    s.headers['authorization'] = 'Bearer ' + 'e4cb96e7c51bd2a3a436c09ceb559c58'
    parameters = {'rows': 10}
    h = s.get('https://edge.qiwi.com/payment-history/v2/persons/' + '+79028464204' + '/payments', params = parameters).json()['data']
    for comments in h:
        if comments["comment"] == f"{user_id}.{deal}" and comments["sum"]["currency"] == 643:
            buffer.append(comments["comment"])
            curs.execute(f"UPDATE users SET money=money+{comments['sum']['amount']} WHERE user_id={user_id};")
            db.commit()
            return True
    if len(buffer) == 0:
        return False