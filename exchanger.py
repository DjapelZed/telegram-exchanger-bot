import requests, settings

class Exchanger:
    def __init__(self):
        self.ACCESS_KEY = settings.ACCESS_KEY
        self.url = "http://api.exchangeratesapi.io/v1"

    def get_latest(self):
        url = f"{self.url}/latest?access_key={self.ACCESS_KEY}"
        response = requests.get(url)
        data = response.json()
        if not "error" in data:
            rates = data["rates"]
            
            usd = rates["USD"]
            for rate in list(rates.keys()):
                rates[rate] /= usd # makes base currency USD
            return rates
        return {}

if __name__ == '__main__':
    ex = Exchanger()
    print(ex.get_latest())
