import asyncio
from telethon import TelegramClient, events
from telethon.extensions import html
from telethon import functions, types
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors import UserBannedInChannelError, ChannelPrivateError, ChatWriteForbiddenError, SlowModeWaitError, UsernameInvalidError, ChatGuestSendForbiddenError, ForbiddenError, ChatAdminRequiredError
from aiogram.utils.markdown import hlink
import config
import os, sys
from sys import stdout
from os import path
import requests, socks
import regex
import random
from datetime import datetime
import time
import aiosqlite
import sqlite3
import urllib.request
import json
#from tgbot.services.api_sqlite import *
#from tgbot.utils.misc_functions import get_position_admin
#from tgbot.utils.const_functions import get_unix, get_date, clear_html

print("RUN SENDER*->")

#api_id = 22110947
#api_hash = '4c1dbb99b7785215a23c6a049b6633a5'
#client = TelegramClient('Forwarder', api_id, api_hash)

#PROXY
if config.PROXY_ENABLED:
    s = socks.socksocket()
    rnd_proxy = random.choice(config.PROXY_IPS).split(":")

api_id = 20974935
api_hash = '9fbac23d7f44aa3cdb065237998a4b14'
client = TelegramClient('Forwarder2', api_id, api_hash, proxy=s.set_proxy(socks.HTTP, rnd_proxy[0], rnd_proxy[1]) )
#client = TelegramClient('Forwarder2', api_id, api_hash)
#client.start()

position_id = 0
message_text = ""
article_url = ""
multi_mode = 0
first = 0


# Получение текущей даты
def get_date():
    this_date = datetime.now().replace(microsecond=0)
    this_date = this_date.strftime("%d.%m.%Y %H:%M:%S")

    return this_date

# Преобразование полученного списка в словарь
def dict_factory(cursor, row):
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}

# Форматирование запроса без аргументов
def update_format(sql, parameters: dict):
    if "XXX" not in sql: sql += " XXX "

    values = ", ".join([
        f"{item} = ?" for item in parameters
    ])
    sql = sql.replace("XXX", values)

    return sql, list(parameters.values())

#Добавление отправки асихронное
async def add_chat_data(chat_id, chat_name, chat_state):
    async with aiosqlite.connect('/var/local/bot3101fc/tgbot/data/database.db') as con:
        con.row_factory = aiosqlite.Row
        await con.execute("INSERT INTO storage_chats "
                          "(chat_id, chat_name, chat_state) "
                          "VALUES (?, ?, ?)",
                          [chat_id, chat_name, chat_state])
        await con.commit()

#Получение городов и url каналов
def get_chats():
    with sqlite3.connect('/var/local/bot3101fc/tgbot/data/database.db') as con:
        con.row_factory = dict_factory
        sql = "SELECT chat_id, chat_name, chat_url FROM chgrdb WHERE chat_url is not Null"
        return con.execute(sql).fetchall()


#Получение городов и url каналов
def get_cities_places():
    with sqlite3.connect('/var/local/bot3101fc/tgbot/data/database.db') as con:
        con.row_factory = dict_factory
        sql = "SELECT id as place_id, city as place_name, vacs_url FROM data_cities WHERE vacs_url is not Null"
        return con.execute(sql).fetchall()


#Добавление отправки асихронное
async def add_sending_positions(chat_id, position_id, position_description, resultx, datetime):
    async with aiosqlite.connect('/var/local/bot3101fc/tgbot/data/database.db') as con:
        con.row_factory = aiosqlite.Row
        await con.execute("INSERT INTO storage_positions_sending "
                          "(chat_id, position_id, position_description, resultx, datetime) "
                          "VALUES (?, ?, ?, ?, ?)",
                          [chat_id, position_id, position_description, resultx, datetime])
        await con.commit()
        #return sending_id


SQL_TEMPLATE_CHAT_ID = "SELECT * FROM storage_chats WHERE chat_id=?"
SQL_TEMPLATE_CHAT_NAME = "SELECT * FROM storage_chats WHERE chat_name=?"

chat_list1 = ['goodnewsrussia1',
              'TG_PR',
              'GruppaZS',
              'wildberries_chatwb',
              'market_place_rf',
              'go_marketplace',
              'tentinder',
              'certificat_centr',
              'poiskinvest',
              'packingBOX_Ff',
              'photoshooting595',
              'otcAsd',
              'wildberries_chat_help',
              'rabota_biznes_freelance',
              'textiles2022',
              'WB_infoChat',
              'google_fb_chat',
              'fb_google_chat',
              'avito_no_ban',
              'zashivayus',
              'textiles2022',
              'duaoptom',
              'sertficat_chat',
              'packingBOX_Ff',
              'newbusinesscommunity',
              'Techno_printt',
              'wb_ozon_fotos',
              'mpgroup_wildberries',
              'rieltor_top',
              'pro_sewubusiness',
              'PenzaBaraholka',
              'scladchina_mphelp']  # replace [...] with the list of chat IDs or usernames

