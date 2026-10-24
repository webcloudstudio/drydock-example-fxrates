import argparse

class UsageError(Exception):
    pass

class FxArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        # Keep the CLI failure contract to one diagnostic line and no usage dump.
        raise UsageError(message.replace("\n", " "))

def build_parser():
    p=FxArgumentParser(prog='fxrates'); s=p.add_subparsers(dest='command', required=True, parser_class=FxArgumentParser)
    s.add_parser('init'); x=s.add_parser('load'); x.add_argument('csv')
    s.add_parser('fetch'); x=s.add_parser('serve'); x.add_argument('--port',type=int,default=8000)
    return p
