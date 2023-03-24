
INSERT INTO OPERATOR (OperatorID, Name)
VALUES (1,'SJ');


INSERT INTO ROUTE (RouteID, Name, OperatorID, StartStationName, EndStationName)
VALUES
    (1,'Day',1,'Trondheim','Bodo'),
    (2,'Night',1,'Trondheim','Bodo'),
    (3,'Morning',1,'Moirana','Trondheim');

  
INSERT INTO ROUTE_TRACK_TRAVERSAL (RouteID, TrackSectionName, Direction)
VALUES
    --Day route traversal
    (1,'TrondheimSteinkjer', 'Main'),
    (1,'SteinkjerMosjoen','Main'),
    (1,'MosjoenMoirana','Main'),
    (1,'MoiranaFauske','Main'),
    (1,'FauskeBodo','Main'),

    --Night route traversal
    (2,'TrondheimSteinkjer', 'Main'),
    (2,'SteinkjerMosjoen','Main'),
    (2,'MosjoenMoirana','Main'),
    (2,'MoiranaFauske','Main'),
    (2,'FauskeBodo','Main'),

    --Morning route traversal
    (3,'TrondheimSteinkjer', 'Opposite'),
    (3,'SteinkjerMosjoen','Opposite'),
    (3,'MosjoenMoirana','Opposite'),
    (3,'MoiranaFauske','Opposite'),
    (3,'FauskeBodo','Opposite');


INSERT INTO ROUTE_WEEKDAY (RouteID, Weekday)
VALUES
    --Day route days
    (1,'Monday'),
    (1,'Tuesday'),
    (1,'Wednesday'),
    (1,'Thursday'),
    (1,'Friday'),

    --Night route days
    (2,'Monday'),
    (2,'Tuesday'),
    (2,'Wednesday'),
    (2,'Thursday'),
    (2,'Friday'),
    (2,'Saturday'),
    (2,'Sunday'),

    --Morning route days
    (3,'Monday'),
    (3,'Tuesday'),
    (3,'Wednesday'),
    (3,'Thursday'),
    (3,'Friday');

INSERT INTO CAR_TYPE(Name, Type, NoRows, NoSeatsInRow, NoCompartments)
VALUES
    --Day route arrangement
    ('SJ-chair car-1', 'Seating', 3, 4, NULL),
    ('SJ-chair car-2', 'Seating', 3, 4, NULL),

    --Night route arrangement
    ('SJ-chair car-3', 'Seating', 3, 4, NULL),
    ('SJ-sleeping car-1', 'Sleeping', NULL, NULL, 4),

    --Morning route arrangement
    ('SJ-chair car-4', 'Seating', 3, 4, NULL);


INSERT INTO ROUTE_STATION_TIME(RouteID, StationName, TimeOfArrival, TimeOfDeparture)
VALUES
    (1, 'Trondheim', NULL, '07:49:00'),
    (1, 'Steinkjer', '09:49:00', '09:51:00'),
    (1, 'Mosjoen2', '13:18:00', '13:20:00'),
    (1, 'Moirana', '14:29:00', '14:31:00'),
    (1, 'Fauske', '16:47:00', '16:49:00'),
    (1, 'Bodo', '17:32:00', NULL),

    (2, 'Trondheim', NULL, '23:05:00'),
    (2, 'Steinkjer', '00:55:00', '00:57:00'),
    (2, 'Mosjoen', '04:39:00', '04:41:00'),
    (2, 'Moirana', '05:53:00', '05:55:00'),
    (2, 'Fauske', '08:17:00', '08:19:00'),
    (2, 'Bodo', '09:03:00', NULL),

    (3, 'Moirana', NULL, '08:11:00'),
    (3, 'Mosjoen', '19:12:00', '09:14:00'),
    (3, 'Steinkjer', '12:29:00', '12:31:00'),
    (3, 'Trondheim', '14:11:00', NULL);


INSERT INTO ARRANGED_CAR(RouteID, Number, CarTypeName)
VALUES
    (1, 1, 'SJ-chair car-1'),
    (1, 2, 'SJ-chair car-2'),

    (2, 1, 'SJ-chair car-3'),
    (2, 2, 'SJ-sleeping car-1'),

    (3, 1, 'SJ-chair car-4');