chat_list2 = ['depress',
              'investing4all',
              'startupchat',
              'ru_f1',
              'pppixel_chat',
              'tashkentchatroom',
              'telha',
              'znakomstva_rus',
              'lepreco',
              'NeLiOne',
              'tranies',
              'chatnight',
              'Gaysiti',
              'lovesup',
              'andromedica',
              'sosedka_tg',
              'mi_mino',
              'VideoChat1',
              'paradisechat',
              'poshlyekhabarovsk',
              'bropickup',
              'dating74',
              'cfriends',
              'gchate',
              'razv',
              'Znacomstva',
              'professionallogisticgroup',
              'orendating',
              'mysql_ru',
              'ponyorm',
              'clickhouse_ru',
              'sqlcom',
              'tarantoolru',
              'bigdata_en',
              'neuroworkshop',
              'mailrucontests',
              'pythontelegrambotgroup',
              'habrachat',
              'violachat',
              'leprachat',
              'ropogXA',
              'habragram',
              'tavernofoverwatch',
              'apple_lepra',
              'krjok',
              'abody',
              'chatshiz',
              'tmmarketing',
              'myusadba',
              'casinoch',
              'vdohnovenyevokrug',
              'kzn_ch',
              'themamaideti',
              'mos_cosmetics',
              'tatarstan_chat',
              'RestoRadio',
              'ritualMSK',
              'TGweapon',
              'rucrash',
              'blackpiratexx',
              'darkcompany',
              'helpmePR',
              'crypto_guide',
              'happyandfree',
              'tattoo_anomalia',
              'auction38',
              'kommersantsouth',
              'BestTatts',
              'nya_vintage',
              'byvilain',
              'drive_club',
              'this_is_interesting',
              'Burenie_RF',
              'mbcrussia',
              'procrastinatorfm',
              'putin_in_focus',
              'minmaksgrupsuper777',
              'kvadratour_hot',
              'nezanesli',
              'Safeweb',
              'Myusli_4e',
              'crimea_nice',
              'prtalk',
              'belarus_bikers',
              'GunFreak',
              'ruzh_ps4',
              'TGRare_chat',
              'autoekb',
              'helpauto',
              'spamimvse',
              'MobiDevices',
              'cryptoreports',
              'driveracmsk',
              'mkflourish',
              'geraclea',
              'hvostovil',
              'vsamoletecom',
              'alltarget',
              'karapuziki']

