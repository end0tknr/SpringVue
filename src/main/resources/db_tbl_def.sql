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
COMMENT ON COLUMN city.code IS '市町村code';

-- 2015年の古いデータの為、対象外
-- CREATE TABLE IF NOT EXISTS estat_jutakutochi (
-- city              varchar(8),
-- setai             int,
-- setai_nushi_age   varchar(1024),
-- setai_year_income varchar(1024),
-- primary key(city) );

CREATE TABLE IF NOT EXISTS estat_jutakutochi_d001 (
pref            varchar(4),
city            varchar(8),
house             bigint,
lived_house       bigint,
nolived_house     bigint,
primary key(pref,city) );

COMMENT ON TABLE estat_jutakutochi_d001 IS
'https://www.e-stat.go.jp/stat-search/files
  ?layout=datalist&toukei=00200522&tstat=000001127155&tclass1=000001133386
市区町村-1
  居住世帯の有無(8区分)別住宅数及び住宅以外で人が
  居住する建物数―全国，都道府県，市区町村';

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
COMMENT ON TABLE estat_jutakutochi_d002 IS
'https://www.e-stat.go.jp/stat-search/files
 ?layout=datalist&toukei=00200522&tstat=000001127155&tclass1=000001133386
市区町村-2
 住宅の建て方(3区分)，階数(4区分)・構造(2区分)・所有の関係(2区分)・
 建築の時期(2区分)別住宅数及び世帯の種類(2区分)別世帯数―全国，都道府県，市区町村';
COMMENT ON COLUMN estat_jutakutochi_d002.detached_house  IS '一戸建';
COMMENT ON COLUMN estat_jutakutochi_d002.tenement_houses IS '長屋建';
COMMENT ON COLUMN estat_jutakutochi_d002.apartment       IS '共同住宅';
COMMENT ON COLUMN estat_jutakutochi_d002.owned_house     IS '持ち家';
COMMENT ON COLUMN estat_jutakutochi_d002.rented_house    IS '借家';

CREATE TABLE IF NOT EXISTS estat_jutakutochi_e006 (
pref            varchar(4),
city            varchar(8),
build_year      varchar(16),
total           bigint,
owned_house     bigint,
rented_house    bigint,
primary key(pref,city,build_year) );
COMMENT ON TABLE estat_jutakutochi_e006 IS
'https://www.e-stat.go.jp/stat-search/files
  ?layout=datalist&toukei=00200522&tstat=000001127155&cycle=0
   &tclass1=000001129435&tclass2=000001129436
住宅の種類，建て方，建築の時期，建物の構造，階数 6-3
  住宅の所有の関係(5区分)，建築の時期(7区分)別住宅数－全国，都道府県，市区町村';
COMMENT ON COLUMN estat_jutakutochi_e006.owned_house     IS '持ち家';
COMMENT ON COLUMN estat_jutakutochi_e006.rented_house    IS '借家';

CREATE TABLE IF NOT EXISTS estat_jutakutochi_e030 (
pref            varchar(4),
city            varchar(8),
own_type        varchar(4),
total           bigint,
solar_water_heater      bigint,
pv                      bigint,
double_sash             bigint,
primary key(pref,city,own_type) );
COMMENT ON TABLE estat_jutakutochi_e030 IS
'https://www.e-stat.go.jp/stat-search/files
  ?layout=datalist&toukei=00200522&tstat=000001127155&cycle=0
  &tclass1=000001129435&tclass2=000001129436
住宅の設備 30-2
  住宅の種類(2区分)，住宅の所有の関係(2区分)，建て方(4区分)，構造(2区分)，
  省エネルギー設備等(7区分)別住宅数－全国，都道府県，市区町村';
COMMENT ON COLUMN estat_jutakutochi_e030.solar_water_heater IS '太陽熱温水';
COMMENT ON COLUMN estat_jutakutochi_e030.pv                 IS '太陽光発電';
COMMENT ON COLUMN estat_jutakutochi_e030.double_sash        IS '二重以上のサッシ';

CREATE TABLE IF NOT EXISTS estat_jutakutochi_e033 (
pref            varchar(4),
city            varchar(8),
damage          varchar(8),
build_year      varchar(16),
owned_house     bigint,
rented_house    bigint,
primary key(pref,city,damage,build_year) );
COMMENT ON TABLE estat_jutakutochi_e033 IS
'https://www.e-stat.go.jp/stat-search/files
 ?layout=datalist&toukei=00200522&tstat=000001127155&cycle=0
 &tclass1=000001129435&tclass2=000001129436
住宅の設備 33-2
 住宅の所有の関係(6区分)，腐朽・破損の有無(2区分)，建築の時期(9区分)別住宅数
 －全国，都道府県，市区町村';
COMMENT ON COLUMN estat_jutakutochi_e033.owned_house     IS '持ち家';
COMMENT ON COLUMN estat_jutakutochi_e033.rented_house    IS '借家';

CREATE TABLE IF NOT EXISTS estat_jutakutochi_e044 (
pref              varchar(4),
city              varchar(8),
own_type          varchar(4),
year_income       varchar(32),
setai             bigint,
primary key(pref,city,own_type,year_income) );
COMMENT ON TABLE estat_jutakutochi_e044 IS
'https://www.e-stat.go.jp/stat-search/files
 ?layout=datalist&toukei=00200522&tstat=000001127155&cycle=0
 &tclass1=000001129435&tclass2=000001129436
住宅の設備 44-4
  世帯の年間収入階級(9区分)，世帯の種類(2区分)，
  住宅の所有の関係(5区分)別普通世帯数，１世帯当たり人員，
  １世帯当たり居住室数及び１世帯当たり居住室の畳数－全国，都道府県，市区町村';
