# python program to find which jobs to apply on cv library website using clustering

## part 1 get the links of the jobs pages
import re, math, os, time, pandas

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

options = Options()
options.add_argument("--ignore-certificate-errors")
options.add_argument("--disable-proxy-certificate-handler")
driver = webdriver.Chrome(
    options=options, 
)

driver.get('https://www.cv-library.co.uk/candidate/login?')
driver.implicitly_wait(2)

# interact with the cookies banner
frame = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 'gdpr-consent-notice'))
)
driver.switch_to.frame(frame)
accept_cookies = driver.find_element(By.ID,'save')
accept_cookies.click()

# interact with the login page
cand_email = driver.find_element(By.ID, 'cand_email')
cand_email.send_keys('youremail')
cand_password = driver.find_element(By.ID, 'cand_password')
cand_password.send_keys('yourpassword')
actions = ActionChains(driver)
actions.send_keys(Keys.ENTER).perform()

# interact with the search bar
driver.find_element(By.ID,'header-search-keywords').send_keys('your keyword')
driver.find_element(By.ID,'header-search-location').send_keys('your location')
actions.send_keys(Keys.ENTER).perform()

# knowing results 
number_of_jobs = driver.find_element(By.CLASS_NAME,'search-header__results').text
number_of_jobs = math.ceil(int(re.search(" (\d{1,}) ",number_of_jobs).group(1))/25)

# save the search result pages, later these will be used to extract links to the job pages
to_save_path = r'path to save the search result pages'

# save the pages
try:
    for i in range(1,number_of_jobs+1):
        htmlname = driver.current_url.split('?')[-1]+".html"
        to_write = os.path.join(to_save_path, htmlname)
        print("To write: ",to_write)
        with open(to_write, "w", encoding='utf-8') as f:
            f.write(driver.page_source)
        driver.find_element(By.CLASS_NAME,'pagination__next').click()
except Exception as E:
    print(E)

driver.quit()

## part 2 get the job pages 
# use beautiful soup to extract links to jobs 
from bs4 import BeautifulSoup

to_save_path = r'path of the saved search pages'

links = []
a=1
for i,j,k in os.walk(to_save_path):
    for html in k:
        path_ = os.path.join(i,html)
        with open(path_, "r", encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
            job_links = set(['https://www.cv-library.co.uk'+link.get('href') for link in soup.find_all('a') if 'sid' in link.get('href') and 'hlkw' in link.get('href')])
            links.append({"page":a,"links":job_links})
            a+=1

to_save_path_ = r"path to save the pages of the jobs"

driver = webdriver.Chrome(
    options=options, 
)

for link in links:
    for j in link["links"]:
        name_=j.split("/")[-2]
        print(name_)
        driver.get(j)
        driver.implicitly_wait(2)
        time.sleep(5)
        to_write = os.path.join(to_save_path_, name_+".html")
        print("To write: ",to_write)
        with open(to_write, "w", encoding='utf-8') as f:
            f.write(driver.page_source)

driver.quit()
        
## part 3 do the clustering and predict the cluster for your CV
to_save_path_ = r"path of job pages"

from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
pd_loc=0
df = pandas.DataFrame(columns = ["jd","id"])
special_characters = "!@#$%^&*()_-–+=<>?/[]{},.:;|~`’"
# clean the data and put it in a dataframe
for i,j,k in os.walk(to_save_path_):
    for name_ in k:
        with open(os.path.join(i,name_),'r',encoding='utf-8') as f:
            soup = BeautifulSoup(f,'html.parser')
            try:
                article = soup.find('article')
                title = article.find(class_="job__title").get_text()
                jd = article.find(class_="job__description").get_text()
                text = jd + " " + title
                for schr in special_characters:
                    text = text.replace(schr," ")
                text = re.sub(r"[^a-zA-Z]\d{1,}"," ",text)
                text = word_tokenize(text)
                lemmatizer = WordNetLemmatizer()
                article_lemm = " ".join([lemmatizer.lemmatize(token) for token in text if len(token) >1]).lower()
            except:
                article = ""
            df.loc[pd_loc] = [article_lemm, name_]
            pd_loc+=1
            print(pd_loc)

# idf for feature creature and kmeans for clustering
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

documents = df['jd'].values.astype("U")
vectorizer = TfidfVectorizer(stop_words='english')
features = vectorizer.fit_transform(documents)

# train the model
k = 10
model = KMeans(n_clusters=k, init='k-means++', max_iter=100, n_init=1, random_state=42)
model.fit(features)

# preprocess your your resume text in similar way
new_document = "text of your resume"
for schr in special_characters:
    new_document = new_document.replace(schr," ")
new_document = re.sub(r"[^a-zA-Z]\d{1,}"," ",new_document)
new_document = word_tokenize(new_document)
lemmatizer = WordNetLemmatizer()
article_lemm = " ".join([lemmatizer.lemmatize(token) for token in new_document if len(token) >1]).lower()

new_document_vector = vectorizer.transform([article_lemm])

# Predict the cluster label for your resume
predicted_cluster = model.predict(new_document_vector)[0]
print("Predicted cluster for the new document:", predicted_cluster)

# see the features or words in the cluster
order_centroids = model.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names_out()
for j in order_centroids[predicted_cluster]:
    print(' %s' % terms[j])


# use cosine_similarity to know how close your resume is to other clusters
from sklearn.metrics.pairwise import cosine_similarity

# Compute cosine similarity between new document vector and cluster centroids
centroid_vectors = model.cluster_centers_
cosine_similarities = cosine_similarity(new_document_vector, centroid_vectors)

# Print cosine similarity for each cluster
for i, similarity in enumerate(cosine_similarities[0]):
    print(f"Cluster {i}: Cosine similarity = {similarity}")

# there you go you can now apply to jobs of your resume cluster and work on skills to inorder to apply to jobs of other clusters