from celery import shared_task

@shared_task()
def buy_from_exchange(crypto_name, amount):
    print(f"Paying {amount} to international exchange for {crypto_name}")