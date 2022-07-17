CREATE TABLE IF NOT EXISTS mlit_fudousantorihiki (
id                      serial,
trade_year_q            int,
shurui                  varchar(16),
chiiki                  varchar(16),
pref                    varchar(4),
city                    varchar(16),
town                    varchar(64),
station                 varchar(32),
from_station_min        int,
price                   bigint,
plan                    varchar(16),
floor_area_m2           int,
land_area_m2            int,
build_year              int,
structure               varchar(16),
new_usage               varchar(16),
youto_chiiki            varchar(32),
primary key(id) );
COMMENT ON TABLE mlit_fudousantorihiki IS
'https://www.land.mlit.go.jp/webland/download.html';
COMMENT ON COLUMN mlit_fudousantorihiki.trade_year_q
     IS '年度と四半期';
COMMENT ON COLUMN mlit_fudousantorihiki.shurui
     IS '宅地(土地と建物), 宅地(土地), 中古マンション等市町村code';
COMMENT ON COLUMN mlit_fudousantorihiki.chiiki IS '住宅地, 宅地見込地';

CREATE TABLE IF NOT EXISTS mlit_fudousantorihiki_by_city (
pref                    varchar(4),
city                    varchar(16),
summary                 varchar(20480),
primary key(pref,city) );

CREATE TABLE IF NOT EXISTS mlit_fudousantorihiki_by_town (
pref                    varchar(4),
city                    varchar(16),
town                    varchar(64),
summary                 varchar(20480),
primary key(pref,city,town) );


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

CREATE TABLE IF NOT EXISTS city_profile (
pref                    varchar(4),
city                    varchar(8),
summary                 varchar(4096),
build_year_summary      varchar(4096),
primary key(pref,city));

CREATE TABLE IF NOT EXISTS near_city (
pref            varchar(4),
city            varchar(8),
near_pref       varchar(4),
near_city       varchar(8),
primary key(pref,city,near_pref,near_city));

CREATE TABLE IF NOT EXISTS town_profile (
pref            varchar(4),
city            varchar(16),
town            varchar(64),
lng             double precision,
lat             double precision,
summary         varchar(4096),
primary key(pref,city,town) );

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
pref            varchar(4),
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
rent_80000_99999        bigint,
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

CREATE TABLE IF NOT EXISTS kokusei_population_b01 (
pref            varchar(4),
city            varchar(8),
pop             bigint,
pop_2015        bigint,
pop_density     int,
setai           int,
setai_2015      int,
primary key(pref,city) );

COMMENT ON TABLE kokusei_population_b01 IS
'https://www.e-stat.go.jp/stat-search/files
  ?layout=datalist&toukei=00200521&tstat=000001136464&cycle=0&tclass1=000001136466
総人口・総世帯数・男女・年齢・配偶関係 1-1
  男女別人口，世帯の種類別世帯数及び世帯人員並びに2015年（平成27年）の人口
  （組替），2015年（平成27年）の世帯数（組替），5年間の人口増減数，
  5年間の人口増減率，5年間の世帯増減数，5年間の世帯増減率，人口性比，
  面積（参考）及び人口密度－全国，都道府県，市区町村（2000年（平成12年）
   市区町村含む）';
COMMENT ON COLUMN kokusei_population_b01.pop_2015    IS '2015年の人口';
COMMENT ON COLUMN kokusei_population_b01.pop_density IS '人口密度. 人/km2';
COMMENT ON COLUMN kokusei_population_b01.setai_2015  IS '2015年の世帯数';

CREATE TABLE IF NOT EXISTS kokusei_population_b02 (
pref            varchar(4),
city            varchar(8),
pop_0_4         bigint,
pop_5_9         bigint,
pop_10_14       bigint,
pop_15_19       bigint,
pop_20_24       bigint,
pop_25_29       bigint,
pop_30_34       bigint,
pop_35_39       bigint,
pop_40_44       bigint,
pop_45_49       bigint,
pop_50_54       bigint,
pop_55_59       bigint,
pop_60_64       bigint,
pop_65_69       bigint,
pop_70_74       bigint,
pop_75_79       bigint,
pop_80_84       bigint,
pop_85_89       bigint,
pop_90_94       bigint,
pop_95_99       bigint,
pop_100         bigint,
primary key(pref,city) );

COMMENT ON TABLE kokusei_population_b02 IS
'https://www.e-stat.go.jp/stat-search/files
  ?layout=datalist&toukei=00200521&tstat=000001136464&cycle=0&tclass1=000001136466