COMMENT ON COLUMN estat_jutakutochi_e044.year_income IS '年収';

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
COMMENT ON TABLE estat_jutakutochi_e048 IS
'https://www.e-stat.go.jp/stat-search/files
 ?layout=datalist&toukei=00200522&tstat=000001127155&cycle=0
 &tclass1=000001129435&tclass2=000001129436
家計を主に支える者と住居 48-2
 住宅の建築の時期(7区分)，建て方(2区分)，構造(2区分)別家計を主に
 支える者の年齢(6区分)別主世帯数及び平均年齢－全国，都道府県，市区町村';

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
COMMENT ON TABLE estat_jutakutochi_e049 IS
'https://www.e-stat.go.jp/stat-search/files
 ?layout=datalist&toukei=00200522&tstat=000001127155&cycle=0
 &tclass1=000001129435&tclass2=000001129436
家計を主に支える者と住居 49-2
  家計を主に支える者の年齢(6区分)別世帯の１か月当たり家賃(10区分)
  別借家に居住する主世帯数及び１か月当たり家賃－全国，都道府県，市区町村';
COMMENT ON COLUMN estat_jutakutochi_e049.rent_0 IS '家賃';

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
COMMENT ON TABLE estat_jutakutochi_e101 IS
'https://www.e-stat.go.jp/stat-search/files
 ?layout=datalist&toukei=00200522&tstat=000001127155&cycle=0
 &tclass1=000001129435&tclass2=000001129436
持ち家の購入･新築･建て替え等の状況 101-3
  住宅の建築の時期(7区分)，住宅の購入・新築・建て替え等(8区分)別持ち家数
  －全国，都道府県，市区町村';
COMMENT ON COLUMN estat_jutakutochi_e101.buy_new     IS '新築の住宅を購入';
COMMENT ON COLUMN estat_jutakutochi_e101.buy_used    IS '中古住宅を購入';
COMMENT ON COLUMN estat_jutakutochi_e101.build_new   IS '新築';
COMMENT ON COLUMN estat_jutakutochi_e101.rebuild     IS '建て替え';
COMMENT ON COLUMN estat_jutakutochi_e101.inheritance IS '相続・贈与';

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
COMMENT ON TABLE estat_jutakutochi_g157 IS
'https://www.e-stat.go.jp/stat-search/files
 ?layout=datalist&toukei=00200522&tstat=000001127155&cycle=0
 &tclass1=000001129435&tclass2=000001129436
持ち家の増改築・改修工事,高齢者等のための設備工事,
耐震改修工事,耐震診断の有無,リフォーム工事の状況 157-3
  住宅の建築の時期(7区分)，2014年以降の住宅の増改築
  ・改修工事等(8区分)別持ち家数－全国，都道府県，市区町村';
COMMENT ON COLUMN estat_jutakutochi_g157.reform_plan  IS '増築・間取りの変更';
COMMENT ON COLUMN estat_jutakutochi_g157.reform_kitchen_bath
                                     IS '台所・トイレ・浴室・洗面所の改修工事';
COMMENT ON COLUMN estat_jutakutochi_g157.reform_floor_inner_wall
                                     IS '天井・壁・床等の内装の改修工事';
COMMENT ON COLUMN estat_jutakutochi_g157.reform_roof_outer_wall
                                     IS '屋根・外壁等の改修工事';
COMMENT ON COLUMN estat_jutakutochi_g157.reform_pillar_basic
                                     IS '壁・柱・基礎等の補強工事';
COMMENT ON COLUMN estat_jutakutochi_g157.reform_insulation
                                     IS '窓・壁等の断熱・結露防止工事';

CREATE TABLE IF NOT EXISTS estat_jutakutochi_g158 (
pref            varchar(4),
city            varchar(8),
year_income     varchar(32),
reform_plan             bigint,
reform_kitchen_bath     bigint,
reform_floor_inner_wall bigint,
reform_roof_outer_wall  bigint,
reform_pillar_basic     bigint,
reform_insulation       bigint,
reform_other            bigint,
primary key(pref,city,year_income) );
COMMENT ON TABLE estat_jutakutochi_g158 IS
'https://www.e-stat.go.jp/stat-search/files
 ?layout=datalist&toukei=00200522&tstat=000001127155&cycle=0
 &tclass1=000001129435&tclass2=000001129436
持ち家の増改築・改修工事,高齢者等のための設備工事,
耐震改修工事,耐震診断の有無,リフォーム工事の状況 158-4
世帯の年間収入階級(5区分)，2014年以降の住宅の増改築・改修工事等(8区分)
 別持ち家数－全国，都道府県，市区町村';
COMMENT ON COLUMN estat_jutakutochi_g158.reform_plan  IS '増築・間取りの変更';
COMMENT ON COLUMN estat_jutakutochi_g158.reform_kitchen_bath
                                     IS '台所・トイレ・浴室・洗面所の改修工事';
COMMENT ON COLUMN estat_jutakutochi_g158.reform_floor_inner_wall
                                     IS '天井・壁・床等の内装の改修工事';
COMMENT ON COLUMN estat_jutakutochi_g158.reform_roof_outer_wall
                                     IS '屋根・外壁等の改修工事';
COMMENT ON COLUMN estat_jutakutochi_g158.reform_pillar_basic
                                     IS '壁・柱・基礎等の補強工事';
COMMENT ON COLUMN estat_jutakutochi_g158.reform_insulation
                                     IS '窓・壁等の断熱・結露防止工事';

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
