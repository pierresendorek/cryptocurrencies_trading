from time import time


overtime_execution_list = []
monitoring_dict = {}

# decorator
def monitor_execution_time_stats(time_over_which_execution_is_logged):
    def monitor_execution_time_stats_(func):
        def wrapper(*args, **kwargs):
            t_start = time()
            res = func(*args, **kwargs)
            execution_time = time() - t_start
            max_time = func.__dict__.get("max_time", -float("inf"))
            if execution_time > max_time:
                func.__dict__["max_time"] = execution_time
                func.__dict__["argmax_time"] = {"args":args, "kwargs":kwargs}
            n_executions = func.__dict__.get("n_executions", 0) + 1
            func.__dict__["sum_execution_time"] = func.__dict__.get("sum_execution_time", 0) + execution_time
            func.__dict__["avg_execution_time"] = func.__dict__["sum_execution_time"] / n_executions
            func.__dict__["n_executions"] = n_executions
            #overtime_execution_list = func.__dict__.get("overtime_execution_list", [])
            #overtime_execution_list.append(execution_time)
            #func.__dict__["overtime_execution_list"] = overtime_execution_list
            if execution_time > time_over_which_execution_is_logged:
                #print("execution_time_is ", execution_time, " with ", {"args":args, "kwargs":kwargs})
                overtime_execution_list.append({"args": args, "kwargs": kwargs})
            return res
        wrapper.__dict__ = func.__dict__
        monitoring_dict[func.__name__] = func.__dict__
        return wrapper
    return monitor_execution_time_stats_



def get_monitoring_dict():
    return monitoring_dict

#def save_monitoring_dict():



if __name__ == "__main__":
    @monitor_execution_time_stats(1.0)
    def h(x):
        s = 0
        for i in range(10 ** x):
            s += 1
        return s

    for i in range(9):
        h(i)

    print(get_monitoring_dict())