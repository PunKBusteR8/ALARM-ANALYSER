import  datetime as dt

def dummyAPIendPoint(pntId:str, start_time: dt.datetime, end_time: dt.datetime) -> []:
    """ retun a list of values
    """
    try:
        #numOfsamples = []
        num_of_samples = int((end_time - start_time).total_seconds() // 60)
        # Calculate difference
        #time_difference = end_time - start_time
        #numOfsamples = int(time_difference.total_seconds() // 60)
        # generate n number of value in numOfsamples between 200 to 300
        # numOfsamples = [1,2,3,4]
        random_values = [random.randint(200, 300) for _ in range(num_of_samples)]
        #return numOfsamples
        return random_values
    except Exception as e:
             # In case of error, return an empty list (or raise the error for debugging)
        print(f"API Error: {e}")
        return []
        