総人口・総世帯数・男女・年齢・配偶関係 2-7
男女，年齢（5歳階級及び3区分），国籍総数か日本人別人口，平均年齢，
年齢中位数及び人口構成比［年齢別］－全国，都道府県，
市区町村（2000年（平成12年）市区町村含む）';


CREATE TABLE IF NOT EXISTS kokusei_population_b06 (
pref            varchar(4),
city            varchar(8),
setai_total     bigint,
setai_1         bigint,
setai_pop       real,
primary key(pref,city) );

COMMENT ON TABLE kokusei_population_b06 IS
'https://www.e-stat.go.jp/stat-search/files
  ?layout=datalist&toukei=00200521&tstat=000001136464&cycle=0&tclass1=000001136466
世帯の種類・世帯人員・世帯の家族類型 6-3
世帯人員の人数別一般世帯数，会社などの独身寮の単身者数，
間借り・下宿などの単身者数，一般世帯人員及び一般世帯の1世帯当たり人員－全国，
都道府県，市区町村';
COMMENT ON COLUMN kokusei_population_b06.setai_total IS '一般世帯数 総数';
COMMENT ON COLUMN kokusei_population_b06.setai_1     IS '一般世帯数 世帯人員が1人';
COMMENT ON COLUMN kokusei_population_b06.setai_pop   IS '1世帯当たり人員';


CREATE TABLE IF NOT EXISTS kokusei_population_b12 (
pref            varchar(4),
city            varchar(8),
owner_age       varchar(8),
total_setai     bigint,
family_setai    bigint,
other_setai     bigint,
single_setai    bigint,
unknown_setai   bigint,
primary key(pref,city,owner_age) );

COMMENT ON TABLE kokusei_population_b12 IS
'https://www.e-stat.go.jp/stat-search/files
  ?layout=datalist&toukei=00200521&tstat=000001136464&cycle=0&tclass1=000001136466
世帯の種類・世帯人員・世帯の家族類型 12-3
世帯主の男女，世帯主の年齢（5歳階級），世帯の家族類型別一般世帯数－全国，
都道府県，市区町村';

COMMENT ON COLUMN kokusei_population_b12.total_setai   IS '総数';
COMMENT ON COLUMN kokusei_population_b12.family_setai  IS '親族のみの世帯';
COMMENT ON COLUMN kokusei_population_b12.other_setai   IS '非親族を含む世帯';
COMMENT ON COLUMN kokusei_population_b12.single_setai  IS '単独世帯';
COMMENT ON COLUMN kokusei_population_b12.unknown_setai IS '世帯の家族類型 不詳';


CREATE TABLE IF NOT EXISTS kokusei_population_b18 (
pref            varchar(4),
city            varchar(8),
owned_house     bigint,
public_rented   bigint,
private_rented  bigint,
company_house   bigint,
primary key(pref,city) );

COMMENT ON TABLE kokusei_population_b18 IS
'https://www.e-stat.go.jp/stat-search/files
  ?layout=datalist&toukei=00200521&tstat=000001136464&cycle=0&tclass1=000001136466
住宅の所有関係・住宅の建て方 18-4
住宅の所有の関係別一般世帯数－全国，都道府県，
市区町村（2000年（平成12年）市区町村含む）';

COMMENT ON COLUMN kokusei_population_b18.owned_house    IS '持ち家';
COMMENT ON COLUMN kokusei_population_b18.public_rented
                                IS '公営・都市再生機構・公社の借家';
COMMENT ON COLUMN kokusei_population_b18.private_rented IS '民営の借家';
COMMENT ON COLUMN kokusei_population_b18.company_house  IS '給与住宅';


CREATE TABLE IF NOT EXISTS kokusei2015_population_003 (
pref            varchar(4),
city            varchar(8),
pop_0_4         bigint,
pop_5_9         bigint,
pop_10_14       bigint,
pop_15_19       bigint,
pop_20_24       bigint,
pop_25_29       bigint,
pop_30_34       bigint,
pop_35_39       bigint,
pop_40_44       bigint,
pop_45_49       bigint,
pop_50_54       bigint,
pop_55_59       bigint,
pop_60_64       bigint,
pop_65_69       bigint,
pop_70_74       bigint,
pop_75_79       bigint,
pop_80_84       bigint,
pop_85_89       bigint,
pop_90_94       bigint,
pop_95_99       bigint,
pop_100         bigint,
primary key(pref,city) );

COMMENT ON TABLE kokusei2015_population_003 IS
'https://www.e-stat.go.jp/stat-search/files?toukei=00200521&tstat=000001080615
 男女・年齢・配偶関係 3-2
 年齢(各歳)，男女別人口，年齢別割合，平均年齢及び年齢中位数(総数及び日本人)
 － 都道府県※，都道府県市部・郡部，市区町村※，平成12年市町村';

