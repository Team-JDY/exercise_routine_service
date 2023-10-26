import sys#
sys.path.append("utils/db_simulator")

import psycopg2, random, datetime, faker, string


class db_Simulator:
    def __init__(self, db_name, user, passwd, user_num, db_month, routine_avg, success_prob_avg, port=5432, host="localhost"):
        self.db_name = db_name
        self.user = user
        self.passwd = passwd
        self.user_num = user_num
        self.routine_avg = routine_avg
        self.success_prob = success_prob_avg
        self.port = port
        self.host = host

        last_day = 30 if db_month in [4, 6, 9, 11] else 31 if db_month in [1, 3, 5, 7, 8, 10, 12] else 28
        self.first_day = datetime.datetime(2023, db_month, 1).date()
        self.last_day = datetime.datetime(2023, db_month, last_day).date()

        self.exercise_list = ["사이클", "수영", "웨이트", "런닝", "걷기", "축구", "등산", "배드민턴", "농구", "크로스핏", "테니스", "골프",
                              "배구", "피구", "탁구", "클라이밍", "없음"]
        self.user_list = []
        #self.nickname_list = []
        self.serial_list = []

        self.db_connector = None
        self.db_manager = None
        self.namer = faker.Faker()

        self.count = 0

    def db_connect(self):
        '''db connection method'''
        try:
            self.db_connector = psycopg2.connect(
                dbname=self.db_name,
                user=self.user,
                password=self.passwd,
                host=self.host,
                port=self.port
            )
            self.db_manager = self.db_connector.cursor()
        except Exception as e:
            print(e)
            raise e

    def disconnect_db(self):
        '''db connection down'''
        self.db_manager.close()
        self.db_connector.close()

    def insert_users(self, col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11):
        '''Insert users tuple'''
        self.db_manager.execute(
            """
            INSERT INTO users (user_id, sns_login_info, nickname, height, weight, goal_weight, gender, birthdate, 
            weekly_exercise_freq, usual_exercise_intensity, preferred_exercise_type)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11)
        )
        #self.db_connector.commit()

    def insert_exercise_routines(self, col1, col2, col3, col4, col5, col6, col7, col8):
        '''Insert exercise_routines tuple'''
        self.db_manager.execute(
            """
            INSERT INTO exercise_routines (routine_id, user_id, exercise_name, start_time, end_time, base_date, 
            repetition_type, repetition_value)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (col1, col2, col3, col4, col5, col6, col7, col8)
        )
        #self.db_connector.commit()

    def insert_exercise_log(self, col1, col2, col3, col4, col5):
        '''Insert exercise_log tuple'''
        self.db_manager.execute(
            """
            INSERT INTO exercise_logs (log_id, user_id, routine_id, exercise_date, completed)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (col1, col2, col3, col4, col5)
        )
        #self.db_connector.commit()

    def generate_str(self, length):
        '''Generate random string'''
        text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

        return text

    def generate_serial_value(self, start, end):
        '''Random generation of serial values for each table'''
        while True:
            random_serial = random.randint(start, end)
            if random_serial not in self.serial_list:
                self.serial_list.append(random_serial)
                return random_serial

    def generate_gender(self):
        '''Random generation of gender values'''
        gender = random.choices(['M', 'F'], weights=[50, 50], k=1)[0]

        return gender

    def generate_date(self, start_date, end_date):
        '''DATE attribute generation method'''
        delta = end_date - start_date
        random_days = random.randint(0, delta.days)
        random_date = start_date + datetime.timedelta(days=random_days)

        return random_date.strftime('%Y-%m-%d')

    def generate_time(self):
        '''TIME attribute generation method'''
        temp_hour = random.randint(6, 22)
        temp_minute = random.randint(0, 59)
        time_value = f'{temp_hour:02}:{temp_minute:02}'

        return time_value

    def generate_repetition_value(self):
        '''Method for generating repetitions and days of repetitions'''
        header = random.choices(["1", "0"], weights=[80, 20], k=1)[0]  # 1: 반복 / 0: 하루
        week = "".join([str(random.randint(0, 1)) for _ in range(7)])

        return int(header + week, 2)

    def generate_routine_count(self):
        '''Routine Count Random Generation Method'''
        max_deviation = self.routine_avg // 2
        delta = random.randint(0, max_deviation)
        count_value = self.routine_avg + delta if random.choice([True, False]) else self.routine_avg - delta

        return count_value

    def repeat_day(self, start_day, last_day, repeat_bit):
        '''Create a list of exercise dates based on repeated bit values'''
        current_day = datetime.datetime.strptime(start_day, '%Y-%m-%d').date()
        repeat_type = (repeat_bit & 0b10000000) >> 7
        repeat_value = repeat_bit & 0b01111111

        if repeat_type == 0:
            return [current_day]

        date_list = []
        while current_day <= last_day:
            current_day_bit = 1 << (6 - current_day.weekday())

            if repeat_value & current_day_bit:
                date_list.append(current_day)

            current_day += datetime.timedelta(days=1)

        return date_list

    def convert_count_value(self):
        '''Convert count value by digit'''
        count_filled = str(self.count).zfill(5)

        return count_filled

    def user_generator(self):
        '''User generated methods'''
        #while True:
            #nickname = self.namer.first_name()
            #if nickname not in self.nickname_list:
                #self.nickname_list.append(nickname)
                #break
        nickname = self.namer.first_name()
        user_id = self.convert_count_value()
        sns_info = self.generate_str(20)
        gender = self.generate_gender()
        birthdate = self.generate_date(datetime.datetime(1980, 1, 1), datetime.datetime(2010, 12, 31))
        exercise_freq = random.randint(0, 7)
        exercise_intensity = random.randint(1, 5)
        exercise_type = self.exercise_list[random.randint(0, len(self.exercise_list) - 1)]
        if gender == "M":
            height = round(random.uniform(165, 190), 1)
            weight = round(random.uniform(60, 100), 1)
            goal_weight = weight - round(random.uniform(3, 7), 1)
        else:
            height = round(random.uniform(150, 168), 1)
            weight = round(random.uniform(40, 60), 1)
            goal_weight = weight - round(random.uniform(3, 10), 1)

        self.user_list.append(user_id)
        self.insert_users(user_id, sns_info, nickname, height, weight, goal_weight, gender, birthdate, exercise_freq,
                          exercise_intensity, exercise_type)

    def routine_log_generator(self, user_id):
        '''Method of adding routine and generating exercise history'''
        routine_id = self.generate_serial_value(10000, 99999)
        user_id = user_id
        exercise_name = self.generate_str(5)
        start_time = self.generate_time()
        end_time = (datetime.datetime.strptime(start_time, '%H:%M') + datetime.timedelta(hours=1)).strftime('%H:%M')
        base_date = (self.first_day + datetime.timedelta(days=random.randint(0, 25))).strftime('%Y-%m-%d')
        repetition_type = random.randint(1, 9)  # NOT USE
        repetition_value = self.generate_repetition_value()

        self.insert_exercise_routines(routine_id, user_id, exercise_name, start_time, end_time, base_date,
                                      repetition_type, repetition_value)

        date_list = self.repeat_day(base_date, self.last_day, repetition_value)
        for date in date_list:
            log_id = self.generate_serial_value(1000000, 9999999)
            exercise_date = date.strftime('%Y-%m-%d')
            completed = random.choices(["true", "false"], weights=[self.success_prob, 100 - self.success_prob], k=1)[0]

            self.insert_exercise_log(log_id, user_id, routine_id, exercise_date, completed)

    def generate_process(self):
        '''Actual operation process'''
        for _ in range(self.user_num):
            self.count += 1
            self.user_generator()
            if self.count % 100 == 0:
                print(f'Complete creation of {self.count} users')

        for user_id in self.user_list:
            for _ in range(self.generate_routine_count()):
                self.routine_log_generator(user_id)
            print(f'Complete creation of {self.user_list.index(user_id) + 1} users')

        self.db_connector.commit()
        #self.user_list.clear()
        #self.nickname_list.clear()
        #self.serial_list.clear()

db_name = "test"
user = "testuser2"
passwd = "test123"
user_num = 10000
db_month = 10
routine_avg = 10
success_prob_avg = 60

test_obj = db_Simulator(db_name, user, passwd, user_num, db_month, routine_avg, success_prob_avg)
test_obj.db_connect()
test_obj.generate_process()
#test_obj.disconnect_db()