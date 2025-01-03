import asyncio
from playwright.async_api import async_playwright
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

nltk.download('vader_lexicon', quiet=True)

async def scrape_reviews(url):
    reviews = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, timeout=120000)

        title = await page.title()
        print(f"Page Title: {title}")

        await page.wait_for_selector('.w8nwRe', timeout=60000)
        more_buttons = await page.query_selector_all('.w8nwRe')
        if more_buttons is not None:
            for button in more_buttons:
                await button.click()
                await page.wait_for_timeout(1000)

        await page.wait_for_selector('.jftiEf', timeout=60000)
        elements = await page.query_selector_all('.jftiEf')
        for element in elements:
            await page.wait_for_selector('.MyEned')
            snippet = await element.query_selector('.MyEned')
            text = await page.evaluate("selected => selected.textContent", snippet)
            reviews.append(text)

        await browser.close()
    return reviews, title

def analyze_sentiments(reviews):
    sia = SentimentIntensityAnalyzer()
    sentiments = []
    for review in reviews:
        score = sia.polarity_scores(review)
        compound = score['compound']
        if compound >= 0.05:
            sentiments.append('positive')
        elif compound <= -0.05:
            sentiments.append('negative')
        else:
            sentiments.append('neutral')
    return sentiments

async def scrape_and_analyze(url):
    reviews, title = await scrape_reviews(url)
    sentiments = analyze_sentiments(reviews)
    
    total_reviews = len(sentiments)
    positive = sum(1 for sentiment in sentiments if sentiment == 'positive')
    neutral = sum(1 for sentiment in sentiments if sentiment == 'neutral')
    negative = sum(1 for sentiment in sentiments if sentiment == 'negative')
    
    sentiment_percentages = {
        'positive': round((positive / total_reviews) * 100, 2),
        'neutral': round((neutral / total_reviews) * 100, 2),
        'negative': round((negative / total_reviews) * 100, 2),
    }
    
    return {
        'title': title,
        'total_reviews': total_reviews,
        'sentiment_percentages': sentiment_percentages,
        'reviews': reviews[:10]  # Return only the first 10 reviews
    }

