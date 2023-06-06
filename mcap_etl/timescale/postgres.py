import psycopg2
import pandas as pd


class TimescaleWrapper:

    ROS_TO_POSTGRES = {
        'bool': 'bool',
        'float32': 'float4',
        'float64': 'float8',
        'int8': 'int2',
        'int16': 'int2',
        'int32': 'int4',
        'int64': 'int8',
        'uint8': 'int2',
        'uint16': 'int4',
        'uint32': 'int8',
        'uint64': 'numeric(20,0)',
        'string': 'text'
    }

    def __init__(self, host='localhost', port='5432', user='postgres', pwd='password', name='postgres'):
        try:
            self.__conn = psycopg2.connect(f'postgres://{user}:{pwd}@{host}:{port}/{name}')
        except psycopg2.OperationalError as e:
            print(e)
            exit()
        self.__curs = self.__conn.cursor()

    def convert(self, ros_type):
        return self.ROS_TO_POSTGRES[ros_type]

    def exists(self, name):
        self.__curs.execute(f"SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = '{name.lower()}');")
        return self.__curs.fetchone()[0]

    def columns(self, name):
        self.__curs.execute(f"SELECT * FROM {name.lower()} LIMIT 0")
        return [desc[0] for desc in self.__curs.description]

    def create(self, name, fields):
        create_cols = ['ts TIMESTAMPTZ NOT NULL']
        for field in fields:
            create_cols.append(f'{field.name} {self.convert(field.ros_type)}')

        sql = f"CREATE TABLE {name.lower()} ( {', '.join(create_cols)} );"
        self.__curs.execute(sql)

        try:
            sql = f"SELECT create_hypertable('{name.lower()}', 'ts');"
            self.__curs.execute(sql)
        except psycopg2.errors.UndefinedFunction:
            print('ERROR: TimescaleDB extension not installed')
            exit(1)

        sql = f"CREATE INDEX ix_ts_{name.lower()} ON {name.lower()} (ts DESC);"
        self.__curs.execute(sql)

        self.__conn.commit()

    def update(self, name, new_fields):
        add_cols = list()
        for field in new_fields:
            add_cols.append(f'ADD COLUMN {field.name} {self.convert(field.ros_type)}')

        sql = f"ALTER TABLE {name.lower()} {', '.join(add_cols)};"
        self.__curs.execute(sql)
        self.__conn.commit()

    def insert(self, name, df):
        table_cols = self.columns(name)
        values_sql = list()
        ordered_cols = list()

        for idx, row in df.iterrows():
            values = list()

            for col, val in row.items():
                if col == 'ts':
                    val = pd.to_datetime(val, unit='ms')
                    val = val.strftime('%Y-%m-%d %H:%M:%S.%f %Z')
                elif col not in table_cols:
                    continue

                if pd.isna(val):
                    values.append('NULL')
                elif isinstance(val, str):
                    val = val.replace("'", "\"")
                    values.append(f"'{val}'")
                else:
                    values.append(str(val))
                
                if idx == 0:
                    ordered_cols.append(col)
            
            values_sql.append('(' + ', '.join(values) + ')')
        
        sql = f"INSERT INTO {name.lower()} ({', '.join(ordered_cols)}) VALUES {', '.join(values_sql)};"
        self.__curs.execute(sql)
        self.__conn.commit()
