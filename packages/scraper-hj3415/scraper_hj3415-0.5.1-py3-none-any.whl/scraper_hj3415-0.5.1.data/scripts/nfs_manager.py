import os
import sys
import argparse
import pprint

from krx_hj3415 import krx
from util_hj3415 import noti

from scraper_hj3415.miscrapy import scraper as scraper_mi
from scraper_hj3415.nfscrapy import scraper as scraper_nfs

from db_hj3415 import dbpath


import logging
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.INFO)


if __name__ == '__main__':
    spiders = ['c101', 'c106', 'c108', 'c103', 'c104']
    present_addr = dbpath.load()

    # reference form https://docs.python.org/3.3/howto/argparse.html#id1
    parser = argparse.ArgumentParser(
        prog="nfs_manager",
        description="My Scraper program",
        epilog=f"Present addr - {present_addr}",
    )
    parser.add_argument('-m', '--message', action='store_true', help='Send telegram message with result after work.')
    subparsers = parser.add_subparsers(
        title='Subcommands',
        description='valid subcommands',
        help='Additional help',
        dest="subcommand"
    )

    # create the parser for the "nf" command
    nf_parser = subparsers.add_parser(
        'nf',
        description=f"Scrape naver finance",
        help='Scrape naver finance',
        epilog=f"Present addr - {present_addr}",
    )
    nf_parser.add_argument('spider', choices=spiders)
    spiders_group = nf_parser.add_mutually_exclusive_group()
    spiders_group.add_argument('-c', '--code', metavar='code', help='Scrape one code')
    spiders_group.add_argument('-a', '--all', action='store_true', help='Scrape all codes')

    # create the parser for the "mi" command
    mi_parser = subparsers.add_parser(
        'mi',
        description=f"Scrape market index",
        help='Scrape market index',
        epilog=f"Present addr - {present_addr}",
    )

    # create the parser for the "gm" command
    gm_parser = subparsers.add_parser(
        'gm',
        description=f"Scrape global market",
        help='Scrape global market',
        epilog=f"Present addr - {present_addr}",
    )

    # create the parser for the "db" command
    db_parser = subparsers.add_parser(
        'db',
        description=f"Help to set the mongo database address",
        help='Help to set the mongo database address',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"{pprint.pformat(dbpath.make_path(('<ID>', '<PASS>')))}"
    )
    db_parser.add_argument('cmd', choices=['set', 'print'])
    db_parser.add_argument('-t', choices=['ATLAS', 'INNER', 'LOCAL', 'OUTER'])
    db_parser.add_argument('-i', help='Set id with address')
    db_parser.add_argument('-p', help='Set password with address')

    args = parser.parse_args()
    logger.debug(args)

    if args.subcommand == 'nf':
        if args.code:
            scraper_nfs.run(args.spider, [args.code, ])
            if args.message:
                noti.telegram_to('manager',
                                 f'>>> python {os.path.basename(os.path.realpath(__file__))} {args.subcommand} -c {args.code}')
        elif args.all:
            scraper_nfs.run(args.spider, list(krx.get_codes()))
            if args.message:
                noti.telegram_to('manager',
                                 f'>>> python {os.path.basename(os.path.realpath(__file__))} {args.subcommand} -a')
        sys.exit()
    elif args.subcommand == 'mi':
        if args.message:
            noti.telegram_to('manager',
                             f'>>> python {os.path.basename(os.path.realpath(__file__))} {args.subcommand}')
        scraper_mi.mi()
        sys.exit()
    elif args.subcommand == 'gm':
        pass
    elif args.subcommand == 'db':
        if args.cmd == 'print':
            print(present_addr)
        elif args.cmd == 'set':
            path = dbpath.make_path((args.i, args.p))[args.t]
            # print(path)
            # mongo2.connect_mongo(path)
            dbpath.save(path)
    else:
        parser.print_help()
        sys.exit()
