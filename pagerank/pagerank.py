import os
import random
import re
import sys
import numpy

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    return_dict = dict()
    # initializing the dictionary
    for i in corpus:
        return_dict[i] = 0    
    N = len(corpus) # number of pages in the corpus
    linked_pages = corpus[page]
    n = len(linked_pages) # number of pages it's linked to

    if n > 0:
        random_chosen_prob = (1 - damping_factor) / N
    elif n == 0:
        random_chosen_prob = 1/N

    for i in return_dict:
        return_dict[i] = return_dict[i] + random_chosen_prob

    if n == 0:
        return return_dict
    linked_prob = damping_factor/n
    for i in linked_pages:
        return_dict[i] = return_dict[i] + linked_prob
    return return_dict

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    markov_model = []
    all_pages = []
    for i in corpus:
        all_pages.append(i)
    first_page = numpy.random.choice(all_pages)
    markov_model.append(first_page)
    transition_model1 = transition_model(corpus, first_page, damping_factor)
    for i in range(n):
        pages = []
        probabilites = []
        for j in transition_model1:
            pages.append(j)
            probabilites.append(transition_model1[j])
        next_page = numpy.random.choice(a=pages, p=probabilites)
        markov_model.append(next_page)
        transition_model1 = transition_model(corpus, next_page, damping_factor)
    adding_factor = 1/n
    return_dict = dict()
    for i in corpus:
        return_dict[i] = 0
    for j in markov_model:
        return_dict[j] = return_dict[j] + adding_factor
    return return_dict

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pageranks = dict()
    N = len(corpus)

    # setting all values of corpus to 1/N
    init_value = 1/N
    for i in corpus:
        pageranks[i] = init_value
        if len(corpus[i]) == 0:
            corpus[i] = corpus.keys()
    converged = False
    # each updating round
    while (not converged):
        converged = True
        new_pageranks = dict()
        # update each value using the formula
        for i in pageranks:
            new_rank = (1-damping_factor)/N # first part of the formula
            # linked_pages = corpus[i]
            pages_that_link_to_i = []
            for page in corpus:
                if i in corpus[page]:
                    pages_that_link_to_i.append(page)
                    
            summation = 0
            for j in pages_that_link_to_i:
                summation = summation + (pageranks[j]/len(corpus[j]))
            new_rank = new_rank + (damping_factor * summation) # adding the second part of the formula
            if abs(pageranks[i] - new_rank) > 0.001:
                 converged = False
            new_pageranks[i] = new_rank
        pageranks = new_pageranks
    return pageranks


if __name__ == "__main__":
    main()
