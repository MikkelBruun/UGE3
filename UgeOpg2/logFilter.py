LOGLEVELS = [
    "SUCCESS",
    "INFO",
    "WARNING",
    "ERROR"
]
try:
    with open("app_log.log", "r") as (_log):
        log = _log.readlines()
        for lvl in LOGLEVELS:
            with open(lvl+"__app_log.log", "w") as newFile:
                newFile.writelines(list(filter(lambda l: lvl in l,log)))
except Exception as err:
    print(err)