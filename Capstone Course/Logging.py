import datetime

class Logging:
    """ Class used to log to an external file """
    def __init__(self):
        self.date = datetime.datetime.now()
        self.file = open("logs/{}-{}-{}_{}-{}-{}.txt".format(self.date.strftime("%d"), self.date.strftime("%m"), self.date.strftime("%y"), self.date.strftime("%H"), self.date.strftime("%M"), self.date.strftime("%S")), "w")

    def write_to_file(self, string) -> None:
        """ Writes the string given to the Logging file """
        self.file.write(string+"\r\n")

    def close(self) -> None:
        """ Closes the Logging file """
        self.file.close()