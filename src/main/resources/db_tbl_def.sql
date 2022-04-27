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


CREATE TABLE IF NOT EXISTS mlit_fudousantorihiki (
id              serial,
shurui          varchar(16),
chiiki          varchar(16),
pref            varchar(4),
city            varchar(16),
street          varchar(16),
price           bigint,
area_m2         int,
build_year      int,
trade_year      int,
primary key(id) );

CREATE TABLE IF NOT EXISTS population_city (
pref            varchar(4),
city            varchar(8),
pop             bigint,
pop_2015        bigint,
pop_density     int,
avg_age         int,
aget_14         int,
aget_15_64      int,
aget_65         int,
setai           int,
setai_2015      int,
primary key(pref,city) );
COMMENT ON TABLE population_city IS
'国勢調査 人口 https://www.e-stat.go.jp/stat-search/files?toukei=00200521&tstat=000001049104';
COMMENT ON COLUMN population_city.pop_2015    IS '2015年の人口';
COMMENT ON COLUMN population_city.pop_density IS '人口密度. 人/km2';
COMMENT ON COLUMN population_city.aget_14     IS '年齢別人口. ～14歳';
COMMENT ON COLUMN population_city.aget_15_64  IS '年齢別人口. 15～64歳';
COMMENT ON COLUMN population_city.aget_65     IS '年齢別人口. 65歳～';
COMMENT ON COLUMN population_city.pop_density IS '人口密度. 人/km2';
COMMENT ON COLUMN population_city.setai_2015  IS '2015年の世帯数';

