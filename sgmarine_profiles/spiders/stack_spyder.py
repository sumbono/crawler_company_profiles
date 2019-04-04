from scrapy import Spider
from scrapy import Request
from scrapy.selector import Selector
import datetime
import json

class StackSpider(Spider):
    name = "sgmarine_profiles"
    allowed_domains = ["www.sgmaritime.com"]

    start_urls = []

    with open("company_index.json", 'r') as infile:
        list_contents = json.load(infile)

        for item in list_contents:
            for key,val in item.items():
                if "url" in key:
                    start_urls.append(val)

    # unique url
    start_urls = list(set(start_urls))
    # print(start_urls)

    def parse(self, response):
        item = {}

        # get company name:
        comp_name = Selector(response).xpath('//*[@id="Contentplaceholder1_T5CE92B6B022_Col01"]/div/div[@class="col-md-9 company-details"]/h3/text()').extract()
        if len(comp_name) > 0:
            comp_name = " ".join(comp_name[0].split())
            item['company name'] = comp_name
        else:
            comp_name2 = Selector(response).xpath('//*[@id="Contentplaceholder1_T5CE92B6B022_Col01"]/div/div[@class="col-md-9 company-details"]/text()').extract()
            if len(comp_name2)>0:
                comp_name2 = " ".join(comp_name2[0].split())
                item['company name'] = comp_name2
        
        # get company url:
        comp_url = response.url
        item['company_url'] = comp_url

        # get company address:
        address = Selector(response).xpath('//*[@id="Contentplaceholder1_T5CE92B6B022_Col01"]/div/div[@class="col-md-9 company-details"]/div/div[@class="col-md-7 company-contact"]/p[1]/text()').extract() #extract the data list address
        join_address = " ".join("".join(address).split())
        item['company address'] = join_address

        # get company country:
        item['country'] = "Singapore" #as default

        # get company phone & fax:
        phone = Selector(response).xpath('//*[@id="Contentplaceholder1_T5CE92B6B022_Col01"]/div/div[@class="col-md-9 company-details"]/div/div[@class="col-md-7 company-contact"]/div[@class="valuephone"]/a/text()').extract()[0].strip()
        
        if len(Selector(response).xpath('//*[@id="Contentplaceholder1_T5CE92B6B022_Col01"]/div/div[@class="col-md-9 company-details"]/div/div[@class="col-md-7 company-contact"]/div[@class="valuefax"]/a/text()').extract())>0:
            fax = Selector(response).xpath('//*[@id="Contentplaceholder1_T5CE92B6B022_Col01"]/div/div[@class="col-md-9 company-details"]/div/div[@class="col-md-7 company-contact"]/div[@class="valuefax"]/a/text()').extract()[0].strip()
            item['company phone number'] = [" ".join(phone.split()), " ".join(fax.split())]
        else:
            item['company phone number'] = [" ".join(phone.split())]

        # get company email:
        if len(Selector(response).xpath('//*[@id="Contentplaceholder1_T5CE92B6B022_Col01"]/div/div[@class="col-md-9 company-details"]/div/div[@class="col-md-7 company-contact"]/a[@id="textemail"]/@onclick').extract())>0:
            email = Selector(response).xpath('//*[@id="Contentplaceholder1_T5CE92B6B022_Col01"]/div/div[@class="col-md-9 company-details"]/div/div[@class="col-md-7 company-contact"]/a[@id="textemail"]/@onclick').extract()[0]
            item['company email'] = email.split("'")[1]

        # get company website:
        if len(Selector(response).xpath('//*[@id="Contentplaceholder1_T5CE92B6B022_Col01"]/div/div[@class="col-md-9 company-details"]/div/div[@class="col-md-7 company-contact"]/div[@class="valuewebsite"]/a/@href').extract())>0:
            web = Selector(response).xpath('//*[@id="Contentplaceholder1_T5CE92B6B022_Col01"]/div/div[@class="col-md-9 company-details"]/div/div[@class="col-md-7 company-contact"]/div[@class="valuewebsite"]/a/@href').extract()[0]
            item['company website'] = web.strip()

        # get company description:
        if len(Selector(response).xpath('//*[@id="Contentplaceholder1_T5CE92B6B022_Col01"]/div/div[@class="col-md-12"]/div[@class="company-description"]/text()').extract())>0:
            comp_description = Selector(response).xpath('//*[@id="Contentplaceholder1_T5CE92B6B022_Col01"]/div/div[@class="col-md-12"]/div[@class="company-description"]/text()').extract()
            comp_description = "".join(comp_description)
            if comp_description.strip() != "":
                item['company description'] = comp_description.strip()

        # get company product & services:
        if len(Selector(response).xpath('//*[@id="Contentplaceholder1_T5CE92B6B022_Col01"]/div/div[@class="col-md-12"]/div[@class="owl-carousel-container"]/div[1]/div[@class="item"]/a/img/@title').extract())>0:
            comp_ps = Selector(response).xpath('//*[@id="Contentplaceholder1_T5CE92B6B022_Col01"]/div/div[@class="col-md-12"]/div[@class="owl-carousel-container"]/div[1]/div[@class="item"]/a/img/@title').extract()
            item['products and services'] = comp_ps

        # get company categories:
        if len(Selector(response).xpath('//*[@id="Contentplaceholder1_T5CE92B6B022_Col01"]/div/div[@class="col-md-12"]/div[@class="company-description"]/ul/ul/li/a/text()').extract())>0:
            comp_cat = Selector(response).xpath('//*[@id="Contentplaceholder1_T5CE92B6B022_Col01"]/div/div[@class="col-md-12"]/div[@class="company-description"]/ul/ul/li/a/text()').extract()
            item['category'] = comp_cat

        # get company contacts:
        if len(Selector(response).xpath('//*[@id="Contentplaceholder1_T5CE92B6B022_Col01"]/div/div[@class="col-md-9 company-details"]/div/div[@class="col-md-7 company-contact"]/p[2]/text()').extract())>0:
            contacts_raw = Selector(response).xpath('//*[@id="Contentplaceholder1_T5CE92B6B022_Col01"]/div/div[@class="col-md-9 company-details"]/div/div[@class="col-md-7 company-contact"]/p[2]/text()').extract()
            contacts = []
            for elem in contacts_raw:
                elem = elem.strip()
                if elem != "Contact":
                    if "Tel" not in elem:
                        if "Mobile" not in elem:
                            if "mail" not in elem:        
                                elem = elem.split(",")
                                el = {}
                                if len(elem)>1:    
                                    el['job_title'] = elem[1]
                                    el['name'] = elem[0]
                                    contacts.append(el)
                                    item['contacts'] = contacts
                                elif len(elem) == 1:
                                    if elem[0] != "":
                                        el['name'] = elem[0]
                                        contacts.append(el)
                                        item['contacts'] = contacts
                                        
                                # still can't handle for email's contact
                                # emails_raw = Selector(response).xpath('//*[@id="Contentplaceholder1_T5CE92B6B022_Col01"]/div/div[@class="col-md-9 company-details"]/div/div[@class="col-md-7 company-contact"]/p[2]/a/text()').extract()

        yield item