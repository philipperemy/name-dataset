# First and Last Names Dataset

[![Downloads](https://pepy.tech/badge/names-dataset)](https://pepy.tech/project/names-dataset)
[![Downloads](https://pepy.tech/badge/names-dataset/month)](https://pepy.tech/project/names-dataset/month)

This module is useful when you have a name and you want to check if it looks like a legit name. 

If you have the full text and you want to find where the names are, it is probably better to use a [NER library like the Stanford one](https://nlp.stanford.edu/software/CRF-NER.html).

*Composition:*

- v1 (2018): 160K first names, 100K last names - from IMDB, Names databases scraped from internet.
- v2 (2021): 1.6M first names, 3.5M last names - from the [Facebook massive dump (533M users)](https://www.theguardian.com/technology/2021/apr/03/500-million-facebook-users-website-hackers).


## Installation

*PyPI*
```bash
pip install names-dataset
```

## Usage

Once it's installed, run those commands to familiarize yourself with the library:

```python
from names_dataset import NameDataset # v2
from names_dataset import NameDatasetV1 # v1

# v2
# The V2 lib takes time to init (the database is massive).
m = NameDataset() # init it only once in your app because the V2 takes much more time to init than the V1.
# The scores are calculated based on the frequencies of the names for a given country. For example, the 
# most popular first name in Morocco is Mohamed so Mohamed will have a score of 100.
print(m.search_first_name('محمد')) # 100.0
print(m.search_first_name('영수')) # 88.803089
print(m.search_first_name('Joe')) # 45.238095
print(m.search_last_name('Remy')) # 11.282479
print(m.search_first_name('Dog')) # 0.0

# v1
# V1 does not give any score. Just a True or False.
m = NameDatasetV1()
print(m.search_first_name('Joe')) # True
print(m.search_last_name('Remy')) # True
print(m.search_first_name('Dog')) # False
```

- The V1 returns `True`/`False`.
- The V2 returns a score between 0.0 and 100.0 to control for the precision and the recall.
- You can find a suitable threshold to detect if a word is a name or not:
```python
m.search_first_name('Joe') > 1 # will only return the VERY VERY COMMON names like "Joe" or "Anna".
# True
```
- You can adjust the threshold based on this table (If you want to match roughly the same number of names as in the V1, set the threshold to 0.15 for first names and 1.0 for last names):

| Threshold | Top First names | Top Second names |
|-----------|-----------------|------------------|
| 10        | 7231            | 6155             |
| 1         | 45624           | 94648            |
| 0.1       | 192195          | 624436           |
| 0.01      | 671110          | 2068468          |
| 0.001     | 1455485         | 3327665          |
| 0         | 1642641         | 3479437          |

- You can also see if any name is more likely to be a first name, than a last name, by comparing the two scores:

```python
print(m.search_first_name('Joe'), m.search_last_name('Joe'))
# 45.238095 9.226714
```

- If you are interested to know the country of a given name, you can have a look here: [WIP-14](https://github.com/philipperemy/name-dataset/issues/14).

## 105 Countries supported in the V2

Afghanistan, Albania, Algeria, Angola, Argentina, Austria, Azerbaijan, Bahrain, Bangladesh, Belgium, Bolivia, Botswana, Brazil, Brunei, Bulgaria, Burkina_Faso, Burundi, Cambodia, Cameroon, Canada, Chile, China, Colombia, Costa_Rica, Croatia, Cyprus, Czech_Republic, Denmark, Djibouti, Ecuador, Egypt, El_Salvador, Estonia, Ethiopia, Fiji, Finland, France, Georgia, Germany, Ghana, Greece, Guatemala, Haiti, Honduras, Hong_Kong, Hungary, Iceland, India, Indonesia, Iran, Iraq, Ireland, Israel, Italy, Jamaica, Japan, Jordan, Kazakhstan, Kuwait, Lebanon, Libya, Lithuania, Luxemburg, Macao, Malaysia, Maldives, Malta, Mauritius, Mexico, Moldova, Morocco, Namibia, Netherlands, Nigeria, Norway, Oman, Palestine, Panama, Peru, Philippines, Poland, Portugal, Puerto_Rico, Qatar, Russia, Saudi_Arabia, Serbia, Singapore, Slovenia, South_Africa, South_Korea, Spain, Sudan, Sweden, Switzerland, Syria, Taiwan, Tunisia, Turkey, Turkmenistan, Uae, Uk, Uruguay, Usa, Yemen.

## License

- I don't own the data obviously. For the V1, it's fetched from the websites listed in: [generate.sh](https://github.com/philipperemy/name-dataset/blob/master/generation/generate.sh).
- For the V2, it's fetched from the massive Facebook Leak (533M accounts).
- Lists of names are [not copyrightable](https://www.justia.com/intellectual-property/copyright/lists-directories-and-databases/), generally speaking, but if you want to be completely sure you should talk to a lawyer.

## Citation

```
@misc{NameDataset2021,
  author = {Philippe Remy},
  title = {Name Dataset},
  year = {2021},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/philipperemy/name-dataset}},
}
```
