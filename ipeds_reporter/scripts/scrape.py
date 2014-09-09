#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
WIP thing to scrape ipeds for me.

Usage:
    ./scrape.py test
    ./scrape.py --uid=<uid_path> --mvl=<mvl_path>
"""
import os

from docopt import docopt
from selenium import webdriver
from project_runpy import env
import requests


def get_uids(path):
    with open(path) as f:
        institutions = f.readlines()
    return [x.split('|', 2)[0] for x in institutions]


def download_data(driver):
    """Get info from webdriver and use requests to download a csv."""
    # FIXME does not work
    cookies = {x['name']: x['value'] for x in driver.get_cookies()}
    post_data = driver.execute_script('return $("form:eq(1)").serialize();')
    url = 'http://nces.ed.gov/ipeds/datacenter/Data.aspx'
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.94 Safari/537.36'
    response = requests.post(url,
        cookies=cookies,
        headers={
            'Referer': url,
            'User-Agent': user_agent,
        },
    )


def main(uid_path, mvl_path):
    if not os.path.isfile(uid_path):
        exit('.uid file must exist')
    if not os.path.exists(mvl_path):
        exit('.mvl must exist')
    driver = webdriver.Chrome()  # DELETEME Chrome can go to Hell
    # driver = webdriver.Firefox()  # XXX Firefox, why do you keep breaking?
    # start session
    driver.get('http://nces.ed.gov/ipeds/datacenter/')
    # Go back to the Data Center
    driver.get('http://nces.ed.gov/ipeds/datacenter/')
    # "Compare Institutions"
    driver.find_element_by_id('tdInstData').click()
    # > sent to http://nces.ed.gov/ipeds/datacenter/login.aspx
    # TODO explicitly click "use final release data"
    driver.find_element_by_id('ibtnLoginLevelOne').click()
    # > sent to http://nces.ed.gov/ipeds/datacenter/InstitutionByName.aspx
    driver.execute_script('$("#tbInstitutionSearch").val("{}")'
        .format(u','.join(get_uids(uid_path))))
    driver.find_element_by_id('ctl00_contentPlaceHolder_ibtnSelectInstitutions').click()
    # > sent to "1. Select Institutions" part two - checkboxes
    driver.execute_script('CheckGVInstitutions()')
    driver.find_element_by_id('ctl00_contentPlaceHolder_ibtnContinue').click()
    # > sent to "1. Select Institutions" part three - final list
    driver.get('http://nces.ed.gov/ipeds/datacenter/mastervariablelist.aspx?stepId=2')
    # > sent to "2. Select Variables"
    driver.get('http://nces.ed.gov/ipeds/datacenter/UploadMasterList.aspx?stepId=2')
    # login to enable upload by variable
    driver.get('http://nces.ed.gov/ipeds/datacenter/PowerUserLogin.aspx')
    driver.find_element_by_id('tbPowerUserEmail').send_keys(env.require('IPEDS_EMAIL'))
    driver.find_element_by_id('tbPowerUserPassword').send_keys(env.require('IPEDS_PASSWORD'))
    driver.find_element_by_id('ibtnLogin').click()  # submit
    # Go back to this screen
    driver.get('http://nces.ed.gov/ipeds/datacenter/UploadMasterList.aspx?stepId=2')
    ################ upload mvl
    # TODO loop through .mvl files
    field = driver.find_element_by_id('ctl00_contentPlaceHolder_fulFile')
    field.send_keys(mvl_path)
    driver.find_element_by_id('ctl00_contentPlaceHolder_ibtnSubmit').click()  # submit
    driver.find_element_by_xpath('//a[text()="Select all"]').click()
    driver.find_element_by_id('ctl00_contentMainBody_iActionButton').click()  # submit
    # select "Short variable name"
    driver.find_element_by_id('ctl00_contentPlaceHolder_rbShortVariableName').click()
    # Download Report
    # download_data(driver)
    driver.find_element_by_id('ctl00_contentPlaceHolder_imgbtnGetCustomDataSet').click()

    # Clear Variables
    driver.get('http://nces.ed.gov/ipeds/datacenter/mastervariablelist.aspx?delete=true')
    # Pause until user input
    raw_input('Press Enter to end.')  # DELETEME DEBUG
    driver.close()


def test():
    pass


if __name__ == '__main__':
    arguments = docopt(__doc__)
    if arguments['test']:
        test()
    else:
        main(uid_path=arguments['--uid'], mvl_path=arguments['--mvl'])
