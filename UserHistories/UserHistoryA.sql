INSERT INTO TRACK_SECTION(Name, DrivingEnergy)
VALUES('Nordlandsbanen', 'Diesel');


INSERT INTO STATION (Name, Altitude)
VALUES
    (
      'Trondheim',
      51
    ),
    (
      'Steinkjer',
      36
    ),
    (
      'Mosjoen',
      68
    ),
    (
      'Moirana',
      35
    ),
    (
      'Fauske',
      340
    ),
    (
      'Bodo',
      41
    );


INSERT INTO SUB_SECTION (
  Station1Name, 
  Station2Name,
  SectionName,
  Length,
  TrackType
)
VALUES
    (
      'Trondheim',
      'Steinkjer',
      'Nordlandsbanen',
      120,
      'Double'
    ),
    (
      'Steinkjer',
      'Mosjoen',
      'Nordlandsbanen',
      280,
      'Single'
    ),
    (
      'Mosjoen',
      'Moirana',
      'Nordlandsbanen',
      90,
      'Single'
    ),
    (
      'Moirana',
      'Fauske',
      'Nordlandsbanen',
      170,
      'Single'
    ),
    (
      'Fauske',
      'Bodo',
      'Nordlandsbanen',
      60,
      'Single'
    );
