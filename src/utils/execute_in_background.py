from multiprocessing import Process, Pipe


class BackgroundExecutor:
    def __init__(self, function, iterator):
        self.parent_conn, child_conn = Pipe()

        def loop(conn):
            results = []
            for arg in iterator:
                results.append(function(arg))
                if conn.poll() and conn.recv() == 1:
                    conn.send(results)

        self.process = Process(target=loop, args=(child_conn,))

    def execute_now(self):
        self.process.start()
        return self

    def get_most_up_to_date_results(self):
        if self.process.is_alive():
            self.parent_conn.send(1)
            self.results = self.parent_conn.recv()
        return self.results

    def join(self):
        self.process.join()


if __name__ == "__main__":
    #######################
    #### Usage example ####
    #######################
    from time import sleep


    # A function that takes time to execute
    def function(x):
        sleep(1)
        return x * (x - 1)


    # Launching execution in background
    background_executor = BackgroundExecutor(function, range(10)).execute_now()
    sleep(5)

    # Execute this to get most up to date results
    print(background_executor.get_most_up_to_date_results())
    sleep(5)

    print(background_executor.get_most_up_to_date_results())
