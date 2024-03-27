class Settings:
    def __init__(self):
        pass

    @classmethod
    def validateBooleanSetting(cls, argument):
        validValues = {
            "true": True,
            "yes": True,
            "on": True,
            "1": True,
            "false": False,
            "no": False,
            "off": False,
            "0": False,
        }

        if argument.lower() in validValues:
            return validValues[argument.lower()]
        else:
            raise ValueError("Invalid boolean")

    @classmethod
    def getSetting(cls, settings, settingName):
        if settingName.lower() in cls.validSettings:
            if settingName.lower() in settings:
                return settings[settingName.lower()]
            else:
                return cls.validSettings[settingName.lower()]["defaultValue"]

        else:
            raise ValueError("Invalid setting")

    @classmethod
    def setSetting(cls, settings, settingName, settingValue):
        settings[settingName.lower()] = settingValue

    @classmethod
    def parseSetting(cls, settingName, settingValue):
        return cls.validSettings[settingName.lower()]["validateFunction"](settingValue)

    @classmethod
    def validSetting(cls, setting):
        return setting.lower() in cls.validSettings


Settings.validSettings = {
    "autosendresults": {
        "validateFunction": Settings.validateBooleanSetting,
        "defaultValue": False,
    }
}
