#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
WIP thing to scrape ipeds for me.
"""
from selenium import webdriver


def main():
    print 'driver'
    driver = webdriver.Chrome()
    # driver = webdriver.Chrome('/path/to/chromedriver')
    # driver = webdriver.Firefox()
    print 'start'
    # start session
    driver.get('http://nces.ed.gov/ipeds/datacenter/')
    # "Compare Institutions"
    driver.find_element_by_id('tdInstData').click()
    # > sent to http://nces.ed.gov/ipeds/datacenter/login.aspx
    # TODO explicitly click "use final release data"
    driver.find_element_by_id('ibtnLoginLevelOne').click()
    # > sent to http://nces.ed.gov/ipeds/datacenter/InstitutionByName.aspx
    # driver.close()


if __name__ == '__main__':
    main()
