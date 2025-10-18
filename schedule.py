class Schedule:
    #runs on a 24hr clock    
    def __init__(self, opening = 9, closing = 17, lunch = False):
        self.time = [opening, closing]
        self.lunch_break = lunch
        
        self.week = {
            "mon": [self.time[0], self.time[1]],
            "tues": [self.time[0], self.time[1]],
            "wed": [self.time[0], self.time[1]],
            "thurs": [self.time[0], self.time[1]],
            "fri": [self.time[0], self.time[1]],
            "sat": [self.time[0], self.time[1]],
            "sun": [self.time[0], self.time[1]]
            }
    
    def add_time(self, day, start, end):
        self.week[day] = [start, end]
        
    def add_lunch_break(self, start, end, lunch_day = 'all'):
        self.lunch_break = True
            #this may be a useless but it's for data integrity
        if lunch_day == 'all':
            for day in self.week:
                self.week[day].append([True, start, end])
            return
        self.week[day].append([True, start, end])
    
    def __str__(self):
        return str(self.week)
    
def test():
    test = Schedule()
    test.add_lunch_break(13, 15)
    
    print(test)
    
    print('\n\n')
    temp = test.week["mon"]
    print(type(temp))
    print(temp[0])
    print(temp[1])
    print(temp[2][0])


if __name__ == "__main__":
    test()