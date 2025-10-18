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
        #if price == _default: ignore method
        #make it so method can only be "per visit" or "monthly"
    
        
    def add_age(self, lower_bound, upper_bound):
        ages_covered[0] = lower_bound
        ages_covered[1] = upper_bound
    
    #TODO: code verify phone_number is in proper form
    #TODO: hide price_method completely if price == _default
        
    def __str__(self):
        return f"name:\t\t{self.name}\naddress:\t{self.address}\nspecialty:\t{self.specialty}\ncall num:\t{self.phone_number}\nemail:\t\t{self.email}\nwebsite:\t{self.website}\naccepting new:\t{self.accepting_new_clients}\ntreats ages:\t{self.ages_covered[0]}-{self.ages_covered[1]}\nall ages:\t{self.all_ages}\n\nschedule:\n\t{self.schedule}"

def test():
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
    
    print(test)


if __name__ == "__main__":
    test()
