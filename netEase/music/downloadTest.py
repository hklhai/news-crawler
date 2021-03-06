# -*- coding: utf-8 -*-
import re
import time

import requests

from netEase.music.common import get_user_agent

url = "http://music.163.com/song/media/outer/url?id=1397674264.mp3"

url_list = ['http://music.163.com/song/media/outer/url?id=1481164987.mp3',
            'http://music.163.com/song/media/outer/url?id=1487528112.mp3',
            'http://music.163.com/song/media/outer/url?id=1443838552.mp3',
            'http://music.163.com/song/media/outer/url?id=1397674264.mp3',
            'http://music.163.com/song/media/outer/url?id=1426649237.mp3',
            'http://music.163.com/song/media/outer/url?id=1486672308.mp3',
            'http://music.163.com/song/media/outer/url?id=1459950258.mp3',
            'http://music.163.com/song/media/outer/url?id=1368398851.mp3',
            'http://music.163.com/song/media/outer/url?id=1303289043.mp3',
            'http://music.163.com/song/media/outer/url?id=523250334.mp3',
            'http://music.163.com/song/media/outer/url?id=1463165983.mp3',
            'http://music.163.com/song/media/outer/url?id=1403318151.mp3',
            'http://music.163.com/song/media/outer/url?id=1383972145.mp3',
            'http://music.163.com/song/media/outer/url?id=465921195.mp3',
            'http://music.163.com/song/media/outer/url?id=1471285412.mp3',
            'http://music.163.com/song/media/outer/url?id=1489065373.mp3',
            'http://music.163.com/song/media/outer/url?id=1442508316.mp3',
            'http://music.163.com/song/media/outer/url?id=1477539203.mp3',
            'http://music.163.com/song/media/outer/url?id=1490093393.mp3',
            'http://music.163.com/song/media/outer/url?id=1363948882.mp3',
            'http://music.163.com/song/media/outer/url?id=1401671455.mp3',
            'http://music.163.com/song/media/outer/url?id=1462875618.mp3',
            'http://music.163.com/song/media/outer/url?id=493735012.mp3',
            'http://music.163.com/song/media/outer/url?id=1344897943.mp3',
            'http://music.163.com/song/media/outer/url?id=1413585838.mp3',
            'http://music.163.com/song/media/outer/url?id=558071673.mp3',
            'http://music.163.com/song/media/outer/url?id=1436709403.mp3',
            'http://music.163.com/song/media/outer/url?id=1394997085.mp3',
            'http://music.163.com/song/media/outer/url?id=1436910205.mp3',
            'http://music.163.com/song/media/outer/url?id=1456443773.mp3',
            'http://music.163.com/song/media/outer/url?id=1435449062.mp3',
            'http://music.163.com/song/media/outer/url?id=1471064193.mp3',
            'http://music.163.com/song/media/outer/url?id=1330348068.mp3',
            'http://music.163.com/song/media/outer/url?id=1398663411.mp3',
            'http://music.163.com/song/media/outer/url?id=1387581250.mp3',
            'http://music.163.com/song/media/outer/url?id=407450223.mp3',
            'http://music.163.com/song/media/outer/url?id=1486513704.mp3',
            'http://music.163.com/song/media/outer/url?id=5238992.mp3',
            'http://music.163.com/song/media/outer/url?id=1481657185.mp3',
            'http://music.163.com/song/media/outer/url?id=207497.mp3',
            'http://music.163.com/song/media/outer/url?id=1471055851.mp3',
            'http://music.163.com/song/media/outer/url?id=1449678888.mp3',
            'http://music.163.com/song/media/outer/url?id=1413142894.mp3',
            'http://music.163.com/song/media/outer/url?id=1423241987.mp3',
            'http://music.163.com/song/media/outer/url?id=1407551413.mp3',
            'http://music.163.com/song/media/outer/url?id=483937795.mp3',
            'http://music.163.com/song/media/outer/url?id=1384026889.mp3',
            'http://music.163.com/song/media/outer/url?id=1400256289.mp3',
            'http://music.163.com/song/media/outer/url?id=32835565.mp3',
            'http://music.163.com/song/media/outer/url?id=29004400.mp3',
            'http://music.163.com/song/media/outer/url?id=1346104327.mp3',
            'http://music.163.com/song/media/outer/url?id=1421256202.mp3',
            'http://music.163.com/song/media/outer/url?id=441491828.mp3',
            'http://music.163.com/song/media/outer/url?id=1331819951.mp3',
            'http://music.163.com/song/media/outer/url?id=1460682363.mp3',
            'http://music.163.com/song/media/outer/url?id=1297742167.mp3',
            'http://music.163.com/song/media/outer/url?id=1374329431.mp3',
            'http://music.163.com/song/media/outer/url?id=1359356908.mp3',
            'http://music.163.com/song/media/outer/url?id=1363205817.mp3',
            'http://music.163.com/song/media/outer/url?id=1426112587.mp3',
            'http://music.163.com/song/media/outer/url?id=1488796175.mp3',
            'http://music.163.com/song/media/outer/url?id=1445761206.mp3',
            'http://music.163.com/song/media/outer/url?id=1406642934.mp3',
            'http://music.163.com/song/media/outer/url?id=1365898499.mp3',
            'http://music.163.com/song/media/outer/url?id=569213220.mp3',
            'http://music.163.com/song/media/outer/url?id=1383927243.mp3',
            'http://music.163.com/song/media/outer/url?id=1365393542.mp3',
            'http://music.163.com/song/media/outer/url?id=1488563891.mp3',
            'http://music.163.com/song/media/outer/url?id=1446769897.mp3',
            'http://music.163.com/song/media/outer/url?id=1453972194.mp3',
            'http://music.163.com/song/media/outer/url?id=1297498908.mp3',
            'http://music.163.com/song/media/outer/url?id=1487212156.mp3',
            'http://music.163.com/song/media/outer/url?id=1460656959.mp3',
            'http://music.163.com/song/media/outer/url?id=1463168014.mp3',
            'http://music.163.com/song/media/outer/url?id=31010566.mp3',
            'http://music.163.com/song/media/outer/url?id=1476239407.mp3',
            'http://music.163.com/song/media/outer/url?id=1459023707.mp3',
            'http://music.163.com/song/media/outer/url?id=460578140.mp3',
            'http://music.163.com/song/media/outer/url?id=1429716422.mp3',
            'http://music.163.com/song/media/outer/url?id=1403215687.mp3',
            'http://music.163.com/song/media/outer/url?id=1480204501.mp3',
            'http://music.163.com/song/media/outer/url?id=1479706965.mp3',
            'http://music.163.com/song/media/outer/url?id=1450574147.mp3',
            'http://music.163.com/song/media/outer/url?id=1484967131.mp3',
            'http://music.163.com/song/media/outer/url?id=1382596189.mp3',
            'http://music.163.com/song/media/outer/url?id=523251474.mp3',
            'http://music.163.com/song/media/outer/url?id=26305527.mp3',
            'http://music.163.com/song/media/outer/url?id=569200213.mp3',
            'http://music.163.com/song/media/outer/url?id=405599470.mp3',
            'http://music.163.com/song/media/outer/url?id=1383954630.mp3',
            'http://music.163.com/song/media/outer/url?id=1336856777.mp3',
            'http://music.163.com/song/media/outer/url?id=1293886117.mp3',
            'http://music.163.com/song/media/outer/url?id=1479526505.mp3',
            'http://music.163.com/song/media/outer/url?id=1438865533.mp3',
            'http://music.163.com/song/media/outer/url?id=1425626819.mp3',
            'http://music.163.com/song/media/outer/url?id=496370620.mp3',
            'http://music.163.com/song/media/outer/url?id=1463165960.mp3',
            'http://music.163.com/song/media/outer/url?id=1442332360.mp3',
            'http://music.163.com/song/media/outer/url?id=1313354324.mp3',
            'http://music.163.com/song/media/outer/url?id=21157332.mp3',
            'http://music.163.com/song/media/outer/url?id=1381755293.mp3',
            'http://music.163.com/song/media/outer/url?id=536622304.mp3',
            'http://music.163.com/song/media/outer/url?id=1398508295.mp3',
            'http://music.163.com/song/media/outer/url?id=1459232593.mp3',
            'http://music.163.com/song/media/outer/url?id=1406649619.mp3',
            'http://music.163.com/song/media/outer/url?id=569214250.mp3',
            'http://music.163.com/song/media/outer/url?id=1425814935.mp3',
            'http://music.163.com/song/media/outer/url?id=417859631.mp3',
            'http://music.163.com/song/media/outer/url?id=574566207.mp3',
            'http://music.163.com/song/media/outer/url?id=553755659.mp3',
            'http://music.163.com/song/media/outer/url?id=1455717202.mp3',
            'http://music.163.com/song/media/outer/url?id=1411358329.mp3',
            'http://music.163.com/song/media/outer/url?id=1335350269.mp3',
            'http://music.163.com/song/media/outer/url?id=1441758494.mp3',
            'http://music.163.com/song/media/outer/url?id=1478568147.mp3',
            'http://music.163.com/song/media/outer/url?id=1456200611.mp3',
            'http://music.163.com/song/media/outer/url?id=1380075991.mp3',
            'http://music.163.com/song/media/outer/url?id=1382985712.mp3',
            'http://music.163.com/song/media/outer/url?id=1357999894.mp3',
            'http://music.163.com/song/media/outer/url?id=1456286877.mp3',
            'http://music.163.com/song/media/outer/url?id=1356350562.mp3',
            'http://music.163.com/song/media/outer/url?id=1336856864.mp3',
            'http://music.163.com/song/media/outer/url?id=1455965526.mp3',
            'http://music.163.com/song/media/outer/url?id=1391891631.mp3',
            'http://music.163.com/song/media/outer/url?id=1376873330.mp3',
            'http://music.163.com/song/media/outer/url?id=865021614.mp3',
            'http://music.163.com/song/media/outer/url?id=1433562661.mp3',
            'http://music.163.com/song/media/outer/url?id=1399112638.mp3',
            'http://music.163.com/song/media/outer/url?id=513360721.mp3',
            'http://music.163.com/song/media/outer/url?id=1405283464.mp3',
            'http://music.163.com/song/media/outer/url?id=254574.mp3',
            'http://music.163.com/song/media/outer/url?id=528326686.mp3',
            'http://music.163.com/song/media/outer/url?id=550138197.mp3',
            'http://music.163.com/song/media/outer/url?id=1389090775.mp3',
            'http://music.163.com/song/media/outer/url?id=1490362193.mp3',
            'http://music.163.com/song/media/outer/url?id=1386460251.mp3',
            'http://music.163.com/song/media/outer/url?id=1433338551.mp3',
            'http://music.163.com/song/media/outer/url?id=1404885266.mp3',
            'http://music.163.com/song/media/outer/url?id=65766.mp3',
            'http://music.163.com/song/media/outer/url?id=461347998.mp3',
            'http://music.163.com/song/media/outer/url?id=25706282.mp3',
            'http://music.163.com/song/media/outer/url?id=1372060183.mp3',
            'http://music.163.com/song/media/outer/url?id=442314990.mp3',
            'http://music.163.com/song/media/outer/url?id=208902.mp3',
            'http://music.163.com/song/media/outer/url?id=1385856956.mp3',
            'http://music.163.com/song/media/outer/url?id=1451145776.mp3',
            'http://music.163.com/song/media/outer/url?id=480580003.mp3',
            'http://music.163.com/song/media/outer/url?id=1306507078.mp3',
            'http://music.163.com/song/media/outer/url?id=406475394.mp3',
            'http://music.163.com/song/media/outer/url?id=1334295185.mp3',
            'http://music.163.com/song/media/outer/url?id=1394963332.mp3',
            'http://music.163.com/song/media/outer/url?id=35678875.mp3',
            'http://music.163.com/song/media/outer/url?id=515453363.mp3',
            'http://music.163.com/song/media/outer/url?id=1384450197.mp3',
            'http://music.163.com/song/media/outer/url?id=1476849.mp3',
            'http://music.163.com/song/media/outer/url?id=1386259535.mp3',
            'http://music.163.com/song/media/outer/url?id=1383876635.mp3',
            'http://music.163.com/song/media/outer/url?id=1373168742.mp3',
            'http://music.163.com/song/media/outer/url?id=415792881.mp3',
            'http://music.163.com/song/media/outer/url?id=1397345903.mp3',
            'http://music.163.com/song/media/outer/url?id=1412559986.mp3',
            'http://music.163.com/song/media/outer/url?id=514761281.mp3',
            'http://music.163.com/song/media/outer/url?id=1460706496.mp3',
            'http://music.163.com/song/media/outer/url?id=346089.mp3',
            'http://music.163.com/song/media/outer/url?id=316686.mp3',
            'http://music.163.com/song/media/outer/url?id=1487527157.mp3',
            'http://music.163.com/song/media/outer/url?id=28018075.mp3',
            'http://music.163.com/song/media/outer/url?id=1343756008.mp3',
            'http://music.163.com/song/media/outer/url?id=1445670554.mp3',
            'http://music.163.com/song/media/outer/url?id=1456673752.mp3',
            'http://music.163.com/song/media/outer/url?id=1457707546.mp3',
            'http://music.163.com/song/media/outer/url?id=108390.mp3',
            'http://music.163.com/song/media/outer/url?id=1367452194.mp3',
            'http://music.163.com/song/media/outer/url?id=1387592437.mp3',
            'http://music.163.com/song/media/outer/url?id=1489269048.mp3',
            'http://music.163.com/song/media/outer/url?id=449818741.mp3',
            'http://music.163.com/song/media/outer/url?id=1358848433.mp3',
            'http://music.163.com/song/media/outer/url?id=1475124792.mp3',
            'http://music.163.com/song/media/outer/url?id=31445772.mp3',
            'http://music.163.com/song/media/outer/url?id=32507038.mp3',
            'http://music.163.com/song/media/outer/url?id=1426959223.mp3',
            'http://music.163.com/song/media/outer/url?id=413812448.mp3',
            'http://music.163.com/song/media/outer/url?id=1460682463.mp3',
            'http://music.163.com/song/media/outer/url?id=1489257173.mp3',
            'http://music.163.com/song/media/outer/url?id=456185577.mp3',
            'http://music.163.com/song/media/outer/url?id=1296833312.mp3',
            'http://music.163.com/song/media/outer/url?id=1356499052.mp3',
            'http://music.163.com/song/media/outer/url?id=554241732.mp3',
            'http://music.163.com/song/media/outer/url?id=1336856449.mp3',
            'http://music.163.com/song/media/outer/url?id=1384527426.mp3',
            'http://music.163.com/song/media/outer/url?id=1487009099.mp3',
            'http://music.163.com/song/media/outer/url?id=1412672813.mp3',
            'http://music.163.com/song/media/outer/url?id=1297802566.mp3',
            'http://music.163.com/song/media/outer/url?id=1436076578.mp3',
            'http://music.163.com/song/media/outer/url?id=1404511131.mp3',
            'http://music.163.com/song/media/outer/url?id=1453086724.mp3',
            'http://music.163.com/song/media/outer/url?id=1454732243.mp3',
            'http://music.163.com/song/media/outer/url?id=1490306026.mp3',
            'http://music.163.com/song/media/outer/url?id=1404906595.mp3',
            'http://music.163.com/song/media/outer/url?id=1365221826.mp3']
