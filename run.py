import argparse
import sys
from datetime import datetime
from omegaconf import OmegaConf

from src.phish_scraper.phish_scraper import PhishScraper
from src.browserstack.browserstack_runner import BrowserstackRunner
from src.url_checker.url_checker import URLChecker
from src.cve_searcher.cve_searcher import CVESearcher

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
def save_page_source(args):
    config = OmegaConf.load(CONFIG_FILE)
    x = BrowserstackRunner(config=config)
    if args.session_id:
        x.save_page_source_session_id(args.session_id)
    elif args.unique_id:
        x.save_page_source_unique_id(args.unique_id)
def save_logs(args):
    config = OmegaConf.load(CONFIG_FILE)
    x = BrowserstackRunner(config=config)
    if args.session_id:
        x.save_logs_session_id(args.session_id)
    elif args.unique_id:
        x.save_logs_unique_id(args.unique_id)
def save_all(args):
    config = OmegaConf.load(CONFIG_FILE)
    x = BrowserstackRunner(config=config)
    if args.session_id:
        x.save_all_session_id(args.session_id)
    elif args.unique_id:
        x.save_all_unique_id(args.unique_id)
def save_run_info(args):
    config = OmegaConf.load(CONFIG_FILE)
    x = BrowserstackRunner(config=config)
    x.save_run_info(args.build_name)

# PHISHTANK FUNCTIONS
def phish_scraper(args):
    config = OmegaConf.load(CONFIG_FILE)
    x = PhishScraper(config=config)
    if args.source == 'phishtank':
        if args.manual:
            x.manual_phishtank(args.num_urls)
        else:
            x.fetch_phishtank(args.num_urls)
    else:
        print("Source not selected.")

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
    elif args.mode == 'ocsp':
        x.check_ocsp(args.url)
    elif args.mode == 'crl':
        x.check_crl(args.url)

# CVE SEARCHER FUNCTIONS
def cve_searcher_browser(args):
    config = OmegaConf.load(CONFIG_FILE)
    x = CVESearcher(config=config)
    x.scrape_browser_cves(args.source)
def cve_searcher_versions(args):
    config = OmegaConf.load(CONFIG_FILE)
    x = CVESearcher(config=config)
    x.parse_browser_versions()
# def cve_searcher_os(args):
#     config = OmegaConf.load(CONFIG_FILE)
#     x = CVESearcher(config=config)
#     x.scrape_os_cves(args.source)