chat_list2 = ['novosibirsk_chat',
              'ekaterinburgg',
              'mosclub',
              'Voronezh_night',
              'ufarb02',
              'vrn_night',
              'myklgd',
              'ActiveSamara',
              'nsk',
              'telnsk',
              'ufachat',
              'saratov_public',
              'tashkentcitychat',
              'kub23',
              'probkimsk',
              'vlchat',
              'ekbstile',
              'rzd_leningradka',
              'samuichat',
              'zhknekrasovka',
              'VLGChat',
              'pmik_tversu',
              'onlineNN',
              'berlin_ru',
              'TomskChat',
              'simf82',
              'kievchat',
              'palata6',
              'smolchat',
              'mdpskurgan',
              'ramchat',
              'petroskoi',
              'dvizh_od',
              'tashkenttatar',
              'Ruskeu',
              'arenda_bishkek',
              'yocitychat',
              'podval_41',
              'uazzz',
              'rigach',
              'chattolyatti',
              'russiandenmark',
              'boyar',
              'pushkino',
              'narvacity',
              'lgbtfr',
              'mdpschel174',
              'KyivHelp',
              'New_GoodStory',
              'khvchat',
              'goodyaroslavl',
              'ruslov',
              'ua_hackathon',
              'dnrtg',
              'novoshakh',
              'welcome_to_Russia_baby',
              'omskinspb',
              'AstraChat',
              'petrogradchat',
              'Kiev24onlain',
              'Taganroglove',
              'ChatBerlin',
              'Kharkov24onlain',
              'Odessa24onlain',
              'soc93',
              'chat_dv',
              'lipetskcity',
              'ekibastuz_vip',
              'tgnpets',
              'sfo_chat',
              'livecrimea',
              'buhara',
              'tomskpublic',
              'velokat_krd',
              'elektrostal_city',
              'nedimon_saratov',
              'pmmchat',
              'kb51alt',
              'gomelbel',
              'flirtchat34region',
              'academNSK',
              'indiagoaforum',
              'Mining102',
              'IvChat',
              'prmprotest',
              'mamuz',
              'chat_tomsk',
              'baraholkakazani',
              'Telega_UA',
              'ZnakomstvaNN',
              'donstuchat',
              'SevOnline',
              'dmd_chat',
              'bprumyan',
              'telbtc',
              'bizach',
              'chat_of_hyips',
              'BTC_top',
              'avitotop',
              'cointalk',
              'FYBIcoin',
              'CtrlvMining',
              'NemXemRu',
              'postcoinrussia',
              'novapromotions',
              'telvdl',
              'Place_Of_Meeting',
              'kklub',
              'ru_startup',
              'UzExpoCentr',
              'workoninternet',
              'businessempire',
              'VideoReklama1',
              'openbz',
              'uzb',
              'busypeople',
              'proAmazon ',
              'biz_club',
              'yuppie_chat',
              'chatmlm',
              'investingtalk',
              'BitRus',
              'ProVendingChat',
              'Best_Sellers',
              'myjobit',
              'coinmarket1',
              'fish25ru_gruz',
              'rabotavtaganroge',
              'finteh',
              'preICO',
              'Crypto_Traders_group',
              'AlexYanovsky',
              'btc_p2p',
              'mkmarket',
              'freedmanclub',
              'crypto_On',
              'finfreelance_chat',
              'CryptoTalksRu',
              'pandaChat',
              '2chs',
              'telizb',
              'telpoc',
              'ask911',
              'telinoi',
              'kingdomchat',
              'otkrytyy',
              'shumibl',
              'obshny',
              'tasix',
              'bestalkota',
              'goldenbuhara',
              'depra',
              'potreshyalkino',
              'telmem',
              'Bulbousness',
              'tintvk',
              'everest_lite',
              'alterchat',
              'razzyvova',
              'go_underground',
              'optimist',
              'vkchan',
              'somniya',
              'telconfa4',
              'onemoretime',
              'institutb',
              'planetchat',
              'outsiide',
              'yelik',
              'peach',
              'dobrochat',
              'teldeks',
              'TopChatt',
              'evacho',
              'faberzhe',
              'krutochat',
              'h4xen',
              'HIVECafe',
              'chaticrus',
              'sprite',
              'Whiskarev',
              'cloudchat',
              'telfatumchat',
              'group',
              'sova',
              'telranak',
              'spravy',
              'chattelega',
              'konfa',
              'TalkChat',
              'No_Rules_chat',
              'tupichok_krd',
              'furrichat',
              'Sorryveryblya',
              'gclub',
              'dimavolkovnostradamus',
              'kompashka',
              'tusavkavtg',
              'confaaa',
              'palatalordov',
              'Temles',
              'lampach',
              'kyivrus',
              'trashnyak',
              'dirtyminds',
              'mynutka',
              '2chdeutch',
              'trikotage',
              'welcome_to_sprite',
              'gymnast',
              'straightup_chat',
              'aefoundation',
              'consolelife',
              'readallhumans',
              'printer_ru',
              'youchat_ru',
              'instabloggers',
              '2chhw',
              'telmafia',
              'qpRvp',
              'xiaomimiui',
              'girlsandwomen',
              'TatarChat',
              'ludomania',
              'smmblogs',
              'biker_chat',
              'onichat',
              'temaplus',
              'lesbitemabi',
              'WickedHeaven',
              'varenichki',
              'yapishu',
              'trap_trans',
              'minecraft_ru',
              'hschat',
              'dushevnay',
              'mlpach',
              'hearthstone',
              'blender_ru',
              'ru_photo',
              'vinglish',
              'yaoi_chat',
              'naval',
              'igcomments',
              'castleoff',
              'over2ch',
              'nnovnaval',
              'AnimeKafe',
              'beardy_chat',
              'telid',
              'everypony',
              'chatUSSR',
              'samogon',
              'nimsesclub',
              'chatvzaimopomoshi',
              'vapecity',
              'fanfik',
              'edmprod',
              'warh40k',
              'ProEsp8266',
              'zdorovie_info',
              'motochat',
              'papacarder',
              'refnd',
              'puastatechat',
              'Videography_ru',
              'ThreeDDD',
              'teamnavalny_sochi',
              'nimses_off',
              'handmademasters',
              'esoterics_chat',
              'alichat',
              'to_best_world',
              'worldtanks',
              'vegrawspirit',
              'Shopping_on',
              'ezoter',
              'Singyoubitch',
              'returnegypt',
              'aviamili',
              'alcospirit',
              'TYCOOP',
              'dirtytractor',
              'ru_travel',
              'ppcchat',
              'sovushki',
              'youtube_chat',
              'SpiritOfMagic',
              'blacklist4',
              'Shizach',
              'zvukochat',
              'irkmason',
              'knigach',
              'gamestel',
              'tes_thread',
              'give',
              'spbsue',
              'zayavi_o_sebe',
              'englishleo',
              'Yaesm',
              'interesnuj_bloger',
              'dkitchen',
              'spbavtohelp',
              'torgopt',
              'PRTalk_one',
              'netvoyne',
              'mm_online',
              'gwent_ru',
              'CoCflood',
              'zt4dm',
              'anime_momentos_chat',
              'SpiritOfTheSky',
              'reptiloids_chat',
              'ourbetsua',
              'streamchat',
              'zdorovoz',
              'shizoconf',
              'baraholka_ukr',
              'trinityme',
              'marketingrf',
              'recentre',
              'lingvachat',
              'icryptogeek',
              'burimenov',
              'sad_ogorod',
              'pasekazello',
              'astralos',
              'kaknayti',
              'in_clouds',
              'tzzntchat',
              'chessconf',
              'SovaReklama',
              'shadynickiminaj',
              'musicandit',
              'Vegra',
              'mafia_wolf',
              'korea_chat',
              'customdevice',
              'northtower',
              'perevoz',
              'ThatLevelAgainChat',
              'ProMiningClub',
              'mejfrak',
              'cafemam',
              'DivinityOriginalSin2',
              'supergoodadvice',
              'tesolibrarychat',
              'CasualChat',
              'futbolstavkisport',
              'slabotochniki',
              'Crestbook',
              'tashkentchatroom',
              'telha',
              'znakomstva_rus',
              'lepreco',
              'NeLiOne',
              'tranies',
              'chatnight',
              'Gaysiti',
              'lovesup',
              'andromedica',
              'sosedka_tg',
              'mi_mino',
              'VideoChat1',
              'paradisechat',
              'poshlyekhabarovsk',
              'bropickup',
              'dating74',
              'cfriends',
              'gchate',
              'razv',
              'Znacomstva',
              'professionallogisticgroup',
              'orendating',
              'tgchat',
              'laravel_pro',
              'jschat',
              'javascript_jobs',
              'telhabrit',
              'telhabr',
              'freelancechat',
              'ru_ubuntu',
              'vostok404',
              'MikrotikRu',
              'android_talks',
              'bitrixfordevelopers',
              'proGO',
              'botoid',
              'android_ru',
              'telyii2',
              'apple_ru',
              'ru_raspberry',
              'ProCxx',
              'ru_modx',
              'reactnative_ru',
              'frontend_ru',
              'php_jobs',
              'telsysadm',
              'tel2chweb',
              'jvmchat',
              'tel1',
              'bigdata_ru',
              'unlimitedseo',
              'gogolang',
              'darkweby',
              'qa_jobs',
              'techat',
              'ru_python',
              'aboutsmmchat',
              'ioslords',
              'prowindows',
              'netdev',
              'nodejs_ru',
              'pro_ansible',
              'vertxpro',
              'weblive',
              'gnulinuxru',
              'deepinru',
              'xredminote4x',
              'android_questions',
              'pure_c',
              'CSharpChat',
              'ntwrk',
              'telwin10',
              'rubytalk',
              'jslang_new',
              'JSlang',
              'ios_ru',
              'angular_js',
              'asterisk_ru',
              'ctfchat',
              'proelixir',
              'devschat',
              'datasciencechat',
              'proasm',
              'devops_jobs',
              'ru_laravel',
              'codenamecrud',
              'archlinux_ru',
              'nag_public',
              'ru_voip',
              'typescript_ru',
              'mobile_jobs',
              'proRust',
              'proRuby',
              'dba_ru',
              'ZabbixPro',
              'wp4dev',
              'rubylang',
              'ArchLinuxChatRu',
              'pydjango',
              'joomlaru',
              'protelecom',
              'kubernetes_ru',
              'rudepython',
              'frontAndBack',
              'phpclubru',
              'xmpp_ru',
              'proembedded',
              'PostgreSQL_1C_Linux',
              'propython',
              'brutal_docker',
              'prozabbix',
              'chatops_ru',
              'railschat',
              'freebsd_ru',
              'glpi_ru',
              'chatbots_jobs',
              'reactos_ru',
              'MongoDBRussian',
              'devall',
              'codebynet',
              'pgsql',
              'puppet_ru',
              'pro_openstack',
              'phpinfo',
              'webjob',
              'css_ru',
              'javascript_ru',
              'kazdigital',
              'hadoopusers',
              'ittalks',
              'ohmy3dsmax',
              'custommanagement',
              'proCrystal',
              'OpsMgr',
              'configmgr',
              'webschool_rus_chat',
              'fordev',
              'augmoscow',
              'asterisk_expert',
              'wordpress_ru',
              'technoview',
              'thepalatalordov',
              'wpchat',
              'deeprefactoring',
              'ChatPython',
              'crmlist',
              'allvision',
              'augspb',
              'ru_flask',
              'AugKiev',
              'telanekdot',
              'telvik',
              'vipgif',
              'vapingclub',
              'lightpaint',
              'okolohookah_chat',
              'belweder',
              'dev_konf',
              'konfat',
              'tulpvoice',
              'gadaniekofe',
              'o_futbole',
              'teljuv',
              'juventus',
              'liverpoolfc',
              'DotNetRuChat',
              'extremecode',
              'elm_ru',
              'Fsharp_chat',
              'js_ru',
              'javastart',
              'javanese_questions',
              'scala_ru',
              'kotlin_lang',
              'ru_nim_talks',
              'modernperl',
              'usePerlOrDie',
              'ru_python_beginners',
              'prophp7',
              'reasonml_ru',
              'rubyschool',
              'rubyata',
              'moscowrb',
              'rustlang_ru',
              'embedded_rs',
              'frp_ru',
              'fp_ru',
              'cilchat',
              'clojure_ru',
              'powershell_pro',
              'powershellrus',
              'nativescript_ru',
              'ru_1c',
              'angular_ru',
              'emacs_ru',
              'laravelrus',
              'yii2ru',
              'dotnettalks',
              'dotnetgroup',
              'DotNetChat',
              'pro_net',
              'springframeworkio',
              'symfony_php',
              'symfony_ru',
              'electron_ru',
              'fire_monkey',
              'vuejs_ru',
              'wordpress1',
              'netbeans_ru',
              'vimedit_ru',
              'weex_ru',
              'webdesign_ru',
              'noobrank',
              'spbpython',
              'coding_ru',
              'codingteam',
              'Iot_chat',
              'proalgorithms',
              'atomicdesign',
              'microsoftschool',
              'eth_ru',
              'ru_hashicorp',
              'tilda_dev',
              'eoscode',
              'moscowProgers',
              'saintprug',
              'highloadcup',
              'avrahackathon',
              'pychel',
              'UnrealEngine4',
              'gamedevtalk',
              'gameanalysts',
              'sourceengine',
              'pro_hosting',
              'ceph_ru',
              'openstack_ru',
              'ru_hyper',
              'ru_freeswitch',
              'pro_mikrotik',
              'pro_kvm',
              'pro_enterprise',
              'aws_ru',
              'ru_nas',
              'specialistoffnet',
              'git_ru',
              'ru_email',
              'SourceBasedOS',
              'proasterisk',
              'ru_devops',
              'ru_docker',
              'metrics_ru',
              'mysql_ru',
              'ponyorm',
              'clickhouse_ru',
              'sqlcom',
              'tarantoolru',
              'bigdata_en',
              'neuroworkshop',
              'mailrucontests',
              'calculate_linux',
              'CentOSRu',
              'DebianRu',
              'fedora',
              'russianfedora',
              'russian_gentoo',
              'kdeneon',
              'LMInter',
              'macOS_ru',
              'macosx86',
              'manjarolinux',
              'OpenSuseRu',
              'rosa_linux',
              'smartos_ru',
              'that_is_linux',
              'xubuntu_runet',
              'safelinux',
              'mechmath',
              'higher_math',
              'comput_math',
              'physpub',
              'xamarin_russia',
              'iosgt',
              'idroidt',
              'upworkcom',
              'products_jobs',
              'agile_jobs',
              'getFreelance',
              'microsoftstackjobs',
              'eth_jobs',
              'bigdata_jobs',
              'django_jobs',
              'products_ru',
              'agile_ru',
              'agilegames',
              'spbitpeople',
              'newspblug',
              'chaosconstructions',
              'PiterPy',
              'DEFCON',
              'joinchat/ABI4pz3M7FCxoDZcdcfVUA',
              'pogromisty',
              'ru_board',
              'qa_ru',
              'ru_freelancers',
              'itsectalk',
              'joinchat/CD0D_D31vVD8L1FO4UutnQ',
              'mrl_hack',
              'ru_ASUTP',
              'ru_CAD',
              'linuxcoders',
              'Be_Tux',
              'it_holywars',
              'dev_seagulls',
              'ru_mechcult',
              'cloud_ru',
              'cloud_flood',
              'free_raspberry',
              'meshnet',
              'decentralized_social',
              'spb_auto',
              'distributed',
              'ru_politics',
              'ru_traders',
              'uxchat',
              'MOCKBAchat',
              'YandexPeopleMap',
              'spbcoa',
              'forgeekschat',
              'airbase_ru',
              'telecatethysis',
              'ru_electronics',
              'ru_arduino',
              'smmchat',
              'rusmmchat',
              'pizneschat',
              'bookz',
              'bookcrossing_spb',
              'ru_philosophy',
              'EducationChat',
              'bigmedchat',
              'cardiologlove',
              'septoplastic',
              'endocrinologlove',
              'proradio',
              'nocproject',
              'DC7499',
              'linkmeup_chat',
              'gikmechat',
              'RCmodels',
              'aviafan',
              'andycast',
              'tpair',
              'radioma',
              'bikechat',
              'DTPublish',
              'chatanonhownow',
              'podlodka',
              'GettCoinToday',
              'BitRussia',
              'varlamovnews',
              'FromBerek',
              'geeksChat',
              'inst_admins',
              'lampmining',
              'lazytool_chat',
              'NEMru',
              'web_structure',
              'digitaljob',
              'mlmchat',
              'dnative_chat',
              'pythontelegrambotgroup',
              'pro_krasnodar',
              'grouplinux',
              'targetchat',
              'habrachat',
              'abstract_opposition',
              'dim0n_spb',
              'contextchat',
              'python_beginners',
              'violachat',
              'investchat',
              'techmediachat',
              'ru2chvg',
              'Quizarium',
              'leprachat',
              'anime_ru',
              'ropogXA',
              'RaiBlocksRU',
              'FreedomZone',
              'durovkonf',
              'SynergyTeam',
              'zavtrachat',
              'iCrimea',
              'MiDevices',
              'habragram',
              'designerschat',
              'uiux_chat',
              'smmlove',
              'NavalnyNN',
              'tavernofoverwatch',
              'rupython',
              'amocrmhelp',
              'XiaomiFan',
              'apple_lepra',
              'vikipermchat',
              'krjok',
              'gruppettochat',
              'airpirates',
              'kinokotiki',
              'annekdot',
              'quiz_group',
              'evilarthas_pride',
              'windows_insider',
              'batya_chat',
              'trassam4don',
              'unlimited_seo',
              'sadnesschat',
              'okoe_chat',
              'samchat',
              'altlana',
              'pokemongo_ru',
              'abody',
              'chatshiz',
              'skovorodochka',
              'tmmarketing',
              'myusadba',
              'poputchikekb',
              'casinoch',
              'vdohnovenyevokrug',
              'i_vegan',
              'off_plankton',
              'chatbdsm',
              'kzn_ch',
              'themamaideti',
              'mos_cosmetics',
              'tatarstan_chat',
              'jokehubnews',
              'RestoRadio',
              'ritualMSK',
              'TGweapon',
              'kotovskRU',
              'fourfiveone',
              'record_guinness/1',
              'rucrash',
              'exitfrommatrix',
              'piarit',
              'SuperFacts',
              'svokzal',
              'blackpiratexx',
              'darkcompany',
              'helpmePR',
              'crypto_guide',
              'happyandfree',
              'tattoo_anomalia',
              'Summertime_S',
              'sladostipoleznosti/467',
              'schnorkel',
              'kurskkk',
              'togifka',
              'vidizarabotka',
              'allj_sayonaraboy',
              'pristroy_tao138',
              'auction38',
              'cheats_fifa',
              'kommersantsouth',
              'bitcoin2017crane',
              'BestTatts',
              'podarkoff',
              'strtart',
              'nya_vintage',
              'byvilain',
              'yarbaraholkaVzrosloe',
              'linecinema',
              'http://t.me/videoprosvet',
              'super_aliexpress',
              'drive_club',
              'this_is_interesting',
              'NowOrNeverMaaan',
              'dvchat',
              'proIIIiFFKING',
              'nailchat',
              'Burenie_RF',
              'tix24',
              'hitechlentach',
              'mbcrussia',
              'ya_mamka',
              'lifepenetration',
              'procrastinatorfm',
              'arabid',
              'putin_in_focus',
              'minmaksgrupsuper777',
              'kvadratour_hot',
              'Cvetovod',
              'ChinaGoodBuy',
              'nezanesli',
              'VK_Zarabotok',
              'sir_terry',
              'do3dru',
              'baraholkamoscow',
              'lohotrona_net',
              'Safeweb',
              'trehgorka',
              'radiorinki',
              'biosdump',
              'minsktmlive',
              'Myusli_4e',
              'crimea_nice',
              'prtalk',
              'mlm_legko',
              'belarus_bikers',
              'brestchat',
              'grimerka',
              'ideasworld',
              'razvratniki',
              'dejawe',
              'GunFreak',
              'ruzh_ps4',
              'edim_polezno',
              'fotoekb',
              'TGRare_chat',
              'autoekb',
              'baraholkaekb',
              'interesting_world',
              'helpauto',
              'baraholkavrn',
              'thebuzz7',
              'animationnnnnn',
              'spamimvse',
              'KinoChat',
              'MobiDevices',
              'cryptoreports',
              'music4escape',
              'readarticles',
              'driveracmsk',
              'natella_parfume',
              'mkflourish',
              'geraclea',
              'zakupki44fz',
              'myaforizm',
              'fleamarketmsk',
              'hvostovil',
              'vsamoletecom',
              'alltarget',
              'otgolosky',
              'chat1k',
              'karapuziki',
              'ylubka']

