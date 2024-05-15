import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
import schedule

class TwitterScraper:
    def __init__(self, driver_location, accounts, word, interval):
        self.driver = self.open_driver(driver_location)
        self.accounts = accounts
        self.word = word
        self.interval = interval
        self.round = 0
        self.total_count = 0
        self.tweet_texts = []

    def open_driver(self, driver_location):
        PATH = driver_location
        cService = webdriver.ChromeService(executable_path=PATH)
        driver = webdriver.Chrome(service = cService)
        return driver
        
    def scrape_tweet(self, account):
        self.driver.get(account)
        sleep(3)
        new_tweets=[]
        tweets = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid='tweet']")
        for tweet in tweets:
            if tweet.text not in self.tweet_texts:
                new_tweets.append(tweet.text)
                self.tweet_texts.append(tweet.text)
        count = sum(tweet_text.count(word) for tweet_text in new_tweets)
        return count

    def report(self):
        for account in self.accounts:
            count = self.scrape_tweet(account)
            self.total_count += count
            print(f"Scraped {account}: found {count} mentions of {self.word}")
        self.round+=1
        print(f"{self.word} was mentioned {self.total_count} times in the last {self.round} minutes.")

        if self.round == self.interval:
            print(f"{self.word} was mentioned {self.total_count} times in the last {self.interval} minutes.")
            self.round = 0
            self.total_count = 0
            self.tweet_texts = []


    def scheduler(self):
        schedule.every(1).minutes.do(self.report)
        self.report() 
        while True:
            schedule.run_pending()
            sleep(1)
            


if __name__ == "__main__":
    accounts = [
        "https://twitter.com/Mr_Derivatives", 
        "https://twitter.com/warrior_0719",
        "https://twitter.com/ChartingProdigy",
        "https://twitter.com/allstarcharts",
        "https://twitter.com/yuriymatso",
        "https://twitter.com/TriggerTrades",
        "https://twitter.com/AdamMancini4",
        "https://twitter.com/CordovaTrades", 
        "https://twitter.com/Barchart",
        "https://twitter.com/RoyLMattox"
    ]

    word = input("Enter the stock word to look for (e.g., $TSLA): ")
    interval = int(input("Enter the time interval (in minutes) for scraping: "))
    driver_location = "C:\\Program Files\\Google\\Chrome\\Application\\chromedriver-win64\\chromedriver.exe"

    scraper = TwitterScraper(driver_location, accounts, word, interval)
    print(f"Starting scraper for accounts: {accounts} looking for ticker: {word} every {interval} minutes.")
    scraper.scheduler()
