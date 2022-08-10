from it.Utils.Utils import levenshtein, random
from it.Exceptions.TreesExceptions import *

from configparser import ConfigParser

import queue
import os


class LocalVoices:
    def __init__(self) -> None:
        cfg = ConfigParser()
        cfg.read(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../config.ini"))
        path = cfg["path"]["voicelines"]
        if path:
            self.path_voicelines = os.path.join(path, "voicelines")
        else:
            self.path_voicelines = os.path.join(os.path.dirname(os.path.realpath(__file__)), "voicelines")
        self.tree = {}

    def __updateTree(self, god: str, skin: str, vgs: str) -> None:
        vgss = os.listdir(os.path.join(self.path_voicelines, god, skin, vgs))
        for vgs_ in vgss:
            self.tree[god][skin][vgs].put(vgs_)

    def getvgs(self, god: str, skin: str, vgs: str, flag: bool = False) -> [str, str, str, str]:

        if not os.path.exists(self.path_voicelines):
            raise NoVoicesError

        god = god.replace(" ", "_")
        skin = skin.replace(" ", "_")
        vgs = vgs.replace(" ", "_")

        if god == '*' or skin == "*" or vgs == "*":

            if god == "*" and skin == "*" and vgs == "*":
                try:
                    god = random(os.listdir(self.path_voicelines))
                    path_god = os.path.join(self.path_voicelines, god)
                    skin = random(os.listdir(path_god))
                    path_skin = os.path.join(path_god, skin)
                    vgs = random(os.listdir(path_skin))
                    path_vgs = os.path.join(path_skin, vgs)
                except Exception:
                    raise NoVoicesGodError
            elif god != "*" and skin == "*" and vgs == "*":
                try:
                    try:
                        god = levenshtein(god, os.listdir(self.path_voicelines), 2)
                        path_god = os.path.join(self.path_voicelines, god)
                    except Exception:
                        raise NoVoicesGodError
                    skin = random(os.listdir(path_god))
                    path_skin = os.path.join(path_god, skin)
                    vgs = random(os.listdir(path_skin))
                    path_vgs = os.path.join(path_skin, vgs)
                except Exception:
                    raise NoVoicesSkinError
            elif god != "*" and skin != "*" and vgs == "*":
                try:
                    try:
                        god = levenshtein(god, os.listdir(self.path_voicelines), 2)
                        path_god = os.path.join(self.path_voicelines, god)
                    except Exception:
                        raise NoVoicesGodError
                    try:
                        skin = levenshtein(skin, os.listdir(path_god), 2)
                        path_skin = os.path.join(path_god, skin)
                    except Exception:
                        raise NoVoicesSkinError
                    vgs = random(os.listdir(path_skin))
                    path_vgs = os.path.join(path_skin, vgs)
                except Exception:
                    raise NoVGSError
            elif flag:
                god = random(os.listdir(self.path_voicelines))
                path_god = os.path.join(self.path_voicelines, god)
                skin = random(os.listdir(path_god))
                path_skin = os.path.join(path_god, skin)
                path_vgs = os.path.join(path_skin, vgs)
            else:
                print("Sintassi errata")
                raise Exception

        else:
            try:
                god = levenshtein(god, os.listdir(self.path_voicelines), 2)
                path_god = os.path.join(self.path_voicelines, god)
            except Exception:
                raise NoVoicesGodError

            try:
                skin = levenshtein(skin, os.listdir(path_god), 2)
                path_skin = os.path.join(path_god, skin)
            except Exception:
                raise NoVoicesSkinError

            path_vgs = os.path.join(path_skin, vgs)
            if not os.path.exists(path_vgs):
                raise NoVGSError

        # path_vgs = os.path.join(path_skin, vgs)
        print(god, skin, vgs)

        if god not in self.tree:
            self.tree[god] = {}
            self.tree[god][skin] = {}
            self.tree[god][skin][vgs] = queue.Queue()
            self.__updateTree(god, skin, vgs)

        elif skin not in self.tree[god]:
            self.tree[god][skin] = {}
            self.tree[god][skin][vgs] = queue.Queue()
            self.__updateTree(god, skin, vgs)

        elif vgs not in self.tree[god][skin]:
            self.tree[god][skin][vgs] = queue.Queue()
            self.__updateTree(god, skin, vgs)

        if self.tree[god][skin][vgs].qsize() != len(os.listdir(path_vgs)):
            self.__updateTree(god, skin, vgs)

        url = self.tree[god][skin][vgs].get()
        self.tree[god][skin][vgs].put(url)

        return os.path.join(path_vgs, url), god, skin, vgs

    def voicelines(self, god: str) -> [str, str]:

        if not os.path.exists(self.path_voicelines):
            raise NoVoicesError

        try:
            god = levenshtein(god, os.listdir(self.path_voicelines), 2)
            path_god = os.path.join(self.path_voicelines, god)
        except Exception:
            raise NoVoicesGodError

        voicelines = os.listdir(path_god)
        voicelines.remove("default")

        skins = [
            "{}: {}".format(i + 1, voiceline.replace("_", " ").capitalize()) for i, voiceline in enumerate(voicelines)
        ]

        return god.capitalize(), "\n".join(skins)
