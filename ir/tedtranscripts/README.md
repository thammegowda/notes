# Ted Transcripts Crawler

This is a miniature crawler aimed to create parellel corpus (for Machine Translation).
This crawler scrapes trascripts of talks on TED.com.
The output text contains all additional information such as timestamp and id to
  align sentences across languages.


# Requirements
Scrapy 1.4, python 3.3+


# How to run

    scrapy crawl TedSpider -a lang=kn -o kannada.jl
    scrapy crawl TedSpider -a lang=en [-a talks=kannada.jl] -o english.jl

   1. `-a lang=<>` is the two digit language code reverse engineered from https://www.ted.com/talks/
   2. `-a talks=<>` is file path of previous ouput. This is an optional parameter.
      When this argument is missing, the crawler will fetch all talks available for the specified language
      When the previous output is specified, it fetches only those available talks but in the new desired language.
   3. `-o file.jl` is the path to out put file.







