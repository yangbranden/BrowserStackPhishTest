import argparse
import sys
from omegaconf import OmegaConf

from src.fetch_phishtank import PhishtankFetcher
from src.browserstack.browserstack_runner import BrowserstackRunner
from src.url_checker.url_checker import URLChecker

CONFIG_FILE = "config.yml"

# BROWSERSTACK FUNCTIONS
def browserstack_runner(args):
    config = OmegaConf.load(CONFIG_FILE)
    x = BrowserstackRunner(config=config)
    x.run_browserstack()
def target_generator(args):
    config = OmegaConf.load(CONFIG_FILE)
    x = BrowserstackRunner(config=config)
    x.generate_targets(args.platform)
def save_outcome(args):
    config = OmegaConf.load(CONFIG_FILE)
    x = BrowserstackRunner(config=config)
    if args.session_id:
        x.save_outcome_session_id(args.session_id)
    elif args.unique_id:
        x.save_outcome_unique_id(args.unique_id)
def save_logs(args):
    config = OmegaConf.load(CONFIG_FILE)
    x = BrowserstackRunner(config=config)
    if args.session_id:
        x.save_logs_session_id(args.session_id)
    elif args.unique_id:
        x.save_logs_unique_id(args.unique_id)

# PHISHTANK FUNCTIONS
def phishtank_fetcher(args):
    config = OmegaConf.load(CONFIG_FILE)
    x = PhishtankFetcher(config=config)
    x.fetch_phishtank(args.num_urls)

# URL CHECKER FUNCTIONS
def url_checker(args):
    config = OmegaConf.load(CONFIG_FILE)
    x = URLChecker(config=config)
    if args.mode == 'all':
        x.check_all(args.url)
    elif args.mode == 'google_safebrowsing':
        x.check_google_safebrowsing(args.url)
    elif args.mode == 'phishtank':
        x.check_phishtank(args.url)
    elif args.mode == 'check_ocsp':
        x.check_ocsp(args.url)
    elif args.mode == 'check_crl':
        x.check_crl(args.url)

def main():
    parser = argparse.ArgumentParser(description="Mobile Phishing framework")
    subparsers = parser.add_subparsers(dest="module", required=True, help="Module to run")

    # Subparser for browserstack
    browserstack_parser = subparsers.add_parser("browserstack", help="Use browserstack submodule")
    browserstack_subparsers = browserstack_parser.add_subparsers(dest="browserstack_module", required=True, help="Browserstack submodule to run")
    # Subsubparser for running browserstack
    browserstack_exec = browserstack_subparsers.add_parser("exec", help="Execute browserstack using the configuration in the config.yml file")
    # other options for this module should be specified in config.yml
    browserstack_exec.set_defaults(func=browserstack_runner)
    # Subsubparser for generating browserstack targets
    browserstack_generate_targets = browserstack_subparsers.add_parser("generate_targets", help="Generate target list to be used by browserstack")
    browserstack_generate_targets.add_argument("-p", "--platform", choices=['all', 'android', 'ios', 'windows', 'macosx'], default='all', required=True, help="Value must be among [all, android, ios, windows, macosx]")
    browserstack_generate_targets.set_defaults(func=target_generator)
    # Subsubparser for saving browserstack outcome
    browserstack_save_outcome = browserstack_subparsers.add_parser("save_outcome", help="Save and analyze the detected outcome of a completed browserstack session")
    id_mutex_group = browserstack_save_outcome.add_mutually_exclusive_group(required=True)
    id_mutex_group.add_argument("-s", "--session_id", help="The session ID of the completed browserstack session")
    id_mutex_group.add_argument("-u", "--unique_id", help="The unique string ID within the title of the relevant browserstack builds (randomly generated by our framework)")
    browserstack_save_outcome.set_defaults(func=save_outcome)
    # Subsubparser for saving browserstack logs
    browserstack_save_logs = browserstack_subparsers.add_parser("save_logs", help="Save and analyze logs of a completed browserstack session")
    id_mutex_group = browserstack_save_logs.add_mutually_exclusive_group(required=True)
    id_mutex_group.add_argument("-s", "--session_id", help="The session ID of the completed browserstack session")
    id_mutex_group.add_argument("-u", "--unique_id", help="The unique string ID within the title of the relevant browserstack builds (randomly generated by our framework)")
    browserstack_save_logs.add_argument("-l", "--logs", choices=[], default='all', help="The log types of the completed session(s) to save; saves everything by default")
    browserstack_save_logs.set_defaults(func=save_logs)

    # Subparser for phishtank_fetcher
    phishtank_fetcher_parser = subparsers.add_parser("phishtank_fetcher", help="Use phishtank_fetcher submodule")
    phishtank_fetcher_parser.add_argument("-n", "--num_urls", type=int, required=False, help="The number of phishing URLs to fetch from PhishTank")
    phishtank_fetcher_parser.set_defaults(func=phishtank_fetcher)

    url_checker_parser = subparsers.add_parser("url_checker", help="Use url_checker submodule")
    src_mutex_group = url_checker_parser.add_mutually_exclusive_group(required=True)
    src_mutex_group.add_argument("-u", "--url", help="The URL to check")
    src_mutex_group.add_argument("-f", "--file", help="The set of URLs to check, in a CSV formatted file") # TODO: add support for other filetypes
    url_checker_parser.add_argument("-m", "--mode", choices=['all', 'google_safebrowsing', 'phishtank', 'ocsp', 'crl'], default='all', help="Value must be among [all, google_safebrowsing, phishtank, ocsp, crl]")
    url_checker_parser.set_defaults(func=url_checker)

    # Parse the arguments and call the appropriate function
    args = parser.parse_args()

    if args.module in list(subparsers.choices.keys()):
        args.func(args)
    else:
        print(f"Unknown module: {args.module}")

if __name__ == "__main__":
    main()