name_list = ['001会不会（吉他版）.mp3', '002经济舱\xa0(Live).mp3', '003他只是经过.mp3', '004偏爱.mp3', '005海底.mp3',
             '006唯一\xa0(prod.gc).mp3', '007是想你的声音啊 - (你快听\xa0滴答滴).mp3', '008游京.mp3', '009囍（Chinese\xa0Wedding）.mp3',
             '010永不失联的爱.mp3', '011天外来物.mp3', '012把回忆拼好给你.mp3', '013欢.mp3', '014还是分开.mp3', '015沉醉的青丝 - (如果回忆容易).mp3',
             '016会不会（正式版）.mp3', '017丢了你.mp3', '018执迷不悟.mp3', '019别再想见我.mp3', '020世间美好与你环环相扣.mp3',
             '021Love\xa0Is\xa0Gone\xa0(feat.\xa0Dylan\xa0Matthew)\xa0(Acoustic).mp3', '022不怪她 - (Blame).mp3',
             '023无人之岛.mp3', '024你是人间四月天.mp3', '025与我无关.mp3', '026你走demo.mp3', '027夏天的风 - (原唱：温岚).mp3',
             '028我像一个傻瓜（Frowned\xa0blueface）.mp3', '029好想爱这个世界啊\xa0(Live).mp3', '030隔岸 - (你呀你\xa0冻我心房).mp3',
             '031收敛.mp3', '032隔岸（DJ完整版）.mp3', '033起风了.mp3', '034冬眠.mp3', '035MOM.mp3', '036爸爸妈妈.mp3', '037彩券.mp3',
             '038偏爱 - (电视剧《仙剑奇侠传三》插曲).mp3', '039是想你的声音啊（DJ完整版）.mp3', '040DEAR\xa0JOHN.mp3', '041游山恋.mp3',
             '042回到夏天 - (我多想回到那个夏天).mp3', '043大眠\xa0(完整版) - (原唱：王心凌).mp3', '0447\xa0%.mp3', '045麻雀.mp3',
             '046撒野 - (巫哲小说《撒野》官方主题曲).mp3', '047所念皆星河.mp3', '048你的答案.mp3', '049国王与乞丐.mp3', '050烟火里的尘埃.mp3',
             '051多想在平庸的生活拥抱你.mp3', '052谪仙.mp3', '053水星记.mp3', '054像鱼.mp3', '055爱，存在.mp3', '056MELANCHOLY.mp3',
             '057Dancing\xa0With\xa0Your\xa0Ghost.mp3', '058晚安.mp3', '059你走以后1.0.mp3', '060下雨天.mp3', '061顽家.mp3',
             '062雨爱.mp3', '063我要找到你.mp3', '064失眠飞行.mp3', '065像我这样的人.mp3', '066这一生关于你的风景.mp3', '067孤身.mp3',
             '068致明日的舞.mp3', '069Lovefool.mp3', '070忘不了的是你.mp3', '071Walk\xa0Thru\xa0Fire.mp3', '072下一段旅程.mp3',
             '073你走 - (原唱：松紧先生（李宗锦）).mp3', '074不爱我.mp3', '075Sold\xa0Out.mp3', '076所念皆星河 - (演唱版).mp3',
             '077信仰 - (原唱：张信哲).mp3', '078感谢你曾来过.mp3', '079一个人想着一个人\xa0.mp3', '080想见你想见你想见你 - (电视剧《想见你》片尾曲).mp3',
             '081Salt.mp3', '082是你想成为的大人吗.mp3', '083情人.mp3', '084孤独.mp3', '085嚣张.mp3',
             '086说散就散 - (电影《前任3：再见前任》主题曲).mp3', '087江南.mp3', '088消愁.mp3', '089疑心病.mp3', '090Hey\xa0KONG.mp3',
             '091我曾.mp3', '092年少有为.mp3', '093虞兮叹.mp3', '094过活.mp3', '095万有引力 - (原唱：汪苏泷).mp3', '096断线.mp3', '097我要.mp3',
             '098Astronomia\xa0(Original\xa0Mix).mp3', '099出山.mp3', '100One\xa0Day.mp3', '101山楂树之恋 - (原唱：大能人).mp3',
             '102Lemon - (日剧《非自然死亡》主题曲).mp3', '103多情种.mp3', '104But\xa0U.mp3', '105有些.mp3', '106借.mp3', '107愿你余生漫长.mp3',
             '108我好像在哪见过你 - (电影《精灵王座》主题曲).mp3', '109盗将行.mp3', '110可不可以.mp3', '111苦尽甘来.mp3', '112勇气.mp3', '113生而为人.mp3',
             '114晚风.mp3', '115Not\xa0Angry.mp3', '116爱的恰恰.mp3', '117暗恋是一个人的事.mp3', '118根本你不懂得爱我（女生版）.mp3',
             '119归去来兮.mp3', '120爱，存在 - (原唱：魏奇奇).mp3', '121这一生关于你的风景.mp3', '122形容.mp3', '123下落不明.mp3', '124嗜好.mp3',
             '125吹梦到西洲.mp3', '126尘土.mp3', '127大天蓬\xa0(女生版).mp3', '128心似烟火 - (原曲：绊).mp3', '129云烟成雨 - (动画《我是江小白》片尾曲).mp3',
             '130句号.mp3', '131后来.mp3', "132I\xa0don't\xa0wanna\xa0see\xa0u\xa0anymore.mp3", '133没有理由.mp3', '134蓝.mp3',
             '135以梦为马 - (网易云音乐黑胶VIP品牌歌曲).mp3', '136天下 - (原唱：张杰).mp3', '137MOM - (原唱：蜡笔小心).mp3', '138下山.mp3',
             '139富士山下.mp3', '140Something\xa0Just\xa0Like\xa0This.mp3', '141夜空中最亮的星.mp3', '142空.mp3', '143后继者.mp3',
             '144红色高跟鞋.mp3', '145太阳.mp3', '146绝世舞姬.mp3', '147再也没有.mp3', '148Can\xa0We\xa0Kiss\xa0Forever.mp3',
             '149Wonderful\xa0U\xa0(Demo\xa0Version).mp3', '150写给黄淮.mp3', '151你应该很快乐.mp3', '152呼吸决定.mp3',
             '153All\xa0Falls\xa0Down.mp3', '154Remember\xa0Our\xa0Summer.mp3',
             '155Tonight\xa0(Best\xa0You\xa0Ever\xa0Had).mp3', '156飞 - (风浪没平息).mp3', '157迷人的危险.mp3', '158Señorita.mp3',
             '159刚刚好.mp3', '160悬溺.mp3', '161吹灭小山河 - (独家国风自制企划《观风月·竹马篇》).mp3', '162白羊.mp3', '163殉情的抹香鲸.mp3',
             '164海阔天空.mp3', '165处处吻.mp3', '166珍珠幻象\xa0(Live).mp3', '167你就不要想起我.mp3', '168太多 - (原唱：陈冠蒲).mp3',
             '169海底 - (原唱：一支榴莲).mp3', '170晚夜微雨问海棠.mp3', '171Love\xa0Story.mp3', '172说谎.mp3', '173我的一个道姑朋友.mp3',
             '174关山酒.mp3', '175半山腰的风景\xa0(Live).mp3', '176光年之外 - (电影《太空旅客》中文主题曲).mp3', '177追.mp3', '178我走后.mp3',
             '179理想三旬.mp3', '180演员.mp3', '181尘埃 - (原唱：家家).mp3', '182大鱼 - (动画电影《大鱼海棠》印象曲).mp3',
             '183How\xa0Are\xa0You - (中国新说唱).mp3', '184positions.mp3', '185Fractures.mp3', '186想你想你想我.mp3',
             '187你的姑娘.mp3', '188我的名字.mp3', '189告白 - (原唱：王欣宇).mp3', '190不得不爱.mp3', '191大反派.mp3',
             '192青丝 - (原唱：时光胶囊乐队).mp3', '193盗墓笔记·十年人间 - (八一七稻米节主题推广曲).mp3', '194COCO.mp3', '195Blueming.mp3',
             '196脆弱星球.mp3', '197只对你有感觉.mp3', '198小段.mp3', '199没有理由.mp3', '200四块五.mp3']

headers = {
    "User-Agent": get_user_agent(),
}

a = range(0, len(url_list))
for m in reversed(a):
    time.sleep(5)
    session = requests.session()
    res = session.get(url=url_list[m], headers=headers)
    chunk_size = 1024
    fileName = re.sub('[\/:*?"<>|]', '-', name_list[m])
    with open(fileName, 'wb') as f:
        for data in res.iter_content(chunk_size=chunk_size):
            f.write(data)
