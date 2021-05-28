import scrapy
import json


class QuotesSpider(scrapy.Spider):
    name = "novel"
    daftar_kata_novel = []

    def start_requests(self):
        url = 'https://www.worldnovel.online/'
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        novels_update = response.css('#index > section:nth-child(5) > div > table > tbody > tr > td:nth-child(1) > a')
        list_judul = [novels_update[node].attrib['title'] for node in range(20,25)]
        list_href = [novels_update[node].attrib['href'] for node in range(20,25)]

        
        
        for url in list_href:
            user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0'
            yield response.follow(url=url, callback=self.pindah_ke_ch)


    def pindah_ke_ch(self,response):
        id_novel = response.css('.js-chapter-in-novel').attrib['data-novel']
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0'
        url = 'https://www.worldnovel.online/wp-json/novel-id/v1/dapatkan_chapter_dengan_novel?category={}&perpage=100&order=ASC&paged=1'

        yield response.follow(url.format(id_novel), self.parse_novel)



    def parse_novel(self, response):
        ambil = json.loads(response.text)
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0'
        for node in range(0,10):
            url = ambil[node]['permalink']
            yield response.follow(url, self.parse_chaper)


    
    def parse_chaper(self,response):
        paragraf_satu = response.css('#soop > p:nth-child(3)::text').get()
        pecah = paragraf_satu.split(' ')
        if len(pecah)>3:
            kata = pecah[3]
        else:
            kata = pecah[0]
        self.daftar_kata_novel.append(kata)
        if len(self.daftar_kata_novel) == 49 :
            print('Kata Dalam Novel 1')
            for kata in range(0,10):
                print(self.daftar_kata_novel[kata])

            print('Kata Dalam Novel 2')
            for kata in range(10,20):
                print(self.daftar_kata_novel[kata])
            
            print('Kata Dalam Novel 3')
            for kata in range(20,30):
                print(self.daftar_kata_novel[kata])

            print('Kata Dalam Novel 4')
            for kata in range(30,40):
                print(self.daftar_kata_novel[kata])

            print('Kata Dalam Novel 5')
            for kata in range(40,50):
                print(self.daftar_kata_novel[kata])