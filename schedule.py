class Schedule:
    #runs on a 24hr clock    
    def __init__(self, opening = 9, closing = 17):
        self.time = [opening, closing]
        self.lunch_break = False
        
        self.week = {
            "Monday": self.time,
            "Tuesday": self.time,
            "Wednesday": self.time,
            "Thursday": self.time,
            "Friday": self.time,
            "Saturday": self.time,
            "Sunday": self.time
            }
    
    def add_time(self, day, start, end):
        self.week[day] = [start, end]
        
    def add_lunch_break(self, start = 12, end = 1, lunch_day = 'all'):
        if self.lunch_break == True:
            self.change_lunch_break(start, end, lunch_day)
            return
        
        self.lunch_break = True
        
        if lunch_day == 'all':
            for day in self.week:
                self.week[day].append([start, end])
            return
        self.week[day].append([start, end])
        
    def change_lunch_break(self, start, end, lunch_day = 'all'):
        if self.lunch_break == True:
            if lunch_day == 'all':
                for day in self.week:
                    self.week[day][2][0] = start
                    self.week[day][2][1] = end
            else:
                self.week[lunch_day][2][0]=start
                self.week[lunch_day][2][1]=end
        
    def translate_to_am_pm(self, num=13):
        num = int(num)
        if int(num) > 12:
            return str(num-12)+'pm'
        return str(num)+'am'
    
    ##turn string into a 24 hr number
    def translate_from_am_pm(self, num):
        num = str.lower(num)
        
        spot = num.find('am')
        if(spot != -1):
            return int(num[:spot])
        
        spot = num.find('pm')
        if(spot != -1):
            return (int(num[:spot])+12)%24
        
        return False
    
    def close_day(self, day):
        self.week[day] = "Closed"
        
    def detect_closed(self):
        for day in self.week:
            o = self.week[day][0]
            c = self.week[day][1]
            if o == c:
                self.close_day(day)
            
    def __str__(self):
        output = ""
        for day in self.week:
            #print(type(self.week[day]))
            output = output + day + ':\n\t' + (self.translate_to_am_pm(self.week[day][0]) + '-' + self.translate_to_am_pm(self.week[day][1]) + ("\n\tClosed from: " + self.translate_to_am_pm(self.week[day][2][0]) + '-' + (self.translate_to_am_pm(self.week[day][2][1])) if self.lunch_break == True else '') if type(self.week[day]) is list else self.week[day])
            output = output + '\n'
        return output
    
def test():
    
    testit = Schedule()
                       
    print(testit)
        #test initialization
    print('\n')
    testit.add_lunch_break(13, 15)
    print(testit)
        #test adding lunch
    print('\n')
    testit.change_lunch_break('13',14)
    print(testit)
        #test changing lunch break
    print('\n')
    testit.add_lunch_break(14,15)
    print(testit)
        #test error checking on adding a lunch that already exists
    
    print(testit.translate_from_am_pm("1am"))
    print(testit.translate_from_am_pm("4pm"))
        #test translation function
    
    print('\n')
    testit.add_time("Monday", 0,0)
    testit.detect_closed()
    print(testit)


if __name__ == "__main__":
    test()