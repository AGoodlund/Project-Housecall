from schedule import Schedule

class Provider:
    _default = "unknown"
    
    name = _default
    address = _default
    specialty = _default
    phone_number = _default
        #USE AS STRING IN THE FORM OF ###-###-####
    email = _default
    website = _default
    accepting_new_clients = False
    ages_covered = [0,100]
    all_ages = False
    schedule = _default
    price = _default
    price_method = _default
        
    def add_age(self, lower_bound, upper_bound):
        self.ages_covered[0] = lower_bound
        self.ages_covered[1] = upper_bound
    
    def format_number(self):
        num = self.phone_number.split('-')
        print(num)
    #TODO: code verify phone_number is in proper form
    #TODO: hide price_method completely if price == _default
        
    def __str__(self):
        string = f"name:\t\t{self.name}\naddress:\t{self.address}\nspecialty:\t{self.specialty}\ncall num:\t{self.phone_number}\nemail:\t\t{self.email}\nwebsite:\t{self.website}\naccepting new:\t{self.accepting_new_clients}\ntreats ages:\t{self.ages_covered[0]}-{self.ages_covered[1]}\nall ages:\t{self.all_ages}"
        
        string = string + (f"\ncost:\t\t{self.price} per {self.price_method}" if self.price != self._default else '\t')
        
        string = string + f"\n\nschedule:\n{self.schedule}"
        return string

def testit():
    test = Provider()
    test.name = "healthy health people"
    test.address = "here there and everywhere"
    test.specialty = "bones"
    test.phone_number = "111-222-3344"
    test.email = "welldrinkyourbones@doctor.doctor"
    test.website = "notavampire.com"
    test.accepting_new_clients = True
    test.ages_covered = [5, 65]
    test.all_ages = True
    test.schedule = Schedule()
    
    #test.schedule.add_lunch_break(-1, 3)
        #this is a bug that would be fixed in a full project
    
    print(test)
    
    print("\ntesting functions:\n\tphone number:")
    test.format_number()


if __name__ == "__main__":
    testit()
