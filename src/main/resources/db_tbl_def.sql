CREATE TABLE IF NOT EXISTS gis_latlng_addr (
lat             double precision,
lng             double precision,
mesh_code       varchar(8),
zip_code        varchar(8),
address         varchar(50),
primary key(lat,lng));
