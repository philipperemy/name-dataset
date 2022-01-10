# First and Last Names Dataset

*From 533M Facebook records.*

[![Downloads](https://pepy.tech/badge/names-dataset)](https://pepy.tech/project/names-dataset)
[![Downloads](https://pepy.tech/badge/names-dataset/month)](https://pepy.tech/project/names-dataset/month)

This Python library provides information about names: popularity (rank), country (105 countries supported) and gender.

*NOTE: If you have the full text and are looking for a named entity recognition library (NER), I advise you to checkout this one
from [Stanford University](https://nlp.stanford.edu/software/CRF-NER.html).*

**Composition:** v3 (2022): 730K first names, 983K last names - extracted from
the [Facebook massive dump (533M users)](https://www.theguardian.com/technology/2021/apr/03/500-million-facebook-users-website-hackers)
.

## Installation

*PyPI*

```bash
pip install names-dataset
```

## Usage

Once it's installed, run those commands to familiarize yourself with the library:

```python
from names_dataset import NameDataset

# The V3 lib takes time to init (the database is massive). Tip: Put it into the init of your app.
nd = NameDataset()

print(nd.search('Walter'))
# {'first_name': {'country': {'Argentina': 0.062, 'Austria': 0.037, 'Bolivia, Plurinational State of': 0.042, 'Colombia': 0.096, 'Germany': 0.044, 'Italy': 0.295, 'Peru': 0.185, 'United States': 0.159, 'Uruguay': 0.036, 'South Africa': 0.043}, 'gender': {'Female': 0.007, 'Male': 0.993}, 'rank': {'Argentina': 37, 'Austria': 34, 'Bolivia, Plurinational State of': 67, 'Colombia': 250, 'Germany': 214, 'Italy': 193, 'Peru': 27, 'United States': 317, 'Uruguay': 44, 'South Africa': 388}}, 'last_name': {'country': {'Austria': 0.036, 'Brazil': 0.039, 'Switzerland': 0.032, 'Germany': 0.299, 'France': 0.121, 'United Kingdom': 0.048, 'Italy': 0.09, 'Nigeria': 0.078, 'United States': 0.172, 'South Africa': 0.085}, 'gender': {}, 'rank': {'Austria': 106, 'Brazil': 805, 'Switzerland': 140, 'Germany': 39, 'France': 625, 'United Kingdom': 1823, 'Italy': 3564, 'Nigeria': 926, 'United States': 1210, 'South Africa': 1169}}}

print(nd.search('White'))
# {'first_name': {'country': {'United Arab Emirates': 0.044, 'Egypt': 0.294, 'France': 0.061, 'Hong Kong': 0.05, 'Iraq': 0.094, 'Italy': 0.117, 'Malaysia': 0.133, 'Saudi Arabia': 0.089, 'Taiwan, Province of China': 0.044, 'United States': 0.072}, 'gender': {'Female': 0.519, 'Male': 0.481}, 'rank': {'Taiwan, Province of China': 6940, 'United Arab Emirates': None, 'Egypt': None, 'France': None, 'Hong Kong': None, 'Iraq': None, 'Italy': None, 'Malaysia': None, 'Saudi Arabia': None, 'United States': None}}, 'last_name': {'country': {'Canada': 0.035, 'France': 0.016, 'United Kingdom': 0.296, 'Ireland': 0.028, 'Iraq': 0.016, 'Italy': 0.02, 'Jamaica': 0.017, 'Nigeria': 0.031, 'United States': 0.5, 'South Africa': 0.04}, 'gender': {}, 'rank': {'Canada': 46, 'France': 1041, 'United Kingdom': 18, 'Ireland': 66, 'Iraq': 1307, 'Italy': 2778, 'Jamaica': 35, 'Nigeria': 425, 'United States': 47, 'South Africa': 416}}}

print(nd.search('محمد'))
# {'first_name': {'country': {'Algeria': 0.018, 'Egypt': 0.441, 'Iraq': 0.12, 'Jordan': 0.027, 'Libya': 0.035, 'Saudi Arabia': 0.154, 'Sudan': 0.07, 'Syrian Arab Republic': 0.062, 'Turkey': 0.022, 'Yemen': 0.051}, 'gender': {'Female': 0.035, 'Male': 0.965}, 'rank': {'Algeria': 4, 'Egypt': 1, 'Iraq': 2, 'Jordan': 1, 'Libya': 1, 'Saudi Arabia': 1, 'Sudan': 1, 'Syrian Arab Republic': 1, 'Turkey': 18, 'Yemen': 1}}, 'last_name': {'country': {'Egypt': 0.453, 'Iraq': 0.096, 'Jordan': 0.015, 'Libya': 0.043, 'Palestine, State of': 0.016, 'Saudi Arabia': 0.118, 'Sudan': 0.146, 'Syrian Arab Republic': 0.058, 'Turkey': 0.017, 'Yemen': 0.037}, 'gender': {}, 'rank': {'Egypt': 2, 'Iraq': 3, 'Jordan': 1, 'Libya': 1, 'Palestine, State of': 1, 'Saudi Arabia': 3, 'Sudan': 1, 'Syrian Arab Republic': 2, 'Turkey': 44, 'Yemen': 1}}}

print(nd.get_top_names(n=10, gender='Male', country_alpha2='US'))
# {'US': {'M': ['Jose', 'David', 'Michael', 'John', 'Juan', 'Carlos', 'Luis', 'Chris', 'Alex', 'Daniel']}}

print(nd.get_top_names(n=5, country_alpha2='ES'))
# {'ES': {'M': ['Jose', 'Antonio', 'Juan', 'Manuel', 'David'], 'F': ['Maria', 'Ana', 'Carmen', 'Laura', 'Isabel']}}

print(nd.get_country_codes(alpha_2=True))
# ['AE', 'AF', 'AL', 'AO', 'AR', 'AT', 'AZ', 'BD', 'BE', 'BF', 'BG', 'BH', 'BI', 'BN', 'BO', 'BR', 'BW', 'CA', 'CH', 'CL', 'CM', 'CN', 'CO', 'CR', 'CY', 'CZ', 'DE', 'DJ', 'DK', 'DZ', 'EC', 'EE', 'EG', 'ES', 'ET', 'FI', 'FJ', 'FR', 'GB', 'GE', 'GH', 'GR', 'GT', 'HK', 'HN', 'HR', 'HT', 'HU', 'ID', 'IE', 'IL', 'IN', 'IQ', 'IR', 'IS', 'IT', 'JM', 'JO', 'JP', 'KH', 'KR', 'KW', 'KZ', 'LB', 'LT', 'LU', 'LY', 'MA', 'MD', 'MO', 'MT', 'MU', 'MV', 'MX', 'MY', 'NA', 'NG', 'NL', 'NO', 'OM', 'PA', 'PE', 'PH', 'PL', 'PR', 'PS', 'PT', 'QA', 'RS', 'RU', 'SA', 'SD', 'SE', 'SG', 'SI', 'SV', 'SY', 'TM', 'TN', 'TR', 'TW', 'US', 'UY', 'YE', 'ZA']
```
## API

The `search` call provides information about:
- `country`: The probability of the name belonging to a country. Only the top 10 countries matching the name are returned.
- `gender`: The probability of the person to be a `Male` or `Female`.
- `rank`: The rank of the name in his country. `1` means the most popular name.

- **NOTE**: `first_name/last_name`: the `gender` does not apply to `last_name`.

The `get_top_names` call gives the most popular names:

- `n`: The number of names to return matching some criteria. Default is 100.
- `gender`: Filters on `Male` or `Female`. Default is None.
- `use_first_names`: Filters on the first names or last names. Default is True.
- `country_alpha2`: Filters on the country (e.g. GB is the United Kingdom). Default is None.

The `get_country_codes` returns the supported country codes (or full `pycountry` objects).

- `alpha_2`: Only returns the country codes: 2-char code. Default is False.

## Full curated dataset

- The full (curated) dataset containing first, last names along with gender and countries has been uploaded here: [
full.tar.bz2 (2.3G)](https://drive.google.com/file/d/1wRQfw5EYpzulvRfHCGIUWB2am5JUYVGk/view?usp=sharing).

## License

- For the V3, it's fetched from the massive Facebook Leak (533M accounts).
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
