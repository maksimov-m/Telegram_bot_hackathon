import sqlite3


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def add_user(self, user_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO `users` (`user_id`) VALUES (?)", (user_id,))

    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            return bool(len(result))

    def add_history(self, user_id, req_id, uid_doctor, uid_usl, date):
        with self.connection:
            return self.cursor.execute("INSERT INTO `history` (`user_id`, `req_id`, `name_doctor`, `name_usl`, `date`) VALUES (?, ?, ?, ?, ?)",
                                         (user_id, req_id, uid_doctor, uid_usl, date,))

    def set_question(self, user_id, question):
        with self.connection:
            status = "waiting"
            return self.cursor.execute("INSERT INTO `questions_clients` (`user_id`, `question`, `status`) VALUES (?, ?, ?)", (user_id, question, status,))

    def set_name(self, user_id, name):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `name` = ? WHERE `user_id` = ?", (name, user_id,))

    def set_secondname(self, user_id, secondname):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `secondname` = ? WHERE `user_id` = ?", (secondname, user_id,))

    def set_patronymic(self, user_id, patronymic):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `patronymic` = ? WHERE `user_id` = ?", (patronymic, user_id,))

    def get_questions(self):
        with self.connection:
            return self.cursor.execute("SELECT * FROM `questions_clients`").fetchall()

    def set_data_birth(self, user_id, data):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `data_of_birth` = ? WHERE `user_id` = ?", (data, user_id,))

    def set_sex(self, user_id, sex):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `sex` = ? WHERE `user_id` = ?", (sex, user_id,))

    def set_number(self, user_id, number):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `number` = ? WHERE `user_id` = ?", (number, user_id,))

    def set_status_answer(self, answer, id):
        with self.connection:
            return self.cursor.execute("UPDATE `questions_clients` SET `status` = 'done', `answer` = ? WHERE `id` = ?", (answer, id,))

    def get_FAQ(self):
        with self.connection:
            result = self.cursor.execute("SELECT `question`, `answer` FROM `FAQ`")
            mass = []
            for i in result:
                mass.append(i)
            return mass

    def get_signup(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `signup` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                signup = str(row[0])
            return signup

    def get_name(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `name` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                name = str(row[0])
            return name

    def get_secondname(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `secondname` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                secondname = str(row[0])
            return secondname

    def get_patronymic(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `patronymic` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                patronymic= str(row[0])
            return patronymic

    def get_birth_day(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `data_of_birth` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                data_of_birth = str(row[0])
            return data_of_birth

    def get_sex(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `sex` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                sex = str(row[0])
            return sex

    def get_user_ud(self):
        with self.connection:
            result = self.cursor.execute("SELECT `user_id` FROM `users`").fetchall()
            return result

    def get_number(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `number` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                number = str(row[0])
            return number

    def get_history(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `history` WHERE `user_id` = ?", (user_id,)).fetchall()
            return result

    def del_history(self, user_id, req_id):
        with self.connection:
            result = self.cursor.execute("DELETE FROM `history` WHERE `user_id` = ? AND `req_id` = ?", (user_id,req_id,))
            return result


    def set_signup(self, user_id, signup):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `signup` = ? WHERE `user_id` = ?", (signup, user_id,))
