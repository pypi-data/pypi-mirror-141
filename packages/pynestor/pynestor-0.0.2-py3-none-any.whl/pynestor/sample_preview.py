import sys

import gitlab
import os
from datetime import date
from pynestor.pynestor import (
    NestorInstance,
    NestorManualSetOpt,
    NestorGitDesc,
    NestorDescList,
)

######################################
# Python wraping nestor
######################################


set1 = NestorManualSetOpt("test", 1)
set2 = NestorManualSetOpt("test", 2)

l = NestorDescList()
l.append(set1)
l.append(set2)

print(l)