#Добавление отправки асихронное
async def get_chat_data(search_param):
    sql_query = ""

    if isinstance(search_param, int):
        sql_query = SQL_TEMPLATE_CHAT_ID
    elif isinstance(search_param, str):
        sql_query = SQL_TEMPLATE_CHAT_NAME
    else:
        raise Exception("Invalid parameter type. It should be either integer (for chat_id) or string (for chat_name).")
    async with aiosqlite.connect('/var/local/bot3101fc/tgbot/data/database.db') as con:
        con.row_factory = aiosqlite.Row
        cursor = await con.execute(sql_query, (search_param,))
        records = await cursor.fetchall()
        return records

#Добавление отправки асихронное
async def get_all_chatsxs():
    async with aiosqlite.connect('/var/local/bot3101fc/tgbot/data/database.db') as con:
        con.row_factory = aiosqlite.Row
        cursor = await con.execute("SELECT * FROM storage_chats")
        records = await cursor.fetchall()
        #await cursor.close()
        return records


#Добавление отправки асихронное
async def get_new_positionxs():
    async with aiosqlite.connect('/var/local/bot3101fc/tgbot/data/database.db') as con:
        con.row_factory = aiosqlite.Row
        cursor = await con.execute("SELECT * FROM storage_position WHERE position_state='Approved' OR position_state='Broadcast'")
        records = await cursor.fetchall()
        #await cursor.close()
        return records