CREATE TABLE IF NOT EXISTS kokusei2015_population_007 (
pref            varchar(4),
city            varchar(8),
setai_total     bigint,
setai_1         bigint,
setai_pop       real,
primary key(pref,city) );

COMMENT ON TABLE kokusei2015_population_007 IS
'https://www.e-stat.go.jp/stat-search/files?toukei=00200521&tstat=000001080615
 世帯数・世帯人員 7
 世帯の種類(2区分)，施設等の世帯の種類(6区分)，世帯人員(10区分/4区分)別世帯数，
 世帯人員及び1世帯当たり人員(間借り・下宿などの単身者及び会社などの独身寮の単身者
 －特掲) － 都道府県※，都道府県市部・郡部，市区町村※，平成12年市町村';
COMMENT ON COLUMN kokusei2015_population_007.setai_total IS '一般世帯数 総数';
COMMENT ON COLUMN kokusei2015_population_007.setai_1
                                                IS '一般世帯数 世帯人員が1人';
COMMENT ON COLUMN kokusei2015_population_007.setai_pop   IS '1世帯当たり人員';


CREATE TABLE IF NOT EXISTS kokusei2015_population_013 (
pref            varchar(4),
city            varchar(8),
owner_age       varchar(8),
total_setai     bigint,
family_setai    bigint,
other_setai     bigint,
single_setai    bigint,
unknown_setai   bigint,
primary key(pref,city,owner_age) );

COMMENT ON TABLE kokusei2015_population_013 IS
'https://www.e-stat.go.jp/stat-search/files?toukei=00200521&tstat=000001080615
世帯の家族類型・世帯主との続き柄 13-2
世帯の家族類型(16区分)，世帯主の年齢(5歳階級)，世帯主の男女別一般世帯数及び
一般世帯人員(3世代世帯，間借り・下宿などの単身者及び会社などの独身寮の単身者
－特掲) － 都道府県※，都道府県市部・郡部，市区町村※';

COMMENT ON COLUMN kokusei2015_population_013.total_setai   IS '総数';
COMMENT ON COLUMN kokusei2015_population_013.family_setai  IS '親族のみの世帯';
COMMENT ON COLUMN kokusei2015_population_013.other_setai   IS '非親族を含む世帯';
COMMENT ON COLUMN kokusei2015_population_013.single_setai  IS '単独世帯';
COMMENT ON COLUMN kokusei2015_population_013.unknown_setai
                                                        IS '世帯の家族類型 不詳';

CREATE TABLE IF NOT EXISTS kokusei2015_population_018 (
pref            varchar(4),
city            varchar(8),
owned_house     bigint,
public_rented   bigint,
private_rented  bigint,
company_house   bigint,
primary key(pref,city) );

COMMENT ON TABLE kokusei2015_population_018 IS
'https://www.e-stat.go.jp/stat-search/files?toukei=00200521&tstat=000001080615
住居の状態 18-2
住居の種類・住宅の所有の関係(6区分)別一般世帯数，一般世帯人員及び1世帯当たり人員
－ 都道府県※，都道府県市部・郡部，市区町村※，平成12年市町村';

COMMENT ON COLUMN kokusei2015_population_018.owned_house    IS '持ち家';
COMMENT ON COLUMN kokusei2015_population_018.public_rented
                                IS '公営・都市再生機構・公社の借家';
COMMENT ON COLUMN kokusei2015_population_018.private_rented IS '民営の借家';
COMMENT ON COLUMN kokusei2015_population_018.company_house  IS '給与住宅';


CREATE TABLE IF NOT EXISTS suumo_search_result_url (
build_type      varchar(32),
url             varchar(256),
primary key(url) );


CREATE TABLE IF NOT EXISTS suumo_bukken (
url             varchar(128),
build_type      varchar(32),
bukken_name     varchar(64),
price           bigint,
price_org       varchar(64),
pref            varchar(4),
city            varchar(8),
address         varchar(128),
plan            varchar(64),
build_area_m2   int,
build_area_org  varchar(64),
land_area_m2    int,
land_area_org   varchar(64),
build_year      int,
shop_org        varchar(64),
shop            varchar(64),
total_house     int,
house_for_sale  int,
found_date      date,
show_date       date,
check_date      date,
update_time     timestamp,
primary key ( url )
);


