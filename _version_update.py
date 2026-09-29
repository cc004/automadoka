"""Update from APKPure, or build/activate a downloaded XAPK offline."""
import argparse
import os


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apk', help='Local XAPK; omitted means APKPure latest')
    parser.add_argument('--prepare-only', action='store_true', help='Build and validate without activating')
    parser.add_argument('--cache-dir', help='Separate cache for testing or another instance')
    args = parser.parse_args()
    if args.cache_dir:
        os.environ['AUTOPCR_CACHE_DIR'] = os.path.abspath(args.cache_dir)
    from autopcr.core.version import _update_version_sync
    _update_version_sync(args.apk, activate=not args.prepare_only)


if __name__ == '__main__':
    main()