# for testing new functionality
def test(args):
    print("doing nothing rn")
    # config = OmegaConf.load(CONFIG_FILE)
    # x = BrowserstackRunner(config=config)
    # x.save_run_info("JwIZY1fx_All_Targets")


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
    # Subsubparser for saving browserstack outcome(s)
    browserstack_save_outcome = browserstack_subparsers.add_parser("save_outcome", help="Save and analyze the detected outcome(s) of a completed browserstack session")
    id_mutex_group = browserstack_save_outcome.add_mutually_exclusive_group(required=True)
    id_mutex_group.add_argument("-s", "--session_id", help="The session ID of the completed browserstack session")
    id_mutex_group.add_argument("-u", "--unique_id", help="The unique string ID within the title of the relevant browserstack builds (randomly generated by our framework)")
    browserstack_save_outcome.set_defaults(func=save_outcome)
    # Subsubparser for saving browserstack page source(s)
    browserstack_save_page_source = browserstack_subparsers.add_parser("save_pagesrc", help="Save the page source(s) of a completed browserstack session")
    id_mutex_group = browserstack_save_page_source.add_mutually_exclusive_group(required=True)
    id_mutex_group.add_argument("-s", "--session_id", help="The session ID of the completed browserstack session")
    id_mutex_group.add_argument("-u", "--unique_id", help="The unique string ID within the title of the relevant browserstack builds (randomly generated by our framework)")
    browserstack_save_page_source.set_defaults(func=save_page_source)
    # Subsubparser for saving browserstack logs
    browserstack_save_logs = browserstack_subparsers.add_parser("save_logs", help="Save and analyze logs of a completed browserstack session")
    id_mutex_group = browserstack_save_logs.add_mutually_exclusive_group(required=True)
    id_mutex_group.add_argument("-s", "--session_id", help="The session ID of the completed browserstack session")
    id_mutex_group.add_argument("-u", "--unique_id", help="The unique string ID within the title of the relevant browserstack builds (randomly generated by our framework)")
    browserstack_save_logs.add_argument("-l", "--logs", choices=[], default='all', help="The log types of the completed session(s) to save; saves everything by default")
    browserstack_save_logs.set_defaults(func=save_logs)
    # Subsubparser for saving browserstack outcome(s)
    browserstack_save_all = browserstack_subparsers.add_parser("save_all", help="Save all data of a completed browserstack session")
    id_mutex_group = browserstack_save_all.add_mutually_exclusive_group(required=True)
    id_mutex_group.add_argument("-s", "--session_id", help="The session ID of the completed browserstack session")
    id_mutex_group.add_argument("-u", "--unique_id", help="The unique string ID within the title of the relevant browserstack builds (randomly generated by our framework)")
    browserstack_save_all.set_defaults(func=save_all)
    # Subsubparser for saving browserstack build info (generate info.json file)
    browserstack_save_run_info = browserstack_subparsers.add_parser("save_info", help="Save run info of a completed browserstack session (generate info.json file)")
    browserstack_save_run_info.add_argument("-b", "--build_name", required=True, help="The name of the build folder to generate info.json for")
    browserstack_save_run_info.set_defaults(func=save_run_info)

    # Subparser for phish_scraper
    phish_scraper_parser = subparsers.add_parser("phish_scraper", help="Use phish_scraper submodule")
    phish_scraper_parser.add_argument("-s", "--source", choices=['phishtank'], default='phishtank', help="Source to get URLs from; currently only supports PhishTank")
    phish_scraper_parser.add_argument("-n", "--num_urls", type=int, required=False, help="The number of phishing URLs to fetch")
    phish_scraper_parser.add_argument("-m", "--manual", action="store_true", help="Manually check the phishing sites to see if they are online")
    phish_scraper_parser.set_defaults(func=phish_scraper)

    # Subparser for url_checker
    url_checker_parser = subparsers.add_parser("url_checker", help="Use url_checker submodule")
    src_mutex_group = url_checker_parser.add_mutually_exclusive_group(required=True)
    src_mutex_group.add_argument("-u", "--url", help="The URL to check")
    src_mutex_group.add_argument("-f", "--file", help="The set of URLs to check, in a CSV formatted file") # TODO: add support for other filetypes
    url_checker_parser.add_argument("-m", "--mode", choices=['all', 'google_safebrowsing', 'phishtank', 'ocsp', 'crl'], default='all', help="Value must be among [all, google_safebrowsing, phishtank, ocsp, crl]")
    url_checker_parser.set_defaults(func=url_checker)
    
    # Subparser for cve_searcher
    cve_searcher_parser = subparsers.add_parser("cve_searcher", help="Use cve_searcher submodule")
    cve_searcher_subparsers = cve_searcher_parser.add_subparsers(dest="cve_searcher_module", required=True, help="CVE Searcher submodule to run")
    cve_search_browser = cve_searcher_subparsers.add_parser("browser", help="Searches for phishing-related CVEs for browsers")
    cve_search_browser.add_argument("-s", "--source", choices=['cvedetails', 'mitre'], default='cvedetails', help="The CVE database to search from")
    cve_search_browser.add_argument("-y", "--year", default=(datetime.now().year-2), help="Get CVEs until [year] ago; default is 2 years old")
    cve_search_browser.set_defaults(func=cve_searcher_browser)
    
    cve_parse_version = cve_searcher_subparsers.add_parser("parse_version", help="Parse browser versions from CVEs")
    cve_parse_version.set_defaults(func=cve_searcher_versions)

    
    # cve_search_os = cve_searcher_subparsers.add_parser("os", help="Searches for phishing-related CVEs for OSs")
    # cve_search_os.add_argument("-s", "--source", choices=['cvedetails', 'mitre'], default='cvedetails', help="The CVE database to search from")
    # cve_search_os.add_argument("-y", "--year", default=(datetime.now().year-2), help="Get CVEs until [year] ago; default is 2 years old")
    # cve_search_os.set_defaults(func=cve_searcher_os)
    
    # for testing new functionality
    test_parser = subparsers.add_parser("test")
    test_parser.set_defaults(func=test)
    

    # Parse the arguments and call the appropriate function
    args = parser.parse_args()

    if args.module in list(subparsers.choices.keys()):
        args.func(args)
    else:
        print(f"Unknown module: {args.module}")

if __name__ == "__main__":
    main()