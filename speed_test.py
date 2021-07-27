import speedtest

class SpeedTester():

    def speed_check(self):
        try:
            print('Testing...')
            s = speedtest.Speedtest()
            s.get_best_server()
            s.download()
            s.upload()
            res = s.results.dict()

            server = []
            server.append(res["server"]["name"])
            server.append(res["server"]["country"])
            server.append(res["server"]["sponsor"])

            client = []
            client.append(res["client"]["ip"])
            client.append(res["client"]["isp"])

            speed = []
            ONE_MB = 1000000
            speed.append((round((res["download"]/ONE_MB), 2)))
            speed.append((round((res["upload"]/ONE_MB), 2)))
            speed.append((round((res["ping"]), 2)))

            print(f'IP address : {client[0]}\nService Provider : {client[1]}')
            print(f'Connected to {server[2]} server\nLocation : {server[0]}, {server[1]}')
            print(f'Download speed  : {speed[0]} mpbs\nUpload speed : {speed[1]} mpbs\nPing : {speed[2]} ms ')

            speedtest_result = f'Download speed is {speed[0]} megabytes per second. Upload speed is {speed[1]} megabytes per second. Ping is {speed[2]} milliseconds.'
            return speedtest_result
        except Exception as e:
            print("Could not execute speedtest.")
