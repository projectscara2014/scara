import time
import sys
gui = sys.modules['__main__']

def log(error) :

    class get_time() :

        def __init__(self) :
            self.t = ''
            self.year = ''
            self.month = ''
            self.day = ''
            self.hour = ''
            self.minute = ''
            self.second = ''
            self.week_day = ''

            self.get_time()

        def __print__(self) :
            print('time : ',self.t)
            print('year : ',self.year)
            print('month : ',self.month)
            print('day : ',self.day)
            print('hour : ',self.hour)
            print('minute : ',self.minute)
            print('second : ',self.second)
            print('week_day : ',self.week_day)

        def get_time(self) :

            def get_before_and_after(string,after,before) :
                
                dont_need_character_list = [' ']
                if((after in string) and (before in string)) :
                    i = string.index(after) + len(after)
                    j = string.index(before,i,i+5)
                    return_string = ''
                    for k in range(i,j) :
                        if(string[k] not in dont_need_character_list) :
                            return_string += string[k]
                    return return_string
                else :
                    print('before or after not in string')

            def one_character_to_two_character(string) : 
                if len(string) == 1 : 
                    return('0' + string)
                else : 
                    return(string)
                    
            self.t = str(time.localtime())
            self.year = get_before_and_after(self.t,'tm_year=',',')
            self.month = get_before_and_after(self.t,'tm_mon=',',')
            self.day = get_before_and_after(self.t,'tm_mday=',',')
            
            self.hour = one_character_to_two_character(get_before_and_after(self.t,'tm_hour=',','))
            self.minute = one_character_to_two_character(get_before_and_after(self.t,'tm_min=',','))
            self.second = one_character_to_two_character(get_before_and_after(self.t,'tm_sec=',','))
            
            self.week_day = get_before_and_after(self.t,'tm_wday=',',')
            day = {
                '00':'Mon',
                '01':'Tue',
                '02':'Wed',
                '03':'Thu',
                '04':'Fri',
                '06':'Sat',
                '07':'Sun'
            }
            month = {
                '1':'Jan',
                '2':'Feb',
                '3':'Mar',
                '4':'Apr',
                '5':'May',
                '6':'Jun',
                '7':'Jul',
                '8':'Aug',
                '9':'Sep',
                '10':'Aug',
                '11':'Nov',
                '12':'Dec'
            }

            self.week_day = day.get(self.week_day)
            self.month = month.get(self.month)

    t = get_time()
    return_string = t.day + '/' + t.month + '/' + t.year \
    + ' ' + t.hour + ':' + t.minute + ':' + t.second\
    + ' --> ' + error + '\n'

    with open(gui.WORKING_DIRECTORY + '/log.txt','a') as log: 
        log.write(return_string)
        
