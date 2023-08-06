"""copy_kibana_objects CLI
Usage:
    copy_kibana_objects.py [--origin_env=<origin_env>] [--destination_env=<destination_env>]
                           [--origin_space_id=<origin_space_id>] [--destination_space_id=<destination_space_id>]
                            [--dashboard_id=<dashboard_id>] [--new_index_pattern=<new_index_pattern>]
    copy_kibana_objects.py -h|--help

Options:
    -h --help  Show this screen.
"""

from docopt import docopt
from tl_scripts.copy_kibana_objects import copy_kibana_objects


def __main__():
    arguments = docopt(__doc__)
    copy_kibana_objects()


if __name__ == '__main__':
    __main__()
