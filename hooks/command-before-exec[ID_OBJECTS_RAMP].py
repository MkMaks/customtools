# -*- coding: UTF-8 -*-
from pyrevit import EXEC_PARAMS
from pyrevit import forms, script

# img = 'https://traviswhitecommunications.com/wp-content/uploads/2012/09/dont-do-it.jpg'
# script.open_url(img)

# forms.toast(
#     "Toto nerob!",
#     title="STOP",
#     appid="CustomTools",
#     click="https://eirannejad.github.io/pyRevit/",
#     actions={
#         "GFI Wiki":"https://gfi.miraheze.org/m/3vk"
#         },
#     icon="C:\Users\davidv\Desktop\work families\pyrevit\CustomTools.extension\hooks\icon.png")

res = forms.alert("POZOR!\n\n"
                  "Rampy je lepšie modelovať ako Floor v spáde.\n"
                  "- rampy nemajú možnosť pridávať vrstvy\n"
                  "- na rampy sa nedá umiestniť šípka spádu ani plavák\n"
                  "- v budúcnosti bude musieť po tebe niekto rampu premodelovať na Floor",
                  title="Ramp",
                  footer="CustomTools Hooks",
                  options=["Aj napriek tomu vytvoriť rampu",
                           "Zrušiť",
                           "Viac info o kategórii Ramp"])
if res  == "Aj napriek tomu vytvoriť rampu":
   EXEC_PARAMS.event_args.Cancel = False
   # logging to server
   from hooksScripts import hooksLogger
   hooksLogger("Ramp")

elif res  == "Zrušiť":
   EXEC_PARAMS.event_args.Cancel = True
elif res  == "Viac info o kategórii Ramp":
   EXEC_PARAMS.event_args.Cancel = True
   url = 'https://gfi.miraheze.org/wiki/Postupy,_ktor%C3%BDm_je_potrebn%C3%A9_sa_vyhn%C3%BA%C5%A5_-_Revit#Rampy'
   script.open_url(url)
   
else:
   EXEC_PARAMS.event_args.Cancel = True