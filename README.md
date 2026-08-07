![Tests](https://github.com/dhav211/pokeapi_testing/actions/workflows/tests.yml/badge.svg)

# What is this?
This is my attempt to learn more about API testing with python, pytest, and requests. It serves no practical real world solution other than education, which I suppose would be a solution to most the worlds problems. I was going through Brian Okken's excellent book titled "Python Testing with pytest" so as I learnt about fixtures, I would add a fixture. It really cemented my knowledge of what I was learning.

# Test Plan
## Scope
I will be covering the basics of the pokeapi, as it fairly in depth and I could be writing tests for the next several months. I will be testing the standard response codes, the first layer of the pokemon response (such as name, basic details, and abilities), and also digging deep into pagination. I felt these were the most important and anything after that was dimishing returns. Our time is very important.

### What's covered

**Pagination**
- Default pagination behavior (count, page size, next/previous links)
- Custom `limit` values, including edge cases: zero, negative, decimal, non-numeric,
  and mixed alphanumeric input
- `offset` correctness, including negative offsets and offsets beyond the dataset size
- First-page and last-page boundary behavior
- Next/previous link consistency when paging forward and backward
- No duplicate results across a full paginated walk of all Pokemon

**Resource retrieval**
- Correct data returned for known Pokemon, validated against expected Pydantic models
- Case-insensitivity of name lookups
- Cross-reference consistency (a Pokemon's type endpoint correctly links back to it)
- Nested resource links (e.g. species URL) resolve successfully

**Error handling**
- 404s for non-existent Pokemon, out-of-range IDs, and malformed identifiers
- 400s for injection-style input (SQL injection strings) and special characters
- 414 for excessively long input
- Response headers (content-type) and response time sanity checks

# How to build
First clone this repo:
`git clone https://github.com/dhav211/pokeapi-testing.git`

Create the virtual enviorment:
```
python -m venv venv
source venv/bin/activate
```

Then install the deps:
`pip install -r requirements.txt`

Finally to run the whole test suite
`pytest`