# Получение позиции
def get_new_positionx():
    print('Получение позиции api_sqlite.py 318')
    with sqlite3.connect('/var/local/bot3101fc/tgbot/data/database.db') as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_position WHERE position_state='Approved' OR position_state='Broadcast'"
        return con.execute(sql).fetchall()

# Изменение позиции
def update_positionx(position_id, **kwargs):
    print('Изменение позиции api_sqlite.py 306')
    with sqlite3.connect('/var/local/bot3101fc/tgbot/data/database.db') as con:
        con.row_factory = dict_factory
        sql = "UPDATE storage_position SET"
        sql, parameters = update_format(sql, kwargs)
        parameters.append(position_id)
        con.execute(f"{sql}WHERE position_id = ?", parameters)
        con.commit()


def extract_hashtags(text):
    ht = ""
    pat = regex.compile(r'#\w*')
    hashtags = pat.findall(text)
    for ht in hashtags:
        print(ht)
    return ht

#text = '''
#In the summer, I love to travel to #beach destinations and relax under the #sun.
##VacationMode #SummerVibes
#'''

#print(hashtags)


async def download_image(url, file_path):
    print("3")
    f = urllib.request.urlretrieve(url, file_path)
    print(f)


async def callback_pr(current, total):
    print('Uploaded', current, 'out of', total, 'bytes: {:.2%}'.format(current / total))


