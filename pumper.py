from oanda import *


if __name__ == "__main__":
    instrument = Instrument(security.auth_key, 'AUD_SGD', 'S5')
    max_timestamp = instrument.conn.select_max(instrument.name, 'timestamp')
    if max_timestamp is None:
        max_timestamp = 0
    print('max_timestamp', max_timestamp)
    iter = 0

    while True:
        iter += 1
        print('iter', iter)
        print(instrument.name)

        if max_timestamp + 5 < datetime.now().timestamp():
            print('now', datetime.now().timestamp())
            print('get new candles')
            max_timestamp = instrument.get_last_candles()
            print('new max_timestamp', max_timestamp)
        else:
            delay = (max_timestamp + 5) - datetime.now().timestamp()
            print('max_timestamp', max_timestamp)
            print('now', datetime.now().timestamp())
            print('delay', delay)
            sleep(delay)

