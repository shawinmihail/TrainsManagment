# -*- coding: utf-8 -*-
class ScheduleViewer:

    FOLDER = "../schedules/"
    time_point_coef = 5.33

    @staticmethod
    def generate_csv_schedule(scheme, name, start_time=None):
        from datetime import datetime, timedelta
        from collections import OrderedDict
        if start_time is None:
            start_time = datetime.now()
        table = OrderedDict()
        max_line = 0
        row = -1
        trains = [x for x in scheme.trains]
        trains.sort(key=lambda x: x.name)
        for train in trains:
            row += 1
            line = 0
            table[(line, row)] = ";%s" % (train.name)
            for position in train.schedule:
                if position.status == position.STATUS_MOVING and position.time_in_way == 0:
                    line += 1
                    if line > max_line:
                        max_line = line
                    time = (start_time + timedelta(minutes=ScheduleViewer.time_point_coef * position.time)).strftime("%H:%M %d.%m")
                    table[(line, row)] = ("%s;%s" % (position.dispatch().name, time))

        txt = ""
        train_num = 0
        for key, value in table.items():
            if train_num != key[1]:
                train_num = key[1]
                txt += "\n\n"
            txt += value + "\n"

        file = open(ScheduleViewer.FOLDER + name + ".csv", "w")
        file.write(txt)
        file.close()