async def send_message(client, chat_id, position_id=None, message_type=None, message_text=None, caption=None, image_url=None, file_path=None, broadcast=0):
    try:
        #while True:
        # Check for GeneratorExit and exit the coroutine if raised
        if asyncio.current_task().cancelled():
            return
        # Your other code here
        print(client)
        if message_type == 'photo':
            if image_url:
                file_path = '/var/local/bot3101fc/images/photo.png'
                await download_image(image_url, file_path)
                print("4")
                print(image_url, file_path)
                try:
                    #client.parse_mode = "HTML"
                    #caption = client.parse(caption)
                    caption = caption.replace("<b>", "*bold \*").replace("</b>", "*")
                    img = await client.upload_file(file_path, progress_callback=callback_pr)
                    await client.send_file(chat_id, file_path, caption=caption, progress_callback=callback_pr) #, parse_mode='HTML'

                except UserBannedInChannelError:
                    print("Приехали 5.")
                    print("5")
                    return

            elif file_path:
                try:
                    client.parse_mode = "HTML"
                    if broadcast == 0:
                        update_positionx(position_id, position_state="Posted")
                    datetime = get_date()
                    await add_sending_positions(chat_id, position_id, caption, "Posted", datetime)
                    await client.send_file(chat_id, file_path, caption=caption, progress_callback=callback_pr)
                    print(f"Отправлено в чат :{chat_id} успешно.")
                    #await update_positionx(position_id, position_state="Posted")
                    #if multi_mode == 1:
                    await asyncio.sleep(0.5)

                except UserBannedInChannelError:
                    print(f"Аккаунт забанен в этом чате:{chat_id}.")
                    datetime = get_date()
                    await add_sending_positions(chat_id, position_id, caption, "User Banned", datetime)
                    await asyncio.sleep(30)

                except ChannelPrivateError:
                    print(f"Чат оказался приватным: {chat_id}.")
                    datetime = get_date()
                    await add_sending_positions(chat_id, position_id, caption, "Channel Private", datetime)
                    await asyncio.sleep(30)

                except ChatWriteForbiddenError:
                    print(f"Аккаунту запретили писать в этот чат: {chat_id}.")
                    datetime = get_date()
                    await add_sending_positions(chat_id, position_id, caption, "Chat Write Forbidden", datetime)
                    await asyncio.sleep(30)

                except ChatGuestSendForbiddenError:
                    print(f"Необхдоимо вступить в группу: {chat_id}.")
                    datetime = get_date()
                    await add_sending_positions(chat_id, position_id, caption, "Chat Guest Send Forbidden", datetime)
                    await asyncio.sleep(30)

                except SlowModeWaitError as e:
                    print(f"В чате медленный режим для аккаунта, пауза на {e.seconds}: {chat_id}.")
                    datetime = get_date()
                    await add_sending_positions(chat_id, position_id, caption, "Slow Mode Wait", datetime)

                except ForbiddenError as e:
                    print(f"В чат запрещено отправлять {e}: {chat_id}.")
                    datetime = get_date()
                    await add_sending_positions(chat_id, position_id, caption, "ForbiddenError", datetime)

                except ChatAdminRequiredError:
                    print(f"Необхдоимо вступить в группу: {chat_id}.")
                    datetime = get_date()
                    await add_sending_positions(chat_id, position_id, caption, "Required Chat Admin", datetime)
                    await asyncio.sleep(30)

                if broadcast == 1:
                    print("SLEEP 40 WHILE BC PERIOD PASSED")
                    await asyncio.sleep(40)

            else:
                await client.send_file(chat_id, '/var/local/bot3101fc/images/photo.png', caption=caption)
                print("4-2")

        elif message_type == 'text':
            await client.send_message(chat_id, message_text)
        else:
            print('Invalid message type')

    except GeneratorExit:
        # Clean up resources or perform finalization tasks
        pass


