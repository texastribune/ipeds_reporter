#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
WIP thing to scrape ipeds for me.
"""
from selenium import webdriver


def main():
    driver = webdriver.Firefox()
    driver.close()


if __name__ == '__main__':
    main()
