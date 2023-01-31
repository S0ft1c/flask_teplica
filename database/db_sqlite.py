import sqlite3 as sql


class DataBase:
    """
    This is class for working with sqlite3
    """
    conn = None  # this is variable for a connection to sqlite3
    c = None  # this is the cursor for an execution operations to sqlite3

    def __init__(self, dropping_tables):
        """
        Initialization of cursor a connection to db
        and creating all needed tables
        :param: dropping_tables - if we want drop all data (for testing)
        """
        self.conn = sql.connect('data.db')
        self.c = self.conn.cursor()

        if dropping_tables:  # if we want drop all data (for testing)
            self.c.execute("""drop table if exists `params`""")
            # TODO: add new tables as needed

        # create a table with user parameters
        self.c.execute("""create table if not exists `params` (
                        id integer primary key,
                        `temperature` real,
                        `humanity`    real,
                        `hb_percent`  real
        )""")

        # it's to be cool, create a line with default parameters in `params` table (we don't needed to write ADD func)
        self.c.execute("""insert into `params` (`temperature`, `humanity`, `hb_persent`) values (10, 10, 10)""")

        self.conn.commit()

    def update_user_params(self, t=-1, h=-1, hb=-1):
        """
        This function updates user parameters from `params`
        :parameter: t - user's new temperature (default = -1, that means that we don't need to change info)
                    h - user's new humanity (default = -1, , that means that we don't need to change info)
                    hb - user's new ground_humanity % (default = -1, , that means that we don't need to change info)
        :return: bool (True - good or False - not good)
        """
        # if we have data, we'll update it
        if t != -1:
            self.c.execute("""update `params` set `temperature`=?""", (t,))
        if h != -1:
            self.c.execute("""update `params` set `humanity`=?""", (h,))
        if hb != -1:
            self.c.execute("""update `params` set `hb_percent`=?""", (hb,))

        return True

    def get_user_params(self):
        """
        this function gets all user parameters from sqlite3
        :return: list of data
        """
        params_data = self.c.execute("""select * from `params` where id=1""")
        params = params_data.fetchone()
        return params