async def check_chatchannelslist(chat_list):
    verified_chats = []
    for chat in chat_list:
        print(f"Чат:{chat}|||||||||||||||||||||||||||||||||")
        chat_res = await get_chat_data(chat)
        if len(chat_res) > 0:
            print("ALSO PRESENT IN DB")
        elif len(chat_res) == 0:
            try:
                response = await client.get_entity(chat)
                print(response)
                chat_id = response.id
                #verified_chats[chat_id] = response.title
                #verified_chats[chat_id] = chat
                verified_chats.append(chat_id)
                print("CHAT ADDED IN DB")
                print(verified_chats)
                await add_chat_data(response.id, chat, "verified")

            except ValueError as e:
                print (f'Value Error{e}')
                continue

            except UsernameInvalidError as e:
                print (f'Value Error{e}')
                continue

    return verified_chats


async def get_positionafj(position_id):
    try:
        #читаем файл позиций
        filename = '/var/local/bot3101fc/positions.json'
        if path.isfile('/var/local/bot3101fc/positions.json') is False:
            raise Exception("File not found")

        with open(filename) as f:
            exist_positions = json.load(f)

        for row in exist_positions:
            if 'position_id' in row and row['position_id'] == position_id:
                article_url = row['article_url']
                return article_url

        return None

    except FileNotFoundError as e:
        print(f"Error: {e}")

    except Exception as e:
        print(f"Error: {e}")


