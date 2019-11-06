import os, json

def ParseConfigFile(path):
    with open(path, "r") as cfgFile:
        config = json.loads(cfgFile.read())
        cfgFile.close()
        
        watch = config['watch']
        exclude = config['exclude']
        execute = config['execute']

        if exclude is None or watch is None:
            raise Exception

        return {
            'watch': watch,
            'exclude': exclude,
            'execute': execute
        }