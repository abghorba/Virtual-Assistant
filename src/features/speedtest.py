from speedtest import Speedtest

ONE_MEGABYTE_IN_BYTES = 1000000


class SpeedTester:
    def speed_check(self):
        """
        Performs a speed test, which tests for the
        upload, download, and ping

        :return: String result of the speed test
        """

        speedtest_result = ""

        try:
            print("Testing...")
            speedtest = Speedtest()
            speedtest.get_best_server()
            speedtest.download()
            speedtest.upload()
            speedtest_results = speedtest.results.dict()

            # Get variables from results dictionary
            server_name = speedtest_results["server"]["name"]
            server_country = speedtest_results["server"]["country"]
            server_sponsor = speedtest_results["server"]["sponsor"]
            client_ip = speedtest_results["client"]["ip"]
            client_isp = speedtest_results["client"]["isp"]
            download_speed_in_mb = round(
                (speedtest_results["download"] / ONE_MEGABYTE_IN_BYTES), 2
            )
            upload_speed_in_mb = round(
                (speedtest_results["upload"] / ONE_MEGABYTE_IN_BYTES), 2
            )
            ping_in_ms = round((speedtest_results["ping"]), 2)

            print(
                f"Connected to {server_sponsor} server\nLocation : {server_country}, {server_name}"
            )
            print(f"IP address : {client_ip}\nService Provider : {client_isp}")
            print(
                f"Download speed  : {download_speed_in_mb} mpbs\nUpload speed : {upload_speed_in_mb} mpbs\nPing : "
                f"{ping_in_ms} ms"
            )

            speedtest_result = (
                f"Download speed is {download_speed_in_mb} megabytes per second. Upload speed is "
                f"{upload_speed_in_mb} megabytes per second. Ping is {ping_in_ms} milliseconds."
            )

        except Exception:
            print("Could not execute speedtest.")

        return speedtest_result
