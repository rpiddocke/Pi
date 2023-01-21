
# Define variables
ds_pin = machine.Pin(16)  # Set pin to check and get onewire to look at it.
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))
sensors = ds_sensor.scan()

date_time = time.localtime()
date_string = "{}-{:02d}-{:02d}".format(date_time[0], date_time[1], date_time[2])

filename = f'{date_string}.csv'
#define function for reading temp sensors and writing to data file.

def tempsensor():

# Open a CSV file in append mode
#file = open("data.csv", "w")
    file = open(filename, "a")
    file.write("time,water,air\n")
    counter = 0
    while counter < 144: #cycle 144 times 10 minutes x 144 = 1440 minutes in a day
        ds_sensor.convert_temp()
        current_time = time.localtime()
        time_string = "{}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(current_time[0], current_time[1], current_time[2], current_time[3], current_time[4], current_time[5])
        time.sleep_ms(750)
        temp1 = round(ds_sensor.read_temp(sensors[0]), 2)
        temp2 = round(ds_sensor.read_temp(sensors[1]), 2)
        print("{},{},{}\n".format(time_string, temp1, temp2))
        file.write("{},{},{}\n".format(time_string, temp1, temp2))
        time.sleep(600) #write one reading every 10 minutes - 600
        counter += 1

        file.flush()

def putFile():
    ftp = FTP('192.168.0.10', 21, 'ftp_user', '|pV92W') # connect to host, default port
    ftp.pwd() # default, i.e.: user anonymous, passwd anonymous@
    ftp.storbinary('STOR ' +filename, open(filename)) # file to upload
    ftp.quit()               #disconect from FTP server
    os.remove(filename)
    
    