-- CREATE TABLE IF NOT EXISTS lifell_bukken (
-- build_type      varchar(32)  NOT NULL DEFAULT '',
-- bukken_name     varchar(64)  NOT NULL DEFAULT '',
-- price           bigint,
-- price_org       varchar(64),
-- pref            varchar(4)   NOT NULL DEFAULT '',
-- city            varchar(8)   NOT NULL DEFAULT '',
-- address         varchar(128) NOT NULL DEFAULT '',
-- plan            varchar(64)  NOT NULL DEFAULT '',
-- build_area_m2   int,
-- build_area_org  varchar(64)  NOT NULL DEFAULT '',
-- land_area_m2    int,
-- land_area_org   varchar(64)  NOT NULL DEFAULT '',
-- build_year      int          NOT NULL DEFAULT 0,
-- found_date      date,
-- check_date      date,
-- primary key ( build_type,bukken_name,pref,city,address,plan,
--               build_area_org,land_area_org,build_year)
-- );


CREATE TABLE IF NOT EXISTS mlit_seisanryokuchi (
pref            varchar(4),
city            varchar(8),
area_ha         int,
area_count      int,
primary key(pref,city) );


CREATE TABLE IF NOT EXISTS site_access (
site            varchar(64),
client_ip       varchar(16),
lng             double precision,
lat             double precision,
pref            varchar(4),
city            varchar(16),
address_other   varchar(64),
primary key(site,client_ip) );


CREATE TABLE IF NOT EXISTS client_ip_pos (
client_ip       varchar(16),
ip_type         varchar(8),
lng             double precision,
lat             double precision,
pref            varchar(4),
city            varchar(16),
address_other   varchar(64),
primary key(client_ip) );


CREATE TABLE IF NOT EXISTS soumu_zeisei_j51_20_b (
pref                    varchar(4),
city                    varchar(8),
pop                     bigint,
salary                  bigint,
separate_long_capital   bigint,
separate_short_capital  bigint,
general_stock_capital   bigint,
listed_stock_capital    bigint,
listed_stock_dividend   bigint,
future_trading_income   bigint,
taxable_income          bigint,
primary key(pref,city) );

COMMENT ON TABLE soumu_zeisei_j51_20_b IS
'https://www.soumu.go.jp/main_sosiki/jichi_zeisei/czaisei/czaisei_seido/xls/J51-20-b.xlsx
市町村別内訳
第11表　課税標準額段階別令和２年度分所得割額等に関する調（合計）
（所得割納税義務者数・課税対象所得・課税標準額・所得割額）';

COMMENT ON COLUMN soumu_zeisei_j51_20_b.pop
     IS '所得割の納税義務者数';
COMMENT ON COLUMN soumu_zeisei_j51_20_b.salary
     IS '総所得金額等';
COMMENT ON COLUMN soumu_zeisei_j51_20_b.separate_long_capital
     IS '分離長期譲渡所得金額に係る所得金額';
COMMENT ON COLUMN soumu_zeisei_j51_20_b.separate_short_capital
     IS '分離短期譲渡所得金額に係る所得金額';
COMMENT ON COLUMN soumu_zeisei_j51_20_b.general_stock_capital
     IS '一般株式等に係る譲渡所得金額';
COMMENT ON COLUMN soumu_zeisei_j51_20_b.listed_stock_capital
     IS '上場株式等に係る譲渡所得金額';
COMMENT ON COLUMN soumu_zeisei_j51_20_b.listed_stock_dividend
     IS '上場株式等に係る配当所得金額';
COMMENT ON COLUMN soumu_zeisei_j51_20_b.future_trading_income
     IS '先物取引に係る雑所得金額';
COMMENT ON COLUMN soumu_zeisei_j51_20_b.taxable_income
     IS '課税対象所得';


ALTER TABLE gis_chika_koji ADD COLUMN pref varchar(4);
ALTER TABLE gis_chika_koji ADD COLUMN city varchar(8);
ALTER TABLE gis_chika      ADD COLUMN pref varchar(4);
ALTER TABLE gis_chika      ADD COLUMN city varchar(8);

CREATE INDEX gis_jinko_suikei_500m_lng_lat ON gis_jinko_suikei_500m (lng,lat);
CREATE INDEX gis_chika_koji_lng_lat        ON gis_chika_koji        (lng,lat);
CREATE INDEX gis_chika_lng_lat             ON gis_chika_koji        (lng,lat);


CREATE TABLE IF NOT EXISTS real_estate_shop (
government              varchar(16),
licence                 varchar(16),
shop                    varchar(64),
primary key(government,licence)
);

CREATE TABLE IF NOT EXISTS newbuild_sales_count_by_shop (
pref                    varchar(4),
shop                    varchar(64),
calc_date               date,
onsale_count            int,
onsale_price            bigint,
onsale_days             int,
discuss_count           int,
discuss_price           bigint,
discuss_days            int,
primary key(pref,shop,calc_date) );

