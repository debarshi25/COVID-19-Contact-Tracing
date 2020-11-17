from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from math import sin, cos, sqrt, atan2, radians
import pprint
import datetime
import sys
import os

current_location = os.path.dirname(os.path.abspath(__file__))
PEOPLE = []

class Person:

    def __init__(self, db_id, start_date, end_date, is_target=False):
        self.db_id = db_id
        self.start_date = start_date
        self.end_date = end_date
        self.is_target = is_target
        self.Base = automap_base()
        self.get_db()
        self.possible_times = self.get_possible_times()
        self.contacted_ids = []

    def get_db(self):
        sqlite_path = "sqlite:///" + current_location + "/LifeMap_GS" + str(self.db_id) + ".db"
        self.engine = create_engine(sqlite_path)
        self.session = Session(self.engine)
        self.Base.prepare(self.engine, reflect=True)
        self.apTable = self.Base.classes.apTable
        self.batteryTable = self.Base.classes.batteryTable
        self.categorySetTable = self.Base.classes.categoryTable
        self.cellEdgeTable = self.Base.classes.cellEdgeTable
        self.cellNodeTable = self.Base.classes.cellNodeTable
        self.cellTable = self.Base.classes.cellTable
        self.configureTable = self.Base.classes.configureTable
        self.edgeTable = self.Base.classes.edgeTable
        self.locationTable = self.Base.classes.locationTable
        self.noRadioTable = self.Base.classes.noRadioTable
        self.sensorUsageTable = self.Base.classes.sensorUsageTable
        self.stayCommentTable = self.Base.classes.stayCommentTable
        self.stayTable = self.Base.classes.stayTable

    def convert_to_date(self, date):
        return datetime.datetime.strptime(date[:-3], '%Y%m%d%H%M%S')
    
    def get_possible_times(self):
        possible_times = []
        times = self.session.query(self.stayTable).all()
        times = times if times else []
        for stay in sorted(times, key=lambda x: self.convert_to_date(x._stay_start_time)):
            stay_start_time = self.convert_to_date(stay._stay_start_time)
            if self.start_date <= stay_start_time and stay_start_time < self.end_date:
                possible_times.append(stay)
        return possible_times
    
    def is_within_n_miles(self, t_lat, t_lon, s_lat, s_lon, miles=5):
        R = 6373.0 #Earth Radius in km
        lat1 = radians(t_lat)
        lon1 = radians(t_lon)
        lat2 = radians(s_lat)
        lon2 = radians(s_lon)

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2*atan2(sqrt(a), sqrt(1-a))

        distance = R*c
        distance /= 1.609344 #Convert to miles
        return distance < miles

    
    def has_been_in_contact(self, person, target_possible_times):
        if person.db_id in self.contacted_ids:
            return True
        for target_time in target_possible_times:
            for stay_time in person.possible_times:
                t_start = self.convert_to_date(target_time._stay_start_time) - datetime.timedelta(minutes=30)
                t_end = self.convert_to_date(target_time._time_stay) + datetime.timedelta(minutes=30)

                s_start = self.convert_to_date(stay_time._stay_start_time)
                s_end = self.convert_to_date(stay_time._time_stay)

                latest_start = max(t_start, s_start)
                earliest_end = min(t_end, s_end)
                delta = (earliest_end - latest_start)
                #print(earliest_end, latest_start, delta.total_seconds())
                if delta.total_seconds() > 0:
                    target_loc = self.session.query(self.locationTable).filter(self.locationTable._node_id == target_time._node_id).first()
                    stay_loc = person.session.query(person.locationTable).filter(person.locationTable._node_id == stay_time._node_id).first()
                    t_lat, t_lon = target_loc._latitude/10**6, target_loc._longitude/10**6
                    s_lat, s_lon = stay_loc._latitude/10**6, stay_loc._longitude/10**6
                    if self.is_within_n_miles(t_lat, t_lon, s_lat, s_lon, miles=5):
                        person.contacted_ids.append(self.db_id)
                        self.contacted_ids.append(person.db_id)

                        start_idx = [self.convert_to_date(x._stay_start_time) for x in person.possible_times].index(s_start)
                        for new_target in [x for x in PEOPLE if x.db_id not in person.contacted_ids and x.db_id != person.db_id]:
                            person.has_been_in_contact(new_target, person.possible_times[start_idx:])
                        return





if __name__ == '__main__':
    db_id = int(sys.argv[1])
    date = datetime.datetime.strptime(sys.argv[2], '%m/%d/%Y')
    start_date = date + datetime.timedelta(days=-7) 
    end_date = date 
    target = Person(db_id, start_date, end_date, is_target=True)
    PEOPLE = [Person(x, start_date, end_date) for x in range(1,12) if x != db_id]

    for person in PEOPLE:
        target.has_been_in_contact(person, target.possible_times)

    PEOPLE.append(target)

    adj_matrix = [[0]*len(PEOPLE) for x in range(len(PEOPLE))]
    for person in PEOPLE:
        for p_id in range(1, 12):
            adj_matrix[person.db_id - 1][p_id-1] =  1 if p_id in person.contacted_ids else 0
        adj_matrix[person.db_id - 1][person.db_id-1] =  1 if len(person.contacted_ids) > 0 else 0

    pprint.pprint(adj_matrix)