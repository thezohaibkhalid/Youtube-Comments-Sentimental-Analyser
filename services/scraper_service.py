import asyncio
from playwright.async_api import async_playwright
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

# nltk.download('vader_lexicon', quiet=True)

async def scrape_reviews(url):
    reviews = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, timeout=120000)

        title = await page.title()
        print(f"Page Title: {title}")

        # Click "More reviews" button multiple times
        for _ in range(5):  # Adjust this number to load more reviews
            try:
                more_button = await page.wait_for_selector('//button[contains(text(), "More reviews")]', timeout=5000)
                if more_button:
                    await more_button.click()
                    await page.wait_for_timeout(2000)  # Wait for new reviews to load
                else:
                    break
            except:
                break  # Break the loop if the button is not found

        await page.wait_for_selector('.jftiEf', timeout=60000)
        elements = await page.query_selector_all('.jftiEf')
        for element in elements:
            try:
                # Extract review text
                snippet = await element.query_selector('.MyEned')
                text = await snippet.inner_text() if snippet else ""

                # Extract author name
                author_element = await element.query_selector('.d4r55')
                author = await author_element.inner_text() if author_element else "Anonymous"

                # Extract rating
                rating_element = await element.query_selector('.kvMYJc')
                rating = await rating_element.get_attribute('aria-label') if rating_element else "No rating"
                rating = rating.split(' ')[0] if rating else "N/A"

                reviews.append({
                    "text": text,
                    "author": author,
                    "rating": rating
                })
            except Exception as e:
                print(f"Error extracting review: {e}")

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
    review_texts = [review['text'] for review in reviews]
    sentiments = analyze_sentiments(review_texts)
    
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
        'reviews': reviews[:10] 
    }



# import asyncio
# from playwright.async_api import async_playwright
# from nltk.sentiment import SentimentIntensityAnalyzer
# import nltk

# nltk.download('vader_lexicon', quiet=True)

# async def scrape_reviews(url):
#     reviews = []
#     async with async_playwright() as p:
#         browser = await p.chromium.launch(headless=True)
#         page = await browser.new_page()
#         await page.goto(url, timeout=120000)

#         title = await page.title()
#         print(f"Page Title: {title}")

#         # Scroll to load more reviews and click "View More" button if it exists
#         for _ in range(20):   
#             await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
#             await page.wait_for_timeout(3000)   

#             # Try to click "View More" button using the correct XPath locator
#             try:
#                 # Use `locator().xpath()` to locate by XPath
#                 more_button = page.locator(
#                     'xpath=/html/body/div[2]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[46]/div/button'
#                 )
#                 if await more_button.is_visible():  
#                     print("Clicking 'View More' button")
#                     await more_button.click()
#                     await page.wait_for_timeout(3000)   
#             except Exception as e:
#                 print(f"Error clicking 'View More' button: {e}")

#         # Wait for review elements to load
#         await page.wait_for_selector('.jftiEf', timeout=60000)
#         elements = await page.query_selector_all('.jftiEf')

#         for element in elements:
#             try:
#                 # Extract review text
#                 snippet = await element.query_selector('.MyEned')
#                 text = await snippet.inner_text() if snippet else ""

#                 # Extract author name
#                 author_element = await element.query_selector('.d4r55')
#                 author = await author_element.inner_text() if author_element else "Anonymous"

#                 # Extract rating
#                 rating_element = await element.query_selector('.kvMYJc')
#                 rating = await rating_element.get_attribute('aria-label') if rating_element else "No rating"
#                 rating = rating.split(' ')[0] if rating else "N/A"

#                 reviews.append({
#                     "text": text,
#                     "author": author,
#                     "rating": rating
#                 })
#             except Exception as e:
#                 print(f"Error extracting review: {e}")

#         await browser.close()
#     return reviews, title

# def analyze_sentiments(reviews):
#     sia = SentimentIntensityAnalyzer()
#     sentiments = []
#     for review in reviews:
#         score = sia.polarity_scores(review)
#         compound = score['compound']
#         if compound >= 0.05:
#             sentiments.append('positive')
#         elif compound <= -0.05:
#             sentiments.append('negative')
#         else:
#             sentiments.append('neutral')
#     return sentiments

# async def scrape_and_analyze(url):
#     reviews, title = await scrape_reviews(url)
#     review_texts = [review['text'] for review in reviews]
#     sentiments = analyze_sentiments(review_texts)
    
#     total_reviews = len(sentiments)
#     positive = sum(1 for sentiment in sentiments if sentiment == 'positive')
#     neutral = sum(1 for sentiment in sentiments if sentiment == 'neutral')
#     negative = sum(1 for sentiment in sentiments if sentiment == 'negative')
    
#     sentiment_percentages = {
#         'positive': round((positive / total_reviews) * 100, 2),
#         'neutral': round((neutral / total_reviews) * 100, 2),
#         'negative': round((negative / total_reviews) * 100, 2),
#     }
    
#     return {
#         'title': title,
#         'total_reviews': total_reviews,
#         'sentiment_percentages': sentiment_percentages,
#         'reviews': reviews[:20]  # Limiting the number of reviews displayed
#     }
