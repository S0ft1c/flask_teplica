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

            # create a table with user parameters
            self.c.execute("""create table if not exists `params` (
                                    id integer primary key,
                                    `temperature` real,
                                    `humanity`    real,
                                    `hb_persent`  real
                    )""")

            # this table for states of forks, hum. systems and 6 HB devices
            self.c.execute("""create table if not exists `states` (
                              id integer primary key,
                              `fork_state` bool,
                              `humanity_state` bool,
                              `hb_1` bool,
                              `hb_2` bool,
                              `hb_3` bool,
                              `hb_4` bool,
                              `hb_5` bool,
                              `hb_6` bool                                
                        )""")

            # it's to be cool, create a line with default parameters in `params` table (we don't needed to write ADD)
            self.c.execute("""insert into `params` (`temperature`, `humanity`, `hb_persent`) values (10, 10, 10)""")

            # insert data (default FALSE) for all devices
            self.c.execute("""insert into `states` (
            `fork_state`, 
            `humanity_state`,
            `hb_1`,
            `hb_2`,
            `hb_3`,
            `hb_4`,
            `hb_5`,
            `hb_6`
            ) values (
            False,
            FALSE,
            FALSE,
            FALSE,
            FALSE,
            FALSE,
            FALSE,
            FALSE
            )""")

        self.conn.commit()

    def update_user_params(self, t=0, h=0, hb=0):
        """
        This function updates user parameters from `params`
        :parameter: t - user's new temperature (default = -1, that means that we don't need to change info)
                    h - user's new humanity (default = -1, , that means that we don't need to change info)
                    hb - user's new ground_humanity % (default = -1, , that means that we don't need to change info)
        :return: bool (True - good or False - not good)
        """
        # if we have data, we'll update it
        if t != 0:
            self.c.execute("""update `params` set `temperature`=? where `id`=1""", (t,))
            self.conn.commit()
        if h != 0:
            self.c.execute("""update `params` set `humanity`=? where `id`=1""", (h,))
            self.conn.commit()
        if hb != 0:
            self.c.execute("""update `params` set `hb_persent`=? where `id`=1""", (hb,))
            self.conn.commit()
        return True

    def get_user_params(self):
        """
        this function gets all user parameters from sqlite3
        :return: tuple of data (id, temperature, humanity, hb_persent)
        """
        params_data = self.c.execute("""select * from `params` where id=1""")
        params = params_data.fetchone()
        return params

    def get_fork(self):
        """
        This function gets information about fork
        :return: tuple of data (fork_state)
        """
        fork_state = self.c.execute("""select `fork_state` from `states` where id=1""")
        return fork_state.fetchone()

    def update_fork(self, new_state: bool):
        """
        This function updates the state of fork
        :param new_state: new state of fork in boolean type (True or False)
        :return: None
        """
        self.c.execute("""update `states` set `fork_state`=? where id=1""", (new_state,))
        self.conn.commit()

    def get_humanity(self):
        """
        This funcrion gets information about humanity system state
        :return: tuple of data (humanity_state)
        """
        humanity_state = self.c.execute("""select `humanity_state` from `states` where id=1""")
        return humanity_state.fetchone()

    def update_humanity(self, new_state):
        """
        This function updates the state of humanity system
        :param new_state: new state of system in boolean type (True or False)
        :return: None
        """
        self.c.execute("""update `states` set `humanity_state`=? where id=1""", (new_state,))
        self.conn.commit()

    def get_hb_device(self, device_id):
        """
        This function gets information about state of hb_device
        :param device_id: the number of device (1-6)
        :return: tuple of data (device_state)
        """
        device_state = self.c.execute(f"""select `hb_{device_id}` from `states` where id=1""")
        return device_state.fetchone()

    def update_hb_device(self, device_id, new_state):
        """
        This function updates state of one hb_device
        :param device_id: device_id: the number of device (1-6)
        :param new_state: new state of system in boolean type (True or False)
        :return: None
        """
        self.c.execute(f"""update `states` set `hb_{device_id}`=? where id=1""", (new_state,))
        self.conn.commit()
