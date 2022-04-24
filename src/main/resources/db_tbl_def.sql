CREATE TABLE IF NOT EXISTS gmap_latlng_addr (
lng             double precision,
lat             double precision,
zip_code        varchar(8),
address         varchar(50),
primary key(lat,lng));

CREATE TABLE IF NOT EXISTS city (
code            varchar(6),
pref            varchar(4),
city            varchar(8),
lng             double precision,
lat             double precision,
primary key(code));

CREATE TABLE IF NOT EXISTS estat_jutakutochi (
city              varchar(8),
setai             int,
setai_nushi_age   varchar(1024),
setai_year_income varchar(1024),
primary key(city) );

