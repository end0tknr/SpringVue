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

CREATE TABLE IF NOT EXISTS estat_jutakutochi_d001 (
pref            varchar(4),
city            varchar(8),
house             bigint,
lived_house       bigint,
nolived_house     bigint,
primary key(pref,city) );

CREATE TABLE IF NOT EXISTS estat_jutakutochi_d002 (
pref            varchar(4),
city            varchar(8),
total           bigint,
detached_house  bigint,
tenement_houses bigint,
apartment       bigint,
owned_house     bigint,
rented_house    bigint,
primary key(pref,city) );

CREATE TABLE IF NOT EXISTS estat_jutakutochi_e006 (
pref            varchar(4),
city            varchar(8),
build_year      varchar(16),
total           bigint,
owned_house     bigint,
rented_house    bigint,
primary key(pref,city,build_year) );

CREATE TABLE IF NOT EXISTS estat_jutakutochi_e030 (
pref            varchar(4),
city            varchar(8),
own_type        varchar(4),
total           bigint,
solar_water_heater      bigint,
pv                      bigint,
double_sash             bigint,
primary key(pref,city,own_type) );

CREATE TABLE IF NOT EXISTS estat_jutakutochi_e033 (
pref            varchar(4),
city            varchar(8),
damage          varchar(8),
build_year      varchar(16),
owned_house     bigint,
rented_house    bigint,
primary key(pref,city,damage,build_year) );

CREATE TABLE IF NOT EXISTS estat_jutakutochi_e044 (
pref              varchar(4),
city              varchar(8),
own_type          varchar(4),
year_income       varchar(32),
setai             bigint,
primary key(pref,city,own_type,year_income) );

CREATE TABLE IF NOT EXISTS estat_jutakutochi_e048 (
pref              varchar(4),
city            varchar(8),
build_year      varchar(16),
owner_age_24    bigint,
owner_age_25_34 bigint,
owner_age_35_44 bigint,
owner_age_45_54 bigint,
owner_age_55_64 bigint,
owner_age_65    bigint,
owner_age_unknown bigint,
primary key(pref,city,build_year) );

CREATE TABLE IF NOT EXISTS estat_jutakutochi_e049 (
pref            varchar(4),
city            varchar(8),
owner_age       varchar(8),
rent_0                  bigint,
rent_1_9999             bigint,
rent_10000_19999        bigint,
rent_20000_39999        bigint,
rent_40000_59999        bigint,
rent_60000_79999        bigint,
rent_90000_99999        bigint,
rent_100000_149999      bigint,
rent_150000_199999      bigint,
rent_200000             bigint,
rent_unknown            bigint,
primary key(pref,city,owner_age) );

CREATE TABLE IF NOT EXISTS estat_jutakutochi_e101 (
pref            varchar(4),
city            varchar(8),
build_year      varchar(16),
buy_new         bigint,
buy_used        bigint,
build_new       bigint,
rebuild         bigint,
inheritance     bigint,
other           bigint,
primary key(pref,city,build_year) );

CREATE TABLE IF NOT EXISTS estat_jutakutochi_g157 (
pref            varchar(4),
city            varchar(8),
build_year      varchar(16),
reform_plan             bigint,
reform_kitchen_bath     bigint,
reform_floor_inner_wall bigint,
reform_roof_outer_wall  bigint,
reform_pillar_basic     bigint,
reform_insulation       bigint,
reform_other            bigint,
primary key(pref,city,build_year) );

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


CREATE TABLE IF NOT EXISTS suumo_search_result_url (
build_type      varchar(32),
url             varchar(256),
primary key(url) );

CREATE TABLE IF NOT EXISTS suumo_bukken (
id              serial,
build_type      varchar(32),
bukken_name     varchar(64),
price           bigint,
price_org       varchar(64),
address         varchar(128),
plan            varchar(32),
build_area_m2   int,
build_area_org  varchar(64),
land_area_m2    int,
land_area_org   varchar(64),
build_year      int,
primary key(id) );

CREATE TABLE IF NOT EXISTS mlit_seisanryokuchi (
city            varchar(8),
area_ha         int,
area_count      int,
primary key(city) );