async def tg_send_message(client):

    broadcast = 0
    await client.start()

    if not await client.is_user_authorized():
        print('Telegram client failed to start.')
        return

    while True:

        success_chats = {}
        perm_list1 = ['test_rabota_permi_101', 'goodnewsrussia1']
        perm_list = ['test_rabota_permi_101']

        positions = await get_new_positionxs()

        chat_list = ""
        perm_list = ['test_rabota_permi_101']
        perm_list2 = ['goodnewsrussia1']
        vacs_list = ['goodnewsrussia1', 'vacsmsk', 'vacsspb', 'vacssam', 'vacspnz', 'vacskzn']

        if len(chat_list) > 0:
            for chat_id in chat_list:
                furl = f"t.me/{chat_id}"
                target_group = await client.get_entity(furl)
                target_group_entity = await client.get_entity(InputPeerChannel(target_group.id, target_group.access_hash))
        else:

            for position in positions:
                print(position['position_id'])
                position_description = position['position_description']
                file_path = f"/var/local/bot3101fc/tgbot/images/position{position['position_id']}.png"
                article_url = await get_positionafj(position['position_id'])
                chat_id = position['vacs_url']

                if position['position_state'] == "Approved":

                    if position_description:
                        shortml = 200
                        descritionlen = len(position_description)
                        if descritionlen >= shortml:
                            shortmestext = f"{position_description[0:shortml]}...\n\n"
                            hashtags = extract_hashtags(position_description)
                        elif descritionlen < shortml:
                            shortmestext = position_description

                        #добавляем ссылку на полную версию
                        htlinktext = f"<a href={article_url}>читать далее...</a>"
                        alinktext = f"[читать далее...]({article_url})"
                        shortmestext += f"\n{htlinktext}"
                        if descritionlen >= shortml:
                            shortmestext += f"\n\n{hashtags}"

                    else: shortmestext = "Текст отсутствует"
                else: shortmestext = position_description

                message_type = 'photo'  # replace with your type variable  file='file_id'
                image_url = None
                message_text = None

                if position['vacs_url'] == "ALL_CHANNELS" and position['position_state'] == "Approved":
                    places = get_cities_places()
                    for place in places:
                        chat_id = place['vacs_url']
                        if chat_id != "ALL_CHANNELS":
                            broadcast = 0
                            await send_message(client, chat_id, position_id=position['position_id'], message_type=message_type, message_text=message_text, caption=shortmestext, image_url=image_url, file_path=file_path, broadcast=broadcast)

                elif position['position_state'] == "Broadcast":
                    places = get_chats()
                    print(places)
                    for place in places:
                        chat_id = place['chat_url']
                        broadcast = 1
                        await send_message(client, chat_id, position_id=position['position_id'], message_type=message_type, message_text=message_text, caption=shortmestext, image_url=image_url, file_path=file_path, broadcast=broadcast)

                else:
                    broadcast = 0
                    await send_message(client, chat_id, position_id=position['position_id'], message_type=message_type, message_text=message_text, caption=shortmestext, image_url=image_url, file_path=file_path, broadcast=broadcast)
                #await update_positionx(position['position_id'], state="Posted")
                #if multi_mode == 1:
                await asyncio.sleep(0.5)

        first = 1
        positions = None
        print('ON AIR +>>>.')
        if broadcast == 1:
            print("MAIN CYCLE SLEEP 400 WHILE BC PERIOD PASSED")
            await asyncio.sleep(400)
            #await asyncio.sleep(10)
        print("MAIN CYCLE SLEEP 30 WHILE BC PERIOD PASSED")
        await asyncio.sleep(30)
        #await client.disconnect()

        '''task = asyncio.current_task()
        if task is not None:
            task.cancel()'''


print(sys.argv)

print("1")
api_id = 28712772
api_hash = '2e3785d00832ceee5cb453d7138b99ea'
#image = "https://www.donzella.ru/images/thumbs/000/0007490_erstnoj-kostm-ermenegildo-zegna_1002.jpeg"
#asyncio.get_event_loop().run_until_complete(tg_send_message(client = TelegramClient('Forwarder', api_id, api_hash), message_type="photo", message_text=None, caption="ADV MESSAGE TEST", image_url=image))
async def send_telegram_message(message_type="photo", message_text=None, caption=None, image_url=None):
#async def send_telegram_message(client=TelegramClient('Forwarder', api_id, api_hash), message_type="photo", message_text=None, caption=None, image_url=None):
    #asyncio.get_event_loop().run_until_complete(await tg_send_message(message_type="photo", message_text=message_text, caption=caption, image_url=image_url))
    #asyncio.run(await tg_send_message(message_type="photo", message_text=message_text, caption=caption, image_url=image_url))
    print("1")
    api_id = 28712772
    api_hash = '2e3785d00832ceee5cb453d7138b99ea'
    await tg_send_message(client = TelegramClient('Forwarder', api_id, api_hash), message_type=message_type, message_text=message_text, caption=caption, image_url=image_url)


#await tg_send_message(client = TelegramClient('Forwarder', api_id, api_hash), message_type=message_type, message_text=message_text, caption=caption, image_url=image_url)
#asyncio.get_event_loop().run_until_complete(tg_send_message(client = TelegramClient('Forwarder', api_id, api_hash), message_type="photo", message_text=None)) #, caption=caption, image_url=image_url
'''x = 0
try:
    while True:
        asyncio.run(positions = get_new_positionxs())
        if len(positions) > 0:
            asyncio.get_event_loop().run_until_complete(tg_send_message(client = TelegramClient('Forwarder', api_id, api_hash)))
            x+=1
            print(f"Итерация:{x}")

        time.sleep(5)

except GeneratorExit:
    # Clean up resources or perform finalization tasks
    pass'''

async def process_new_records():
    positions = await get_new_positionxs()
    for position in positions:
        asyncio.get_event_loop().run_until_complete(tg_send_message(client = TelegramClient('Forwarder', api_id, api_hash)))
        await process_position(position)

async def process_record(record):
    # Perform your new function here
    print(record)

# Run the process_new_records function asynchronously
asyncio.get_event_loop().run_until_complete(tg_send_message(client))