CREATE TABLE IF NOT EXISTS newbuild_sales_count_by_shop_city (
pref                    varchar(4),
city                    varchar(16),
shop                    varchar(64),
calc_date               date,
onsale_count            int,
onsale_price            bigint,
onsale_days             int,
discuss_count           int,
discuss_price           bigint,
discuss_days            int,
primary key(pref,city,shop,calc_date) );

CREATE TABLE IF NOT EXISTS newbuild_sales_count_by_city (
pref                    varchar(4),
city                    varchar(16),
calc_date               date,
onsale_count            int,
onsale_price            bigint,
onsale_days             int,
discuss_count           int,
discuss_price           bigint,
discuss_days            int,
sold_count              numeric,
sold_price              bigint,
primary key(pref,city,calc_date) );

CREATE TABLE IF NOT EXISTS newbuild_sales_count_by_town (
pref                    varchar(4),
city                    varchar(16),
town                    varchar(64),
calc_date               date,
onsale_count            int,
onsale_price            bigint,
onsale_days             int,
discuss_count           int,
discuss_price           bigint,
discuss_days            int,
sold_count              numeric,
sold_price              bigint,
primary key(pref,city,town,calc_date) );

CREATE TABLE IF NOT EXISTS newbuild_sales_count_by_city_price (
pref                    varchar(4),
city                    varchar(16),
price                   int,
calc_date               date,
onsale_count            int,
onsale_days             int,
discuss_count           int,
discuss_days            int,
sold_count              numeric,
primary key(pref,city,price,calc_date) );

CREATE TABLE IF NOT EXISTS newbuild_sales_count_by_shop_scale (
pref                    varchar(4),
shop                    varchar(64),
calc_date               date,
scale_sales             varchar(4096),
primary key(pref,shop,calc_date) );

CREATE TABLE IF NOT EXISTS newbuild_sales_count_by_shop_city_scale (
pref                    varchar(4),
city                    varchar(16),
shop                    varchar(64),
calc_date               date,
scale_sales             varchar(4096),
primary key(pref,city,shop,calc_date) );

CREATE TABLE IF NOT EXISTS newbuild_sales_count_by_city_scale (
pref                    varchar(4),
city                    varchar(16),
calc_date               date,
scale_sales             varchar(4096),
primary key(pref,city,calc_date) );

CREATE TABLE IF NOT EXISTS newbuild_sales_count_by_town_scale (
pref                    varchar(4),
city                    varchar(16),
town                    varchar(64),
calc_date               date,
scale_sales             varchar(4096),
primary key(pref,city,town,calc_date) );

CREATE TABLE IF NOT EXISTS sumstock_sales_count_by_shop (
pref                    varchar(4),
shop                    varchar(64),
calc_date               date,
onsale_count            int,
onsale_price            bigint,
onsale_days             int,
discuss_count           int,
discuss_price           bigint,
discuss_days            int,
primary key(pref,shop,calc_date) );

CREATE TABLE IF NOT EXISTS sumstock_sales_count_by_shop_city (
pref                    varchar(4),
city                    varchar(16),
shop                    varchar(64),
calc_date               date,
onsale_count            int,
onsale_price            bigint,
onsale_days             int,
discuss_count           int,
discuss_price           bigint,
discuss_days            int,
primary key(pref,city,shop,calc_date) );

CREATE TABLE IF NOT EXISTS sumstock_sales_count_by_city (
pref                    varchar(4),
city                    varchar(16),
calc_date               date,
onsale_count            int,
onsale_price            bigint,
onsale_days             int,
discuss_count           int,
discuss_price           bigint,
discuss_days            int,
sold_count              numeric,
sold_price              bigint,
primary key(pref,city,calc_date) );

CREATE TABLE IF NOT EXISTS sumstock_sales_count_by_town (
pref                    varchar(4),
city                    varchar(16),
town                    varchar(64),
calc_date               date,
onsale_count            int,
onsale_price            bigint,
onsale_days             int,
discuss_count           int,
discuss_price           bigint,
discuss_days            int,
sold_count              numeric,
sold_price              bigint,
primary key(pref,city,town,calc_date) );

CREATE TABLE IF NOT EXISTS sumstock_sales_count_by_city_price (
pref                    varchar(4),
city                    varchar(16),
price                   int,
calc_date               date,
onsale_count            int,
onsale_days             int,
discuss_count           int,
discuss_days            int,
sold_count              numeric,
primary key(pref,city,price,calc_date) );


