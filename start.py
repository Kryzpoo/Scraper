import argparse
import time

import collectors
import processors
import writers
from utils.log import setup_log

log = setup_log('scraper', 'scraper.log')


def stop_object(o) -> None:
    # Safe stopping of various objects
    if o:
        try:
            o.stop()
        except Exception:
            pass


def insensitive_str(s: str) -> str:
    # Insensitive string type for ArgumentParser
    return s.lower()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Tool for collecting data')
    parser.add_argument('--url',
                        type=insensitive_str,
                        help='Site URL for collecting',
                        default='https://www.tred.com')
    parser.add_argument('-z', '--zip_code',
                        type=insensitive_str,
                        help='Zip code for collecting',
                        required=True)
    parser.add_argument('-r', '--radius',
                        type=insensitive_str,
                        help='Radius for collecting',
                        required=True)
    parser.add_argument('-w', '--max_workers',
                        type=int,
                        help='Max workers for simultaneous collecting',
                        default=30)
    parser.add_argument('-o', '--output_filename',
                        type=insensitive_str,
                        help='Filename for output data',
                        default='output.xlsx')
    parser.add_argument('--collector',
                        type=insensitive_str,
                        help='Collector type',
                        default='selenium',
                        choices=('selenium',))
    parser.add_argument('--processor',
                        type=insensitive_str,
                        help='Processor type',
                        default='api',
                        choices=('api', 'selenium'))
    parser.add_argument('--writer',
                        type=insensitive_str,
                        help='Writer type',
                        default='excel',
                        choices=('excel', 'csv'))
    args = parser.parse_args()

    log.info(f'Start scrapping with args: {args}')
    time_start = time.time()

    processor = None
    writer = None
    collector = None

    # Determination of given processor
    if args.processor == 'api':
        processor = processors.ApiProcessor(args.url, args.max_workers)
    elif args.processor == 'selenium':
        processor = processors.SeleniumProcessor(args.max_workers)
    else:
        raise ValueError(f'Processor {args.processor} not defined')

    # Determination of given writer
    if args.writer == 'excel':
        writer = writers.ExcelWriter(args.output_filename)
    elif args.writer == 'csv':
        writer = writers.CsvWriter(args.output_filename)
    else:
        raise ValueError(f'Writer {args.writer} not defined')

    # Determination of given collector
    if args.collector == 'selenium':
        collector = collectors.SeleniumCollector(
            args.url, args.zip_code, args.radius, processor, writer)
    else:
        raise ValueError(f'Collector {args.collector} not defined')

    try:
        # Execution process
        processor.start()
        writer.start()
        collector.start()
        collector.collect()
    except Exception as e:
        log.error(e, exc_info=True)
    finally:
        stop_object(processor)
        stop_object(writer)
        stop_object(collector)
    time_stop = time.time()
    log.info(f'Finish scrapping. Elapsed: {time_stop - time_start}')
