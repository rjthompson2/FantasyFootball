import time

def spedometer(function):
    def radar(*args, **kwargs):
        start = time.time()
        function(*args, **kwargs)
        end = time.time()
        print(f"{function.__name__} finished in {end-start} seconds")
    
    return radar