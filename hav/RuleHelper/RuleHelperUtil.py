#!/usr/bin/python

import os
import time
import serial
import logging
import sys

from pathlib import Path

#Creacion del logger para los logs de aplicacion
loggerLog = logging.getLogger('server_logger1')
loggerLog.setLevel(logging.DEBUG)
inf = logging.FileHandler('/data/hab_sonda/logs/rules.log')
inf.setLevel(logging.DEBUG)
formatterInformer = logging.Formatter('[%(asctime)s][%(levelname)s][%(message)s]', datefmt='%Y-%m-%d %H:%M:%S')
inf.setFormatter(formatterInformer)
loggerLog.addHandler(inf)

#metodo que retorna una regla en base a su ID
def getRule(idRule):

    try:
        #TODO
        return "RuleXXXXX"
    except Exception as e:
        loggerLog.error("[RuleHelper][getRule] " + str(e))

        return "Missing Rule"

#Metodo que crea una regla en el motor de reglas
def putRule(idRule, ruleName, ruleDefinition):

    try:
        #TODO
        return 1
    except Exception as e:
        loggerLog.error("[RuleHelper][putRule] " + str(e))

        return 0

#Metodo que lista todas las reglas del motor de reglas
def getAllRules():

    ruleList = []
    try:
        #TODO
        return ruleList
    except Exception as e:
        loggerLog.error("[RuleHelper][putRule] " + str(e))

        return ruleList
