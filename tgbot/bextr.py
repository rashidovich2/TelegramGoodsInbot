from babel.messages.frontend import CommandLineInterface

#CommandLineInterface().run(['pybabel','extract','-F','babel.cfg','-o','locales/mybot.pot','../tgbot', '--project', 'mybot'])
#CommandLineInterface().run(['pybabel','init','-i','locales/mybot.pot','-d','locales', '-l','en', '-D', 'mybot'])
#CommandLineInterface().run(['pybabel','init','-i','locales/mybot.pot','-d','locales', '-l','ru', '-D', 'mybot'])
CommandLineInterface().run(['pybabel','compile','-d','locales', '-D', 'mybot'])
#CommandLineInterface().run(['pybabel','update','-d','locales', '-D', 'mybot', '-i', 'locales/mybot.pot'])