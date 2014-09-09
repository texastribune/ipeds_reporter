#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
WIP thing to scrape ipeds for me.

Usage:
    ./scrape.py <uid_file_path>
"""
from docopt import docopt
from selenium import webdriver
from project_runpy import env


def get_uids(path):
    with open(path) as f:
        institutions = f.readlines()
    return [x.split('|', 2)[0] for x in institutions]


def main(uid_file_path):
    print 'driver'
    driver = webdriver.Chrome()  # DELETEME Chrome can go to Hell
    # driver = webdriver.Firefox()  # XXX Firefox, why do you keep breaking?
    print 'start'
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
    field = driver.find_element_by_id('tbInstitutionSearch')
    uids = get_uids(uid_file_path)
    field.send_keys(u','.join(uids))  # this is so slow!
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
    # driver.close()


if __name__ == '__main__':
    arguments = docopt(__doc__)
    main(uid_file_path=arguments['<uid_file_path>'])
